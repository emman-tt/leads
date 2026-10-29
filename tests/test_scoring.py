from __future__ import annotations

"""Tests for stage-3 scoring: known good and bad leads."""
import json
import sqlite3
import unittest

from pipeline.db import brand_key, SCHEMA, _migrate
from pipeline.scoring import score_business, factor_health
from pipeline import config


def _row(**over):
    base = {
        "id": 1, "source": "ghanayello", "source_id": "99", "name": "Golden Glow Salon",
        "slug": "gg", "brand_key": brand_key("Golden Glow Salon"), "city": "Accra",
        "region": None, "address": "Osu Oxford St", "phone": "+233 24 400 0000",
        "whatsapp": "+233 24 400 0000", "website": None, "has_website": 0,
        "website_status": "none", "weakness_score": 100, "weakness_flags": "[\"no_website\"]",
        "email": None, "emails": None, "established_year": None, "employees": None,
        "description": "knotless braids, lashes", "categories": ["beauty_salons"],
        "rating": 4.8, "reviews_count": 14, "photos_count": 12, "latitude": 5.55,
        "longitude": -0.17, "logo_url": None, "images": "[\"https://x/1.jpg\"]",
        "videos": None, "socials": "[{\"facebook\":\"fb.com/gg\"}]" if False else json.dumps(
            {"facebook": "fb.com/gg"}),
        "discovered_at": None, "profile_fetched_at": None, "website_checked_at": None,
        "area": "Osu", "ghana_post": None, "language": "en", "phone_e164": "+233244000000",
        "source_of": "ghanayello", "area_key": "accra|osu", "dedupe_key": None,
        "signals": None, "evidence": None, "accept_score": None, "tier": None,
        "score_breakdown": None, "reason": None, "objection": None, "media_ready": 8,
        "scored_at": None, "media_at": None, "brief_at": None, "opt_out": 0,
    }
    base.update(over)
    return base


def _conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _migrate(conn)
    return conn


class ScoringTests(unittest.TestCase):
    def _good(self, **over):
        """Deliberately strong lead: premium category, active, reachable, ready."""
        kwargs = {
            "categories": ["restaurants"] if "categories" not in over else over.pop("categories"),
            "socials": json.dumps({"facebook": "fb.com/gg", "instagram": "instagram.com/gg"}),
            "signals": json.dumps({"posts_30d": 12}),
            "evidence": json.dumps({"metrics": {"has_momo": True, "has_booking": False}}),
        }
        kwargs.update(over)
        return _row(**kwargs)

    def test_good_lead_is_tier_a(self):
        """Strong signals everywhere -> A tier."""
        conn = _conn()
        out = score_business(conn, self._good())
        self.assertGreaterEqual(out["accept_score"], 75)
        self.assertEqual(out["tier"], "A")
        breakdown = json.loads(out["score_breakdown"])
        self.assertIn("health", breakdown)

    def test_low_category_caps_not_dq(self):
        """A no-website beauty salon with decent signals != disqualified, but not A."""
        conn = _conn()
        out = score_business(conn, self._good(categories=["beauty_salons"]))
        self.assertEqual(out["tier"], "B")

    def test_government_entity_is_disqualified(self):
        conn = _conn()
        out = score_business(conn, _row(website_status="none", name="Ministry of Works Salon",
                                        signals=json.dumps({})))
        self.assertEqual(out["tier"], "DISQUALIFIED")
        self.assertIn("government_or_ngo", out["reason"])

    def test_opt_out_is_disqualified(self):
        conn = _conn()
        out = score_business(conn, _row(opt_out=1))
        self.assertEqual(out["tier"], "DISQUALIFIED")

    def test_inactive_lead_is_disqualified(self):
        conn = _conn()
        out = score_business(conn, _row(signals=json.dumps({"updated_ago_days": 180})))
        self.assertEqual(out["tier"], "DISQUALIFIED")
        self.assertIn("inactive_over_90_days", out["reason"])

    def test_strong_site_is_disqualified(self):
        conn = _conn()
        out = score_business(conn, _row(website="https://top-tier.com", website_status="OK",
                                        weakness_score=12, has_website=1))
        self.assertEqual(out["tier"], "DISQUALIFIED")
        self.assertIn("already_strong_site", out["reason"])

    def test_e164_only_contact_not_disqualified(self):
        """Audit keeps phone_e164 canonical for non-Ghana sources; scoring must
        treat it as a working contact (Kenya rows lost `phone` to the old
        sanitizer and were all disqualified)."""
        conn = _conn()
        row = _row(phone=None, whatsapp=None, email=None,
                   phone_e164="+254202166281", socials=json.dumps({}))
        out = score_business(conn, row)
        self.assertNotEqual(out["tier"], "DISQUALIFIED")

    def test_weak_contact_lead_loses_reach_not_dq(self):
        conn = _conn()
        row = _row(website="https://something.com", has_website=1, website_status="weak",
                   weakness_score=55, phone=None, whatsapp=None, email=None,
                   socials=json.dumps({"instagram": "instagram.com/gg"}), media_ready=8)
        out = score_business(conn, row)
        # no phone/wa but has socials -> not hard DQ, but reach factor must be low
        self.assertEqual(out["tier"], "B")
        self.assertLess(json.loads(out["score_breakdown"])["reach"]["score"], 5)

    def test_social_only_with_professional_signals_beats_no_signals(self):
        conn = _conn()
        pro = _row(signals=json.dumps({"posts_30d": 8, "runs_ads": True}),
                   evidence=json.dumps({"metrics": {"has_momo": True, "has_booking": False}}))
        amateur = _row()
        pro_score = score_business(conn, pro)
        amateur_score = score_business(conn, amateur)
        self.assertGreater(pro_score["accept_score"], amateur_score["accept_score"])

    def test_weighted_sum_never_exceeds_100(self):
        conn = _conn()
        out = score_business(conn, _row(media_ready=15))
        self.assertLessEqual(out["accept_score"], 100)

    def test_health_zero_posts_is_floor(self):
        score, why = factor_health(_row(), {"posts_30d": 0})
        self.assertEqual(score, 1)
        self.assertIn("no posts", why)


if __name__ == "__main__":
    unittest.main()
