"""Pipeline configuration: Ghana only. Cities, areas, categories, weights, tokens."""

# Priority city -> areas to crawl. Ghana-only; no multi-country layers anywhere.
CITIES = {
    "Accra": {
        "priority": 0,
        "areas": ["Tema", "Madina", "Spintex", "East Legon", "Osu", "Airport City", "Adenta", "Dansoman"],
    },
    "Kumasi": {"priority": 1, "areas": ["Adum", "KNUST", "Ahodwo", "Suame"]},
    "Takoradi": {"priority": 2, "areas": ["Market Circle", "Beach Road"]},
    "Tamale": {"priority": 3, "areas": ["Central"]},
    "Cape Coast": {"priority": 4, "areas": ["Kotokuraba", "Elmina Road"]},
}

# GhanaYello category slugs worth scanning first (pay-capable, design-hungry).
CATEGORIES = [
    "beauty_salons", "hotels", "restaurants", "event_organisers", "lawyers",
    "pharmacies", "kitchen_furniture", "travel_agents", "photography",
    "fashion", "private_schools", "clinics",
]

# Businesses that can actually pay for design work (ability-to-pay signal).
PREMIUM_CATEGORIES = {"hotels", "lawyers", "pharmacies", "event_organisers",
                      "travel_agents", "private_schools", "clinics",
                      "restaurants", "fashion", "photography", "kitchen_furniture"}

# Countries the pipeline may operate in. One at a time by default; the scan
# stages become aware of `--country`. Ghana is the base install; Nigeria has
# no robots-compliant bulk directory source yet (probed 2026-10-20: all
# blocked) -> mark unscannable until a compliant source is wired.
COUNTRIES = {
    "ghana": {"cc": "+233", "currency": "GHS",
              "cities": CITIES},
    "kenya": {"cc": "+254", "currency": "KES",
              "cities": {"Nairobi": {"priority": 0, "areas": ["CBD", "Westlands", "Ngara", "Kilimani"]},
                         "Mombasa": {"priority": 1, "areas": ["Central"]},
                         "Kisumu": {"priority": 2, "areas": ["Central"]}}},
    "nigeria": {"cc": "+234", "currency": "NGN", "scannable": True,
                "source": "businesslist.com.ng (crawl-delay 40 = slow, compliant)",
                "cities": {"Lagos": {"priority": 0, "areas": ["Ikeja", "Lekki", "Yaba", "Surulere"]},
                           "Abuja": {"priority": 1, "areas": ["Central"]},
                           "Port Harcourt": {"priority": 2, "areas": ["Central"]},
                           "Ibadan": {"priority": 3, "areas": ["Central"]}}},
}
DEFAULT_COUNTRY = "ghana"

# Stage 3 weights (recalibrated from outcomes only through the weights table).
WEIGHTS = {
    "health": 0.25,     # business health
    "readiness": 0.20,  # digital readiness
    "need": 0.20,       # need signal
    "pay": 0.15,        # ability to pay
    "reach": 0.10,      # decision-maker reachability
    "assets": 0.10,     # asset availability
}
TIERS = {"A": 75, "B": 55, "C": 0}          # threshold -> tier
INACTIVE_DAYS_DQ = 90                        # hard disqualifier
HERO_MIN_WIDTH = 1080                        # under this = not hero-suitable

# Per-source politeness budget (seconds between requests).
RATE_LIMITS = {
    "ghanayello": 1.5,
    "businessghana": 3.0,
    "ngex": 4.0,     # ngex.com (Nigeria Galleria keyword search)
    "kenyayp": 3.5,  # yellowpageskenya.com
    "blng": 41.0,    # businesslist.com.ng — their robots asks crawl-delay 40
    "search": 4.5,   # lite.duckduckgo.com (socials stage; gentle, jittered)
    "tonaton": 3.0,
    "jiji": 4.0,
    "places": 0.5,
    "facebook": 1.0,
    "instagram": 1.0,
    "tiktok": 1.0,
}

# Optional official-API credentials (none required; sources degrade gracefully).
PLACES_API_KEY = _env = None  # set via env below
import os as _os
PLACES_API_KEY = _os.environ.get("GOOGLE_PLACES_KEY") or ""
FB_GRAPH_TOKEN = _os.environ.get("FB_GRAPH_TOKEN") or ""
IG_TOKEN = _os.environ.get("IG_TOKEN") or ""
TIKTOK_TOKEN = _os.environ.get("TIKTOK_TOKEN") or ""

# Entities we never pitch or contact (Act 843 / hard DQ: government, NGO).
BLOCKLIST_TERMS = ("ministry", "government", "assembly", "commission",
                   "foundation", "ngo", "charity", "non-profit", "npp", "ndc")
