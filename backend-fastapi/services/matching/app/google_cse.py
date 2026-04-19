"""Google Custom Search Engine (CSE) integration for wishlist matching.

Official Google API — $5 per 1000 queries, 100 queries/day free tier.
Complements SerperDev with an independent search source and returns
results in the same format for unified scoring.

Setup:
  1. Create a Programmable Search Engine at https://programmablesearchengine.google.com
  2. Enable "Search the entire web"
  3. Get the Search Engine ID (cx)
  4. Enable Custom Search API in Google Cloud Console
  5. Create an API key
  6. Set GOOGLE_CSE_API_KEY and GOOGLE_CSE_CX in environment
"""

import logging
from typing import List

import httpx
from shared.config.settings import get_settings
from app.serper import (
    build_serper_queries,
    _compute_match_score,
    _extract_price_from_text,
    _is_category_page,
    _is_rejected_domain,
    _get_must_have_keywords,
    _title_has_keyword,
    _detect_source,
    LISTING_URL_PATTERNS,
)

logger = logging.getLogger(__name__)

CSE_URL = "https://www.googleapis.com/customsearch/v1"


def search_google_cse(queries: List[str], num_results: int = 10) -> List[dict]:
    """Call Google Custom Search API and return raw results."""
    settings = get_settings().google_cse
    if not settings.api_key or not settings.cx:
        logger.debug("Google CSE not configured, skipping")
        return []

    results = []
    seen_urls = set()

    for query in queries:
        try:
            with httpx.Client(timeout=15.0) as client:
                resp = client.get(
                    CSE_URL,
                    params={
                        "key": settings.api_key,
                        "cx": settings.cx,
                        "q": query,
                        "num": min(num_results, 10),
                        "gl": "in",
                        "cr": "countryIN",
                    },
                )
                resp.raise_for_status()
                data = resp.json()
        except Exception as e:
            logger.error(f"Google CSE search failed for '{query}': {e}", exc_info=True)
            continue

        for idx, item in enumerate(data.get("items", []), 1):
            url = item.get("link", "")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)

            title = item.get("title", "")
            snippet = item.get("snippet", "")
            price = _extract_price_from_text(f"{title} {snippet}")

            # Extract image from pagemap if available
            image_url = None
            pagemap = item.get("pagemap", {})
            cse_images = pagemap.get("cse_image", [])
            if cse_images and isinstance(cse_images, list):
                image_url = cse_images[0].get("src")

            results.append({
                "url": url,
                "source": _detect_source(url),
                "title": title,
                "description": snippet,
                "price": price,
                "formatted_price": None,
                "image_url": image_url,
                "position": idx,
            })

    logger.info(f"Google CSE returned {len(results)} raw results for {len(queries)} queries")
    return results


def search_and_score_google_cse(wishlist: dict) -> List[dict]:
    """Search Google CSE for a wishlist, apply same strict filtering as SerperDev."""
    queries = build_serper_queries(wishlist)
    if not queries:
        return []

    raw_results = search_google_cse(queries)
    if not raw_results:
        return []

    filters = wishlist.get("filters_json") or {}
    if not isinstance(filters, dict):
        filters = {}
    must_have = _get_must_have_keywords(wishlist, filters)

    scored = []
    for r in raw_results:
        url = r["url"]
        if _is_rejected_domain(url):
            continue
        if _is_category_page(url):
            continue
        if must_have and not _title_has_keyword(r["title"], must_have):
            continue

        score = _compute_match_score(r, wishlist)
        if LISTING_URL_PATTERNS.search(url):
            score += 10
        score = min(score, 100)

        if score < 30:
            continue

        r["score"] = score
        scored.append(r)

    scored.sort(key=lambda x: x["score"], reverse=True)
    logger.info(f"Google CSE scored {len(scored)} exact matches for '{wishlist.get('title', '')}'")
    return scored
