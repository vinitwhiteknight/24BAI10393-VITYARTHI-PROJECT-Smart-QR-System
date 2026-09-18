"""
storage.py
----------
All database access lives here. No other file should talk to SQLite
directly - they call functions from this module instead.

Table design (matches the ER diagram in the project report):

    SCAN
    --------------------------------
    scan_id        INTEGER PRIMARY KEY
    code_type      TEXT
    decoded_data   TEXT
    scan_date      TEXT   (DD-MM-YYYY)
    scan_time      TEXT   (HH:MM:SS)
"""

import csv
import os
import sqlite3

from config import DB_PATH, EXPORT_CSV_PATH
from utils import ensure_data_dir_exists, get_current_date_str, get_current_time_str


def get_connection():
    """Open (and implicitly create, if missing) the SQLite database file."""
    ensure_data_dir_exists()
    return sqlite3.connect(DB_PATH)


def init_db():
    """
    Create the SCAN table if it doesn't exist yet.
    Safe to call every time the app starts - CREATE TABLE IF NOT EXISTS
    is a no-op on subsequent runs.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS SCAN (
            scan_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            code_type    TEXT NOT NULL,
            decoded_data TEXT NOT NULL,
            scan_date    TEXT NOT NULL,
            scan_time    TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def save_scan(decoded_data, code_type):
    """
    Insert one new scan record. Called by scanner.py only after
    validation + duplicate-checking has already passed.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO SCAN (code_type, decoded_data, scan_date, scan_time)
        VALUES (?, ?, ?, ?)
        """,
        (code_type, decoded_data, get_current_date_str(), get_current_time_str()),
    )
    conn.commit()
    conn.close()


def get_all_scans():
    """
    Return every scan, most recent first, as a list of dicts.
    Used by the CLI history/analytics commands and CSV export.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SCAN ORDER BY scan_id DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def was_recently_scanned(decoded_data, cooldown_seconds):
    """
    Duplicate-prevention check backed by the database itself (rather
    than only an in-memory dict in scanner.py). This means duplicate
    prevention also works across separate CLI invocations.

    Returns True if 'decoded_data' was stored within the last
    `cooldown_seconds` seconds.
    """
    import datetime

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT scan_date, scan_time FROM SCAN
        WHERE decoded_data = ?
        ORDER BY scan_id DESC
        LIMIT 1
        """,
        (decoded_data,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return False

    last_seen = datetime.datetime.strptime(
        f"{row[0]} {row[1]}", "%d-%m-%Y %H:%M:%S"
    )
    elapsed = (datetime.datetime.now() - last_seen).total_seconds()
    return elapsed < cooldown_seconds


def export_to_csv(output_path=None):
    """
    Write all scan records to a CSV file and return its path.
    The output path can be supplied by the CLI.
    """
    scans = get_all_scans()
    path = output_path or EXPORT_CSV_PATH
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["scan_id", "code_type", "decoded_data", "scan_date", "scan_time"])
        for scan in scans:
            writer.writerow(
                [scan["scan_id"], scan["code_type"], scan["decoded_data"],
                 scan["scan_date"], scan["scan_time"]]
            )

    return path


def clear_all_scans():
    """Delete all scan records while keeping the database/table available."""
    conn = get_connection()
    conn.execute("DELETE FROM SCAN")
    conn.commit()
    conn.close()
