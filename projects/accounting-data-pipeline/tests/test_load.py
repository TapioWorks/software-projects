"""Tests for src/load.py. Run with: python -m unittest discover tests"""

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))

from load import TotLoader, parse_amount, parse_month  # noqa: E402

HEADER = "Yhtiötunnus;Vuosikuukausi;Tilin numero;Kustannuspaikka;Konsernikustannuspaikka;Summa;Vyörytetty kustannuspaikka\n"


def make_db():
    conn = sqlite3.connect(":memory:")
    conn.executescript((PACKAGE / "data" / "schema.sql").read_text(encoding="utf-8"))
    conn.execute("""INSERT INTO "Yhtiö" VALUES (1, 'Testiyhtiö', 'AS')""")
    conn.executemany("""INSERT INTO "Kustannuspaikka" VALUES (?, ?)""",
                     [(1, "16000"), (2, "16750"), (3, "YLKU")])
    return conn


def write_csv(lines):
    f = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".csv", delete=False)
    f.write(HEADER + "".join(line + "\n" for line in lines))
    f.close()
    return f.name


def amounts(conn):
    sql = """SELECT "Kustannuspaikka", "Vuosikuukausi", "Summa_snt" FROM "TOT" ORDER BY 1, 2"""
    return conn.execute(sql).fetchall()


class ParseTest(unittest.TestCase):
    def test_parse_month(self):
        self.assertEqual(parse_month("202107"), "2021-07-01")

    def test_parse_amount(self):
        self.assertEqual(parse_amount("100.50"), 10050)
        self.assertEqual(parse_amount("-20.00"), -2000)


class LoadTest(unittest.TestCase):
    def setUp(self):
        self.conn = make_db()
        self.initial = write_csv([
            "AS;202106;3000;16000;;100.50;",
            "AS;202107;3000;16000;;200.00;",
            "AS;202107;3000;16750;;12.25;YLKU",
        ])

    def test_initial_load(self):
        stats = TotLoader(self.conn).run(self.initial)
        self.assertEqual(stats["inserted"], 3)
        self.assertEqual(amounts(self.conn), [(1, "2021-06-01", 10050), (1, "2021-07-01", 20000), (2, "2021-07-01", 1225)])

    def test_rerun_changes_nothing(self):
        TotLoader(self.conn).run(self.initial)
        stats = TotLoader(self.conn).run(self.initial)
        self.assertEqual(stats, {"inserted": 0, "updated": 0, "deleted": 0, "unchanged": 3})

    def test_changed_amount_is_updated(self):
        TotLoader(self.conn).run(self.initial)
        changed = write_csv([
            "AS;202106;3000;16000;;100.50;",
            "AS;202107;3000;16000;;250.00;",
            "AS;202107;3000;16750;;12.25;YLKU",
        ])
        stats = TotLoader(self.conn).run(changed)
        self.assertEqual(stats["updated"], 1)
        self.assertIn((1, "2021-07-01", 25000), amounts(self.conn))

    def test_removed_row_is_deleted(self):
        TotLoader(self.conn).run(self.initial)
        removed = write_csv([
            "AS;202106;3000;16000;;100.50;",
            "AS;202107;3000;16000;;200.00;",
        ])
        stats = TotLoader(self.conn).run(removed)
        self.assertEqual(stats["deleted"], 1)
        self.assertEqual(len(amounts(self.conn)), 2)

    def test_removed_row_from_older_month_is_deleted(self):
        # First, load the original CSV with the June and July rows into the database.
        TotLoader(self.conn).run(self.initial)

        # Create a new CSV where the June row has been removed.
        # Both July rows are still present in the new file.
        updated_csv = write_csv([
            # The first July row is still in the CSV.
            "AS;202107;3000;16000;;200.00;",

            # The second July row is also still in the CSV.
            "AS;202107;3000;16750;;12.25;YLKU",
        ])

        # Run the loader again using the updated CSV.
        # The loader should notice that the June row is missing.
        stats = TotLoader(self.conn).run(updated_csv)

        # Check that exactly one row was deleted from the database.
        self.assertEqual(stats["deleted"], 1)

        # Check that the database now contains only the two July rows.
        # This also checks that their amounts are still correct.
        self.assertEqual(
            amounts(self.conn),
            [
                (1, "2021-07-01", 20000),
                (2, "2021-07-01", 1225),
            ],
        )

    def test_schema_allows_duplicate_natural_keys(self):
        # First load the original CSV data into the database.
        TotLoader(self.conn).run(self.initial)

        # Try to insert another row with the same natural key as the existing June row.
        # Only the amount is different so the six key fields are still the same.
        self.conn.execute("""
            INSERT INTO "TOT" (
                "Yhtiötunnus",
                "Vuosikuukausi",
                "Tilin numero",
                "Kustannuspaikka",
                "Konsernikustannuspaikka",
                "Summa_snt",
                "Vyörytetty kustannuspaikka"
            )
            VALUES (1, '2021-06-01', 3000, 1, NULL, 9999, NULL)
        """)

        # Count how many rows now have this same combination of key fields.
        count = self.conn.execute("""
            SELECT COUNT(*)
            FROM "TOT"
            WHERE "Yhtiötunnus" = 1
            AND "Vuosikuukausi" = '2021-06-01'
            AND "Tilin numero" = 3000
            AND "Kustannuspaikka" = 1
            AND "Konsernikustannuspaikka" IS NULL
            AND "Vyörytetty kustannuspaikka" IS NULL
        """).fetchone()[0]  # Get the count value from the query result.

        # Expect two rows because the current schema allows duplicate natural keys.
        self.assertEqual(count, 2)

    def test_rerun_with_null_cost_centre_does_not_insert_duplicate(self):
        # Create a CSV with one row where all three cost centre fields are empty.
        # These empty values should be stored as NULL in the database.
        csv_path = write_csv([
            "AS;202107;3000;;;100.00;",
        ])

        # Load the CSV into the database for the first time.
        TotLoader(self.conn).run(csv_path)

        # Get the ID of the row that was just inserted.
        # We save it so we can check if the same row is reused later.
        first_id = self.conn.execute(
            'SELECT "Id" FROM "TOT"'
        ).fetchone()[0]

        # Load the exact same CSV again.
        # The loader should recognise that this row already exists.
        TotLoader(self.conn).run(csv_path)

        # Get the ID again after the second load.
        second_id = self.conn.execute(
            'SELECT "Id" FROM "TOT"'
        ).fetchone()[0]

        # Count how many rows exist in TOT.
        # There should still only be one row after loading the same file twice.
        count = self.conn.execute(
            'SELECT COUNT(*) FROM "TOT"'
        ).fetchone()[0]

        # Check that the row has kept the same ID after the second load.
        self.assertEqual(first_id, second_id)

        # Check that the loader did not insert a duplicate row.
        self.assertEqual(count, 1)

    def test_empty_csv_does_not_delete_existing_rows(self):
        # First, load some existing data into TOT.
        loader = TotLoader(self.conn)
        loader.run(self.initial)

        # Create a CSV with a header but no data rows.
        empty_csv = write_csv([])

        before = self.conn.execute(
            'SELECT COUNT(*) FROM "TOT"'
        ).fetchone()[0]

        # The loader should reject the empty snapshot.
        with self.assertRaisesRegex(ValueError, "no data rows"):
            loader.run(empty_csv)

        # Existing rows must remain untouched.
        after = self.conn.execute(
            'SELECT COUNT(*) FROM "TOT"'
        ).fetchone()[0]

        self.assertEqual(after, before)

if __name__ == "__main__":
    unittest.main()
