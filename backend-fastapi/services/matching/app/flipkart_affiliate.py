"""Flipkart Affiliate API integration for wishlist matching.

Official Flipkart Affiliate program — legal product search API.
Returns real product listings with affiliate tracking links.

Setup:
  1. Sign up at https://affiliate.flipkart.com
  2. Get Affiliate ID and Token after approval
  3. Set FLIPKART_AFFILIATE_ID and FLIPKART_AFFILIATE_TOKEN in environment

API docs: https://affiliate.flipkart.com/api-docs
"""

import logging
from typing import List, Optional

import httpx
from shared.config.settings import get_settings
from app.serper import _compute_match_score, _is_category_page, _parse_price

logger = logging.getLogger(__name__)

FLIPKART_AFFILIATE_URL = "https://affiliate-api.flipkart.net/affiliate/1.0/search.json"


def _build_flipkart_query(wishlist: dict) -> str:
    """Build a search query string from wishlist fields."""
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


def search_flipkart_affiliate(wishlist: dict) -> List[dict]:
    """Search Flipkart via their official Affiliate API."""
    settings = get_settings().affiliate
    if not settings.flipkart_affiliate_id or not settings.flipkart_affiliate_token:
        logger.debug("Flipkart Affiliate API not configured, skipping")
        return []

    query = _build_flipkart_query(wishlist)
    if not query:
        return []

    filters = wishlist.get("filters_json") or {}
    price = filters.get("price") or filters.get("max_price") or filters.get("budget")

    headers = {
        "Fk-Affiliate-Id": settings.flipkart_affiliate_id,
        "Fk-Affiliate-Token": settings.flipkart_affiliate_token,
    }

    results = []
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.get(
                FLIPKART_AFFILIATE_URL,
                headers=headers,
                params={"query": query, "resultCount": 20},
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        logger.error(f"Flipkart Affiliate search failed: {e}", exc_info=True)
        return []

    products = data.get("products", []) or data.get("productInfoList", []) or []

    for idx, item in enumerate(products[:20], 1):
        try:
            product_info = item.get("productBaseInfoV1", item)

            title = product_info.get("title", "")
            if not title:
                continue

            # Price
            mrp = product_info.get("maximumRetailPrice", {})
            fsp = product_info.get("flipkartSellingPrice", {})
            item_price = fsp.get("amount") or mrp.get("amount") or 0
            currency = fsp.get("currency", "INR")

            # Skip if over budget
            if price and item_price and float(item_price) > float(price) * 1.2:
                continue

            # URL (affiliate tracked)
            product_url = product_info.get("productUrl", "")
            if not product_url:
                continue

            # Image
            image_urls = product_info.get("imageUrls", {})
            image_url = image_urls.get("400x400") or image_urls.get("200x200") or image_urls.get("unknown")

            # Description
            desc_parts = []
            if product_info.get("productBrand"):
                desc_parts.append(product_info["productBrand"])
            if product_info.get("attributes", {}).get("color"):
                desc_parts.append(product_info["attributes"]["color"])
            if product_info.get("attributes", {}).get("size"):
                desc_parts.append(product_info["attributes"]["size"])

            formatted = f"\u20b9{int(item_price):,}" if item_price else None

            results.append({
                "url": product_url,
                "source": "flipkart_affiliate",
                "title": title,
                "description": " | ".join(desc_parts) if desc_parts else "",
                "price": float(item_price) if item_price else None,
                "formatted_price": formatted,
                "image_url": image_url,
                "position": idx,
            })
        except Exception as e:
            logger.debug(f"Flipkart affiliate parse error: {e}")
            continue

    logger.info(f"Flipkart Affiliate returned {len(results)} products")
    return results


def search_and_score_flipkart(wishlist: dict) -> List[dict]:
    """Search Flipkart Affiliate API, score and filter results."""
    raw_results = search_flipkart_affiliate(wishlist)
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
    logger.info(f"Flipkart Affiliate scored {len(scored)} matches for '{wishlist.get('title', '')}'")
    return scored
