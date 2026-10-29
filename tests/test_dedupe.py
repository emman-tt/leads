from __future__ import annotations

"""Tests for normalization + deduplication rules."""
import sqlite3
import unittest

from pipeline.geo import normalize_phone, extract_ghana_post, detect_language
from pipeline.db import brand_key, dedupe_key, find_duplicate, upsert_business, SCHEMA, _migrate
from pipeline import config


def _conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _migrate(conn)
    return conn


class PhoneTests(unittest.TestCase):
    def test_local_form(self):
        self.assertEqual(normalize_phone("024 400 0000"), "+233244000000")

    def test_international_form(self):
        self.assertEqual(normalize_phone("+233 54 123 4567"), "+233541234567")

    def test_digits_with_00233(self):
        self.assertEqual(normalize_phone("00233201234567"), "+233201234567")

    def test_short_or_fixedline_rejected(self):
        self.assertIsNone(normalize_phone("12345"))
        self.assertIsNone(normalize_phone("+1 415 555 2671"))

    def test_nonsense_is_none(self):
        self.assertIsNone(normalize_phone("whatsapp only"))
        self.assertIsNone(normalize_phone(""))


class GhanaPostTests(unittest.TestCase):
    def test_extract(self):
        self.assertEqual(extract_ghana_post("GA-183-8164 near Osu"), "GA-183-8164")
        self.assertIsNone(extract_ghana_post("no address here"))


class LanguageTests(unittest.TestCase):
    def test_twi_detected(self):
        text = "Akwaaba! Ɛte sɛn? Medaase for visiting our salon ɛyɛ"
        self.assertEqual(detect_language(text), "tw")

    def test_english_default(self):
        self.assertEqual(detect_language("Best tilapia in town. Come through, we deliver"), "en")


class BrandKeyTests(unittest.TestCase):
    def test_branches_collapse(self):
        self.assertEqual(brand_key("Pizzaman Chickenman"), brand_key("Pizzaman Chickenman (Osu)"))
        self.assertNotEqual(brand_key("Kobe Salon"), brand_key("Kobe Hotel"))

    def test_ltd_noise_removed(self):
        self.assertEqual(brand_key("Adwoa Beauty Ltd"), "adwoa beauty")


class DedupeTests(unittest.TestCase):
    def _card(self, name="Adwoa Salon", phone_e164="+233244000000", area="osu", source_id="7"):
        return {"source": "ghanayello", "source_id": "7", "name": name, "city": "Accra",
                "phone": phone_e164, "phone_e164": phone_e164, "area": area,
                "area_key": "accra|osu", "language": "en", "ghana_post": None,
                "source_of": "ghanayello", "categories": ["beauty_salons"],
                "website_status": "unknown"}

    def test_exact_duplicate_not_reinserted(self):
        conn = _conn()
        upsert_business(conn, self._card())
        n0 = conn.execute("SELECT COUNT(*) FROM businesses").fetchone()[0]
        dup = find_duplicate(conn, self._card(source_id="999"))
        self.assertIsNotNone(dup)
        conn.execute("UPDATE businesses SET phone_e164=? WHERE id=?",
                     (dup["phone_e164"], dup["id"]))
        upsert_business(conn, self._card(source_id="777", name="Adwoa Salon",
                                         phone_e164="+233244000000", area="osu"))
        # find_duplicate on same key matches again
        self.assertIsNotNone(find_duplicate(conn, self._card(source_id="888")))
        n1 = conn.execute("SELECT COUNT(*) FROM businesses").fetchone()[0]
        self.assertEqual(n0, n1)

    def test_different_area_kept_separate(self):
        conn = _conn()
        upsert_business(conn, self._card())
        same_name_different_area = self._card(area="tema")
        self.assertIsNone(find_duplicate(conn, same_name_different_area))

    def test_missing_phone_still_matches_on_name_plus_area(self):
        conn = _conn()
        upsert_business(conn, self._card())
        row2 = self._card(phone_e164=None)
        self.assertIsNotNone(find_duplicate(conn, row2))

    def test_config_weights_sum_to_one(self):
        self.assertAlmostEqual(sum(config.WEIGHTS.values()), 1.0, places=6)


if __name__ == "__main__":
    unittest.main()
