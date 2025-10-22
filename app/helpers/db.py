from contextlib import contextmanager
from pathlib import Path
from os import getenv
from dotenv import load_dotenv
import sqlite3

from app.helpers.log import get_logger, truncate

load_dotenv()
LOCAL_DB_PATH = getenv("LOCAL_DB_PATH", "app/db/data.sqlite")

DB_LOG_PREFIX = "[DBASE]"


@contextmanager
def connect_db():
    """Create a database connection with Rich logging"""
    app_logger = get_logger()
    connection = sqlite3.connect(LOCAL_DB_PATH)

    # Return dictionaries from queries
    connection.row_factory = lambda cursor, row: dict(
        zip([col[0] for col in cursor.description], row)
    )

    class LoggingCursor:
        def __init__(self, cursor, sql_type):
            self._cursor = cursor
            self._sql_type = sql_type

        def fetchall(self):
            rows = self._cursor.fetchall()
            if self._sql_type == 'SELECT':
                num_rows = len(rows)
                row_text = f"{num_rows} {'row' if num_rows == 1 else 'rows'}"
                app_logger.debug(f"[blue]{DB_LOG_PREFIX}  Result:[/blue] {row_text} returned")

                # Log first few rows (preview)
                if num_rows > 0:
                    preview = rows[:3]  # First 3 rows
                    for row in preview:
                        app_logger.debug(f"[blue]{DB_LOG_PREFIX}         [/blue] {truncate(row)}")
                    if num_rows > 3:
                        app_logger.debug(f"[blue]{DB_LOG_PREFIX}         [/blue] ... and {num_rows - 3} more")
            return rows

        def fetchone(self):
            row = self._cursor.fetchone()
            if self._sql_type == 'SELECT':
                row_text = "1 row" if row else "0 rows"
                app_logger.debug(f"[blue]{DB_LOG_PREFIX}  Result:[/blue] {row_text} returned")
                if row:
                    app_logger.debug(f"[blue]{DB_LOG_PREFIX}         [/blue] {truncate(row)}")
            return row

        def __getattr__(self, name):
            return getattr(self._cursor, name)

    # Create a wrapper class that intercepts execute calls
    class LoggingConnection:
        def __init__(self, conn):
            self._conn = conn

        def execute(self, sql, params=()):
            try:
                collapsed_sql = ' '.join(sql.split())
                self._log_query(collapsed_sql, params)

                cursor = self._conn.execute(sql, params)


                if sql.strip().upper().startswith('SELECT'):
                    return LoggingCursor(cursor, 'SELECT')

                self._log_result(sql, cursor.rowcount, cursor.lastrowid)

                return cursor

            except sqlite3.Error as e:
                app_logger.error(f"[red bold]{DB_LOG_PREFIX}   Error:[/red bold] {e}")
                raise

        def executemany(self, sql, params):
            try:
                collapsed_sql = ' '.join(sql.split())
                params_list = list(params)
                self._log_query(collapsed_sql, f"{len(params_list)} rows")

                cursor = self._conn.executemany(sql, params_list)

                self._log_result(sql, cursor.rowcount, cursor.lastrowid)

                return cursor

            except sqlite3.Error as e:
                app_logger.error(f"[red bold]{DB_LOG_PREFIX}   Error:[/red bold] {e}")
                raise


        def _log_query(self, sql, params):
            app_logger.debug(f"[blue]{DB_LOG_PREFIX}   Query:[/blue] {sql}")
            app_logger.debug(f"[blue]{DB_LOG_PREFIX}  Params:[/blue] {params}")

        def _log_result(self, sql, rowcount, lastid):
            sql = sql.upper()
            row_text = f"{rowcount} {'row' if rowcount == 1 else 'rows'}"
            if sql.startswith('INSERT'):
                app_logger.debug(f"[blue]{DB_LOG_PREFIX}  Result:[/blue] {row_text} inserted [dim](ID: {lastid})[/dim]")
            elif sql.startswith('UPDATE'):
                app_logger.debug(f"[blue]{DB_LOG_PREFIX}  Result:[/blue] {row_text} updated")
            elif sql.startswith('DELETE'):
                app_logger.debug(f"[blue]{DB_LOG_PREFIX}  Result:[/blue] {row_text} deleted")
            else:
                app_logger.debug(f"[blue]{DB_LOG_PREFIX}  Result:[/blue] {row_text} affected")

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


def init_db():
    """Initialize database - ensure directory exists"""
    db_path = Path(LOCAL_DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)


def init_db_table(app, table_name: str, schema: str, seed_sql: str, seed_data: list):
    """Initialize a database table with schema and seed data"""

    with connect_db() as db:
        # Check if table exists
        table_exists = db.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name=?
        """, (table_name,)).fetchone()

        # Create table if it doesn't exist
        if not table_exists:
            app.logger.info(f"[cyan]{DB_LOG_PREFIX}   Table:[/cyan] creating '{table_name}'")
            db.execute(schema)

            # Seed with sample data
            if seed_data:
                app.logger.info(f"[cyan]{DB_LOG_PREFIX}   Table:[/cyan] seedinmg '{table_name}' with data")
                db.executemany(seed_sql, seed_data)
                app.logger.info(f"[cyan]{DB_LOG_PREFIX}   Table:[/cyan] '{table_name}' created and seeded with {len(seed_data)} rows")


