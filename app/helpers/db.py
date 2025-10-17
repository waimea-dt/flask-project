import sqlite3
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from contextlib import contextmanager

from app.helpers.log import get_sql_logger, wrapped, LOG_COLOURS, ERROR, RESET, DIVIDER

load_dotenv()
LOCAL_DB_PATH = getenv("LOCAL_DB_PATH", "app/db/data.sqlite")

SQL_COLOUR = LOG_COLOURS.get('SQL', "")
sql_logger = get_sql_logger()


def init_db():
    """Initialize database"""

    sql_logger.debug(DIVIDER)
    sql_logger.info(f"DB File: {SQL_COLOUR}{LOCAL_DB_PATH}{RESET}")

    # Ensure the directory exists
    db_path_obj = Path(LOCAL_DB_PATH)
    db_path_obj.parent.mkdir(parents=True, exist_ok=True)


def init_db_table(table_name, schema, seed_insert=None, seed_data=None):
    """Initialize database table and optionally add seed data"""

    with connect_db() as db:
        # Check if table exists
        sql_logger.debug(f"  Table: {SQL_COLOUR}{table_name}{RESET} checking if present...")
        table_exists = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)).fetchone()

        if table_exists:
            sql_logger.info(f"  Table: {SQL_COLOUR}{table_name}{RESET} exists")
        else:
            sql_logger.info(f"  Table: {SQL_COLOUR}{table_name}{RESET} not found, creating...")
            db.execute(schema)

            if seed_insert and seed_data:
                # Seed with sample data
                sql_logger.info(f"  Table: {SQL_COLOUR}{table_name}{RESET} seeding with sample data...")
                db.executemany(seed_insert, seed_data)


@contextmanager
def connect_db():
    """Create a database connection with logging"""

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
                SQL_COLOUR = LOG_COLOURS.get('SQL', "")

                sql_collapsed = ' '.join(sql.split())
                sql_logger.debug(f"  Query: {SQL_COLOUR}{wrapped(sql_collapsed)}{RESET}")
                sql_logger.debug(f" Params: {SQL_COLOUR}{params}{RESET}")

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
                            sql_logger.debug(f" Result: {SQL_COLOUR}{row_text}{RESET} returned")
                        return rows

                    def fetchone(self):
                        row = self._cursor.fetchone()
                        if self._sql_type == 'SELECT':
                            row_text = "1 row" if row else "0 rows"
                            sql_logger.debug(f" Result: {SQL_COLOUR}{row_text}{RESET} returned")
                        return row

                    def __getattr__(self, name):
                        return getattr(self._cursor, name)

                sql_upper = sql.strip().upper()

                if sql_upper.startswith('SELECT'):
                    return LoggingCursor(cursor, 'SELECT')

                # Map SQL commands to their result messages
                row_text = f"{cursor.rowcount} {'row' if cursor.rowcount == 1 else 'rows'}"

                result_messages = {
                    'CREATE': "table created",
                    'INSERT': f"{row_text} created, id={SQL_COLOUR}{cursor.lastrowid}{RESET}",
                    'UPDATE': f"{row_text} updated",
                    'DELETE': f"{row_text} deleted",
                }

                # Find matching command or use default
                for cmd, msg in result_messages.items():
                    if sql_upper.startswith(cmd):
                        sql_logger.debug(f" Result: {SQL_COLOUR}{msg}{RESET}")
                        break
                else:
                    sql_logger.debug(f" Result: {SQL_COLOUR}{row_text}{RESET} affected")

                return cursor

            except sqlite3.Error as e:
                # sql_logger.error(f"{ERROR}  ERROR: {wrapped(e)}{RESET}")
                raise

        def executemany(self, sql, params):
            try:
                SQL_COLOUR = LOG_COLOURS.get('SQL', "")

                sql_logger.debug(f"  Query: {SQL_COLOUR}{' '.join(sql.split())}{RESET}")
                sql_logger.debug(f" Params: {SQL_COLOUR}{len(list(params))} rows{RESET}")

                cursor = self._conn.executemany(sql, params)

                sql_upper = sql.strip().upper()
                row_text = f"{cursor.rowcount} {'row' if cursor.rowcount == 1 else 'rows'}"

                result_messages = {
                    'INSERT': f"{row_text} created",
                    'UPDATE': f"{row_text} updated",
                    'DELETE': f"{row_text} deleted",
                }

                # Find matching command or use default
                for cmd, msg in result_messages.items():
                    if sql_upper.startswith(cmd):
                        sql_logger.debug(f" Result: {SQL_COLOUR}{msg}{RESET}")
                        break
                else:
                    sql_logger.debug(f" Result: {SQL_COLOUR}{row_text}{RESET} affected")

                return cursor

            except sqlite3.Error as e:
                # sql_logger.error(f"{ERROR}  ERROR: {wrapped(e)}{RESET}")
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


