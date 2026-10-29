from __future__ import annotations

"""GhanaYello directory scraper: categories -> listing cards -> company profiles.

Country expansion note: this module implements the Source interface used by
run.py. Adding e.g. Nigeria later means writing the same two functions
(scrape_cards / scrape_profile) against another directory network site
(Woomar network runs per-country portals with near-identical markup).
"""
import re
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .http import Client
from .db import brand_key

BASE = "https://www.ghanayello.com"
CATEGORY_LIST_URL = f"{BASE}/browse-business-directory"
CITY_INDEX_URL = f"{BASE}/browse-business-cities"

CAT_RE = re.compile(r"^/category/([a-z0-9_-]+)$")


def lists_dir() -> Path:
    p = Path(__file__).resolve().parent.parent / "data"
    p.mkdir(parents=True, exist_ok=True)
    return p


# ---------------------------------------------------------------- categories
def list_categories(client: Client) -> dict[str, str]:
    """Return {slug: display_name} for every category on the directory."""
    resp = client.get(CATEGORY_LIST_URL)
    soup = BeautifulSoup(resp.text, "html.parser")
    cats: dict[str, str] = {}
    for a in soup.find_all("a", href=CAT_RE):
        slug = CAT_RE.match(a["href"]).group(1)
        cats.setdefault(slug, a.get_text(strip=True))
    if not cats:
        # fall back to the homepage tile categories
        resp = client.get(BASE)
        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.find_all("a", href=CAT_RE):
            slug = CAT_RE.match(a["href"]).group(1)
            cats.setdefault(slug, a.get_text(strip=True))
    return cats


CITY_SLUG_RE = re.compile(r"^/location/([A-Za-z0-9_]+)$")


def list_cities(client: Client) -> dict[str, str]:
    """Return {city_slug: display_name}."""
    resp = client.get(CITY_INDEX_URL)
    soup = BeautifulSoup(resp.text, "html.parser")
    cities: dict[str, str] = {}
    for a in soup.find_all("a", href=CITY_SLUG_RE):
        slug = CITY_SLUG_RE.match(a["href"]).group(1)
        cities.setdefault(slug, a.get_text(strip=True))
    return cities


# ---------------------------------------------------------------- listing cards
def _card_data(card, client_family: str | None = None) -> dict | None:
    cmp_id = card.get("data-cmpid")
    if not cmp_id or "company_ad" in (card.get("class") or []):
        return None
    h3a = card.select_one("h3 a[href^='/company/']")
    if not h3a:
        return None
    data = {
        "source_id": str(cmp_id),
        "name": h3a.get_text(strip=True),
        "profile_url": urljoin(BASE, h3a["href"]),
        "slug": h3a["href"].rsplit("/", 1)[-1],
    }
    addr = card.select_one("div.address")
    if addr:
        data["address"] = addr.get_text(" ", strip=True)
        bold = addr.find("b")
        if bold:
            data["city"] = bold.get_text(strip=True)
    tagline = card.select_one("div.tagline")
    if tagline:
        data["description"] = tagline.get_text(" ", strip=True)

    # contact icons: <div class="s"><i class="fa fa-phone">...<span><b>phone</b></span></div>
    for s in card.select("div.cont div.s"):
        icon = s.find("i")
        iccls = " ".join(icon.get("class", [])) if icon else ""
        text = s.get_text(" ", strip=True)
        if "fa-phone" in iccls or "fa-whatsapp" in iccls:
            data["phone"] = s.get_text(" ", strip=True)
        elif "fa-globe" in iccls:
            data["has_website"] = 1
        elif "fa-envelope" in iccls:
            data["email_on_file"] = 1  # shown behind login on ghanaYello; no raw email
        elif "fa-picture-o" in iccls and "Photos" in text:
            m = re.search(r"(\d+)", text)
            if m:
                data["photos_count"] = int(m.group(1))
        elif "Established" in text:
            m = re.search(r"(\d{4})", text)
            if m:
                data["established_year"] = int(m.group(1))

    mm = card.find("div", class_="mapmarker")
    if mm:
        try:
            data["latitude"] = float(mm["data-ltd"])
            data["longitude"] = float(mm["data-lng"])
        except (KeyError, ValueError, TypeError):
            pass
    rating = card.select_one("div.company_reviews .rate")
    if rating:
        try:
            data["rating"] = float(rating.get_text(strip=True))
        except ValueError:
            pass
    rev = card.select_one("div.company_reviews")
    if rev:
        m = re.search(r"(\d+)\s+Reviews?", rev.get_text(" ", strip=True))
        if m:
            data["reviews_count"] = int(m.group(1))
    logo = card.select_one("a.logo[data-bg]")
    if logo:
        data["logo_url"] = urljoin(BASE, logo["data-bg"])
    data["brand_key"] = brand_key(data.get("name", ""))
    return data


def category_page_url(slug: str, page: int, city: str | None = None) -> str:
    base = f"{BASE}/category/{slug}" + (f"/city:{city}" if city else "")
    return base if page == 1 else f"{base}/{page}"


def scrape_category(client: Client, slug: str, city: str | None = None,
                    max_pages: int = 5) -> tuple[list[dict], int]:
    """Scrape listing cards page by page. Returns (cards, total_listings)."""
    cards: list[dict] = []
    total = None
    for page in range(1, max_pages + 1):
        url = category_page_url(slug, page, city)
        resp = client.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        found = [c for c in soup.select("div.company") if _card_data(c)]
        for c in found:
            d = _card_data(c)
            if d:
                cards.append(d)
        if total is None:
            ts = soup.select_one("div.pages_container_top strong")
            if ts:
                digits = "".join(ch for ch in ts.get_text() if ch.isdigit())
                total = int(digits) if digits else None
        if not found:
            break
        # stop when there is no explicit "next" page link
        nxt = soup.select_one("a.pages_arrow[rel='next']") or soup.find(
            "a", class_="pages_no", href=re.compile(rf"/{page + 1}$"))
        if not nxt and total is None:
            break
    return cards, (total or len(cards))


# ---------------------------------------------------------------- profile page
def scrape_profile(client: Client, profile_url: str) -> dict:
    resp = client.get(profile_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    d: dict = {}

    name_el = soup.select_one("#company_name")
    if name_el:
        d["name"] = name_el.get_text(strip=True)
    addr = soup.select_one("#company_address")
    if addr:
        d["address"] = addr.get_text(" ", strip=True)
        bold = addr.find("b")
        if bold:
            d["city"] = bold.get_text(strip=True)

    tel = soup.select_one("a[href^='tel:']")
    if tel:
        d["phone"] = tel.get_text(strip=True)
    wa = soup.find("a", href=re.compile(r"https?://wa\.me/\d+"))
    if wa:
        d["whatsapp"] = wa.get_text(strip=True) or re.search(
            r"wa\.me/(\d+)", wa["href"]).group(1)
    web = soup.select_one("div.weblinks a[href]")
    if web:
        d["website"] = web["href"].strip().rstrip("/")
    desc = soup.select_one("div.text.desc")
    if desc:
        d["description"] = desc.get_text(" ", strip=True)

    # photos: data-mfp-src holds the larger version (no leading underscore)
    images = []
    for ph in soup.select("div.photo_href[data-mfp-src]"):
        images.append(urljoin(BASE, ph["data-mfp-src"]))
    if images:
        d["images"] = images
    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        d["logo_url"] = og["content"].strip()

    rate = soup.select_one("#cmp_top .rate, .cmp_rate .rate")
    if rate:
        try:
            d["rating"] = float(rate.get_text(strip=True))
        except ValueError:
            pass
    rev = soup.select_one(".reviews_count")
    if rev:
        m = re.search(r"(\d+)", rev.get_text())
        if m:
            d["reviews_count"] = int(m.group(1))

    # established year / employees
    for info in soup.select(".extra_info .info"):
        label = info.select_one(".label")
        if not label:
            continue
        text = info.get_text(" ", strip=True).lower()
        if "establishment" in text:
            m = re.search(r"(\d{4})", text)
            if m:
                d["established_year"] = int(m.group(1))
        elif "employees" in text:
            d["employees"] = info.get_text(" ", strip=True).split("\n")[-1].strip()

    cats = []
    for a in soup.select("div.tags a[href^='/category/']"):
        slug = a["href"].split("/category/")[-1].split("/")[0]
        if slug not in cats:
            cats.append(slug)
    if cats:
        d["categories"] = cats

    # map link if present (embed coords)
    mapbtn = soup.find(attrs={"data-map-ltd": True})
    if mapbtn:
        try:
            d["latitude"] = float(mapbtn["data-map-ltd"])
            d["longitude"] = float(mapbtn["data-map-lng"])
        except (ValueError, TypeError, KeyError):
            pass
    d["brand_key"] = brand_key(d.get("name") or "")
    return d
