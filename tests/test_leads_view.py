"""Tests for the top-lead view: opt-out exclusion + country filtering.

These run entirely on an in-memory fixture — cmd_leads/cmd_optout call
store.db(), so the context manager is patched for the duration of each test.
The real data/leads.db is never touched here.
"""
from __future__ import annotations

import contextlib
import io
import sqlite3
import types
import unittest
from unittest import mock

from pipeline import run
from pipeline import db as store
from pipeline.db import upsert_business, SCHEMA, _migrate


def _fresh():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _migrate(conn)
    return conn


class _DbCase(unittest.TestCase):
    """Every test gets its own in-memory db behind run.store.db."""

    def setUp(self):
        self.conn = _fresh()
        @contextlib.contextmanager
        def fake_db():
            yield self.conn
        patcher = mock.patch.object(store, "db", fake_db)
        patcher.start()
        self.addCleanup(patcher.stop)


def _card(name="Adwoa Salon", phone_e164="+233244000000", source_id="7",
          country="ghana"):
    return {"source": "ghanayello", "source_id": source_id, "name": name,
            "city": "Accra", "phone": phone_e164, "phone_e164": phone_e164,
            "area": "osu", "area_key": "accra|osu", "language": "en",
            "ghana_post": None, "source_of": "ghanayello",
            "categories": ["beauty_salons"], "country": country,
            "website_status": "unknown"}


def _tiered(conn, **kw):
    rid = upsert_business(conn, _card(**kw))
    conn.execute("UPDATE businesses SET tier='B', accept_score=52 WHERE id=?",
                 (rid,))
    return rid


def _lead_lines(conn, country=None, limit=10):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run.cmd_leads(types.SimpleNamespace(limit=limit, country=country))
    return buf.getvalue()


class LeadsViewTests(_DbCase):
    def test_opted_out_lead_never_listed(self):
        conn = self.conn
        rid = _tiered(conn, name="Adwoa Salon")
        _tiered(conn, name="Kofi Tours", source_id="9",
                phone_e164="+233201111111")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            run.cmd_optout(types.SimpleNamespace(contact="#%d" % rid,
                                                 reason="test"))
        listing = _lead_lines(conn)
        self.assertNotIn("Adwoa Salon", listing)
        self.assertIn("Kofi Tours", listing)
        flag = conn.execute("SELECT opt_out FROM businesses WHERE id=?",
                            (rid,)).fetchone()[0]
        self.assertEqual(flag, 1)
        # the permanent table remembers phone + brand + source so a re-scan
        # of the same brand is excluded at ingest, not just filtered here
        n = conn.execute("SELECT COUNT(*) FROM opt_out").fetchone()[0]
        self.assertEqual(n, 3)

    def test_optout_by_name_part(self):
        conn = self.conn
        rid = _tiered(conn, name="Mama Kate Catering")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            run.cmd_optout(types.SimpleNamespace(contact="kate", reason=None))
        self.assertEqual(
            conn.execute("SELECT opt_out FROM businesses WHERE id=?",
                         (rid,)).fetchone()[0], 1)
        self.assertIn("opted out #", buf.getvalue())

    def test_optout_no_match_is_explicit(self):
        conn = self.conn
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            run.cmd_optout(types.SimpleNamespace(contact="zzz-nonexistent",
                                                 reason=None))
        self.assertIn("no lead matches", buf.getvalue())
        self.assertEqual(
            conn.execute("SELECT COUNT(*) FROM opt_out").fetchone()[0], 0)

    def test_phoneless_optout_recorded_for_ingest(self):
        conn = self.conn
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            run.cmd_optout(types.SimpleNamespace(contact="+233541234567",
                                                 reason=None))
        self.assertEqual(
            conn.execute("SELECT COUNT(*) FROM opt_out").fetchone()[0], 1)

    def test_optout_twice_is_idempotent(self):
        conn = self.conn
        _tiered(conn, name="Adwoa Salon")
        for _ in range(2):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                run.cmd_optout(types.SimpleNamespace(contact="adwoa",
                                                     reason=None))
        self.assertIn("already opted out", buf.getvalue())
        self.assertEqual(
            conn.execute("SELECT COUNT(*) FROM opt_out").fetchone()[0], 3)


class LeadsRotationTests(_DbCase):
    def _leads(self, conn, limit=10, country=None, all_=False, reset=False):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            run.cmd_leads(types.SimpleNamespace(
                limit=limit, country=country, **{"all": all_}, reset=reset))
        return buf.getvalue()

    def _three(self):
        ids = []
        for i, name in enumerate(("Alpha Cafe", "Bravo Salon", "Charlie Tours")):
            ids.append(_tiered(self.conn, name=name, source_id=str(10 + i),
                               phone_e164="+23324400000%d" % i))
        # descending scores, deterministic order
        for rid, score in zip(ids, (52, 51, 50)):
            self.conn.execute(
                "UPDATE businesses SET accept_score=? WHERE id=?", (score, rid))
        return ids

    def test_second_run_serves_next_batch(self):
        ids = self._three()
        first = self._leads(self.conn, limit=2)
        self.assertIn("Alpha Cafe", first)
        self.assertIn("Bravo Salon", first)
        self.assertNotIn("Charlie Tours", first)
        self.assertIn("2 served", first)
        self.assertIn("1 fresh left", first)
        second = self._leads(self.conn, limit=2)
        self.assertNotIn("Alpha Cafe", second)
        self.assertIn("Charlie Tours", second)
        # served table remembers what was shown, once each
        rows = self.conn.execute(
            "SELECT lead_id, times FROM served_leads ORDER BY lead_id").fetchall()
        self.assertEqual([r["lead_id"] for r in rows], [ids[0], ids[1], ids[2]])
        self.assertTrue(all(r["times"] == 1 for r in rows))

    def test_exhausted_message_and_reset(self):
        self._three()
        self._leads(self.conn, limit=3)
        empty = self._leads(self.conn, limit=3)
        self.assertIn("all 3 leads served", empty)
        self.assertIn("--reset", empty)
        cleared = self._leads(self.conn, reset=True)
        self.assertIn("cleared (3 leads)", cleared)
        again = self._leads(self.conn, limit=3)
        self.assertIn("Alpha Cafe", again)
        self.assertIn("Bravo Salon", again)

    def test_all_flag_replays_without_marking(self):
        self._three()
        self._leads(self.conn, limit=1)
        replay = self._leads(self.conn, limit=10, all_=True)
        self.assertIn("Alpha Cafe", replay)
        self.assertIn("Charlie Tours", replay)
        self.assertNotIn("served", replay.split("\n")[-2])
        n = self.conn.execute("SELECT COUNT(*) FROM served_leads").fetchone()[0]
        self.assertEqual(n, 1)  # --all must not add history

    def test_reset_is_country_scoped(self):
        _tiered(self.conn, name="Ghana Lead", country="ghana", source_id="1")
        _tiered(self.conn, name="Kenya Lead", country="kenya", source_id="2",
                phone_e164="+254703000000")
        self._leads(self.conn, country="ghana")
        self._leads(self.conn, country="kenya")
        cleared = self._leads(self.conn, country="ghana", reset=True)
        self.assertIn("cleared (1 leads)", cleared)
        left = self.conn.execute("SELECT COUNT(*) FROM served_leads").fetchone()[0]
        self.assertEqual(left, 1)  # kenya history untouched

    def test_opted_out_never_served(self):
        rid = _tiered(self.conn, name="Opted Co")
        self.conn.execute("UPDATE businesses SET opt_out=1 WHERE id=?", (rid,))
        listing = self._leads(self.conn)
        self.assertNotIn("Opted Co", listing)
        n = self.conn.execute("SELECT COUNT(*) FROM served_leads").fetchone()[0]
        self.assertEqual(n, 0)


class LeadsCountryTests(_DbCase):
    def test_country_filter(self):
        conn = self.conn
        _tiered(conn, name="Ghana Lead", country="ghana", source_id="1")
        _tiered(conn, name="Kenya Lead", country="kenya", source_id="2")
        listing = _lead_lines(conn, country="kenya")
        self.assertNotIn("Ghana Lead", listing)
        self.assertIn("Kenya Lead", listing)

    def test_full_listing_shows_country_tag(self):
        conn = self.conn
        _tiered(conn, name="Ghana Lead", country="ghana", source_id="1")
        listing = _lead_lines(conn, country=None)
        self.assertIn("/gh", listing)

    def test_unknown_country_refused(self):
        conn = self.conn
        _tiered(conn, name="Ghana Lead", country="ghana", source_id="1")
        listing = _lead_lines(conn, country="spain")
        self.assertIn("unknown country", listing)
        self.assertNotIn("Ghana Lead", listing)

    def test_nigeria_prefix_accepted(self):
        conn = self.conn
        _tiered(conn, name="Naija Lead", country="nigeria", source_id="3",
                phone_e164="+2348031234567")
        listing = _lead_lines(conn, country="nigeria")
        self.assertIn("Naija Lead", listing)


if __name__ == "__main__":
    unittest.main()
