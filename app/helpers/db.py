from os import getenv
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from colorama import Fore, Style
from dotenv import load_dotenv

from app.helpers.log import get_sql_logger, LOG_COLOURS

@contextmanager
def connect_db():
    """Create a database connection with logging"""

    load_dotenv()
    LOCAL_DB_PATH = getenv("LOCAL_DB_PATH", "app/db/data.sqlite")

    sql_logger = get_sql_logger()
    connection = sqlite3.connect(LOCAL_DB_PATH)

    # Return dictionaries from queries
    connection.row_factory = lambda cursor, row: dict(
        zip([col[0] for col in cursor.description], row)
    )

    # Create a wrapper class that intercepts execute calls
    class LoggingConnection:
        def __init__(self, conn):
            self._conn = conn

        def execute(self, sql, params=()):
            try:
                SQL_COLOUR = LOG_COLOURS.get('SQL', Fore.WHITE)

                sql_logger.debug(f"  Query: {SQL_COLOUR}{' '.join(sql.split())}{Style.RESET_ALL}")
                sql_logger.debug(f" Params: {SQL_COLOUR}{params}{Style.RESET_ALL}")

                cursor = self._conn.execute(sql, params)

                # Wrap cursor to log when data is fetched
                class LoggingCursor:
                    def __init__(self, cursor, sql_type):
                        self._cursor = cursor
                        self._sql_type = sql_type

                    def fetchall(self):
                        rows = self._cursor.fetchall()
                        if self._sql_type == 'SELECT':
                            num_rows = len(rows)
                            row_text = f"{num_rows} {'row' if num_rows == 1 else 'rows'}"
                            sql_logger.debug(f" Result: {SQL_COLOUR}{row_text} returned{Style.RESET_ALL}")
                        return rows

                    def fetchone(self):
                        row = self._cursor.fetchone()
                        if self._sql_type == 'SELECT':
                            row_text = "1 row" if row else "0 rows"
                            sql_logger.debug(f" Result: {SQL_COLOUR}{row_text} returned{Style.RESET_ALL}")
                        return row

                    def __getattr__(self, name):
                        return getattr(self._cursor, name)

                sql_upper = sql.strip().upper()

                if sql_upper.startswith('SELECT'):
                    return LoggingCursor(cursor, 'SELECT')

                row_text = f"{cursor.rowcount} {'row' if cursor.rowcount == 1 else 'rows'}"
                if sql_upper.startswith('INSERT'):
                    sql_logger.debug(f" Result: {SQL_COLOUR}{row_text} created, ID {cursor.lastrowid}{Style.RESET_ALL}")
                elif sql_upper.startswith('UPDATE'):
                    sql_logger.debug(f" Result: {SQL_COLOUR}{row_text} updated{Style.RESET_ALL}")
                elif sql_upper.startswith('DELETE'):
                    sql_logger.debug(f" Result: {SQL_COLOUR}{row_text} deleted{Style.RESET_ALL}")

                return cursor

            except sqlite3.Error as e:
                sql_logger.error(f"{LOG_COLOURS.get('ERROR')}  ERROR: {e}{Style.RESET_ALL}")
                raise

        def executemany(self, sql, params):
            try:
                SQL_COLOUR = LOG_COLOURS.get('SQL', Fore.WHITE)

                sql_logger.debug(f"  Query: {SQL_COLOUR}{' '.join(sql.split())}{Style.RESET_ALL}")
                sql_logger.debug(f" Params: {SQL_COLOUR}{len(list(params))} rows{Style.RESET_ALL}")

                cursor = self._conn.executemany(sql, params)

                sql_upper = sql.strip().upper()

                row_text = f"{cursor.rowcount} {'row' if cursor.rowcount == 1 else 'rows'}"
                if sql_upper.startswith('INSERT'):
                    sql_logger.debug(f" Result: {SQL_COLOUR}{row_text} created{Style.RESET_ALL}")
                elif sql_upper.startswith('UPDATE'):
                    sql_logger.debug(f" Result: {SQL_COLOUR}{row_text} updated{Style.RESET_ALL}")
                elif sql_upper.startswith('DELETE'):
                    sql_logger.debug(f" Result: {SQL_COLOUR}{row_text} deleted{Style.RESET_ALL}")
                else:
                    sql_logger.debug(f" Result: {SQL_COLOUR}{row_text} affected{Style.RESET_ALL}")

                return cursor

            except sqlite3.Error as e:
                sql_logger.error(f"{LOG_COLOURS.get('ERROR')}  ERROR: {e}{Style.RESET_ALL}")
                raise

        def commit(self):
            return self._conn.commit()

        def rollback(self):
            return self._conn.rollback()

        def close(self):
            return self._conn.close()

        def __getattr__(self, name):
            return getattr(self._conn, name)

    wrapped_connection = LoggingConnection(connection)

    try:
        yield wrapped_connection
        wrapped_connection.commit()
    except Exception:
        wrapped_connection.rollback()
        raise
    finally:
        wrapped_connection.close()


def init_db(app):
    """Initialize database tables and seed data"""

    LOCAL_DB_PATH = getenv("LOCAL_DB_PATH", "app/db/data.sqlite")

    # Ensure the directory exists
    db_path_obj = Path(LOCAL_DB_PATH)
    db_path_obj.parent.mkdir(parents=True, exist_ok=True)

    with connect_db() as db:
        # Check if table exists
        note_table_exists = db.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='note'
        """).fetchone()

        # Create table if it doesn't exist
        if not note_table_exists:
            app.logger.info(f"Local database file: {db_path}")

            db.execute("""
                CREATE TABLE note (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    body TEXT,
                    pinned INTEGER DEFAULT 0,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Seed with sample data
            sample_notes = [
                ("Welcome to Notes", "This is your first note. You can edit or delete it.", 1),
                ("Getting Started", "Create new notes by clicking the 'New Note' button.", 0),
                ("Pinned Notes", "Pinned notes always appear at the top of your list.", 1),
                ("Sample Note", "This is just a sample note with some content.", 0),
            ]

            db.executemany("""
                INSERT INTO note (title, body, pinned)
                VALUES (?, ?, ?)
            """, sample_notes)

            app.logger.info("✓ Database created and seeded with sample notes")