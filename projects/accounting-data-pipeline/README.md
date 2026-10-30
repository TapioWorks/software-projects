# Accounting Data Pipeline

A Python and SQLite data pipeline for loading accounting data from CSV files, detecting changes between data snapshots, and querying historical cost-centre hierarchies.

The project demonstrates data ingestion, validation, incremental loading, change tracking, SQL querying, and automated testing.

## Overview

The pipeline processes accounting data from CSV files and synchronises it with a SQLite database.

The main loader identifies records using a composite natural key and handles:

- Inserting new records
- Updating records when their amounts change
- Deleting records that are no longer present in the input snapshot
- Recording data changes in a separate history table
- Avoiding unnecessary updates when records have not changed

The project also includes a separate cost-centre hierarchy loader and a recursive SQL query for retrieving hierarchy relationships as of a selected date.

## Technologies

- **Python** – data loading, validation, and processing
- **SQLite** – relational database and change history
- **SQL** – data manipulation and recursive queries
- **unittest** – automated tests

The implementation uses Python's standard library and does not require external Python packages.

## Project structure

```text
accounting-data-pipeline/
├── data/
│   └── schema.sql
├── src/
│   ├── db.py
│   ├── load.py
│   └── load_hierarchy.py
├── tests/
│   └── test_load.py
├── hierarchy_query.sql
├── example.env
├── .gitignore
└── README.md
```

## Data loading

The main loader reads accounting records from a CSV file and synchronises them with the database.

Records are matched using a composite natural key. The loader compares incoming records with existing database records and applies the necessary changes.

The loading process includes:

1. Validating the CSV structure and required columns.
2. Reading and processing the incoming records.
3. Identifying existing records using the natural key.
4. Inserting new records.
5. Updating records when their amounts have changed.
6. Removing records that are missing from the new snapshot.
7. Recording inserts, updates, and deletes in the change history table.

Unchanged records are left untouched. The loader uses a transaction so that changes can be rolled back if an error occurs during processing.

**Important:** The deletion logic assumes that the input CSV represents a complete snapshot of the data. An incomplete export could cause existing records to be incorrectly deleted. The loader rejects an empty CSV to help prevent accidental deletion of all records.

## Change history

Changes to accounting records are stored separately in the `TOT_Muutoshistoria` table.

The history records insertions, updates, and deletions, including the previous and new amounts where applicable.

This makes it possible to inspect how the accounting data has changed over time instead of only retaining the current state.

## Cost-centre hierarchy

The project handles cost-centre hierarchy data separately from the accounting records.

`load_hierarchy.py` loads hierarchy relationships from a CSV file into the `Kustannuspaikkahierarkia` table. The loader replaces the existing contents of that table when loading a new hierarchy file.

The `hierarchy_query.sql` file contains a recursive Common Table Expression (CTE) that retrieves the parent hierarchy of a selected cost centre for a specified date.

The query follows parent relationships upwards and filters them using their effective start dates.

The query currently does not explicitly detect circular relationships or resolve conflicting parent relationships with the same effective date.

## Configuration

Database and CSV paths are configured through environment variables.

The repository includes an `example.env` file:

```env
SQLITE_DATABASE=data/anke.db
DAILY_CSV=data/daily.csv
```

Copy the example file to `.env` and adjust the paths if needed.

```bash
cp example.env .env
```

The database defaults to `data/anke.db`, and the daily CSV defaults to `data/daily.csv`.

## Running the project

### 1. Initialise the database

Create the database and execute the schema:

```bash
python -c "import sqlite3; from pathlib import Path; from src.db import DATABASE; DATABASE.parent.mkdir(parents=True, exist_ok=True); conn = sqlite3.connect(DATABASE); conn.executescript(Path('data/schema.sql').read_text(encoding='utf-8')); conn.close()"
```

### 2. Load accounting data

Place a compatible CSV file at the configured path and run:

```bash
python src/load.py
```

### 3. Load cost-centre hierarchy data

Place the hierarchy CSV file at the path expected by the hierarchy loader and run:

```bash
python src/load_hierarchy.py
```

### 4. Run the tests

Run the automated test suite from the project root:

```bash
python -m unittest discover tests
```

## Tests

The test suite uses an in-memory SQLite database and covers key loading behaviours, including:

- Initial data loading
- Idempotent repeated loads
- Updating changed amounts
- Deleting records missing from a new snapshot
- Handling nullable fields in the natural key
- Preventing an empty CSV from deleting existing records

## Limitations and possible improvements

There are several areas where the implementation could be improved further:

- **Performance:** The loader performs record-level processing and uses Python to track previously seen records. Staging tables and set-based SQL operations could improve performance with larger datasets.
- **CSV validation:** Additional validation could detect incomplete exports and invalid field values before loading.
- **Amount parsing:** Using `Decimal` instead of floating-point conversion would provide safer monetary value handling.
- **Hierarchy validation:** Cycle detection and validation of conflicting parent relationships could make hierarchy queries more robust.
- **Testing:** More tests could cover malformed input, hierarchy loading, and failure scenarios.
- **Reconciliation:** Additional checks could compare source totals with database totals to identify discrepancies.

The current implementation has not been benchmarked against very large datasets.

## Data and privacy

The repository does not include the original accounting database or source accounting data.

To run the project, provide compatible CSV input files and initialise the database using the included schema.

Do not commit private accounting data, database files, or local environment configuration to the repository.