from __future__ import annotations

"""Ghana-specific normalization: phones to +233, GhanaPostGPS, area inference,
language flags (Twi / Ga / Ewe / Hausa)."""
import re

# MTN / Telecel / AirtelTigo mobile prefixes (9 national digits after 0/233).
GH_PREFIXES = ("24", "54", "55", "59", "20", "50", "27", "57", "26", "56")

# Nigeria: MTN (070/080/081/090 series), Glo, Airtel, 9mobile powdered ranges
# (10 national digits). Prefix list is broad: any 0[7-9]xx start.
NG_PREFIXES = tuple({f"{p}0"[:2] for p in ()} | {
    "70", "80", "81", "90", "71", "91", "92", "93"})

# Kenya: Safairtel/Airtel mobile 07xx (7/1 lead) + Nairobi landline 020.
KE_PREFIXES = ("70", "71", "72", "73", "74", "75", "76", "77", "78", "79",
               "10", "11", "20", "12", "13")


def normalize_phone(raw: str, country: str = "ghana") -> str | None:
    """Return E.164 (+<cc>XXXXXXXXX) for a working local number, else None.
    Country rules: ghana (+233, 9-digit national), nigeria (+234, 10-digit),
    kenya (+254, 9-digit after leading 0)."""
    rules = PHONE_COUNTRIES.get((country or "ghana").lower())
    if not rules or not raw:
        return None
    cc, valid_prefixes = rules["cc"], rules["prefixes"]
    digits = re.sub(r"\D", "", raw)
    if digits.startswith("00" + cc[1:]):
        digits = digits[2:]
    if digits.startswith(cc[1:]) and len(digits) >= len(cc):
        digits = digits[len(cc) - 1:]
    if digits.startswith("0"):
        digits = digits[1:]
    if len(digits) != rules["length"] or digits[:2] not in valid_prefixes:
        return None
    return cc + digits


PHONE_COUNTRIES = {
    "ghana":   {"cc": "+233", "length": 9, "prefixes": GH_PREFIXES},
    "nigeria": {"cc": "+234", "length": 10, "prefixes": NG_PREFIXES},
    "kenya":   {"cc": "+254", "length": 9, "prefixes": KE_PREFIXES},
}


GHANAPOST_RE = re.compile(r"\b([A-Z]{2})-(\d{3})-(\d{4})\b")

def extract_ghana_post(text: str) -> str | None:
    """GhanaPostGPS digital address, e.g. GA-183-8164."""
    if not text:
        return None
    m = GHANAPOST_RE.search(text.upper())
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None


TARGET_LANGS = ("tw", "ga", "ewe", "ha")

# Curated everyday markers (spellings tolerate ASCII approximations).
LANG_MARKERS = {
    "tw": ["medaase", "mepaakyew", "akwaaba", "ete sen", "ete sɛn", "ɛte sɛn",
           "3te s3n", "wo ho te sɛn", "ɛyɛ", "ey3", "aduane", "yaa amoako",
           "maakye", "emaakye", "mema", "me ma wo", "wob3", "da akwadaa"],
    "ga": ["ojekoo", "ebaala", "ojooo", "gbɛ", "shwɔ", "mli", "ɛnaa", "enaa"],
    "ewe": ["akpe", "miawoezɔ", "miawoenam", "woe zɔ", "eƒe", "megbɔ", "nuwo"],
    "ha": ["sannu", "barka", "ina wuni", "kuwa da", "ko sai", "ka kauce"],
}


def detect_language(text: str) -> str:
    """'en' by default; 'tw'/'ga'/'ewe'/'ha' when the text is clearly that language."""
    if not text:
        return "en"
    low = " " + (text or "").lower().replace("\n", " ") + " "
    best, hits = "en", 0
    for lang, markers in LANG_MARKERS.items():
        n = sum(low.count(m) for m in markers)
        if n > hits:
            best, hits = lang, n
    return best if hits >= 2 else "en"


def infer_area(address: str, city: str) -> str | None:
    """Best-effort area out of a street address; falls back to None."""
    if not address:
        return None
    for area in ("osu", "east legon", "spintex", "madina", "tema", "adenta",
                 "dansoman", "adum", "suame"):
        if area in address.lower():
            return area.title()
    return None
