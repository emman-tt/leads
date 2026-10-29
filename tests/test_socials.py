"""Offline tests for the socials discovery stage (stage 2.5)."""
import unittest

from pipeline.socials import (_SOCIAL_HOSTS, _platform, brand_match,
                              find_socials, parse_results)

SAMPLE = """
<a rel="nofollow" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.instagram.com%2Foceanbluetravel%2F&amp;rut=a1">Ocean Blue Travel (@oceanbluetravel) • Instagram</a>
<a rel="nofollow" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.facebook.com%2FOceanBlueTravel%2Fabout%2F&amp;rut=a2">Ocean Blue Travel - About | Facebook</a>
<a rel="nofollow" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fseekghana.com%2Flisting%2Focean-blue-travel&amp;rut=a3">Seek Ghana listing</a>
<a rel="nofollow" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.instagram.com%2Foceanbluetravel%2F&amp;rut=a4">dup</a>
"""


class FakeClient:
    def __init__(self, body):
        self.body = body
        self.last_url = None

    def get(self, url):
        self.last_url = url
        return type("R", (), {"text": self.body, "status_code": 200})()


class TestParse(unittest.TestCase):
    def test_only_social_links_extracted_and_deduped(self):
        urls = parse_results(SAMPLE)
        self.assertEqual(urls, ["https://www.instagram.com/oceanbluetravel",
                                "https://www.facebook.com/OceanBlueTravel/about"])

    def test_non_social_host_skipped(self):
        self.assertEqual(parse_results('<a href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fseekghana.com%2Fx&amp;rut=b">x</a>'), [])


class TestQuery(unittest.TestCase):
    def test_query_contains_site_filters(self):
        from urllib.parse import unquote_plus
        fc = FakeClient(SAMPLE)
        find_socials(fc, "Ocean Blue Travel Inc", "Kumasi")
        self.assertIn("site:instagram.com", unquote_plus(fc.last_url))
        self.assertIn("Ocean Blue Travel Inc", unquote_plus(fc.last_url))


class TestMatch(unittest.TestCase):
    def test_brand_match_scores_name_tokens(self):
        self.assertEqual(brand_match("https://www.instagram.com/oceanbluetravel", {"ocean", "blue"}), 1.0)
        self.assertEqual(brand_match("https://www.instagram.com/companywheels", {"ocean", "blue"}), 0.0)

    def test_plates_map_platforms(self):
        self.assertEqual(_platform("https://www.instagram.com/x"), "instagram")
        self.assertEqual(_platform("https://linktr.ee/x"), "linktree")
        self.assertEqual(_platform("https://wa.me/233500000000"), "whatsapp")
        self.assertIsNone(_platform("https://seekghana.com/x"))


class TestFind(unittest.TestCase):
    def test_find_socials_ranks_and_dedupes(self):
        cands = find_socials(FakeClient(SAMPLE), "Ocean Blue Travel Inc", "Kumasi")
        plats = [c["platform"] for c in cands]
        self.assertEqual(cands[0]["match"], 0.75)         # ocean/blue/travel hit; 'inc' not in handle
        self.assertIn("instagram", plats)
        self.assertIn("facebook", plats)
        self.assertEqual(len([p for p in plats if p == "instagram"]), 1)  # one per platform
        self.assertTrue(all(c["match"] >= 0.3 for c in cands))


class TestBlock(unittest.TestCase):
    def test_202_challenge_aborts(self):
        import pipeline.socials as sl
        from pipeline.http import HttpError

        class Stub:
            def get(self, url):
                return type("R", (), {"text": "", "status_code": 202})()

        with self.assertRaises(HttpError):
            sl.search_html(Stub(), "query")


if __name__ == "__main__":
    unittest.main()
