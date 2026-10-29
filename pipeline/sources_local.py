from __future__ import annotations

"""Ghana classifieds / local directory adapters: Tonaton + Jiji Ghana.

Politeness-first: each adapter fetches robots.txt and refuses disallowed
paths, then scrapes only public listing pages it is allowed to. Contact data
on Tonaton/Jiji is login-gated by design, so we capture what is public
(business name, area, photos, seller types) and never bypass it.
"""
import re
from urllib.parse import quote_plus, urljoin, urlsplit
from urllib.robotparser import RobotFileParser

from bs4 import BeautifulSoup

from .geo import extract_ghana_post, normalize_phone

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

# Directory detail pages carry script/analytics/asset hrefs next to the real
# business site. kenyayp pages link Google Tag Manager first, which used to
# land in businesses.website on every Kenyan row (a live "website" that made
# lapsed-site leads score like healthy ones). Never accept these as a site.
_NOISE_SITE = (
    "googletagmanager", "google-analytics", "googlesyndication", "doubleclick",
    "gstatic", "googleapis", "google.com", "schema.org", "w3.org",
    "cloudflare", "jsdelivr", "bootstrapcdn", "jquery", "wp-content",
    "wp-includes", "hotjar", "clarity.ms", "facebook.com/tr", "connect.facebook",
)


def plausible_site(url: str) -> bool:
    """True when an href is a real business website (not tracking/asset noise)."""
    u = url.lower()
    if any(n in u for n in _NOISE_SITE):
        return False
    host = urlsplit(u).netloc
    return bool(host) and "." in host


class RobotsBlocked(Exception):
    pass


def _allowed(base: str, path: str, path_re="/.*") -> None:
    rp = RobotFileParser()
    rp.set_url(urljoin(base, "/robots.txt"))
    try:
        rp.read()
    except Exception:
        return  # no robots.txt -> allowed by convention
    if not rp.can_fetch(_UA, urljoin(base, path)):
        raise RobotsBlocked(f"robots.txt disallows {path}")


def _cards_tonaton(html: str, base: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    out = []
    # Tonaton (Nuxt site): ad links look like /a-<id>-<title-slug>.html
    for a in soup.select("a[href^='/a-']")[:20]:
        href = a.get("href", "")
        if not href.startswith("/a-"):
            continue
        slug = href.rsplit("/", 1)[-1]
        # title text from the card if present, else the URL slug
        title_node = a.find(["h2", "h3"]) or a.find(attrs={"data-testid": "ad-card-title"})
        title = title_node.get_text(" ", strip=True) if title_node else ""
        if not title and ".html" in slug:
            body = slug[2:] if slug.startswith("a-") else slug
            parts = body.split("-", 1)
            tail = parts[1].rsplit(".html", 1)[0] if len(parts) > 1 else body
            title = tail.replace("-", " ").title()
        card = {"profile_url": urljoin(base, href), "source": "tonaton", "name": title}
        loc = a.select_one("[data-testid='location-container'], [class*='Location']")
        if loc:
            card["area"] = loc.get_text(" ", strip=True)
        out.append(card)
    return out


def _cards_jiji(html: str, base: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for a in soup.select("a[class*='AdTile'], a[href*='/services/'], a[href*='/products/']")[:20]:
        href = a.get("href", "")
        if not href or "jiji" not in href:
            href = urljoin(base, href)
        card = {"profile_url": href, "source": "jiji"}
        title = a.select_one("[class*='Title'], h2, h3")
        if title:
            card["name"] = title.get_text(" ", strip=True)
        loc = a.select_one("[class*='Location'], [class*='Region']")
        if loc:
            card["area"] = loc.get_text(" ", strip=True)
        out.append(card)
    return out


def _cards_businessghana(html: str, base: str) -> list[dict]:
    """Company cards from a BusinessGhana search page:
    /site/directory/<category>/<numeric-id>/<Name-Slug>. Featured sidebar
    entries repeat on every page -> excluded. Phone digits sit near the card
    in the misc column, found by position (not DOM depth)."""
    out, seen = [], set()
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=re.compile(r"^/site/directory/[a-z\-]+/\d+/[\w\-]+$")):
        m = re.match(r"^/site/directory/[a-z\-]+/(\d+)/([\w\-]+)$", a["href"])
        if not m or m.group(1) in _BG_FEATURED or m.group(1) in seen:
            continue
        seen.add(m.group(1))
        name = m.group(2).replace("-", " ").strip().title()
        card = {"source": "businessghana", "source_id": f"businessghana:{m.group(1)}",
                "profile_url": urljoin(base, a["href"]), "name": name}
        # the misc column with the phone precedes the card's title in page flow
        href_pos = html.find(a["href"])
        if href_pos > -1:
            window = html[max(0, href_pos - 700):href_pos + 100]
            phones = re.findall(r"\b0[2-5]\d{8}\b", re.sub(r"<[^>]+>", " ", window))
            if phones:
                phone = phones[-1]  # nearest number ahead of the name
                # description: the card's own text, tag-stripped
                after = html[href_pos:href_pos + 900]
                desc = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", after))
                desc = desc.split(name, 1)[-1] if name in desc else ""
                card["phone"] = phone
                card["description"] = re.sub(r"[|\s]+", " ", desc).strip()[:280] or None
        out.append(card)
    return out


# BusinessesGhana profile page: pull the real contact block (postal address,
# phone numbers, email, website) that the search card does not show.
def profile_details(client, profile_url: str) -> dict:
    base = "https://www.businessghana.com"
    path = profile_url.replace(base, "") or profile_url
    _allowed(base, path if path.startswith("/") else "/" + path)
    html = client.get(profile_url).text
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "~", re.sub(
        r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)))
    out: dict = {}

    def field(label: str, span: int = 220) -> str | None:
        m = re.search(label + r"(?:\s*~\s*)+([^~|]{2,160})", plain)
        if not m:
            return None
        val = m.group(1).strip(" ~,")
        # empty slot followed by the next label reads as that label -> not a value
        if val.lower() in ("postal address", "street address", "working hours",
                           "name", "phone number", "website", "email", "category"):
            return None
        return val

    phones = re.findall(r"\+?233[ ()\-]?\d{2,3}[ \d]{6,12}|0[23 5]\d[ \d]{7,10}", plain)
    seen = [p.strip() for p in phones if len(re.sub(r"\D", "", p)) >= 9]
    if seen:
        out["phone"] = seen[0]
        out["alt_phone"] = seen[1] if len(seen) > 1 else None
    postal = field("Postal Address")
    street = field("Street Address")
    address = " ; ".join(x for x in (street, postal) if x) or None
    if address:
        out["address"] = address
    email = next((e for e in re.findall(r"[\w.\-]+@[\w.\-]+", plain)
                  if "businessghana.com" not in e), None)
    if email:
        out["email"] = email
    site = field("Website")
    if site and site.startswith("http") and "://none" not in site:
        out["website"] = site.split()[0]
    return out


# ghanayello slugs -> BusinessGhana search terms (its taxonomy is broader)
BG_TERMS = {
    "beauty_salons": "salon", "hotels": "hotel", "restaurants": "restaurant",
    "event_organisers": "event", "lawyers": "law", "pharmacies": "pharmacy",
    "kitchen_furniture": "furniture", "travel_agents": "travel",
    "photography": "photography", "fashion": "fashion",
    "private_schools": "school", "clinics": "clinic",
}

# featured sidebar entries that repeat on every search page
_BG_FEATURED = {"399549", "493932", "492797", "492937", "493735"}

ADAPTERS = {"tonaton": ("https://tonaton.com", "/c_{category}", _cards_tonaton),
            "jiji": ("https://jiji.com.gh", "/services", _cards_jiji),
            "businessghana": ("https://www.businessghana.com",
                              "/site/directory/search?search={category}",
                              _cards_businessghana)}


def search_query(source: str, client, category: str, city: str, limit: int = 3, page: int = 1):
    """Yield normalized candidate dicts; per-source failures are surfaced via
    RobotsBlocked/HttpError, logged upstream (scan_failures)."""
    base, path_fmt, parser = ADAPTERS[source]
    if source == "businessghana":
        category = BG_TERMS.get(category, category)
        path = path_fmt.format(category=quote_plus(category))
        if page and page > 1:
            path += f"&page={page}"
    else:
        query = f"{category} {city}".strip()
        path = path_fmt.format(category=category) + ("" if source == "tonaton" else f"?query={quote_plus(query)}")
    resp = client.get(urljoin(base, path))
    _allowed(base, path)
    out = []
    for card in parser(resp.text, base)[:limit]:
        phone = card.get("phone")
        card["phone_e164"] = normalize_phone(phone or "")
        card["ghana_post"] = extract_ghana_post(" ".join(str(v) for v in card.values()))
        out.append(card)
    return out


# ---------------------------------------------------------------------------
# Kenya: Yellow Pages Kenya (robots-verified allowed, public business listings)
# ---------------------------------------------------------------------------

KENYA_BASE = "https://www.yellowpageskenya.com"

# our category slugs -> Kenya YP category slugs (their taxonomy)
KE_CATEGORIES = {
    "beauty_salons": "beauty-and-fitness", "hotels": "hotels-and-restaurants",
    "restaurants": "hotels-and-restaurants", "event_organisers": "events",
    "lawyers": "legal-services", "pharmacies": "health-and-medical",
    "kitchen_furniture": "furniture", "travel_agents": "travel-and-tours",
    "photography": "photography", "fashion": "shopping-and-fashion",
    "private_schools": "education-and-culture", "clinics": "health-and-medical",
}


def _kenya_robots_ok(path: str) -> bool:
    _allowed(KENYA_BASE, path)
    return True


def cards_kenya(html: str, base: str) -> list[dict]:
    """Business cards from a Yellow Pages Kenya category page:
    /business-category/<category>/business-details/<id>-<name-slug>."""
    out, seen = [], set()
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=re.compile(r"^/business-category/[^/]+/business-details/\d+-[\w\-]+")):
        m = re.match(r"^/business-category/([^/]+)/business-details/(\d+)-([\w\-]+)", a["href"])
        if not m or m.group(2) in seen:
            continue
        seen.add(m.group(2))
        out.append({"source": "kenyayp", "source_id": f"kenyayp:{m.group(2)}",
                    "profile_url": urljoin(base, a["href"]),
                    "name": m.group(3).replace("-", " ").title(),
                    "categories_url": m.group(1)})
    return out


def kenya_category(category: str) -> str:
    return KE_CATEGORIES.get(category, category)


def kenya_profile_details(client, profile_url: str) -> dict:
    """Detail page: phone tokens, email, website, address. Labels on this
    site are noisy, so extraction leans on pattern anchors."""
    t = client.get(profile_url).text
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ~ ", re.sub(
        r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)))
    out: dict = {}
    phones = re.findall(r"\+?254[ \d]{8,12}|0[17]\d[ \d]{7,9}", plain)
    seen = []
    for p in phones:
        p = p.strip()
        if p and p not in seen:
            seen.append(p)
    if seen:
        out["phone"] = seen[0]
        out["alt_phone"] = seen[1] if len(seen) > 1 else None
    email = next((e for e in re.findall(r"[\w.\-]+@[\w.\-]+\.\w{2,6}", plain)
                  if "yellowpageskenya" not in e), None)
    if email:
        out["email"] = email
    # business website: an href that is not the directory itself (any subdomain)
    site = next((h for h in re.findall(r"href=\"(https?://(?![^\"]*?yellowpageskenya)[^\"]{10,120})\"",
                                       t) if "facebook.com" not in h and "instagram" not in h
                 and "linkedin" not in h and "twitter" not in h and "whatsapp" not in h
                 and plausible_site(h)), None)
    if site:
        out["website"] = site
    m = re.search(r"\b(P\.?O\.?[\s,.]*Box[^~|]{5,90})", plain)
    if m:
        out["address"] = m.group(1).strip()
    return out


# ---------------------------------------------------------------------------
# Nigeria: BusinessList.com.ng (robots-checked allowed; asks crawl-delay 40s)
# ---------------------------------------------------------------------------

NIGERIA_BASE = "https://www.businesslist.com.ng"

# our category slugs -> BusinessList Nigeria category slugs (verified live)
NG_CATEGORIES = {
    "beauty_salons": "beauty-salons", "hotels": "hotels",
    "restaurants": "restaurants", "event_organisers": "event-organisers",
    "lawyers": "lawyers", "pharmacies": "pharmacies",
    "kitchen_furniture": "furniture", "travel_agents": "travel-agents",
    "photography": "photographers", "fashion": "fashion",
    "private_schools": "schools", "clinics": "doctors-and-clinic",
}


def cards_nigeria(html: str, base: str) -> list[dict]:
    """Business cards from a /category/<slug> page:
    href="/company/<numeric id>/<name-slug>". Robots allows these paths."""
    out, seen = [], set()
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=re.compile(r"^/company/\d+/[\w\-]+")):
        m = re.match(r"^/company/(\d+)/([\w\-]+)", a["href"])
        if not m or m.group(1) in seen:
            continue
        seen.add(m.group(1))
        out.append({"source": "blng", "source_id": f"blng:{m.group(1)}",
                    "profile_url": urljoin(base, a["href"]),
                    "name": m.group(2).replace("-", " ").title()})
    return out


def nigeria_category(category: str) -> str:
    return NG_CATEGORIES.get(category, category)


def nigeria_profile_details(client, profile_url: str) -> dict:
    """Detail page: phone(s), email, business site, review count, address.
    Labels are positional on this site, so lean on pattern anchors."""
    t = client.get(profile_url).text
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ~ ", re.sub(
        r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)))
    out: dict = {}
    phones = []
    for p in re.findall(r"\+?234[\d\- ]{7,14}|0[7-9]\d[\d\- ]{7,10}", plain):
        p2 = p.strip()
        if p2 and p2 not in phones:
            phones.append(p2)
    if phones:
        out["phone"] = phones[0]
        out["alt_phone"] = phones[1] if len(phones) > 1 else None
    email = next((e for e in re.findall(r"[\w.\-]+@[\w.\-]+\.\w{2,6}", plain)
                  if "businesslist" not in e), None)
    if email:
        out["email"] = email
    site = next((h for h in re.findall(r'href="(https?://(?![^"]*?businesslist)[^"]{10,90})"', t)
                 if not any(x in h for x in ("facebook", "twitter", "instagram",
                                             "linkedin", "google", "apple", "wa.me",
                                             "cdn", "woff", "bootstrap"))
                 and plausible_site(h)), None)
    if site:
        out["website"] = site
    m = re.search(r"(\d+)\s+Reviews?", plain)
    if m:
        out["reviews_count"] = int(m.group(1))
    m = re.search(r"\b([A-Z][\w .,\-]{10,80}(?:Way|Road|Street|Drive|Layout|Close|Avenue|Abuja|Lagos|Ibadan|Kano|Port[\s\-]Harcourt)[\w .,\-]*)", plain)
    if m:
        out["address"] = m.group(1).strip()
    return out


# ---------------------------------------------------------------------------
# Nigeria source 2: NGEX / Nigeria Galleria (robots-allowed; keyword search)
#   /bd/search?q=<term>&place=<City> -> /bd/b/<Name>-<Area>-<City>-Nigeria
#   Detail pages expose rating, review count, address block and +234 phone.
#   (Their JSON-LD is template-stale; the visible text is the source of truth.)
# ---------------------------------------------------------------------------

NGEX_BASE = "https://ngex.com"

# our slugs -> ngex keyword terms (search-driven, no fixed taxonomy needed)
NGEX_TERMS = {
    "beauty_salons": "beauty salon", "hotels": "hotel", "restaurants": "restaurant",
    "event_organisers": "event planner", "lawyers": "law firm", "pharmacies": "pharmacy",
    "kitchen_furniture": "furniture", "travel_agents": "travel agency",
    "photography": "photographers", "fashion": "fashion",
    "private_schools": "school", "clinics": "clinic",
}


def ngex_category(category: str) -> str:
    return NGEX_TERMS.get(category, category)


def cards_ngex(html: str, base: str) -> list[dict]:
    """Cards from an ngex listing/search page.

    Slug shape: /bd/b/<Name...>[_<n>]-<Area>-<City>-Nigeria — the name is the
    token run before the trailing '<Area>-<City>' pair."""
    out, seen = [], set()
    for href in re.findall(r'(?:https?://ngex\.com)?(/bd/b/[^"\']+)', html):
        if href in seen:
            continue
        seen.add(href)
        parts = [p for p in href.strip("/").split("-")]
        if "Nigeria" in parts:
            ni = parts.index("Nigeria")
            core = parts[: max(0, ni - 2)]  # drop trailing Area-City chain
        else:
            if re.search(r"(?i)united-?states", href):
                continue  # international listings — not Nigeria leads
            core = parts[1:]
        name = " ".join(p for p in core if p and not re.match(r"^\d+$", p))
        name = re.sub(r"_\d+", "", name).replace("_", " ").strip().title()
        out.append({"source": "ngex", "profile_url": urljoin(base, href),
                    "source_id": "ngex:" + href.strip("/"),
                    "name": name or href.strip("/").title()})
    return out


def ngex_profile_details(client, profile_url: str) -> dict:
    """Visible-text-only parse: rating, review count, phones, address, site."""
    t = client.get(profile_url).text
    plain = re.sub(r"\s+", " ", re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S))
    plain = re.sub(r"<[^>]+>", " ~ ", plain)
    out: dict = {}
    m = re.search(r"(\d(?:\.\d)?)\s*~+\s*\((\d+)\s*Reviews?\)", plain)
    if m:
        try:
            out["rating"] = float(m.group(1))
            out["reviews_count"] = int(m.group(2))
        except ValueError:
            pass
    phones = []
    for p in re.findall(r"\+?234[\d\- ]{8,13}", plain):
        digits = re.sub(r"\D", "", p)[3:]  # drop the 234
        if len(digits) in (9, 10):
            p2 = "+234" + digits
            if p2 not in phones:
                phones.append(p2)
    if phones:
        out["phone"] = phones[0]
        out["alt_phone"] = phones[1] if len(phones) > 1 else None
    email = next((e for e in re.findall(r"[\w.\-]+@[\w.\-]+\.\w{2,6}", plain) if "ngex" not in e), None)
    if email:
        out["email"] = email
    site = next((h for h in re.findall(r'href="(https?://(?![^"]*?ngex)[^"]{10,90})"', t)
                 if not any(x in h for x in ("facebook.com", "twitter.com", "instagram.com",
                                             "linkedin", "google", "apple", "wa.me",
                                             "fonts.", "cdn", "bootstrap", "maxcdn",
                                             "twitter:", "javascript", "mailto"))
                 and plausible_site(h)), None)
    if site:
        out["website"] = site
    # address block: lines after "Primary Category:" are street address pieces
    m = re.search(r"Primary Category:\s*~+([^~]{2,60})(?:~+(?:[^~]{2,60})){0,3}~+Head Quarter", plain)
    addr_parts = []
    if m:
        seg = plain[m.start():m.start() + 340]
        addr_parts = [p.strip() for p in re.split(r"~+", seg) if p.strip()][:6]
        addr_parts = [p for p in addr_parts if not re.search(r"(?i)primary", p)]
        out["address"] = ", ".join(addr_parts[:4]) if addr_parts else None
    return out
