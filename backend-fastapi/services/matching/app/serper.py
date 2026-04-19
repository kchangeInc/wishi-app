"""SerperDev Google Search integration for wishlist matching.

Builds highly specific search queries using Google operators (intitle:, site:,
inurl:) to find EXACT individual item listings on OLX, NoBroker, and other
Indian marketplaces. Aggressively filters out blogs, reviews, comparison
pages, and category pages — only real buyable listings pass through.
"""

import logging
import re
from typing import List, Optional
from urllib.parse import urlparse

import httpx
from shared.config.settings import get_settings

logger = logging.getLogger(__name__)

SERPER_URL = "https://google.serper.dev/search"

# Primary marketplaces — highest trust + scoring
PRIMARY_DOMAINS = ["olx.in", "nobroker.in"]

# All known listing domains
LISTING_DOMAINS = [
    "olx.in", "nobroker.in",
    "cars24.com", "spinny.com", "cardekho.com", "carwale.com",
    "bikewale.com", "bikedekho.com", "99acres.com", "magicbricks.com",
    "housing.com", "flipkart.com", "amazon.in",
    "snapdeal.com", "quikr.com", "droom.in", "cartrade.com",
    "truebil.com", "credr.com", "cashify.in",
]

# URL path patterns that prove this is an INDIVIDUAL listing (not a search/category)
LISTING_URL_PATTERNS = re.compile(
    r"/item/"               # OLX individual listing
    r"|/property/\d+"       # NoBroker property ID
    r"|/detail/"            # NoBroker detail page
    r"|/buy-used-[^/]+/\w+" # Cars24 individual car
    r"|/used-car-details/"  # CarDekho individual
    r"|/p/"                 # Flipkart product
    r"|/dp/"                # Amazon product
    r"|/gp/product/"        # Amazon product alt
    r"|/property-in-"       # 99acres individual
    r"|/rent-\d+"           # NoBroker rent listing
    r"|/sale-\d+"           # NoBroker sale listing
    r"|/pg-\d+"             # NoBroker PG listing
    r"|/[a-z]+-for-sale-"   # OLX listing pattern
    r"|/ad/"                # Quikr ad
    r"|-iid-"              # OLX item ID in URL
    , re.IGNORECASE,
)

# URL patterns that are DEFINITELY not individual listings — reject immediately
REJECT_URL_PATTERNS = re.compile(
    r"/search\b"
    r"|/category/"
    r"|/browse/"
    r"|/results\b"
    r"|/all-"
    r"|/best-\d+"
    r"|/top-\d+"
    r"|/compare/"
    r"|/review[s]?"
    r"|/news/"
    r"|/blog/"
    r"|/article/"
    r"|/guide/"
    r"|/tips/"
    r"|/how-to"
    r"|/price-list"
    r"|/pricelist"
    r"|/specifications"
    r"|/on-road-price"
    r"|/mileage"
    r"|/variants"
    r"|/colours"
    r"|/images"
    r"|/video[s]?"
    r"|/faq"
    r"|/dealer[s]?"
    r"|wikipedia\.org"
    r"|youtube\.com"
    r"|cardekho\.com/[^/]+/?$"      # CarDekho brand-only pages
    r"|carwale\.com/[^/]+/?$"       # CarWale brand-only pages
    r"|olx\.in/[^/]+/?$"            # OLX city-level pages
    , re.IGNORECASE,
)

# Domains that are NEVER individual listings (news, blogs, review sites)
REJECT_DOMAINS = [
    "youtube.com", "wikipedia.org", "quora.com", "reddit.com",
    "team-bhp.com", "cardekho.com/news", "zigwheels.com",
    "carandbike.com", "financialexpress.com", "cartoq.com",
    "rushlane.com", "motorbeam.com", "gaadiwaadi.com",
    "indianautosblog.com", "autocarindia.com",
]


# ── Query builder ─────────────────────────────────────────────────────────

def build_serper_queries(wishlist: dict) -> List[str]:
    """Build highly targeted search queries that find individual listings only.

    Uses intitle: and site: operators to force Google to return only pages
    whose TITLE contains the product name on known marketplace domains.
    """
    title = (wishlist.get("title") or "").strip()
    if not title:
        return []

    filters = wishlist.get("filters_json") or {}
    if not isinstance(filters, dict):
        filters = {}

    brand = filters.get("brand", "")
    model = filters.get("model", "")
    year = filters.get("year", "")
    fuel_type = filters.get("fuelType", "")
    location = filters.get("location", "")
    price = filters.get("price") or filters.get("max_price") or filters.get("budget")
    item_type = filters.get("itemType", "")
    condition = filters.get("condition", "")
    bedrooms = filters.get("bedrooms", "")
    property_type = filters.get("propertyType", "")

    # Build exact product term from structured fields
    product_parts = []
    if brand:
        product_parts.append(brand)
    if model:
        product_parts.append(model)
    if year:
        product_parts.append(str(year))
    if fuel_type:
        product_parts.append(fuel_type)
    if item_type:
        product_parts.append(item_type)
    if property_type:
        product_parts.append(property_type)
    if bedrooms:
        product_parts.append(f"{bedrooms} BHK")
    if condition:
        product_parts.append(condition)

    product = " ".join(product_parts) if product_parts else title

    # Core keywords that MUST appear in results (brand + model minimum)
    core_term = f"{brand} {model}".strip() if (brand or model) else title

    queries = []
    category = (wishlist.get("category") or "").lower()
    subcategory = (wishlist.get("subcategory") or "").lower()

    # ── Query 1: OLX exact listing search ──
    q1 = f'site:olx.in intitle:"{core_term}"'
    if location:
        q1 += f" {location}"
    queries.append(q1)

    # ── Query 2: NoBroker exact listing search ──
    if category in ("real estate", "") or subcategory in ("flat", "house", "plot", "rent", "pg", "pg/hostel", ""):
        q2 = f'site:nobroker.in intitle:"{core_term}"'
        if location:
            q2 += f" {location}"
        queries.append(q2)

    # ── Query 3: Category-specific secondary marketplace ──
    secondary_sites = _get_secondary_sites(category, subcategory)
    for site in secondary_sites[:2]:
        q = f'site:{site} intitle:"{core_term}"'
        if location:
            q += f" {location}"
        queries.append(q)

    # ── Query 4: Broad search with exact phrase + listing keywords ──
    q_broad = f'"{core_term}" ("for sale" OR "₹" OR "price")'
    if location:
        q_broad += f" {location}"
    if price:
        q_broad += f" under ₹{price}"
    # Exclude known non-listing sites
    q_broad += " -review -comparison -mileage -specifications"
    queries.append(q_broad)

    # ── Query 5: OLX with full product details + inurl:item ──
    q5 = f"site:olx.in {product}"
    if location:
        q5 += f" {location}"
    q5 += " inurl:item"
    queries.append(q5)

    return queries


def _get_secondary_sites(category: str, subcategory: str) -> List[str]:
    """Return secondary marketplace domains for the given category."""
    if category == "automobile" or subcategory in ("car", "bike", "scooter"):
        if subcategory == "car":
            return ["cars24.com", "spinny.com", "cardekho.com"]
        elif subcategory in ("bike", "scooter"):
            return ["bikewale.com", "bikedekho.com"]
        return ["cars24.com"]
    elif category == "real estate" or subcategory in ("flat", "house", "plot", "pg", "rent"):
        return ["99acres.com", "magicbricks.com", "housing.com"]
    elif category == "electronics":
        return ["flipkart.com", "amazon.in"]
    elif category == "fashion":
        return ["flipkart.com", "amazon.in"]
    elif category == "home & living":
        return ["flipkart.com", "amazon.in"]
    return []


# ── SerperDev API caller ──────────────────────────────────────────────────

def search_serper(queries: List[str], num_results: int = 10) -> List[dict]:
    """Call SerperDev API and return raw results."""
    api_key = get_settings().serper.api_key
    if not api_key:
        logger.warning("SERPER_API_KEY not configured, skipping SerperDev search")
        return []

    results = []
    seen_urls = set()

    for query in queries:
        try:
            with httpx.Client(timeout=15.0) as client:
                resp = client.post(
                    SERPER_URL,
                    headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
                    json={"q": query, "location": "India", "gl": "in", "num": num_results},
                )
                resp.raise_for_status()
                data = resp.json()
        except Exception as e:
            logger.error(f"SerperDev search failed for query '{query}': {e}", exc_info=True)
            continue

        for item in data.get("organic", []):
            url = item.get("link", "")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            results.append({
                "url": url,
                "source": _detect_source(url),
                "title": item.get("title", ""),
                "description": item.get("snippet", ""),
                "price": _extract_price_from_text(
                    item.get("title", "") + " " + item.get("snippet", "")
                ),
                "formatted_price": None,
                "position": item.get("position", 99),
            })

        for item in data.get("shopping", []):
            url = item.get("link", "")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            price_raw = item.get("price", "")
            results.append({
                "url": url,
                "source": _detect_source(url),
                "title": item.get("title", ""),
                "description": item.get("source", ""),
                "price": _parse_price(price_raw),
                "formatted_price": str(price_raw) if price_raw else None,
                "position": item.get("position", 99),
            })

    logger.info(f"SerperDev returned {len(results)} raw results for {len(queries)} queries")
    return results


def _detect_source(url: str) -> str:
    """Detect which marketplace a URL belongs to."""
    url_lower = url.lower()
    for domain in PRIMARY_DOMAINS + LISTING_DOMAINS:
        if domain in url_lower:
            return domain.split(".")[0]  # "olx", "nobroker", "cars24", etc.
    return "web"


# ── Score + filter pipeline ───────────────────────────────────────────────

def search_and_score_for_wishlist(wishlist: dict) -> List[dict]:
    """Search SerperDev for a wishlist, aggressively filter and score results.

    Pipeline:
    1. Reject known non-listing domains (blogs, news, youtube)
    2. Reject URLs matching category/search page patterns
    3. Require at least one core keyword in result title
    4. Score remaining results (0-100)
    5. Only return score >= 30 (was > 0 — too lenient)
    6. Boost results from known listing URL patterns
    """
    queries = build_serper_queries(wishlist)
    if not queries:
        return []

    raw_results = search_serper(queries)
    if not raw_results:
        return []

    filters = wishlist.get("filters_json") or {}
    if not isinstance(filters, dict):
        filters = {}

    # Core keywords that result title MUST contain at least one of
    must_have = _get_must_have_keywords(wishlist, filters)

    scored = []
    for r in raw_results:
        url = r["url"]

        # Step 1: Reject non-listing domains
        if _is_rejected_domain(url):
            continue

        # Step 2: Reject category/search page URLs
        if _is_category_page(url):
            continue

        # Step 3: Check title contains at least one core keyword
        if must_have and not _title_has_keyword(r["title"], must_have):
            continue

        # Step 4: Score
        score = _compute_match_score(r, wishlist)

        # Step 5: Bonus for URLs that match known listing patterns
        if LISTING_URL_PATTERNS.search(url):
            score += 10  # confirmed individual listing URL

        score = min(score, 100)

        # Step 6: Minimum threshold
        if score < 30:
            continue

        r["score"] = score
        scored.append(r)

    scored.sort(key=lambda x: x["score"], reverse=True)
    logger.info(
        f"SerperDev: {len(raw_results)} raw -> {len(scored)} exact matches "
        f"for '{wishlist.get('title', '')}'"
    )
    return scored


def _get_must_have_keywords(wishlist: dict, filters: dict) -> List[str]:
    """Return keywords that must appear in result title for it to be relevant.

    At least one of brand, model, or first 2 words of title must match.
    """
    keywords = []
    brand = filters.get("brand", "").strip()
    model = filters.get("model", "").strip()

    if brand:
        keywords.append(brand.lower())
    if model:
        keywords.append(model.lower())

    # If no structured fields, use significant words from title
    if not keywords:
        title_words = wishlist.get("title", "").lower().split()
        keywords = [w for w in title_words if len(w) > 3][:3]

    return keywords


def _title_has_keyword(result_title: str, must_have: List[str]) -> bool:
    """Check if result title contains at least one must-have keyword."""
    title_lower = result_title.lower()
    return any(kw in title_lower for kw in must_have)


def _is_rejected_domain(url: str) -> bool:
    """Return True if URL belongs to a known non-listing domain."""
    url_lower = url.lower()
    return any(domain in url_lower for domain in REJECT_DOMAINS)


def _is_category_page(url: str) -> bool:
    """Return True if URL is a category/search/review page, not an individual listing."""
    if REJECT_URL_PATTERNS.search(url):
        return True

    # URLs with very few path segments are usually category pages
    path = urlparse(url).path.rstrip("/")
    segments = [s for s in path.split("/") if s]
    if len(segments) <= 1:
        return True

    return False


# ── Scoring engine ────────────────────────────────────────────────────────

def _compute_match_score(result: dict, wishlist: dict) -> int:
    """Score a search result (0-100) based on exact match to wishlist.

    Scoring breakdown:
    - Brand+Model+Year keyword match in title:  up to 40 points
    - Price within budget:                       up to 20 points
    - Location match:                            up to 15 points
    - Domain quality (OLX/NoBroker top):         up to 15 points
    - Search position:                           up to 10 points
    """
    score = 0
    result_title = result.get("title", "").lower()
    result_text = (result_title + " " + result.get("description", "")).lower()

    filters = wishlist.get("filters_json") or {}
    if not isinstance(filters, dict):
        filters = {}

    # ── Keyword matching (up to 40 points) ──
    # Weight: brand=15, model=15, year=5, other=5
    brand = filters.get("brand", "").lower().strip()
    model = filters.get("model", "").lower().strip()
    year = str(filters.get("year", "")).strip()

    keyword_score = 0
    if brand and brand in result_title:
        keyword_score += 15
    elif brand and brand in result_text:
        keyword_score += 8  # in description but not title — weaker signal

    if model and model in result_title:
        keyword_score += 15
    elif model and model in result_text:
        keyword_score += 8

    if year and year in result_text:
        keyword_score += 5

    # Additional filters
    extra_keywords = []
    for key in ("fuelType", "itemType", "propertyType"):
        val = filters.get(key, "").lower().strip()
        if val:
            extra_keywords.append(val)
    bedrooms = filters.get("bedrooms", "")
    if bedrooms:
        extra_keywords.append(f"{bedrooms} bhk")

    if extra_keywords:
        extra_matched = sum(1 for kw in extra_keywords if kw in result_text)
        keyword_score += min(int((extra_matched / len(extra_keywords)) * 5), 5)

    # If no structured filters, fall back to title word overlap
    if not brand and not model:
        title_words = [w for w in wishlist.get("title", "").lower().split() if len(w) > 2]
        if title_words:
            matched_in_title = sum(1 for w in title_words if w in result_title)
            matched_in_text = sum(1 for w in title_words if w in result_text)
            # Prefer title matches over body matches
            keyword_score += min(int((matched_in_title / len(title_words)) * 30), 30)
            keyword_score += min(int(((matched_in_text - matched_in_title) / len(title_words)) * 10), 10)

    score += min(keyword_score, 40)

    # ── Price match (up to 20 points) ──
    budget = filters.get("price") or filters.get("max_price") or filters.get("budget")
    result_price = result.get("price")
    if budget and result_price:
        budget_f = float(budget)
        if budget_f > 0:
            if result_price <= budget_f:
                ratio = result_price / budget_f
                if ratio >= 0.5:
                    score += 20  # good price range
                elif ratio >= 0.3:
                    score += 12  # reasonable but might be lesser variant
                else:
                    score += 3   # suspiciously cheap, probably wrong item
            elif result_price <= budget_f * 1.15:
                score += 10  # slightly over budget
    elif budget:
        score += 3  # no price extracted, small credit

    # ── Location match (up to 15 points) ──
    location = (filters.get("location") or "").lower().strip()
    if location:
        if location in result_title:
            score += 15  # location in title = strong signal
        elif location in result_text:
            score += 10  # location in description
        else:
            city_parts = location.split()
            if any(part in result_text for part in city_parts if len(part) > 3):
                score += 6

    # ── Domain quality (up to 15 points) ──
    url = result.get("url", "").lower()
    if any(domain in url for domain in PRIMARY_DOMAINS):
        score += 15  # OLX, NoBroker
    elif any(domain in url for domain in LISTING_DOMAINS):
        score += 10
    elif ".in" in url:
        score += 3

    # ── Search position (up to 10 points) ──
    position = result.get("position", 99)
    if position <= 3:
        score += 10
    elif position <= 5:
        score += 7
    elif position <= 8:
        score += 4
    elif position <= 10:
        score += 2

    return min(score, 100)


# ── Price helpers ─────────────────────────────────────────────────────────

_PRICE_PATTERN = re.compile(
    r"₹\s*([\d,]+(?:\.\d+)?)|Rs\.?\s*([\d,]+(?:\.\d+)?)", re.IGNORECASE
)
_LAC_PATTERN = re.compile(r"([\d.]+)\s*(?:lac|lakh|l)\b", re.IGNORECASE)
_CR_PATTERN = re.compile(r"([\d.]+)\s*(?:cr|crore)\b", re.IGNORECASE)


def _extract_price_from_text(text: str) -> Optional[float]:
    """Extract price from text containing Indian price notations."""
    if not text:
        return None

    m = _CR_PATTERN.search(text)
    if m:
        try:
            return float(m.group(1)) * 10_000_000
        except ValueError:
            pass

    m = _LAC_PATTERN.search(text)
    if m:
        try:
            return float(m.group(1)) * 100_000
        except ValueError:
            pass

    m = _PRICE_PATTERN.search(text)
    if m:
        raw = m.group(1) or m.group(2)
        return _parse_price(raw)

    return None


def _parse_price(price_str) -> Optional[float]:
    """Parse a numeric price from a string like '₹89,999' or '1,234'."""
    if not price_str:
        return None
    if isinstance(price_str, (int, float)):
        return float(price_str)
    try:
        cleaned = "".join(c for c in str(price_str) if c.isdigit() or c == ".")
        return float(cleaned) if cleaned else None
    except (ValueError, TypeError):
        return None
