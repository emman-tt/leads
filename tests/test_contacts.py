"""Contact sanitizer tests — button-text junk must not eat real numbers."""
from __future__ import annotations

import sqlite3
import unittest

from pipeline import db as store
from pipeline.db import SCHEMA, _migrate
from pipeline.run import _sanitize_contacts


def _conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _migrate(conn)
    return conn


def _insert(conn, phone, whatsapp=None, e164=None):
    conn.execute(
        "INSERT INTO businesses (source, source_id, name, city, phone, whatsapp, "
        "phone_e164, country, website_status) VALUES (?,?,?,?,?,?,?,?,?)",
        ("kenyayp", "k:" + str(phone), "Clinic", "Nairobi", phone, whatsapp,
         e164, "kenya", "NONE"))
    conn.commit()
    return conn.execute("SELECT * FROM businesses ORDER BY id DESC LIMIT 1").fetchone()


class SanitizeTests(unittest.TestCase):
    def test_kenyan_number_survives(self):
        conn = _conn()
        _insert(conn, "+254202166281", e164="+254202166281")
        _sanitize_contacts(conn)
        row = conn.execute("SELECT phone, phone_e164 FROM businesses").fetchone()
        self.assertTrue(row["phone"], "real Kenyan number must not be nulled")
        self.assertEqual(row["phone_e164"], "+254202166281")

    def test_e164_never_overwritten_by_raw(self):
        conn = _conn()
        _insert(conn, "call us now", e164="+254780406755")
        _sanitize_contacts(conn)
        row = conn.execute("SELECT phone, phone_e164 FROM businesses").fetchone()
        self.assertIsNone(row["phone"])  # button text dropped
        self.assertEqual(row["phone_e164"], "+254780406755")

    def test_ghana_number_still_normalized(self):
        conn = _conn()
        _insert(conn, "024 400 0000", e164=None)
        _sanitize_contacts(conn)
        row = conn.execute("SELECT phone, phone_e164 FROM businesses").fetchone()
        self.assertEqual(row["phone_e164"], "+233244000000")


if __name__ == "__main__":
    unittest.main()
