"""Amazon Product Advertising API (PA-API 5.0) integration.

Official Amazon Associates program — legal product search API.
Returns real product listings with affiliate tracking links.

Setup:
  1. Sign up at https://affiliate-program.amazon.in
  2. Get approved as Amazon Associate
  3. Get Access Key and Secret Key from PA-API dashboard
  4. Set AMAZON_PARTNER_TAG, AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY in environment

API docs: https://webservices.amazon.in/paapi5/documentation
"""

import hashlib
import hmac
import json
import logging
from datetime import datetime, timezone
from typing import List

import httpx
from shared.config.settings import get_settings
from app.serper import _compute_match_score, _parse_price

logger = logging.getLogger(__name__)

AMAZON_HOST = "webservices.amazon.in"
AMAZON_REGION = "eu-west-1"
AMAZON_SERVICE = "ProductAdvertisingAPI"
AMAZON_ENDPOINT = f"https://{AMAZON_HOST}/paapi5/searchitems"


def _sign_request(payload: str, access_key: str, secret_key: str) -> dict:
    """Create AWS Signature V4 headers for PA-API 5.0."""
    now = datetime.now(timezone.utc)
    datestamp = now.strftime("%Y%m%d")
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    target = "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems"

    headers_to_sign = {
        "content-encoding": "amz-1.0",
        "content-type": "application/json; charset=utf-8",
        "host": AMAZON_HOST,
        "x-amz-date": amz_date,
        "x-amz-target": target,
    }

    signed_headers = ";".join(sorted(headers_to_sign.keys()))
    canonical_headers = "".join(f"{k}:{v}\n" for k, v in sorted(headers_to_sign.items()))

    payload_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = f"POST\n/paapi5/searchitems\n\n{canonical_headers}\n{signed_headers}\n{payload_hash}"

    credential_scope = f"{datestamp}/{AMAZON_REGION}/{AMAZON_SERVICE}/aws4_request"
    string_to_sign = (
        f"AWS4-HMAC-SHA256\n{amz_date}\n{credential_scope}\n"
        f"{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
    )

    def _sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    signing_key = _sign(
        _sign(
            _sign(
                _sign(f"AWS4{secret_key}".encode("utf-8"), datestamp),
                AMAZON_REGION,
            ),
            AMAZON_SERVICE,
        ),
        "aws4_request",
    )

    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    auth_header = (
        f"AWS4-HMAC-SHA256 Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )

    return {
        "Authorization": auth_header,
        "Content-Encoding": "amz-1.0",
        "Content-Type": "application/json; charset=utf-8",
        "Host": AMAZON_HOST,
        "X-Amz-Date": amz_date,
        "X-Amz-Target": target,
    }


def _build_amazon_query(wishlist: dict) -> str:
    """Build search keywords from wishlist fields."""
    title = (wishlist.get("title") or "").strip()
    filters = wishlist.get("filters_json") or {}
    if not isinstance(filters, dict):
        filters = {}

    parts = []
    for key in ("brand", "model", "itemType"):
        val = filters.get(key, "")
        if val:
            parts.append(val)

    return " ".join(parts) if parts else title


# Map wishlist categories to Amazon search indices
CATEGORY_INDEX = {
    "electronics": "Electronics",
    "fashion": "Fashion",
    "home & living": "HomeAndKitchen",
    "automobile": "Automotive",
}


def search_amazon_paapi(wishlist: dict) -> List[dict]:
    """Search Amazon via Product Advertising API 5.0."""
    settings = get_settings().affiliate
    if not settings.amazon_access_key or not settings.amazon_secret_key or not settings.amazon_partner_tag:
        logger.debug("Amazon PA-API not configured, skipping")
        return []

    query = _build_amazon_query(wishlist)
    if not query:
        return []

    category = (wishlist.get("category") or "").lower()
    search_index = CATEGORY_INDEX.get(category, "All")

    filters = wishlist.get("filters_json") or {}
    price = filters.get("price") or filters.get("max_price") or filters.get("budget")

    request_body = {
        "Keywords": query,
        "SearchIndex": search_index,
        "ItemCount": 10,
        "PartnerTag": settings.amazon_partner_tag,
        "PartnerType": "Associates",
        "Marketplace": "www.amazon.in",
        "Resources": [
            "ItemInfo.Title",
            "Offers.Listings.Price",
            "Images.Primary.Large",
            "ItemInfo.Features",
            "BrowseNodeInfo.BrowseNodes",
        ],
    }

    if price:
        request_body["MaxPrice"] = int(float(price) * 100)  # PA-API uses lowest currency unit

    payload = json.dumps(request_body)
    headers = _sign_request(payload, settings.amazon_access_key, settings.amazon_secret_key)

    results = []
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.post(AMAZON_ENDPOINT, headers=headers, content=payload)
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        logger.error(f"Amazon PA-API search failed: {e}", exc_info=True)
        return []

    items = data.get("SearchResult", {}).get("Items", [])

    for idx, item in enumerate(items, 1):
        try:
            asin = item.get("ASIN", "")
            detail_url = item.get("DetailPageURL", "")
            if not detail_url:
                continue

            # Title
            item_info = item.get("ItemInfo", {})
            title_info = item_info.get("Title", {})
            title = title_info.get("DisplayValue", "")

            # Price
            offers = item.get("Offers", {})
            listings = offers.get("Listings", [])
            item_price = None
            formatted_price = None
            if listings:
                price_info = listings[0].get("Price", {})
                item_price = price_info.get("Amount")
                formatted_price = price_info.get("DisplayAmount")

            # Image
            images = item.get("Images", {})
            primary = images.get("Primary", {})
            large = primary.get("Large", {})
            image_url = large.get("URL")

            # Features as description
            features = item_info.get("Features", {}).get("DisplayValues", [])
            description = " | ".join(features[:3]) if features else ""

            results.append({
                "url": detail_url,
                "source": "amazon_affiliate",
                "title": title,
                "description": description[:300],
                "price": float(item_price) if item_price else None,
                "formatted_price": formatted_price,
                "image_url": image_url,
                "position": idx,
            })
        except Exception as e:
            logger.debug(f"Amazon PA-API parse error: {e}")
            continue

    logger.info(f"Amazon PA-API returned {len(results)} products")
    return results


def search_and_score_amazon(wishlist: dict) -> List[dict]:
    """Search Amazon PA-API, score and filter results."""
    raw_results = search_amazon_paapi(wishlist)
    if not raw_results:
        return []

    scored = []
    for r in raw_results:
        score = _compute_match_score(r, wishlist)
        if score <= 0:
            continue
        r["score"] = score
        scored.append(r)

    scored.sort(key=lambda x: x["score"], reverse=True)
    logger.info(f"Amazon PA-API scored {len(scored)} matches for '{wishlist.get('title', '')}'")
    return scored
