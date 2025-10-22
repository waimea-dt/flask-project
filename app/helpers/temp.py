#===========================================================
# Session Related Functions
# - Note that these require tzdata to be imported
#===========================================================

from datetime import datetime
from zoneinfo import ZoneInfo

DEFAULT_LOCAL_TZ = "Pacific/Auckland"
ISO_DATE_FORMAT  = "%Y-%m-%d"
ISO_TIME_FORMAT  = "%H:%M:%S"
DATE_TIME_FORMAT = f"{ISO_DATE_FORMAT} {ISO_TIME_FORMAT}"



#===========================================================
# Note: The following functions are used as Jinja template
#       filters, rather than being called directly


#-----------------------------------------------------------
# Convert a given datetime to local timezone
# - The datetime format is YYYY-MM-DD HH:MM:SS
# - The optional local_timezone defaults to NZ (inc. DST)
#-----------------------------------------------------------
def _utc_datetime_to_local_timezone(
    utc_datetime_str,
    datetime_format = DATE_TIME_FORMAT,
    output_format   = DATE_TIME_FORMAT,
    local_timezone  = DEFAULT_LOCAL_TZ
):
    utc_dt = datetime.strptime(utc_datetime_str, datetime_format)
    utc_dt = utc_dt.replace(tzinfo=ZoneInfo("UTC"))

    # Convert to local timezone
    local_dt = utc_dt.astimezone(ZoneInfo(local_timezone))

    # Format back into datetime string
    return local_dt.strftime(output_format)


#-----------------------------------------------------------
# Convert a given UTC date to local timezone
#-----------------------------------------------------------
def _utc_date_to_local_timezone(utc_date_str, local_timezone = DEFAULT_LOCAL_TZ):
    return _utc_datetime_to_local_timezone(
        utc_date_str,
        ISO_DATE_FORMAT,
        ISO_DATE_FORMAT,
        local_timezone
    )


#-----------------------------------------------------------
# Convert a given UTC time to local timezone
#-----------------------------------------------------------
def _utc_time_to_local_timezone(utc_time_str, local_timezone = DEFAULT_LOCAL_TZ):
    # Need to add in a date for time-only converions
    utc_date_str = datetime.now(ZoneInfo("UTC")).date()
    utc_datetime_str = f"{utc_date_str} {utc_time_str}"
    return _utc_datetime_to_local_timezone(
        utc_datetime_str,
        DATE_TIME_FORMAT,
        ISO_TIME_FORMAT,
        local_timezone
    )


#-----------------------------------------------------------
# Convert a given datetime to a more friendly format
# - The datetime format is YYYY-MM-DD HH:MM:SS
# - The optional format string as per https://strftime.org/
#-----------------------------------------------------------
def _timestamp_friendly(
    timestamp_str,
    datetime_format = DATE_TIME_FORMAT,
    friendly_format = "%a, %d/%m/%Y at %I:%M%p"
):
    dt = datetime.strptime(timestamp_str, datetime_format)

    # Format to a user-friendly string
    return dt.strftime(friendly_format)


#-----------------------------------------------------------
# Convert a given date to a more friendly DD/MM/YYY format
#-----------------------------------------------------------
def _date_friendly(date_str):
    return _timestamp_friendly(date_str, ISO_DATE_FORMAT, "%d/%m/%Y")


#-----------------------------------------------------------
# Convert a given date to a more friendly day of the week format
#-----------------------------------------------------------
def _day_friendly(date_str):
    return _timestamp_friendly(date_str, ISO_DATE_FORMAT, "%a")


#-----------------------------------------------------------
# Convert a given time to a more friendly HH:MM a/pm format
#-----------------------------------------------------------
def _time_friendly(time_str):
    return _timestamp_friendly(time_str, ISO_TIME_FORMAT, "%I:%M%p")


#-----------------------------------------------------------
# Register the above functions as Jinja filters
#-----------------------------------------------------------
def init_datetime(app):
    # Register Jinja filters for timezone adjusting
    app.jinja_env.filters['localtimestamp'] = _utc_datetime_to_local_timezone
    app.jinja_env.filters['localdate']      = _utc_date_to_local_timezone
    app.jinja_env.filters['localtime']      = _utc_time_to_local_timezone
    # Register Jinja filters for friendly versions
    app.jinja_env.filters['nicetimestamp']  = _timestamp_friendly
    app.jinja_env.filters['nicedate']       = _date_friendly
    app.jinja_env.filters['nicetime']       = _time_friendly
    app.jinja_env.filters['niceday']        = _day_friendly



#===========================================================
# Note: The following functions are used directly when
#       processing dates/times from HTML form inputs


#-----------------------------------------------------------
# Create a UTC timestamp, optionally providing a local date
# and local time string (e.g. from a HTML form)
# - local_date_str is in format "YYYY-MM-DD"
# - local_time_str is in format "HH:MM" or "HH:MM:SS"
# - Returns UTC timestamp in format "YYYY-MM-DD HH:MM:SS"
#-----------------------------------------------------------
def utc_datetime_str(
    local_date_str = None,
    local_time_str = None,
    format         = DATE_TIME_FORMAT,
    local_timezone = DEFAULT_LOCAL_TZ
):
    # Deal with optional date/time
    if not local_date_str:
        local_date_str = datetime.now().strftime(ISO_DATE_FORMAT)
    if not local_time_str:
        local_time_str = datetime.now().strftime(ISO_TIME_FORMAT)

    local_tz = ZoneInfo(local_timezone)

    # If no seconds provided, add some
    if len(local_time_str) == 5:
        local_time_str += ":00"

    # Parse the combined date and time string
    local_dt_str = f"{local_date_str} {local_time_str}"
    local_dt = datetime.strptime(local_dt_str, DATE_TIME_FORMAT)
    local_dt = local_dt.replace(tzinfo=local_tz)

    # Convert to UTC
    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))

    # Format as UTC timestamp string
    return utc_dt.strftime(format)


#-----------------------------------------------------------
# Create a UTC datestamp from a given local date
# - local_date_str is in format "YYYY-MM-DD"
# - Returns UTC datestamp in format "YYYY-MM-DD"
#-----------------------------------------------------------
def utc_date_str(
    local_date_str = None,
    local_timezone = DEFAULT_LOCAL_TZ
):
    return utc_datetime_str(
        local_date_str = local_date_str if local_date_str else datetime.now().strftime(ISO_DATE_FORMAT),
        format         = ISO_DATE_FORMAT,
        local_timezone = local_timezone
    )


#-----------------------------------------------------------
# Create a UTC timestamp from a given local time
# - local_time_str is in format "HH:MM:SS" or "HH:MM"
# - Returns UTC timestamp in format "HH:MM:SS"
#-----------------------------------------------------------
def utc_time_str(
    local_time_str = None,
    local_timezone = DEFAULT_LOCAL_TZ
):
    return utc_datetime_str(
        local_time_str = local_time_str if local_time_str else datetime.now().strftime(ISO_TIME_FORMAT),
        format         = ISO_TIME_FORMAT,
        local_timezone = local_timezone
    )



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from os import getenv
from dotenv import load_dotenv
from datetime import datetime
import pytz


load_dotenv()
DEFAULT_TIMEZONE = getenv("DEFAULT_TIMEZONE", "Pacific/Auckland")


# ============================================================================
# Custom Jinja2 Filters for DateTime Conversion
# ============================================================================

def _parse_date_filter(date_string, format='%Y-%m-%d'):
    """Parse a date string from SQLite into a datetime object."""
    if not date_string:
        return None

    try:
        return datetime.strptime(str(date_string), format)
    except ValueError:
        return None


def _format_datetime_filter(dt, format='%Y-%m-%d %H:%M:%S'):
    """Format a datetime object to a string."""
    if dt is None:
        return ''

    # If it's a string, parse it first
    if isinstance(dt, str):
        try:
            dt = datetime.strptime(dt, '%Y-%m-%d')
        except ValueError:
            try:
                dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return str(dt)

    return dt.strftime(format)


def _to_timezone_filter(dt, timezone=DEFAULT_TIMEZONE):
    """Convert a datetime object to a specific timezone."""
    if dt is None:
        return None

    # If it's a string, parse it first
    if isinstance(dt, str):
        try:
            dt = datetime.strptime(dt, '%Y-%m-%d')
        except ValueError:
            try:
                dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return None

    # If datetime is naive, assume it's UTC
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)

    # Convert to target timezone
    target_tz = pytz.timezone(timezone)
    return dt.astimezone(target_tz)


def _to_local_filter(dt, timezone=DEFAULT_TIMEZONE, format='%Y-%m-%d %H:%M:%S'):
    """Convert to timezone AND format in one step."""
    if dt is None:
        return ''

    # If it's a string, parse it first
    if isinstance(dt, str):
        try:
            dt = datetime.strptime(dt, '%Y-%m-%d')
        except ValueError:
            try:
                dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return str(dt)

    # Convert timezone
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)

    target_tz = pytz.timezone(timezone)
    local_dt = dt.astimezone(target_tz)

    return local_dt.strftime(format)


def _humanize_filter(dt, timezone=DEFAULT_TIMEZONE):
    """Convert datetime to human-readable relative time."""
    if dt is None:
        return ''

    # If it's a string, parse it first
    if isinstance(dt, str):
        try:
            dt = datetime.strptime(dt, '%Y-%m-%d')
        except ValueError:
            try:
                dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return str(dt)

    # Ensure datetime is timezone-aware
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)

    # Get current time in the same timezone
    target_tz = pytz.timezone(timezone)
    now = datetime.now(target_tz)
    dt = dt.astimezone(target_tz)

    # Calculate difference
    diff = now - dt
    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif seconds < 31536000:
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = int(seconds / 31536000)
        return f"{years} year{'s' if years != 1 else ''} ago"



def init_date_filters(app):
    """Register all custom date/time filters with the Flask app"""
    app.jinja_env.filters['parsedate'] = _parse_date_filter
    app.jinja_env.filters['format_datetime'] = _format_datetime_filter
    app.jinja_env.filters['to_timezone'] = _to_timezone_filter
    app.jinja_env.filters['to_local'] = _to_local_filter
    app.jinja_env.filters['humanize'] = _humanize_filter



# ==========================================================================

from os import environ, getenv
from sys import exc_info
from dotenv import load_dotenv
from flask import request
from flask.signals import before_render_template
from textwrap import wrap
from colorama import init, Fore, Back, Style
import logging

# Load Flask environment config
load_dotenv()
FLASK_HOST = getenv("FLASK_RUN_HOST", "localhost")
FLASK_PORT = getenv("FLASK_RUN_PORT", "5000")

# Initialize colorama for Windows
init(autoreset=True)

LOG_COLOURS = {
    'APP':      Fore.YELLOW,
    'SQL':      Fore.BLUE,
    'JINJA':    Fore.MAGENTA,
    'DEBUG':    Fore.CYAN,
    'INFO':     Fore.GREEN,
    'WARNING':  Fore.YELLOW,
    'ERROR':    Fore.RED,
    'CRITICAL': Fore.RED + Style.BRIGHT,
}

METHOD_COLOURS = {
    'GET':    Fore.YELLOW,
    'POST':   Fore.GREEN,
    'PUT':    Fore.CYAN,
    'DELETE': Fore.RED,
}

STATUS_COLOURS = {
    '2': Fore.GREEN,   # 2xx - Success
    '3': Fore.CYAN,    # 3xx - Redirection
    '4': Fore.YELLOW,  # 4xx - Client Error
    '5': Fore.RED,     # 5xx - Server Error
}

STATUS_INFO = {
    200: "OK",
    301: "Redirect",
    302: "Redirect",
    304: "Cached",
    400: "Bad Req.",
    401: "Unauthor.",
    403: "Forbidden",
    404: "Not Found",
    405: "Bad Method",
    500: "Server",
}

RESET  = Style.RESET_ALL
BRIGHT = Style.BRIGHT
DIM    = Style.DIM
ERROR  = LOG_COLOURS.get('ERROR')

DIVIDER = "─" * 80
ARROW   = f"{DIM}···→{RESET}"


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        logger_name = record.name.upper()
        name_colour  = LOG_COLOURS.get(logger_name, Fore.WHITE)
        level_colour = LOG_COLOURS.get(record.levelname, Fore.WHITE)
        record.name      = f"{name_colour}[{logger_name}]{RESET}"
        record.levelname = f"{level_colour}{record.levelname:<8}{RESET}"
        return super().format(record)


def init_logging(app):
    """Initialize all loggers with colored formatting"""

    # Configure handler with custom formatter
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter(
        fmt='%(asctime)s %(levelname)s %(name)s %(message)s',
        datefmt='%H:%M:%S'
    ))

    # Flask's app logger
    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG if app.debug else logging.WARNING)

    # SQL logger
    sql_logger = logging.getLogger('sql')
    sql_logger.handlers.clear()
    sql_logger.addHandler(handler)
    sql_logger.setLevel(logging.DEBUG if app.debug else logging.WARNING)

    # Disable built-in Werkzeug logger
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.CRITICAL)

    @app.before_request
    def log_request_start():
        endpoint = request.endpoint
        view_func = app.view_functions.get(endpoint) if endpoint else None

        # Handle static files and lambda functions
        if endpoint == 'static':
            route_name = 'static file'
            func_name = ''
        elif view_func and hasattr(view_func, '__name__'):
            route_name = f"{request.url_rule}" if request.url_rule else ""
            func_name = f"{view_func.__name__}()"
        else:
            route_name = "unknown"
            func_name = ""

        log_colour = LOG_COLOURS.get('APP', Fore.WHITE)
        indent_text = f"{' '*18}{log_colour}[APP]{RESET}"
        divider = f"{DIVIDER}\n{indent_text} " if endpoint != 'static' else ""

        method_colour = METHOD_COLOURS.get(request.method, Fore.WHITE)+BRIGHT
        method_text = f"{method_colour}{request.method.upper()}{RESET}"
        query_text = '?' + request.query_string.decode('utf-8') if request.query_string else ''
        path_text = f"{method_colour}{request.path}{query_text}{RESET}"
        func_text = f" {ARROW} {func_name}" if func_name else ""

        app.logger.debug(f"{divider}Request: {method_text} {path_text} {ARROW} {route_name}{func_text}")

    @app.after_request
    def log_request_end(response):
        method_colour = DIM if app.debug else METHOD_COLOURS.get(request.method, Fore.WHITE)
        method_text   = f"{method_colour}{request.method.upper()}{RESET}"
        path_text     = f"{method_colour}{request.path}{RESET}"
        status_prefix = str(response.status_code)[0]
        status_name   = STATUS_INFO.get(response.status_code, "")
        status_colour = STATUS_COLOURS.get(status_prefix, Fore.WHITE)
        status_text   = f"{status_colour}{response.status_code}{RESET}|{status_colour}{status_name}{RESET}"
        prefix        = " Status" if app.debug else "Request"

        app.logger.info(f"{prefix}: {method_text} {path_text} {ARROW} {status_text}")

        return response

    # Log the start of Jinja template rendering
    @before_render_template.connect_via(app)
    def log_before_render(sender, template, context, **extra):
        jinja_colour = LOG_COLOURS.get('JINJA', "")
        app.logger.debug(f" Render: {jinja_colour}{template.name}{RESET}")

    # Announce the server is up
    if environ.get('WERKZEUG_RUN_MAIN') == 'true':
        app.logger.debug(DIVIDER)
        app.logger.info(f"🚀 Server running at http://{FLASK_HOST}:{FLASK_PORT}")

    return app.logger, sql_logger


def get_sql_logger():
    """Get the SQL logger (call after init_logging)"""
    return logging.getLogger('sql')


def wrapped(text):
    indent = " " * 33
    return f"\n{indent}".join(wrap(f"{text}", width=72))


def truncated(text):
    text = str(text).replace('\n', ' ').replace('\r', '')
    if len(text) > 72:
        return text[:68] + '...'
    return text


def log_exception(error):
    exc_type, exc_value, exc_traceback = exc_info()
    app_logger = logging.getLogger('app')
    error_text = f"({exc_type.__name__}) {str(error)}"
    app_logger.error(f"{ERROR}  ERROR: {wrapped(error_text)}{RESET}")


def log_routes(app):
    """Log all registered routes (call after routes are defined)"""
    if environ.get('WERKZEUG_RUN_MAIN') == 'true':
        app.logger.debug(DIVIDER)
        app.logger.debug("Registered Routes:")
        for rule in app.url_map.iter_rules():
            methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            method_colour = METHOD_COLOURS.get(methods, Fore.WHITE)
            app.logger.debug(f"▪ {method_colour}{methods:8}{RESET} {rule.rule:30} → {rule.endpoint}")


# ==========================================================================

import sqlite3
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from contextlib import contextmanager

from app.helpers.log import get_sql_logger, wrapped, truncated, LOG_COLOURS, ERROR, RESET, DIVIDER

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

                            # Log first few rows (preview)
                            if num_rows > 0:
                                preview = rows[:3]  # First 5 rows
                                for i, row in enumerate(preview, 1):
                                    sql_logger.debug(f"  Row {i}: {SQL_COLOUR}{truncated(row)}{RESET}")
                                if num_rows > 3:
                                    sql_logger.debug(f"     ... and {num_rows - 3} more")
                        return rows

                    def fetchone(self):
                        row = self._cursor.fetchone()
                        if self._sql_type == 'SELECT':
                            row_text = "1 row" if row else "0 rows"
                            sql_logger.debug(f" Result: {SQL_COLOUR}{row_text}{RESET} returned")
                            if row:
                                sql_logger.debug(f"   Data: {SQL_COLOUR}{truncated(row)}{RESET}")
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


