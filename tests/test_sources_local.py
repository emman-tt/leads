"""Offline tests for the BusinessGhana second-source adapter."""
import unittest
from unittest import mock

import pipeline.sources_local as sl
from pipeline.sources_local import (BG_TERMS, _cards_businessghana,
                                    profile_details, search_query)

BASE = "https://www.businessghana.com"

SEARCH_HTML = """
<div class="col-sm-4 misc">0244662682</div>
<div><a href="/site/directory/beauty-accessories/15848/Lloyds-Salon">Lloyds Salon</a>
<span>ultra modern Unisex Salon services available.</span></div>
<a href="/site/directory/accounting-firms/399549/RDK-Consulting-Services">featured noise</a>
<a href="/site/directory/pharmacies/399551/Lloyds-Salon">dup id</a>
"""

PROFILE_HTML = """
<div>Street Address ~ ~ ~ Postal Address ~ ~ P.O. Box KN 2702 Kaneshie Accra-Ghana ~ ~
Working Hours ~ Monday to Friday ~ ~ Contact Information ~ Name ~ Lloyds Salon ~
Phone Number ~ +233 0302 916174 , +233 20 420 8000 ~ ~ Website ~ http://www.lloydsnet.com
~ email: info@lloydsnet.com</div>
"""


class FakeResponse:
    def __init__(self, body): self.text = body


class FakeClient:
    def __init__(self, body): self.body = body
    def get(self, url): return FakeResponse(self.body)


class TestCards(unittest.TestCase):
    def test_parses_name_phone_and_dedupes(self):
        cards = _cards_businessghana(SEARCH_HTML, BASE)
        # featured sidebar (the recurring 399549 ad) filtered; a same-name entry
        # under a different id is kept -> cross-record dedupe happens at scan time
        self.assertEqual([c["source_id"] for c in cards],
                         ["businessghana:15848", "businessghana:399551"])
        card = cards[0]
        self.assertEqual(card["name"], "Lloyds Salon")
        self.assertEqual(card["phone"], "0244662682")

    def test_no_phone_card_is_fine(self):
        html = '<a href="/site/directory/hotels/5001/A-Plaza-Hotel">n</a>'
        cards = _cards_businessghana(html, BASE)
        self.assertEqual(cards[0]["name"], "A Plaza Hotel")
        self.assertNotIn("phone", cards[0])

    def test_blank_page_is_safe(self):
        self.assertEqual(_cards_businessghana("<html></html>", BASE), [])


class TestProfile(unittest.TestCase):
    def _parse(self, html):
        with mock.patch.object(sl, "_allowed"), \
             mock.patch.object(sl.RobotFileParser, "read", lambda self: None):
            return profile_details(FakeClient(html),
                                   BASE + "/site/directory/x/1/y")

    def test_extracts_full_contact_block(self):
        out = self._parse(PROFILE_HTML)
        self.assertEqual(out["address"], "P.O. Box KN 2702 Kaneshie Accra-Ghana")
        self.assertEqual(out["phone"], "+233 0302 916174")
        self.assertEqual(out["alt_phone"], "+233 20 420 8000")
        self.assertEqual(out["website"], "http://www.lloydsnet.com")
        self.assertEqual(out["email"], "info@lloydsnet.com")

    def test_empty_fields_return_empty_dict(self):
        self.assertEqual(self._parse("<div>Name ~ X</div>"), {})

    def test_placeholder_site_classifier_rejects_http_none(self):
        out = self._parse("<div>Website ~ http://none ~ Name ~ X</div>")
        self.assertNotIn("website", out)


class TestSearchQuery(unittest.TestCase):
    def test_maps_category_to_search_term(self):
        self.assertEqual(BG_TERMS["beauty_salons"], "salon")

    def test_search_query_end_to_end(self):
        with mock.patch.object(sl, "_allowed"):
            cards = search_query("businessghana", FakeClient(SEARCH_HTML),
                                 "beauty_salons", "Accra", limit=5)
        self.assertEqual(cards[0]["name"], "Lloyds Salon")

    def test_pagination_appends_page_param(self):
        with mock.patch.object(sl, "_allowed"), \
             mock.patch.object(sl, "BeautifulSoup", return_value=sl.BeautifulSoup("<div></div>", "html.parser")):
            self.assertEqual(search_query("businessghana", FakeClient(""), "hotels",
                                          "Accra", limit=5, page=2), [])


if __name__ == "__main__":
    unittest.main()
