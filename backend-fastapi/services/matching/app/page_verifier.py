"""Page Content Verifier — fetches listing URLs and extracts real data.

After search APIs return candidate URLs, this module visits each page to:
1. Confirm it's a real, live listing (not a 404, blog, or dead link)
2. Extract actual price, title, and key specs from the HTML
3. Re-score the match using verified data instead of search snippets
4. Reject pages that are clearly not individual item listings

This is the final quality gate before a match is stored.
"""

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

# Browser-like headers to avoid being blocked
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-IN,en;q=0.9,hi;q=0.8",
}

# Max page size to download (500KB — listings are lightweight)
_MAX_CONTENT_LENGTH = 500_000


# ── Site-specific extractors ──────────────────────────────────────────────

def _extract_olx(soup: BeautifulSoup, url: str) -> Dict:
    """Extract listing data from OLX India pages."""
    data = {}

    # Title: <h1> or [data-aut-id="itemTitle"]
    title_el = (
        soup.select_one("[data-aut-id='itemTitle']")
        or soup.select_one("h1")
    )
    if title_el:
        data["verified_title"] = title_el.get_text(strip=True)

    # Price: [data-aut-id="itemPrice"] or class containing "price"
    price_el = (
        soup.select_one("[data-aut-id='itemPrice']")
        or soup.select_one("[class*='price' i]")
    )
    if price_el:
        price_text = price_el.get_text(strip=True)
        data["verified_price"] = _extract_price_from_text(price_text)
        data["verified_price_display"] = price_text

    # Location
    loc_el = (
        soup.select_one("[data-aut-id='itemLocation']")
        or soup.select_one("[class*='location' i]")
    )
    if loc_el:
        data["verified_location"] = loc_el.get_text(strip=True)

    # Key details / specs
    specs = {}
    for detail in soup.select("[data-aut-id='itemAttribute'], [class*='detail' i] li"):
        text = detail.get_text(strip=True)
        if ":" in text:
            k, v = text.split(":", 1)
            specs[k.strip().lower()] = v.strip()
    if specs:
        data["verified_specs"] = specs

    # Image
    img_el = soup.select_one("[data-aut-id='itemImage'] img, [class*='gallery' i] img")
    if img_el:
        data["verified_image"] = img_el.get("src") or img_el.get("data-src")

    # Listing status — check if sold/expired
    page_text = soup.get_text().lower()
    if "this ad has expired" in page_text or "this item has been sold" in page_text:
        data["is_dead"] = True

    data["is_listing"] = bool(data.get("verified_title") and data.get("verified_price"))
    return data


def _extract_nobroker(soup: BeautifulSoup, url: str) -> Dict:
    """Extract listing data from NoBroker pages."""
    data = {}

    title_el = soup.select_one("h1, [class*='heading' i]")
    if title_el:
        data["verified_title"] = title_el.get_text(strip=True)

    # Price: NoBroker shows rent or sale price
    price_el = soup.select_one("[class*='price' i], [class*='rent' i]")
    if price_el:
        price_text = price_el.get_text(strip=True)
        data["verified_price"] = _extract_price_from_text(price_text)
        data["verified_price_display"] = price_text

    # Location / address
    loc_el = soup.select_one("[class*='address' i], [class*='location' i]")
    if loc_el:
        data["verified_location"] = loc_el.get_text(strip=True)

    # Specs: BHK, area, furnishing
    specs = {}
    for item in soup.select("[class*='detail' i] span, [class*='info' i] span"):
        text = item.get_text(strip=True).lower()
        if "bhk" in text:
            specs["bhk"] = text
        elif "sq" in text or "sqft" in text:
            specs["area"] = text
        elif "furnished" in text or "unfurnished" in text:
            specs["furnishing"] = text
    if specs:
        data["verified_specs"] = specs

    img_el = soup.select_one("[class*='gallery' i] img, [class*='image' i] img")
    if img_el:
        data["verified_image"] = img_el.get("src") or img_el.get("data-src")

    data["is_listing"] = bool(data.get("verified_title"))
    return data


def _extract_generic(soup: BeautifulSoup, url: str) -> Dict:
    """Generic extractor for any marketplace — uses common HTML patterns."""
    data = {}

    # Title: prefer h1
    title_el = soup.select_one("h1")
    if title_el:
        data["verified_title"] = title_el.get_text(strip=True)[:200]

    # Price: look for structured data first (JSON-LD), then HTML
    price = _extract_jsonld_price(soup)
    if not price:
        for selector in [
            "[class*='price' i]", "[class*='Price']",
            "[itemprop='price']", "[class*='amount' i]",
        ]:
            el = soup.select_one(selector)
            if el:
                price_text = el.get_text(strip=True)
                price = _extract_price_from_text(price_text)
                if price:
                    data["verified_price_display"] = price_text
                    break
    data["verified_price"] = price

    # Location
    for selector in ["[class*='location' i]", "[itemprop='addressLocality']", "[class*='address' i]"]:
        el = soup.select_one(selector)
        if el:
            data["verified_location"] = el.get_text(strip=True)[:100]
            break

    # Image: og:image or first product image
    og_img = soup.select_one("meta[property='og:image']")
    if og_img:
        data["verified_image"] = og_img.get("content")

    # Check if it's really a listing: must have title + (price or specific listing signals)
    page_text = soup.get_text().lower()
    listing_signals = [
        "add to cart", "buy now", "contact seller", "make offer",
        "chat with seller", "call seller", "enquire now", "book now",
        "emi available", "view phone", "schedule visit",
    ]
    has_listing_signal = any(sig in page_text for sig in listing_signals)
    data["is_listing"] = bool(data.get("verified_title") and (price or has_listing_signal))

    # Dead listing checks
    dead_signals = [
        "page not found", "404", "this listing has been removed",
        "no longer available", "expired", "sold out", "item sold",
    ]
    if any(sig in page_text[:2000] for sig in dead_signals):
        data["is_dead"] = True

    return data


def _extract_jsonld_price(soup: BeautifulSoup) -> Optional[float]:
    """Extract price from JSON-LD structured data (schema.org Product/Offer)."""
    import json
    for script in soup.select("script[type='application/ld+json']"):
        try:
            ld = json.loads(script.string or "")
            # Handle single object or list
            items = ld if isinstance(ld, list) else [ld]
            for item in items:
                if item.get("@type") in ("Product", "Vehicle", "RealEstateListing", "Offer"):
                    # Direct price
                    if "price" in item:
                        return float(item["price"])
                    # Nested offers
                    offers = item.get("offers", {})
                    if isinstance(offers, list):
                        offers = offers[0] if offers else {}
                    if "price" in offers:
                        return float(offers["price"])
        except (json.JSONDecodeError, ValueError, TypeError, IndexError):
            continue
    return None


# ── Dispatcher ────────────────────────────────────────────────────────────

_SITE_EXTRACTORS = {
    "olx.in": _extract_olx,
    "nobroker.in": _extract_nobroker,
}


def _get_extractor(url: str):
    """Return the best extractor function for a URL."""
    url_lower = url.lower()
    for domain, extractor in _SITE_EXTRACTORS.items():
        if domain in url_lower:
            return extractor
    return _extract_generic


# ── Main verification pipeline ────────────────────────────────────────────

def verify_candidate(candidate: dict, wishlist: dict) -> Tuple[dict, int]:
    """Fetch a candidate URL and verify it's a real listing matching the wishlist.

    Returns:
        (updated_candidate, score_adjustment)
        - score_adjustment: positive = boost, negative = penalize, -999 = reject
    """
    url = candidate.get("url", "")
    if not url:
        return candidate, -999

    try:
        with httpx.Client(
            timeout=10.0,
            headers=_HEADERS,
            follow_redirects=True,
            max_redirects=3,
        ) as client:
            resp = client.get(url)
    except Exception as e:
        logger.debug(f"Failed to fetch {url}: {e}")
        return candidate, -10  # can't verify, slight penalty

    # Dead link
    if resp.status_code in (404, 410, 403, 500, 502, 503):
        logger.debug(f"Dead link ({resp.status_code}): {url}")
        return candidate, -999  # reject

    if resp.status_code != 200:
        return candidate, -5

    # Check content type
    content_type = resp.headers.get("content-type", "")
    if "text/html" not in content_type:
        return candidate, -999

    # Limit content size
    html = resp.text[:_MAX_CONTENT_LENGTH]
    soup = BeautifulSoup(html, "html.parser")

    # Run site-specific or generic extractor
    extractor = _get_extractor(url)
    extracted = extractor(soup, url)

    # ── Reject dead listings ──
    if extracted.get("is_dead"):
        logger.debug(f"Dead/expired listing: {url}")
        return candidate, -999

    # ── Reject non-listings ──
    if not extracted.get("is_listing"):
        logger.debug(f"Not a listing page: {url}")
        return candidate, -999

    # ── Update candidate with verified data ──
    score_adj = 0

    if extracted.get("verified_title"):
        candidate["title"] = extracted["verified_title"]
        score_adj += 5  # reward: we have real title

    if extracted.get("verified_price"):
        candidate["price"] = extracted["verified_price"]
        candidate["formatted_price"] = extracted.get("verified_price_display")
        score_adj += 5  # reward: we have real price

    if extracted.get("verified_location"):
        candidate["location"] = extracted["verified_location"]

    if extracted.get("verified_image"):
        candidate["image_url"] = extracted["verified_image"]

    if extracted.get("verified_specs"):
        candidate["specs"] = extracted["verified_specs"]

    # ── Re-check price against wishlist budget ──
    filters = wishlist.get("filters_json") or {}
    if isinstance(filters, dict):
        budget = filters.get("price") or filters.get("max_price") or filters.get("budget")
        verified_price = extracted.get("verified_price")
        if budget and verified_price:
            budget_f = float(budget)
            if verified_price <= budget_f:
                score_adj += 5  # confirmed within budget
            elif verified_price <= budget_f * 1.15:
                score_adj += 0  # slightly over, neutral
            else:
                score_adj -= 15  # way over budget

    # ── Re-check keywords in verified title ──
    brand = (filters.get("brand") or "").lower() if isinstance(filters, dict) else ""
    model = (filters.get("model") or "").lower() if isinstance(filters, dict) else ""
    verified_title_lower = (extracted.get("verified_title") or "").lower()

    if brand and brand in verified_title_lower:
        score_adj += 5
    if model and model in verified_title_lower:
        score_adj += 5

    return candidate, score_adj


def verify_and_filter_candidates(
    candidates: List[dict], wishlist: dict, max_verify: int = 20
) -> List[dict]:
    """Verify top candidates by fetching their pages.

    Only verifies top `max_verify` candidates (sorted by search score) to
    limit HTTP requests. Rejected candidates are removed entirely.

    Args:
        candidates: pre-scored candidates from search APIs
        wishlist: the wishlist dict
        max_verify: max number of URLs to fetch (rate limiting)

    Returns:
        Verified and re-scored candidates, sorted by final score.
    """
    if not candidates:
        return []

    # Sort by initial score, verify top N
    candidates.sort(key=lambda x: x.get("score", 0), reverse=True)
    to_verify = candidates[:max_verify]
    skip_verify = candidates[max_verify:]

    verified = []
    for candidate in to_verify:
        updated, score_adj = verify_candidate(candidate, wishlist)

        if score_adj == -999:
            # Rejected — dead link, not a listing, etc.
            logger.debug(f"Rejected after verification: {candidate.get('url', '')}")
            continue

        # Adjust score
        old_score = updated.get("score", 0)
        new_score = max(0, min(100, old_score + score_adj))
        updated["score"] = new_score
        updated["verified"] = True
        verified.append(updated)

    # Add unverified candidates (beyond max_verify) with a small penalty
    for c in skip_verify:
        c["verified"] = False
        c["score"] = max(0, c.get("score", 0) - 5)
        verified.append(c)

    # Final sort and minimum threshold
    verified.sort(key=lambda x: x["score"], reverse=True)
    final = [c for c in verified if c["score"] >= 30]

    logger.info(
        f"Verification: {len(to_verify)} checked, "
        f"{len(verified)} passed, {len(to_verify) - len([v for v in verified if v.get('verified')])} rejected"
    )
    return final
