"""SQLite connection helper and configuration.

Configuration comes from environment variables. A `.env` file in the package
root is read if it exists; variables already set in the environment win.

    SQLITE_DATABASE   path to the database file   (default: data/anke.db)
    DAILY_CSV         path to the daily export    (default: data/daily.csv)
"""

import os
import sqlite3
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PACKAGE_DIR / "data"


def load_env(path=PACKAGE_DIR / ".env"):
    """Read KEY=value lines from a .env file into os.environ without overriding existing values."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def setting(name, default):
    """Return a path setting; relative paths are resolved from the package root."""
    path = Path(os.getenv(name, default))
    return path if path.is_absolute() else PACKAGE_DIR / path


load_env()
DATABASE = setting("SQLITE_DATABASE", DATA_DIR / "anke.db")
DAILY_CSV = setting("DAILY_CSV", DATA_DIR / "daily.csv")


def connect(path=None):
    """Open the exercise database with foreign keys enforced."""
    conn = sqlite3.connect(path or DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
