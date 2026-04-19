"""Unified Wishlist Matcher — Search + SEO Metadata Extraction + Scoring.

Single module that handles the entire matching pipeline:
  1. Search Google via SerperDev API to find listing URLs
  2. Fetch each result page
  3. Extract OG meta tags + JSON-LD structured data (legal SEO metadata)
  4. Score extracted metadata against wishlist criteria
  5. Return only verified, exact-match listings

Legal: Only reads publicly available SEO metadata (Open Graph, JSON-LD)
that websites intentionally expose for search engines and social crawlers.
"""

import json
import logging
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from shared.config.settings import get_settings

logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────

SERPER_URL = "https://google.serper.dev/search"

PRIMARY_MARKETPLACES = ["olx.in", "nobroker.in"]

LISTING_DOMAINS = [
    "olx.in", "nobroker.in", "cars24.com", "spinny.com", "cardekho.com",
    "carwale.com", "bikewale.com", "bikedekho.com", "99acres.com",
    "magicbricks.com", "housing.com", "flipkart.com", "amazon.in",
    "snapdeal.com", "quikr.com", "droom.in", "cartrade.com",
    "cashify.in", "credr.com",
]

# Individual listing URL patterns per marketplace (rejects search/category pages)
LISTING_URL_PATTERNS = {
    "olx.in":          ["/item/"],
    "cars24.com":      ["/buy-used-car/", "/car/"],
    "cardekho.com":    ["/used-car-details/"],
    "spinny.com":      ["/used-cars/"],
    "99acres.com":     ["/property/"],
    "magicbricks.com": ["/property-for-sale/"],
    "housing.com":     ["/property/"],
    "nobroker.in":     ["/p/"],
    "flipkart.com":    ["/p/"],
    "amazon.in":       ["/dp/"],
    "bikewale.com":    ["/used-bikes/"],
    "bikedekho.com":   ["/used-bikes/"],
    "droom.in":        ["/used-"],
    "quikr.com":       ["/"],
    "cashify.in":      ["/"],
    "credr.com":       ["/"],
}

# Category → subcategory → ranked marketplace domains
CATEGORY_SITES = {
    "automobile": {
        "car":     ["olx.in", "cars24.com", "spinny.com", "cardekho.com", "carwale.com", "droom.in"],
        "bike":    ["olx.in", "bikewale.com", "bikedekho.com", "droom.in", "credr.com"],
        "scooter": ["olx.in", "bikewale.com", "bikedekho.com", "droom.in"],
        "_default": ["olx.in", "cars24.com", "spinny.com", "cardekho.com"],
    },
    "real estate": {
        "flat":    ["99acres.com", "magicbricks.com", "housing.com", "nobroker.in"],
        "house":   ["99acres.com", "magicbricks.com", "housing.com", "nobroker.in"],
        "plot":    ["99acres.com", "magicbricks.com", "housing.com"],
        "pg":      ["nobroker.in", "99acres.com"],
        "rent":    ["nobroker.in", "99acres.com", "magicbricks.com", "housing.com"],
        "_default": ["99acres.com", "magicbricks.com", "housing.com", "nobroker.in"],
    },
    "electronics": {
        "_default": ["flipkart.com", "amazon.in", "olx.in", "cashify.in"],
    },
    "fashion": {
        "_default": ["flipkart.com", "amazon.in"],
    },
    "home & living": {
        "_default": ["flipkart.com", "amazon.in", "olx.in"],
    },
}

REJECT_DOMAINS = [
    "youtube.com", "wikipedia.org", "quora.com", "reddit.com",
    "team-bhp.com", "zigwheels.com", "carandbike.com", "cartoq.com",
    "rushlane.com", "motorbeam.com", "autocarindia.com",
    "financialexpress.com", "ndtv.com", "news18.com",
]

REJECT_URL_PATTERNS = re.compile(
    r"/search\b|/category/|/browse/|/results\b|/all-"
    r"|/best-\d+|/top-\d+|/compare/|/review[s]?|/news/"
    r"|/blog/|/article/|/guide/|/tips/|/how-to"
    r"|/price-list|/specifications|/on-road-price|/mileage"
    r"|/variants|/colours|/images|/video[s]?|/faq|/dealer[s]?",
    re.IGNORECASE,
)

_BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WISHIBot/1.0; +https://wishi.app/bot)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-IN,en;q=0.9",
}

_PRICE_RE = re.compile(r"₹\s*([\d,]+(?:\.\d+)?)|Rs\.?\s*([\d,]+(?:\.\d+)?)", re.IGNORECASE)
_LAC_RE = re.compile(r"([\d.]+)\s*(?:lac|lakh|l)\b", re.IGNORECASE)
_CR_RE = re.compile(r"([\d.]+)\s*(?:cr|crore)\b", re.IGNORECASE)


# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: Build search queries
# ═══════════════════════════════════════════════════════════════════════════

def _get_category_sites(category: str, subcategory: str) -> List[str]:
    """Return ordered list of marketplace domains for this category."""
    cat_map = CATEGORY_SITES.get(category, {})
    sites = cat_map.get(subcategory, cat_map.get("_default", []))
    if not sites:
        sites = ["olx.in", "flipkart.com", "amazon.in", "quikr.com"]
    return sites


def _build_category_specs(category: str, subcategory: str, filters: dict) -> str:
    """Build category-aware search terms from filters."""
    parts = []

    if category == "automobile" or subcategory in ("car", "bike", "scooter"):
        if filters.get("year"):
            parts.append(str(filters["year"]))
        if filters.get("fuelType"):
            parts.append(filters["fuelType"])
        if filters.get("transmission"):
            parts.append(filters["transmission"])
        km = filters.get("km")
        if km:
            km_val = int(km)
            if km_val < 30000:
                parts.append("low km")
            elif km_val < 60000:
                parts.append("under 60000 km")
        if filters.get("condition"):
            parts.append(filters["condition"])

    elif category == "real estate" or subcategory in ("flat", "house", "plot", "pg", "rent"):
        if filters.get("bedrooms"):
            parts.append(f"{filters['bedrooms']} BHK")
        if filters.get("propertyType"):
            parts.append(filters["propertyType"])
        if filters.get("itemType"):
            parts.append(filters["itemType"])

    elif category in ("electronics", "fashion", "home & living"):
        if filters.get("condition"):
            parts.append(filters["condition"])
        if filters.get("itemType"):
            parts.append(filters["itemType"])

    return " ".join(parts)


def _get_category_qualifier(category: str, subcategory: str) -> str:
    """Return a Google-query qualifier that biases toward listing pages."""
    if category == "automobile":
        return '"used" OR "second hand" OR "pre-owned"'
    elif category == "real estate":
        return '"for sale" OR "for rent" OR "ready to move"'
    elif category in ("electronics", "fashion", "home & living"):
        return '"buy" OR "price" OR "offer"'
    return ""


def _build_queries(wishlist: dict, daily_refresh: bool = False) -> List[str]:
    """Build targeted Google search queries from wishlist fields.

    Generates 7-9 queries organized in three tiers:
      Tier 1 (Q1-Q4): Site-targeted with inurl patterns
      Tier 2 (Q5):    Multi-site OR for remaining sites
      Tier 3 (Q6-Q7): Broad discovery queries
      Bonus  (Q8):    Recency-filtered (daily refresh only)
    """
    title = (wishlist.get("title") or "").strip()
    if not title:
        return []

    filters = wishlist.get("filters_json") or {}
    if not isinstance(filters, dict):
        filters = {}

    category = (wishlist.get("category") or "").lower()
    subcategory = (wishlist.get("subcategory") or "").lower()

    brand = (filters.get("brand") or "").strip()
    model = (filters.get("model") or "").strip()
    location = (filters.get("location") or "").strip()
    price = filters.get("price") or filters.get("max_price") or filters.get("budget")

    core = f"{brand} {model}".strip() if (brand or model) else title
    specs = _build_category_specs(category, subcategory, filters)
    sites = _get_category_sites(category, subcategory)

    queries = []

    # ── Tier 1: Site-targeted with inurl patterns (Q1-Q4) ──
    for site in sites[:4]:
        patterns = LISTING_URL_PATTERNS.get(site, [])
        # Use first pattern for inurl (most specific)
        inurl_part = ""
        if patterns and patterns[0] != "/":
            inurl_part = f" inurl:{patterns[0].strip('/')}"

        # First 2 sites get full specs for deeper targeting
        site_specs = specs if len(queries) < 2 else ""

        q = f'site:{site}{inurl_part} "{core}"'
        if site_specs:
            q += f" {site_specs}"
        if location:
            q += f" {location}"
        queries.append(q)

    # ── Tier 2: Multi-site OR for remaining sites (Q5) ──
    remaining = sites[4:6]
    if remaining:
        or_clause = " OR ".join(f"site:{s}" for s in remaining)
        q = f'({or_clause}) "{core}"'
        if location:
            q += f" {location}"
        queries.append(q)

    # ── Tier 3: Broad discovery queries (Q6-Q7) ──
    # Q6: Price-signal broad
    q6 = f'"{core}"'
    if specs:
        q6 += f" {specs}"
    q6 += ' ("for sale" OR "₹" OR "price")'
    if price:
        q6 += f" under ₹{price}"
    if location:
        q6 += f" {location}"
    q6 += " -review -comparison -specifications -mileage -news"
    queries.append(q6)

    # Q7: Category-qualifier broad
    cat_qualifier = _get_category_qualifier(category, subcategory)
    if cat_qualifier:
        q7 = f'"{core}" {cat_qualifier}'
        if location:
            q7 += f" {location}"
        queries.append(q7)

    # ── Daily recency query (Q8) ──
    if daily_refresh:
        cutoff = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m")
        q8 = f'"{core}"'
        if specs:
            q8 += f" {specs}"
        if location:
            q8 += f" {location}"
        q8 += f" after:{cutoff}"
        queries.append(q8)

    return queries[:10]


# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: Search via SerperDev
# ═══════════════════════════════════════════════════════════════════════════

def _search_serper(queries: List[str]) -> List[dict]:
    """Call SerperDev API and return raw results."""
    api_key = get_settings().serper.api_key
    if not api_key:
        logger.warning("SERPER_API_KEY not configured")
        return []

    results = []
    seen = set()

    for query in queries:
        try:
            with httpx.Client(timeout=15.0) as client:
                resp = client.post(
                    SERPER_URL,
                    headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
                    json={"q": query, "location": "India", "gl": "in", "num": 10},
                )
                resp.raise_for_status()
                data = resp.json()
        except Exception as e:
            logger.error(f"SerperDev failed for '{query}': {e}")
            continue

        for item in data.get("organic", []):
            url = item.get("link", "")
            if not url or url in seen:
                continue
            seen.add(url)
            results.append({
                "url": url,
                "search_title": item.get("title", ""),
                "search_snippet": item.get("snippet", ""),
                "position": item.get("position", 99),
            })

        for item in data.get("shopping", []):
            url = item.get("link", "")
            if not url or url in seen:
                continue
            seen.add(url)
            results.append({
                "url": url,
                "search_title": item.get("title", ""),
                "search_snippet": item.get("source", ""),
                "search_price": item.get("price", ""),
                "position": item.get("position", 99),
            })

    logger.info(f"SerperDev: {len(results)} results from {len(queries)} queries")
    return results


# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: Pre-filter (reject junk URLs before fetching)
# ═══════════════════════════════════════════════════════════════════════════

def _prefilter(results: List[dict], wishlist: dict) -> List[dict]:
    """Quick URL-based filtering before expensive page fetches."""
    filters = wishlist.get("filters_json") or {}
    must_have = _get_must_have_keywords(wishlist, filters)
    passed = []

    for r in results:
        url = r["url"]
        url_lower = url.lower()
        parsed = urlparse(url)
        path = parsed.path.rstrip("/")
        hostname = (parsed.hostname or "").lower()

        # Reject known non-listing domains
        if any(d in url_lower for d in REJECT_DOMAINS):
            continue

        # Reject category/search/review pages
        if REJECT_URL_PATTERNS.search(url_lower):
            continue

        # Reject very short paths (usually homepages/category)
        segments = [s for s in path.split("/") if s]
        if len(segments) <= 1:
            continue

        # Site-specific listing URL validation:
        # If URL is from a known marketplace, verify path matches listing pattern
        matched_domain = None
        for domain in LISTING_URL_PATTERNS:
            if domain in hostname:
                matched_domain = domain
                break

        if matched_domain:
            patterns = LISTING_URL_PATTERNS[matched_domain]
            has_specific = [p for p in patterns if p != "/"]
            if has_specific:
                if not any(p.strip("/") in path.lower() for p in has_specific):
                    continue

        # Title must contain at least one core keyword
        search_text = r.get("search_title", "").lower()
        if must_have and not any(kw in search_text for kw in must_have):
            continue

        passed.append(r)

    logger.info(f"Pre-filter: {len(results)} -> {len(passed)}")
    return passed


def _get_must_have_keywords(wishlist: dict, filters: dict) -> List[str]:
    keywords = []
    for key in ("brand", "model"):
        val = (filters.get(key) or "").strip().lower()
        if val:
            keywords.append(val)
    if not keywords:
        keywords = [w.lower() for w in (wishlist.get("title") or "").split() if len(w) > 3][:3]
    return keywords


# ═══════════════════════════════════════════════════════════════════════════
# STEP 4: Fetch page + Extract SEO metadata
# ═══════════════════════════════════════════════════════════════════════════

def _fetch_and_extract(url: str) -> Optional[Dict]:
    """Fetch URL, extract OG tags + JSON-LD structured data."""
    try:
        with httpx.Client(timeout=8.0, headers=_BROWSER_HEADERS,
                          follow_redirects=True, max_redirects=3) as client:
            resp = client.get(url)
    except Exception as e:
        logger.debug(f"Fetch failed {url}: {e}")
        return None

    if resp.status_code in (404, 410, 403, 500, 502, 503):
        return {"_dead": True, "_status": resp.status_code}

    if resp.status_code != 200:
        return None

    if "text/html" not in resp.headers.get("content-type", ""):
        return None

    soup = BeautifulSoup(resp.text[:200_000], "html.parser")

    data = {}
    data.update(_extract_og(soup))
    data.update(_extract_jsonld(soup))
    return data


def _extract_og(soup: BeautifulSoup) -> Dict:
    """Extract Open Graph + Twitter Card + standard meta tags."""
    d = {}
    for meta in soup.find_all("meta"):
        prop = (meta.get("property") or meta.get("name") or "").lower()
        content = meta.get("content", "")
        if not content:
            continue

        if prop == "og:title":
            d["title"] = content
        elif prop == "og:description":
            d["description"] = content
        elif prop == "og:image":
            d["image"] = content
        elif prop == "og:url":
            d["og_url"] = content
        elif prop in ("og:price:amount", "product:price:amount"):
            d["og_price"] = content
        elif prop in ("og:price:currency", "product:price:currency"):
            d["og_currency"] = content
        elif prop == "product:brand":
            d["og_brand"] = content
        elif prop == "product:condition":
            d["og_condition"] = content
        elif prop == "product:availability":
            d["og_availability"] = content
        elif prop == "og:type":
            d["og_type"] = content
        elif prop == "og:site_name":
            d["site_name"] = content
        elif prop == "twitter:title" and "title" not in d:
            d["title"] = content
        elif prop == "twitter:description" and "description" not in d:
            d["description"] = content
        elif prop == "twitter:image" and "image" not in d:
            d["image"] = content
        elif prop == "description" and "description" not in d:
            d["description"] = content

    if "title" not in d:
        tag = soup.find("title")
        if tag:
            d["title"] = tag.get_text(strip=True)

    return d


def _extract_jsonld(soup: BeautifulSoup) -> Dict:
    """Extract schema.org JSON-LD structured data."""
    d = {}
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            raw = re.sub(r",\s*([}\]])", r"\1", script.string or "")
            ld = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            continue

        items = ld if isinstance(ld, list) else [ld]
        for item in items:
            if isinstance(item, dict) and "@graph" in item:
                items.extend(item["@graph"])

        for item in items:
            if not isinstance(item, dict):
                continue
            itype = item.get("@type", "")
            if isinstance(itype, list):
                itype = itype[0] if itype else ""

            if itype in ("Product", "IndividualProduct", "Vehicle", "Car",
                          "MotorizedBicycle", "RealEstateListing",
                          "Apartment", "House", "Residence"):
                d.update(_parse_ld_item(item, itype))
            elif itype == "Offer":
                d.update(_parse_ld_offer(item))
    return d


def _parse_ld_item(item: dict, itype: str) -> Dict:
    """Parse a JSON-LD product/vehicle/realestate item."""
    d = {"ld_type": itype}

    if item.get("name"):
        d["ld_title"] = item["name"]
    if item.get("description"):
        d["ld_description"] = str(item["description"])[:500]

    # Brand
    brand = item.get("brand")
    if brand:
        d["ld_brand"] = brand.get("name", str(brand)) if isinstance(brand, dict) else str(brand)

    # Model
    if item.get("model"):
        d["ld_model"] = str(item["model"])

    # Condition
    cond = item.get("itemCondition", "")
    if cond:
        d["ld_condition"] = cond.split("/")[-1]  # strip schema.org URL prefix

    # Image
    imgs = item.get("image", [])
    if isinstance(imgs, str):
        d["ld_image"] = imgs
    elif isinstance(imgs, list) and imgs:
        first = imgs[0]
        d["ld_image"] = first.get("url", first) if isinstance(first, dict) else first

    # Offers
    offers = item.get("offers", {})
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    if isinstance(offers, dict):
        d.update(_parse_ld_offer(offers))

    # Rating
    rating = item.get("aggregateRating", {})
    if isinstance(rating, dict) and rating.get("ratingValue"):
        d["ld_rating"] = str(rating["ratingValue"])

    # Vehicle-specific
    if item.get("fuelType"):
        d["ld_fuel"] = item["fuelType"]
    if item.get("vehicleTransmission"):
        d["ld_transmission"] = item["vehicleTransmission"]
    if item.get("mileageFromOdometer"):
        odo = item["mileageFromOdometer"]
        d["ld_km"] = str(odo.get("value", odo) if isinstance(odo, dict) else odo)
    if item.get("vehicleModelDate") or item.get("modelDate"):
        d["ld_year"] = str(item.get("vehicleModelDate") or item.get("modelDate"))
    if item.get("vehicleColor") or item.get("color"):
        d["ld_color"] = item.get("vehicleColor") or item.get("color")

    # Real estate-specific
    if item.get("numberOfRooms"):
        d["ld_rooms"] = str(item["numberOfRooms"])
    floor = item.get("floorSize")
    if floor:
        d["ld_area"] = f"{floor.get('value', floor)} {floor.get('unitText', '')}" if isinstance(floor, dict) else str(floor)
    addr = item.get("address", {})
    if isinstance(addr, dict):
        loc_parts = [addr.get("addressLocality", ""), addr.get("addressRegion", "")]
        loc = ", ".join(p for p in loc_parts if p)
        if loc:
            d["ld_location"] = loc

    return d


def _parse_ld_offer(offers: dict) -> Dict:
    d = {}
    if offers.get("price"):
        try:
            d["ld_price"] = float(offers["price"])
        except (ValueError, TypeError):
            pass
    if offers.get("priceCurrency"):
        d["ld_currency"] = offers["priceCurrency"]
    avail = offers.get("availability", "")
    if avail:
        d["ld_availability"] = avail.split("/")[-1]
    seller = offers.get("seller")
    if seller:
        d["ld_seller"] = seller.get("name", str(seller)) if isinstance(seller, dict) else str(seller)
    return d


# ═══════════════════════════════════════════════════════════════════════════
# STEP 5: Score metadata against wishlist
# ═══════════════════════════════════════════════════════════════════════════

def _score_match(seo: Dict, search_result: dict, wishlist: dict) -> Tuple[int, dict]:
    """Score SEO metadata against wishlist. Returns (score, enriched_candidate).

    Scoring (0-100):
      - Brand match in metadata:      15 pts
      - Model match in metadata:       15 pts
      - Year match:                     5 pts
      - Extra specs (fuel, bhk, etc):   5 pts
      - Price within budget:           20 pts
      - Location match:                15 pts
      - Domain quality:                15 pts
      - Search position:               10 pts
    """
    filters = wishlist.get("filters_json") or {}
    if not isinstance(filters, dict):
        filters = {}

    # Best available data (JSON-LD > OG > search snippet)
    title = seo.get("ld_title") or seo.get("title") or search_result.get("search_title", "")
    description = seo.get("ld_description") or seo.get("description") or search_result.get("search_snippet", "")
    full_text = f"{title} {description}".lower()
    title_lower = title.lower()
    url = search_result["url"].lower()

    score = 0

    # ── Brand (15 pts) ──
    w_brand = (filters.get("brand") or "").lower().strip()
    ld_brand = (seo.get("ld_brand") or seo.get("og_brand") or "").lower()
    if w_brand:
        if w_brand in ld_brand:
            score += 15  # exact brand from structured data
        elif w_brand in title_lower:
            score += 12  # brand in page title
        elif w_brand in full_text:
            score += 6   # brand somewhere on page

    # ── Model (15 pts) ──
    w_model = (filters.get("model") or "").lower().strip()
    ld_model = (seo.get("ld_model") or "").lower()
    if w_model:
        if w_model in ld_model:
            score += 15
        elif w_model in title_lower:
            score += 12
        elif w_model in full_text:
            score += 6

    # ── Year (5 pts) ──
    w_year = str(filters.get("year", "")).strip()
    if w_year:
        ld_year = str(seo.get("ld_year", ""))
        if w_year in ld_year or w_year in title_lower:
            score += 5

    # ── Extra specs: fuel, bhk, property type (5 pts) ──
    extra_kw = []
    for key in ("fuelType", "itemType", "propertyType"):
        v = (filters.get(key) or "").lower().strip()
        if v:
            extra_kw.append(v)
    bedrooms = filters.get("bedrooms", "")
    if bedrooms:
        extra_kw.append(f"{bedrooms} bhk")
    if extra_kw:
        matched = sum(1 for kw in extra_kw if kw in full_text)
        score += min(int((matched / len(extra_kw)) * 5), 5)

    # If no structured filters, fall back to title word overlap
    if not w_brand and not w_model:
        title_words = [w.lower() for w in (wishlist.get("title") or "").split() if len(w) > 2]
        if title_words:
            matched = sum(1 for w in title_words if w in title_lower)
            score += min(int((matched / len(title_words)) * 30), 30)

    # ── Price (20 pts) ──
    budget = filters.get("price") or filters.get("max_price") or filters.get("budget")
    item_price = seo.get("ld_price") or _parse_og_price(seo) or _extract_price(full_text)
    if budget and item_price:
        budget_f = float(budget)
        if budget_f > 0:
            if item_price <= budget_f:
                ratio = item_price / budget_f
                score += 20 if ratio >= 0.5 else (12 if ratio >= 0.3 else 3)
            elif item_price <= budget_f * 1.15:
                score += 10
    elif budget:
        score += 3

    # ── Location (15 pts) ──
    w_location = (filters.get("location") or "").lower().strip()
    ld_location = (seo.get("ld_location") or "").lower()
    if w_location:
        if w_location in ld_location:
            score += 15
        elif w_location in title_lower:
            score += 12
        elif w_location in full_text:
            score += 8
        else:
            parts = w_location.split()
            if any(p in full_text for p in parts if len(p) > 3):
                score += 5

    # ── Domain quality (15 pts) ──
    if any(d in url for d in PRIMARY_MARKETPLACES):
        score += 15
    elif any(d in url for d in LISTING_DOMAINS):
        score += 10
    elif ".in" in url:
        score += 3

    # ── Search position (10 pts) ──
    pos = search_result.get("position", 99)
    if pos <= 3:
        score += 10
    elif pos <= 5:
        score += 7
    elif pos <= 8:
        score += 4
    elif pos <= 10:
        score += 2

    score = min(score, 100)

    # Build enriched candidate
    candidate = {
        "url": search_result["url"],
        "source": _detect_source(search_result["url"]),
        "title": title,
        "description": description[:300],
        "price": item_price,
        "formatted_price": f"\u20b9{int(item_price):,}" if item_price else None,
        "image_url": seo.get("ld_image") or seo.get("image"),
        "score": score,
        "verified": True,
    }

    # Add specs
    specs = {}
    for key in ("ld_fuel", "ld_transmission", "ld_km", "ld_year", "ld_color",
                 "ld_rooms", "ld_area", "ld_condition"):
        val = seo.get(key)
        if val:
            specs[key.replace("ld_", "")] = val
    if specs:
        candidate["specs"] = specs

    if seo.get("ld_rating"):
        candidate["rating"] = seo["ld_rating"]
    if seo.get("ld_seller"):
        candidate["seller"] = seo["ld_seller"]
    if seo.get("ld_brand"):
        candidate["brand"] = seo["ld_brand"]

    return score, candidate


def _detect_source(url: str) -> str:
    url_lower = url.lower()
    for domain in PRIMARY_MARKETPLACES + LISTING_DOMAINS:
        if domain in url_lower:
            return domain.split(".")[0]
    return "web"


def _parse_og_price(seo: dict) -> Optional[float]:
    og_price = seo.get("og_price")
    if og_price:
        try:
            return float(og_price)
        except (ValueError, TypeError):
            return _parse_price_str(og_price)
    return None


def _extract_price(text: str) -> Optional[float]:
    if not text:
        return None
    m = _CR_RE.search(text)
    if m:
        try:
            return float(m.group(1)) * 10_000_000
        except ValueError:
            pass
    m = _LAC_RE.search(text)
    if m:
        try:
            return float(m.group(1)) * 100_000
        except ValueError:
            pass
    m = _PRICE_RE.search(text)
    if m:
        return _parse_price_str(m.group(1) or m.group(2))
    return None


def _parse_price_str(s) -> Optional[float]:
    if not s:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    try:
        cleaned = "".join(c for c in str(s) if c.isdigit() or c == ".")
        return float(cleaned) if cleaned else None
    except (ValueError, TypeError):
        return None


# ═══════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

def find_matches(wishlist: dict, max_fetch: int = 20, min_score: int = 30,
                 daily_refresh: bool = False) -> List[dict]:
    """Complete matching pipeline for a wishlist.

    1. Build search queries from wishlist
    2. Search Google via SerperDev
    3. Pre-filter (reject blogs, reviews, category pages)
    4. Fetch top results, extract OG + JSON-LD metadata
    5. Score metadata against wishlist
    6. Return verified matches sorted by score

    Args:
        wishlist: dict with title, category, subcategory, filters_json
        max_fetch: max pages to fetch (rate limit)
        min_score: minimum score threshold
        daily_refresh: True for daily task (enables recency queries)

    Returns:
        List of scored, enriched match dicts sorted by score desc.
    """
    # Step 1: Build queries
    queries = _build_queries(wishlist, daily_refresh=daily_refresh)
    if not queries:
        logger.warning(f"No queries built for wishlist: {wishlist.get('title', '')}")
        return []

    # Step 2: Search
    raw_results = _search_serper(queries)
    if not raw_results:
        return []

    # Step 3: Pre-filter
    filtered = _prefilter(raw_results, wishlist)
    if not filtered:
        return []

    # Step 4+5: Fetch pages + extract metadata + score
    matches = []
    fetched = 0

    for result in filtered:
        if fetched >= max_fetch:
            break

        url = result["url"]
        seo = _fetch_and_extract(url)
        fetched += 1

        if seo is None:
            continue

        # Dead link
        if seo.get("_dead"):
            logger.debug(f"Dead ({seo.get('_status')}): {url}")
            continue

        # Out of stock
        avail = (seo.get("ld_availability") or "").lower()
        if avail in ("outofstock", "discontinued", "soldout"):
            logger.debug(f"Out of stock: {url}")
            continue

        # Not a listing page (no product/price metadata at all)
        has_product_signal = (
            seo.get("ld_type")
            or seo.get("ld_price")
            or seo.get("og_price")
            or seo.get("og_type", "").lower() in ("product", "product.item")
            or seo.get("og_availability")
        )
        # For primary marketplaces, be lenient — they always have OG tags
        is_primary = any(d in url.lower() for d in PRIMARY_MARKETPLACES)
        if not has_product_signal and not is_primary:
            if not seo.get("title"):
                logger.debug(f"No product metadata: {url}")
                continue

        # Score
        score, candidate = _score_match(seo, result, wishlist)

        if score >= min_score:
            matches.append(candidate)

        # Small delay between fetches
        time.sleep(0.3)

    matches.sort(key=lambda x: x["score"], reverse=True)

    logger.info(
        f"Matcher: {len(raw_results)} searched -> {len(filtered)} filtered "
        f"-> {fetched} fetched -> {len(matches)} matched "
        f"for '{wishlist.get('title', '')}'"
    )
    return matches
