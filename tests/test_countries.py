"""Offline tests for country expansion: Kenya adapter + multi-country phones."""
import unittest

from pipeline.geo import normalize_phone
from pipeline.sources_local import cards_kenya, KE_CATEGORIES, kenya_category

KE_BASE = "https://www.yellowpageskenya.com"

LISTING_HTML = """
<a href="/business-category/engineering/business-details/2854232-frejed-engineering-services-ltd">FJ</a>
<a href="/process-category/engineering/business-details/2854233-other">other pattern</a>
<a href="https://blog.yellowpageskenya.com/post">noise</a>
"""

DETAIL_HTML = """
<a href="https://www.frejed.co.ke/services">our site</a>
<div>Phone ~ +254101441535 ~ Mobile ~ +25420653799 ~ E-mail ~ info@frejed.co.ke ~
Address ~ P.O. Box 4523-00100 Nairobi GPO ~</div>
<a href="https://facebook.com/KenyaYellowPages">dir social noise</a>
"""


class FakeResp:
    def __init__(self, body): self.text = body


class FakeClient:
    def __init__(self, body): self.body = body
    def get(self, url): return FakeResp(self.body)


class TestKenyaPhones(unittest.TestCase):
    def test_kenya_mobile(self):
        self.assertEqual(normalize_phone("0712345678", "kenya"), "+254712345678")
        self.assertEqual(normalize_phone("254101441535", "kenya"), "+254101441535")

    def test_nigeria_and_ghana(self):
        self.assertEqual(normalize_phone("08031234567", "nigeria"), "+2348031234567")
        self.assertEqual(normalize_phone("0244662682", "ghana"), "+233244662682")

    def test_wrong_country_number_rejected(self):
        self.assertIsNone(normalize_phone("0244662682", "kenya"))


class TestKenyaAdapter(unittest.TestCase):
    def test_cards_parse_ids_and_names(self):
        cards = cards_kenya(LISTING_HTML, KE_BASE)
        self.assertEqual([c["source_id"] for c in cards], ["kenyayp:2854232"])
        self.assertEqual(cards[0]["name"], "Frejed Engineering Services Ltd")

    def test_category_mapping(self):
        self.assertEqual(kenya_category("pharmacies"), "health-and-medical")
        self.assertIn("beauty_salons", KE_CATEGORIES)

    def test_profile_extracts_contacts(self):
        from pipeline.sources_local import kenya_profile_details
        out = kenya_profile_details(FakeClient(DETAIL_HTML),
                                    KE_BASE + "/business-category/x/business-details/1-y")
        self.assertEqual(out["phone"], "+254101441535")
        self.assertEqual(out["email"], "info@frejed.co.ke")
        self.assertEqual(out["website"], "https://www.frejed.co.ke/services")
        self.assertIn("Nairobi", out["address"])
        # 254 landline token like +25420653799 must be the alt, not the lead
        self.assertNotIn("website", [k for k in out.keys() if "api" in str(out[k])])

    def test_tracking_url_never_becomes_website(self):
        """Regression: every Kenya row once carried GTM's script URL as its
        website, which made a lapsed site audit as live."""
        from pipeline.sources_local import kenya_profile_details
        html = """
        <script src="https://www.googletagmanager.com/gtag/js?id=G-Z6HX57VF8P"></script>
        <a href="https://www.googletagmanager.com/gtag/js?id=G-Z6HX57VF8P">gtag</a>
        <a href="https://www.real-clinic.co.ke/">clinic home</a>
        <div>Phone ~ +254101441535 ~ E-mail ~ hello@real-clinic.co.ke</div>
        """
        out = kenya_profile_details(FakeClient(html),
                                    KE_BASE + "/business-category/x/business-details/2-z")
        self.assertEqual(out["website"], "https://www.real-clinic.co.ke/")

    def test_tracking_only_page_has_no_website(self):
        from pipeline.sources_local import kenya_profile_details
        html = """
        <a href="https://www.googletagmanager.com/gtag/js?id=G-X">gtag</a>
        <a href="https://fonts.googleapis.com/css?family=Roboto">font</a>
        <div>Phone ~ +254101441535 ~</div>
        """
        out = kenya_profile_details(FakeClient(html),
                                    KE_BASE + "/business-category/x/business-details/3-w")
        self.assertNotIn("website", out)

    def test_plausible_site_helper(self):
        from pipeline.sources_local import plausible_site
        self.assertFalse(plausible_site("https://www.googletagmanager.com/gtag/js?id=G-1"))
        self.assertFalse(plausible_site("https://fonts.googleapis.com/css2?family=Inter"))
        self.assertFalse(plausible_site("https://cdn.jsdelivr.net/npm/x.js"))
        self.assertTrue(plausible_site("https://vitalray.com/"))
        self.assertTrue(plausible_site("https://www.frejed.co.ke/services"))


if __name__ == "__main__":
    unittest.main()
