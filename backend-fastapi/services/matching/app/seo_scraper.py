"""SEO Metadata Scraper — extracts Open Graph tags and JSON-LD structured data.

Legally reads publicly available metadata that websites intentionally expose
for search engines and social media crawlers:

  - Open Graph (og:title, og:description, og:image, og:price, og:url)
  - Twitter Card (twitter:title, twitter:description, twitter:image)
  - JSON-LD schema.org structured data (Product, Vehicle, RealEstateListing, Offer)
  - Standard HTML meta tags (title, description, canonical URL)

This does NOT parse internal page HTML, CSS selectors, or proprietary markup.
It only reads the same metadata that Google/Facebook/Twitter read.
"""

import json
import logging
import re
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from app.serper import (
    _extract_price_from_text,
    _parse_price,
    PRIMARY_DOMAINS,
    LISTING_DOMAINS,
)

logger = logging.getLogger(__name__)

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; WISHIBot/1.0; +https://wishi.app/bot)"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-IN,en;q=0.9",
}

# Only download the <head> section — we don't need body HTML
_MAX_CONTENT_LENGTH = 200_000  # 200KB max (head is usually < 50KB)


# ── OG + Meta extraction ─────────────────────────────────────────────────

def _extract_og_tags(soup: BeautifulSoup) -> Dict[str, str]:
    """Extract all Open Graph and Twitter Card meta tags."""
    og = {}

    for meta in soup.find_all("meta"):
        prop = meta.get("property", "") or meta.get("name", "")
        content = meta.get("content", "")
        if not prop or not content:
            continue

        prop_lower = prop.lower()

        # Open Graph
        if prop_lower == "og:title":
            og["title"] = content
        elif prop_lower == "og:description":
            og["description"] = content
        elif prop_lower == "og:image":
            og["image"] = content
        elif prop_lower == "og:url":
            og["url"] = content
        elif prop_lower == "og:type":
            og["type"] = content
        elif prop_lower in ("og:price:amount", "product:price:amount"):
            og["price"] = content
        elif prop_lower in ("og:price:currency", "product:price:currency"):
            og["currency"] = content
        elif prop_lower == "og:site_name":
            og["site_name"] = content
        elif prop_lower == "og:locale":
            og["locale"] = content
        elif prop_lower == "product:brand":
            og["brand"] = content
        elif prop_lower == "product:condition":
            og["condition"] = content
        elif prop_lower == "product:availability":
            og["availability"] = content
        elif prop_lower == "product:category":
            og["category"] = content

        # Twitter Card
        elif prop_lower == "twitter:title" and "title" not in og:
            og["title"] = content
        elif prop_lower == "twitter:description" and "description" not in og:
            og["description"] = content
        elif prop_lower == "twitter:image" and "image" not in og:
            og["image"] = content

        # Standard meta
        elif prop_lower == "description" and "description" not in og:
            og["description"] = content

    # Fallback: <title> tag
    if "title" not in og:
        title_tag = soup.find("title")
        if title_tag:
            og["title"] = title_tag.get_text(strip=True)

    # Canonical URL
    canonical = soup.find("link", rel="canonical")
    if canonical and canonical.get("href"):
        og["canonical_url"] = canonical["href"]

    return og


# ── JSON-LD structured data extraction ────────────────────────────────────

def _extract_jsonld(soup: BeautifulSoup) -> Dict:
    """Extract product/listing data from JSON-LD schema.org markup.

    Handles: Product, Vehicle, RealEstateListing, Offer, LocalBusiness
    """
    data = {}

    for script in soup.find_all("script", type="application/ld+json"):
        try:
            raw = script.string or ""
            # Some sites have comments or trailing commas
            raw = re.sub(r",\s*([}\]])", r"\1", raw)
            ld = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            continue

        items = ld if isinstance(ld, list) else [ld]

        # Handle @graph wrapper
        for item in items:
            if isinstance(item, dict) and "@graph" in item:
                items.extend(item["@graph"])

        for item in items:
            if not isinstance(item, dict):
                continue

            item_type = item.get("@type", "")
            if isinstance(item_type, list):
                item_type = item_type[0] if item_type else ""

            if item_type in ("Product", "IndividualProduct"):
                data.update(_parse_product_ld(item))
            elif item_type in ("Vehicle", "Car", "MotorizedBicycle"):
                data.update(_parse_vehicle_ld(item))
            elif item_type in ("RealEstateListing", "Apartment", "House", "Residence"):
                data.update(_parse_realestate_ld(item))
            elif item_type == "Offer":
                data.update(_parse_offer_ld(item))
            elif item_type in ("BreadcrumbList",):
                breadcrumbs = _parse_breadcrumbs(item)
                if breadcrumbs:
                    data["breadcrumbs"] = breadcrumbs

    return data


def _parse_product_ld(item: dict) -> Dict:
    """Parse schema.org Product JSON-LD."""
    data = {}
    data["ld_type"] = "Product"

    if item.get("name"):
        data["ld_title"] = item["name"]
    if item.get("description"):
        data["ld_description"] = str(item["description"])[:500]
    if item.get("brand"):
        brand = item["brand"]
        data["ld_brand"] = brand.get("name", str(brand)) if isinstance(brand, dict) else str(brand)
    if item.get("sku"):
        data["ld_sku"] = item["sku"]
    if item.get("gtin13") or item.get("gtin"):
        data["ld_gtin"] = item.get("gtin13") or item.get("gtin")
    if item.get("model"):
        data["ld_model"] = item["model"]
    if item.get("color"):
        data["ld_color"] = item["color"]
    if item.get("itemCondition"):
        data["ld_condition"] = item["itemCondition"].replace("https://schema.org/", "").replace("http://schema.org/", "")

    # Image
    images = item.get("image", [])
    if isinstance(images, str):
        data["ld_image"] = images
    elif isinstance(images, list) and images:
        first = images[0]
        data["ld_image"] = first.get("url", first) if isinstance(first, dict) else first

    # Offers / price
    offers = item.get("offers", {})
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    if isinstance(offers, dict):
        data.update(_parse_offer_ld(offers))

    # Rating
    rating = item.get("aggregateRating", {})
    if isinstance(rating, dict) and rating.get("ratingValue"):
        data["ld_rating"] = str(rating["ratingValue"])
        data["ld_review_count"] = str(rating.get("reviewCount", ""))

    return data


def _parse_vehicle_ld(item: dict) -> Dict:
    """Parse schema.org Vehicle/Car JSON-LD."""
    data = _parse_product_ld(item)  # inherit product fields
    data["ld_type"] = "Vehicle"

    if item.get("vehicleTransmission"):
        data["ld_transmission"] = item["vehicleTransmission"]
    if item.get("fuelType"):
        data["ld_fuel_type"] = item["fuelType"]
    if item.get("mileageFromOdometer"):
        odometer = item["mileageFromOdometer"]
        if isinstance(odometer, dict):
            data["ld_km_driven"] = str(odometer.get("value", ""))
        else:
            data["ld_km_driven"] = str(odometer)
    if item.get("vehicleModelDate") or item.get("modelDate"):
        data["ld_year"] = str(item.get("vehicleModelDate") or item.get("modelDate"))
    if item.get("numberOfDoors"):
        data["ld_doors"] = str(item["numberOfDoors"])
    if item.get("vehicleSeatingCapacity"):
        data["ld_seats"] = str(item["vehicleSeatingCapacity"])
    if item.get("color") or item.get("vehicleColor"):
        data["ld_color"] = item.get("color") or item.get("vehicleColor")

    return data


def _parse_realestate_ld(item: dict) -> Dict:
    """Parse schema.org RealEstateListing JSON-LD."""
    data = _parse_product_ld(item)
    data["ld_type"] = "RealEstate"

    if item.get("numberOfRooms"):
        data["ld_rooms"] = str(item["numberOfRooms"])
    if item.get("floorSize"):
        floor = item["floorSize"]
        if isinstance(floor, dict):
            data["ld_area"] = f"{floor.get('value', '')} {floor.get('unitText', 'sqft')}"
        else:
            data["ld_area"] = str(floor)

    # Address
    address = item.get("address", {})
    if isinstance(address, dict):
        parts = [
            address.get("addressLocality", ""),
            address.get("addressRegion", ""),
        ]
        data["ld_location"] = ", ".join(p for p in parts if p)

    return data


def _parse_offer_ld(offers: dict) -> Dict:
    """Parse schema.org Offer JSON-LD for price info."""
    data = {}
    if offers.get("price"):
        try:
            data["ld_price"] = float(offers["price"])
        except (ValueError, TypeError):
            data["ld_price_raw"] = str(offers["price"])
    if offers.get("priceCurrency"):
        data["ld_currency"] = offers["priceCurrency"]
    if offers.get("availability"):
        avail = offers["availability"]
        data["ld_availability"] = avail.replace("https://schema.org/", "").replace("http://schema.org/", "")
    if offers.get("seller"):
        seller = offers["seller"]
        data["ld_seller"] = seller.get("name", str(seller)) if isinstance(seller, dict) else str(seller)
    if offers.get("url"):
        data["ld_offer_url"] = offers["url"]
    return data


def _parse_breadcrumbs(item: dict) -> List[str]:
    """Extract breadcrumb trail from BreadcrumbList."""
    elements = item.get("itemListElement", [])
    crumbs = []
    for el in sorted(elements, key=lambda x: x.get("position", 0)):
        name = el.get("name", "")
        if name:
            crumbs.append(name)
    return crumbs


# ── Main fetch + extract ──────────────────────────────────────────────────

def fetch_seo_metadata(url: str) -> Optional[Dict]:
    """Fetch a URL and extract all SEO metadata (OG tags + JSON-LD).

    Returns dict with keys:
      - og_*: Open Graph / meta tag values
      - ld_*: JSON-LD structured data values
      - is_live: True if page returned 200
      - is_listing: True if metadata suggests this is a product/listing page
    """
    try:
        with httpx.Client(
            timeout=8.0,
            headers=_HEADERS,
            follow_redirects=True,
            max_redirects=3,
        ) as client:
            resp = client.get(url)
    except Exception as e:
        logger.debug(f"Failed to fetch {url}: {e}")
        return None

    if resp.status_code in (404, 410, 403):
        return {"is_live": False, "is_listing": False, "status_code": resp.status_code}

    if resp.status_code != 200:
        return {"is_live": False, "is_listing": False, "status_code": resp.status_code}

    content_type = resp.headers.get("content-type", "")
    if "text/html" not in content_type:
        return {"is_live": True, "is_listing": False}

    html = resp.text[:_MAX_CONTENT_LENGTH]
    soup = BeautifulSoup(html, "html.parser")

    # Extract both sources
    og_data = _extract_og_tags(soup)
    ld_data = _extract_jsonld(soup)

    # Merge into single result
    result = {"is_live": True}

    # OG data (prefixed)
    for k, v in og_data.items():
        result[f"og_{k}"] = v

    # JSON-LD data (already prefixed with ld_)
    result.update(ld_data)

    # Determine best price
    result["final_price"] = _best_price(result)

    # Determine best title
    result["final_title"] = (
        ld_data.get("ld_title")
        or og_data.get("title")
        or ""
    )

    # Determine best image
    result["final_image"] = (
        ld_data.get("ld_image")
        or og_data.get("image")
    )

    # Is this a listing page?
    result["is_listing"] = _is_listing_page(result, url)

    return result


def _best_price(data: dict) -> Optional[float]:
    """Pick the best price from all available sources."""
    # JSON-LD price is most reliable
    if data.get("ld_price"):
        return float(data["ld_price"])

    # OG price
    og_price = data.get("og_price")
    if og_price:
        parsed = _parse_price(og_price)
        if parsed:
            return parsed

    # Extract from title/description text
    text = f"{data.get('og_title', '')} {data.get('og_description', '')}"
    return _extract_price_from_text(text)


def _is_listing_page(data: dict, url: str) -> bool:
    """Determine if the metadata indicates this is an individual listing."""
    # JSON-LD product/vehicle/real-estate = definitely a listing
    ld_type = data.get("ld_type", "")
    if ld_type in ("Product", "Vehicle", "RealEstate"):
        return True

    # OG type = product
    og_type = data.get("og_type", "").lower()
    if og_type in ("product", "product.item", "og:product"):
        return True

    # Has price in structured data
    if data.get("ld_price") or data.get("og_price"):
        return True

    # Availability info present
    if data.get("ld_availability"):
        return True

    # Known listing domain + has title = likely listing
    url_lower = url.lower()
    if any(d in url_lower for d in PRIMARY_DOMAINS + LISTING_DOMAINS):
        if data.get("final_title"):
            return True

    return False


# ── Batch verify pipeline ─────────────────────────────────────────────────

def enrich_candidates_with_seo(
    candidates: List[dict],
    wishlist: dict,
    max_fetch: int = 20,
) -> List[dict]:
    """Fetch SEO metadata for top candidates and enrich/re-score them.

    Pipeline:
    1. Sort candidates by initial search score
    2. Fetch top N pages, extract OG + JSON-LD metadata
    3. Reject dead links and non-listing pages
    4. Enrich candidate with verified title, price, image, specs
    5. Adjust score based on verified data quality
    6. Return enriched + re-sorted candidates

    Args:
        candidates: pre-scored candidates from search APIs
        wishlist: the wishlist dict
        max_fetch: max URLs to fetch (rate limit)
    """
    if not candidates:
        return []

    candidates.sort(key=lambda x: x.get("score", 0), reverse=True)
    to_fetch = candidates[:max_fetch]
    rest = candidates[max_fetch:]

    filters = wishlist.get("filters_json") or {}
    if not isinstance(filters, dict):
        filters = {}

    enriched = []
    for candidate in to_fetch:
        url = candidate.get("url", "")
        seo = fetch_seo_metadata(url)

        if seo is None:
            # Network error — keep with small penalty
            candidate["score"] = max(0, candidate.get("score", 0) - 5)
            candidate["verified"] = False
            enriched.append(candidate)
            continue

        if not seo.get("is_live"):
            # Dead link — reject
            logger.debug(f"Dead link ({seo.get('status_code')}): {url}")
            continue

        if not seo.get("is_listing"):
            # Not a listing page — reject
            logger.debug(f"Not a listing (no product metadata): {url}")
            continue

        # ── Enrich candidate with verified data ──
        score_adj = 0

        # Title from metadata
        if seo.get("final_title"):
            candidate["title"] = seo["final_title"]
            score_adj += 3

        # Price from structured data
        if seo.get("final_price"):
            candidate["price"] = seo["final_price"]
            currency = seo.get("ld_currency", "INR")
            price_val = seo["final_price"]
            if currency == "INR":
                candidate["formatted_price"] = f"\u20b9{int(price_val):,}"
            score_adj += 5  # verified price is valuable

        # Image
        if seo.get("final_image"):
            candidate["image_url"] = seo["final_image"]
            score_adj += 2

        # Brand match from JSON-LD
        wishlist_brand = (filters.get("brand") or "").lower()
        ld_brand = (seo.get("ld_brand") or "").lower()
        if wishlist_brand and ld_brand and wishlist_brand in ld_brand:
            score_adj += 5  # confirmed brand match

        # Model match
        wishlist_model = (filters.get("model") or "").lower()
        ld_model = (seo.get("ld_model") or "").lower()
        ld_title = (seo.get("ld_title") or "").lower()
        if wishlist_model and (wishlist_model in ld_model or wishlist_model in ld_title):
            score_adj += 5  # confirmed model match

        # Year match (vehicles)
        wishlist_year = str(filters.get("year", "")).strip()
        ld_year = seo.get("ld_year", "")
        if wishlist_year and ld_year and wishlist_year in str(ld_year):
            score_adj += 3

        # Price within budget (verified)
        budget = filters.get("price") or filters.get("max_price") or filters.get("budget")
        verified_price = seo.get("final_price")
        if budget and verified_price:
            budget_f = float(budget)
            if verified_price <= budget_f:
                score_adj += 5  # confirmed within budget
            elif verified_price <= budget_f * 1.15:
                score_adj += 0  # slightly over, neutral
            else:
                score_adj -= 10  # over budget

        # Location match
        wishlist_location = (filters.get("location") or "").lower()
        ld_location = (seo.get("ld_location") or "").lower()
        og_desc = (seo.get("og_description") or "").lower()
        if wishlist_location:
            if wishlist_location in ld_location:
                score_adj += 5
            elif wishlist_location in og_desc:
                score_adj += 3

        # Availability check
        avail = (seo.get("ld_availability") or "").lower()
        if "outofstock" in avail or "discontinued" in avail or "soldout" in avail:
            logger.debug(f"Out of stock: {url}")
            continue  # skip unavailable items

        # Vehicle-specific specs
        specs = {}
        for key in ("ld_fuel_type", "ld_transmission", "ld_km_driven", "ld_year",
                     "ld_color", "ld_rooms", "ld_area", "ld_condition"):
            val = seo.get(key)
            if val:
                specs[key.replace("ld_", "")] = val
        if specs:
            candidate["specs"] = specs

        # Seller info
        if seo.get("ld_seller"):
            candidate["seller"] = seo["ld_seller"]

        # Rating
        if seo.get("ld_rating"):
            candidate["rating"] = seo["ld_rating"]

        # Apply score adjustment
        old_score = candidate.get("score", 0)
        candidate["score"] = max(0, min(100, old_score + score_adj))
        candidate["verified"] = True
        enriched.append(candidate)

    # Add un-fetched candidates with penalty
    for c in rest:
        c["verified"] = False
        c["score"] = max(0, c.get("score", 0) - 5)
        enriched.append(c)

    # Final sort + minimum threshold
    enriched.sort(key=lambda x: x["score"], reverse=True)
    final = [c for c in enriched if c["score"] >= 25]

    verified_count = sum(1 for c in final if c.get("verified"))
    rejected = len(to_fetch) - sum(1 for c in enriched if c.get("verified"))
    logger.info(
        f"SEO enrichment: {len(to_fetch)} fetched, {verified_count} verified, "
        f"{rejected} rejected, {len(final)} final matches"
    )
    return final
