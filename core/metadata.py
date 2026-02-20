from __future__ import annotations
from pathlib import Path
import sqlite3
import time

SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
  filename TEXT PRIMARY KEY,
  added_at INTEGER NOT NULL,
  size_bytes INTEGER NOT NULL,
  description TEXT
);
"""

class MetaStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        # Ensure the parent directory for the database exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # Initialize the database schema if it doesn't exist
        with self._connect() as con:
            con.executescript(SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        # Helper method to open a connection to the SQLite database
        return sqlite3.connect(self.db_path)

    def upsert(self, filename: str, size_bytes: int) -> None:
        # Insert or update a file's metadata (filename, timestamp, size, description)
        now = int(time.time())  # Current Unix timestamp
        with self._connect() as con:
            # Try to fetch the existing description for this file, if any
            row = con.execute(
                "SELECT description FROM files WHERE filename=?",
                (filename,),
            ).fetchone()
            existing_desc = row[0] if row else None

            # Insert new or update existing record for this file
            con.execute(
                """
                INSERT INTO files(filename, added_at, size_bytes, description)
                VALUES(?,?,?,?)
                ON CONFLICT(filename) DO UPDATE SET
                  added_at=excluded.added_at,
                  size_bytes=excluded.size_bytes,
                  description=excluded.description
                """,
                (filename, now, size_bytes, existing_desc),
            )

    def set_description(self, filename: str, description: str) -> None:
        # Set or update the description for a file
        now = int(time.time())  # Current Unix timestamp
        with self._connect() as con:
            # Try to fetch the existing file size, default to 0 if not found
            row = con.execute(
                "SELECT size_bytes FROM files WHERE filename=?",
                (filename,),
            ).fetchone()
            size_bytes = row[0] if row else 0

            # Insert new or update existing record with the new description
            con.execute(
                """
                INSERT INTO files(filename, added_at, size_bytes, description)
                VALUES(?,?,?,?)
                ON CONFLICT(filename) DO UPDATE SET
                  description=excluded.description,
                  added_at=excluded.added_at
                """,
                (filename, now, size_bytes, description),
            )

    def get_description(self, filename: str) -> str | None:
        # retrieve the description for a given file, or None if not found
        with self._connect() as con:
            row = con.execute(
                "SELECT description FROM files WHERE filename=?",
                (filename,),
            ).fetchone()
        return row[0] if row else None

    def list_files(self) -> list[str]:
        # Return a list of all filenames in the database, sorted alphabetically
        with self._connect() as con:
            rows = con.execute("SELECT filename FROM files ORDER BY filename").fetchall()
        return [r[0] for r in rows]