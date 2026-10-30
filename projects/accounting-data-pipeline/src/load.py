"""
Incremental loader for TOT (general ledger) data.

Reads the daily full-history CSV export and synchronises the TOT table so that
only new, changed and removed rows are touched. Unchanged rows are skipped.

Usage:
    python src/load.py [path/to/daily.csv]

The database and CSV paths can also be set with SQLITE_DATABASE and DAILY_CSV
(environment or .env), see db.py.
"""

import csv
import logging
import sys

from db import DAILY_CSV, connect

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

BATCH_SIZE = 10_000

REQUIRED_COLUMNS = {
    "Yhtiötunnus",
    "Vuosikuukausi",
    "Tilin numero",
    "Kustannuspaikka",
    "Konsernikustannuspaikka",
    "Summa",
    "Vyörytetty kustannuspaikka",
}


def parse_month(value: str) -> str:
    """Convert YYYYMM to the ISO date of the first day of the month."""
    return f"{value[:4]}-{value[4:6]}-01"


def parse_amount(value: str) -> int:
    """Convert a euro amount such as '-748.66' to integer cents."""
    return int(float(value) * 100)


def validate_csv(path):
    """Validate the CSV structure and reject empty snapshots."""
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        if reader.fieldnames is None:
            raise ValueError("CSV is empty or missing its header")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(
                f"CSV is missing required columns: {sorted(missing)}"
            )

        if next(reader, None) is None:
            raise ValueError("CSV contains no data rows")


class TotLoader:
    """Synchronises TOT with a full-history CSV export."""

    def __init__(self, conn):
        self.conn = conn
        self.stats = {"inserted": 0, "updated": 0, "deleted": 0, "unchanged": 0}
        self.ensure_index()

    def log_change(self, action, tot_id, old_amount, new_amount):
        # Record the change separately so the current TOT table can represent
        # the latest state while the history table preserves previous amounts.
        self.conn.execute("""
            INSERT INTO "TOT_Muutoshistoria" (
                "TOT_Id", "Muutos", "Vanha_summa_snt", "Uusi_summa_snt"
            )
            VALUES (?, ?, ?, ?)
        """, (tot_id, action, old_amount, new_amount))

    def ensure_index(self):
        """Create a composite index on the natural key to speed up lookups."""
        sql = """
            CREATE INDEX IF NOT EXISTS "TOT_natural_key"
            ON "TOT" ("Yhtiötunnus", "Vuosikuukausi", "Tilin numero", "Kustannuspaikka",
                      "Konsernikustannuspaikka", "Vyörytetty kustannuspaikka")
        """
        self.conn.execute(sql)

    def lookup_id(self, table: str, column: str, value: str):
        """Return the Id of a dimension row, or None for an empty value."""
        if not value:
            return None
        row = self.conn.execute(
            f'SELECT "Id" FROM "{table}" WHERE "{column}" = ?',
            (value,)
        ).fetchone()
        return row[0] if row else None

    def read_csv(self, path):
        """Yield CSV rows converted to TOT column values."""
        with open(path, encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter=";"):
                yield {
                    "Yhtiötunnus": self.lookup_id("Yhtiö", "Kirjanpitotunnus", r["Yhtiötunnus"]),
                    "Vuosikuukausi": parse_month(r["Vuosikuukausi"]),
                    "Tilin numero": int(r["Tilin numero"]),
                    "Kustannuspaikka": self.lookup_id("Kustannuspaikka", "Nimi", r["Kustannuspaikka"]),
                    "Konsernikustannuspaikka": self.lookup_id("Kustannuspaikka", "Nimi", r["Konsernikustannuspaikka"]),
                    "Summa_snt": parse_amount(r["Summa"]),
                    "Vyörytetty kustannuspaikka": self.lookup_id("Kustannuspaikka", "Nimi", r["Vyörytetty kustannuspaikka"]),
                }

    def find_existing(self, row: dict, seen_ids: set):
        """Find an unused matching row, preferring an identical amount."""
        # Use IS for nullable fields so that NULL values can match other NULLs.
        # Exclude IDs already matched to another source row in this run.
        sql = """
            SELECT "Id", "Summa_snt"
            FROM "TOT"
            WHERE "Yhtiötunnus" IS ?
            AND "Vuosikuukausi" = ?
            AND "Tilin numero" IS ?
            AND "Kustannuspaikka" IS ?
            AND "Konsernikustannuspaikka" IS ?
            AND "Vyörytetty kustannuspaikka" IS ?
        """
        params = (
            row["Yhtiötunnus"],
            row["Vuosikuukausi"],
            row["Tilin numero"],
            row["Kustannuspaikka"],
            row["Konsernikustannuspaikka"],
            row["Vyörytetty kustannuspaikka"],
        )

        matches = self.conn.execute(sql, params).fetchall()

        # Prefer a row whose amount is already correct.
        for tot_id, amount in matches:
            if tot_id not in seen_ids and amount == row["Summa_snt"]:
                return tot_id, amount

        # Otherwise reuse an unmatched row and update its amount.
        for tot_id, amount in matches:
            if tot_id not in seen_ids:
                return tot_id, amount

        return None

    def insert(self, row: dict) -> int:
        sql = """
            INSERT INTO "TOT" ("Yhtiötunnus", "Vuosikuukausi", "Tilin numero", "Kustannuspaikka",
                               "Konsernikustannuspaikka", "Summa_snt", "Vyörytetty kustannuspaikka")
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cur = self.conn.execute(sql, (
            row["Yhtiötunnus"],
            row["Vuosikuukausi"],
            row["Tilin numero"],
            row["Kustannuspaikka"],
            row["Konsernikustannuspaikka"],
            row["Summa_snt"],
            row["Vyörytetty kustannuspaikka"],
        ))
        return cur.lastrowid

    def update_amount(self, tot_id: int, amount: int):
        sql = """
            UPDATE "TOT"
            SET "Summa_snt" = ?
            WHERE "Id" = ?
        """
        self.conn.execute(sql, (amount, tot_id))

    def delete_missing(self, seen_ids: set):
        """Delete database rows that were not present in the CSV snapshot."""

        # Store the IDs found in the CSV in a temporary table.
        # This avoids building a potentially huge SQL IN clause in Python.
        self.conn.execute("""
            CREATE TEMP TABLE IF NOT EXISTS "TOT_seen" (
                "Id" INTEGER PRIMARY KEY
            )
        """)

        # Clear IDs left over from a previous run on the same connection.
        self.conn.execute('DELETE FROM "TOT_seen"')

        self.conn.executemany(
            'INSERT INTO "TOT_seen" ("Id") VALUES (?)',
            ((tot_id,) for tot_id in seen_ids),
        )

        # Record deleted rows before removing them, preserving their old amounts
        # in the change history.
        self.conn.execute("""
            INSERT INTO "TOT_Muutoshistoria" (
                "TOT_Id", "Muutos", "Vanha_summa_snt", "Uusi_summa_snt"
            )
            SELECT "Id", 'DELETE', "Summa_snt", NULL
            FROM "TOT"
            WHERE NOT EXISTS (
                SELECT 1
                FROM "TOT_seen"
                WHERE "TOT_seen"."Id" = "TOT"."Id"
            )
        """)

        # The CSV is a full-history snapshot, so any TOT row whose ID was not
        # matched during processing is considered absent and is deleted.
        cur = self.conn.execute("""
            DELETE FROM "TOT"
            WHERE NOT EXISTS (
                SELECT 1
                FROM "TOT_seen"
                WHERE "TOT_seen"."Id" = "TOT"."Id"
            )
        """)

        # Use SQLite's affected-row count to update the deletion statistics.
        self.stats["deleted"] += cur.rowcount

    def run(self, path):
        # Validate the snapshot before making any database changes.
        validate_csv(path)

        # Reset counters so they describe this run, even if the loader is reused.
        self.stats = {
            "inserted": 0,
            "updated": 0,
            "deleted": 0,
            "unchanged": 0,
        }

        # Track matched database IDs so each existing TOT row is reused at most once.
        # IDs not found in the complete snapshot will be deleted after processing.
        seen_ids = set()

        try:
            # Process rows incrementally instead of loading the entire CSV into memory.
            for i, row in enumerate(self.read_csv(path), start=1):
                existing = self.find_existing(row, seen_ids)

                if existing is None:
                    # No unused matching row exists, so insert a new row and record it.
                    tot_id = self.insert(row)
                    self.log_change("INSERT", tot_id, None, row["Summa_snt"])
                    self.stats["inserted"] += 1
                else:
                    tot_id, amount = existing

                    if amount != row["Summa_snt"]:
                        # Save the old and new amounts before updating the current row.
                        self.log_change(
                            "UPDATE", tot_id, amount, row["Summa_snt"]
                        )
                        self.update_amount(tot_id, row["Summa_snt"])
                        self.stats["updated"] += 1
                    else:
                        # Leave unchanged rows untouched to avoid unnecessary writes.
                        self.stats["unchanged"] += 1

                seen_ids.add(tot_id)

                # Report progress without committing; the entire load stays atomic.
                if i % BATCH_SIZE == 0:
                    log.info("Processed %d rows", i)

            # Compare against the complete snapshot, not just the latest month.
            # Missing rows are recorded in the history table before being deleted.
            self.delete_missing(seen_ids)

            # Commit data changes and their history entries together.
            self.conn.commit()

        except Exception:
            # Undo all changes from this run if any step fails.
            self.conn.rollback()
            raise

        log.info("Done: %s", self.stats)
        return self.stats


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else DAILY_CSV
    conn = connect()
    TotLoader(conn).run(csv_path)
    conn.close()
