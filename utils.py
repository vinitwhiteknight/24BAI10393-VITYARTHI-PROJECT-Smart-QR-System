"""
utils.py
--------
Small, reusable helper functions that don't belong to any single module.

Keeping these separate avoids repeating the same three lines of code
inside scanner.py, storage.py and analytics.py.
"""

import os
from datetime import datetime

from config import DATA_DIR


def ensure_data_dir_exists():
    """
    Make sure the 'data/' folder exists before we try to write the
    database or export files into it. Without this, a fresh clone of
    the repository (which has no data/ folder committed, since it's
    normally in .gitignore) would crash on first run.
    """
    os.makedirs(DATA_DIR, exist_ok=True)


def get_current_date_str():
    """Return today's date as DD-MM-YYYY, e.g. '17-09-2026'."""
    return datetime.now().strftime("%d-%m-%Y")


def get_current_time_str():
    """Return the current time as HH:MM:SS, e.g. '20:15:42'."""
    return datetime.now().strftime("%H:%M:%S")


def get_timestamp():
    """
    Return a single combined timestamp used for cooldown/duplicate
    comparisons. Using time.time()-style float is easier to do math on
    than a formatted string.
    """
    return datetime.now().timestamp()
