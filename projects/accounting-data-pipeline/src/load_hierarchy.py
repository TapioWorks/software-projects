import csv
import sys

from db import DATA_DIR, connect


def load_hierarchy(conn, path):
    """Load cost-centre parent relationships from a CSV file."""

    # Open the CSV file. newline="" helps the csv module handle line endings.
    with open(path, encoding="utf-8", newline="") as f:

        # Read each CSV row as a dictionary using the column names from the header.
        # The source file uses semicolons to separate the columns.
        reader = csv.DictReader(f, delimiter=";")

        # Clear the old hierarchy before loading the new CSV data.
        # This assumes the CSV contains the complete hierarchy, not just changes.
        # If you need to preserve older relationships that no longer appear in a new CSV.
        conn.execute('DELETE FROM "Kustannuspaikkahierarkia"')

        # Insert all hierarchy relationships into the table.
        # executemany() runs the INSERT for each row from the CSV.
        conn.executemany(
            """
            INSERT INTO "Kustannuspaikkahierarkia"
                ("Kustannuspaikka", "Emokustannuspaikka", "Voimassa alkaen")
            VALUES (?, ?, ?)
            """,
            (
                (
                    # Remove extra spaces from the cost-centre name.
                    row["Kustannuspaikka"].strip(),

                    # Remove extra spaces from the parent name.
                    # If the parent is empty, store NULL instead of an empty string.
                    # This is used for cost centres that have no parent.
                    row["Emokustannuspaikka"].strip() or None,

                    # Remove extra spaces from the date when this relationship starts.
                    row["Voimassa alkaen"].strip(),
                )
                # Go through the CSV one row at a time instead of making a list
                # containing all the hierarchy rows in memory.
                for row in reader
            ),
        )

    # Save the changes to the database.
    conn.commit()


# Only run this part when the file is executed directly,
# not when load_hierarchy() is imported by another Python file.
if __name__ == "__main__":
    # Use the CSV path supplied by the user if one was given.
    # Otherwise, use the default hierarchy CSV inside DATA_DIR.
    path = sys.argv[1] if len(sys.argv) > 1 else (
        DATA_DIR / "kustannuspaikkahierarkia.csv"
    )

    # Open a connection to the database.
    conn = connect()

    try:
        # Load the hierarchy CSV into the database.
        load_hierarchy(conn, path)

        # Count how many hierarchy relationships were loaded.
        # fetchone() returns the first result row, and [0] gets the count.
        count = conn.execute(
            'SELECT COUNT(*) FROM "Kustannuspaikkahierarkia"'
        ).fetchone()[0]

        # Print the number of relationships currently stored in the table.
        print(f"Loaded {count} hierarchy relationships.")

    except Exception:
        # Undo any uncommitted changes if something goes wrong.
        conn.rollback()

        # Raise the error again so the failure is visible to the user.
        raise

    finally:
        # Always close the database connection, even if loading fails.
        conn.close()
