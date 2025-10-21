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

from flask import Flask, render_template_string
from datetime import datetime
import pytz

app = Flask(__name__)

# ============================================================================
# Custom Jinja2 Filters for DateTime Conversion
# ============================================================================

@app.template_filter('parse_date')
def parse_date_filter(date_string, format='%Y-%m-%d'):
    """
    Parse a date string from SQLite into a datetime object.

    Usage in template:
        {{ '2025-10-21' | parse_date }}
        {{ '2025-10-21 14:30:00' | parse_date('%Y-%m-%d %H:%M:%S') }}
    """
    if not date_string:
        return None

    try:
        return datetime.strptime(str(date_string), format)
    except ValueError:
        return None


@app.template_filter('to_timezone')
def to_timezone_filter(dt, timezone='UTC'):
    """
    Convert a datetime object to a specific timezone.
    Works with both naive (assumes UTC) and aware datetime objects.
    Also accepts date strings and will parse them first.

    Usage in template:
        {{ my_datetime | to_timezone('America/New_York') }}
        {{ '2025-10-21' | to_timezone('America/New_York') }}
    """
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

    # If datetime is naive (no timezone info), assume it's UTC
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)

    # Convert to target timezone
    target_tz = pytz.timezone(timezone)
    return dt.astimezone(target_tz)


@app.template_filter('format_datetime')
def format_datetime_filter(dt, format='%Y-%m-%d %H:%M:%S'):
    """
    Format a datetime object to a string.
    Also accepts date strings and will parse them first.

    Usage in template:
        {{ my_datetime | format_datetime('%B %d, %Y at %I:%M %p') }}
        {{ '2025-10-21' | format_datetime('%B %d, %Y') }}
    """
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
                return str(dt)  # Return as-is if can't parse

    return dt.strftime(format)


@app.template_filter('to_local')
def to_local_filter(dt, timezone='America/New_York', format='%Y-%m-%d %H:%M:%S'):
    """
    Convenience filter that converts to timezone AND formats in one step.
    Also accepts date strings and will parse them first.

    Usage in template:
        {{ my_datetime | to_local('Europe/London', '%B %d, %Y at %I:%M %p') }}
        {{ '2025-10-21' | to_local('Europe/London', '%B %d, %Y') }}
    """
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
                return str(dt)  # Return as-is if can't parse

    # Convert timezone
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)

    target_tz = pytz.timezone(timezone)
    local_dt = dt.astimezone(target_tz)

    # Format
    return local_dt.strftime(format)


@app.template_filter('humanize')
def humanize_filter(dt, timezone='UTC'):
    """
    Convert datetime to human-readable relative time (e.g., "2 hours ago").
    Also accepts date strings and will parse them first.

    Usage in template:
        {{ my_datetime | humanize }}
        {{ my_datetime | humanize('America/New_York') }}
        {{ '2025-10-21' | humanize }}
    """
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
                return str(dt)  # Return as-is if can't parse

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


# ============================================================================
# Demo Route
# ============================================================================

@app.route('/')
def index():
    # Simulate data from SQLite database (stored as text strings)
    sqlite_dates = [
        '2025-10-21',           # Date only (today)
        '2024-12-25',           # Christmas 2024
        '2025-01-01',           # New Year 2025
        '2025-10-15',           # Recent date
    ]

    # Also simulate datetime strings from SQLite
    sqlite_datetimes = [
        '2025-10-21 14:30:00',
        '2024-12-25 10:30:00',
        '2025-01-01 00:00:00',
        '2025-10-15 14:45:30',
    ]

    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SQLite Date String Conversion</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 40px;
                background: #f5f7fa;
            }
            h1 { color: #2c3e50; }
            .section {
                background: white;
                padding: 25px;
                margin: 20px 0;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            h2 {
                color: #3498db;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
                margin-top: 0;
            }
            .example {
                background: #ecf0f1;
                padding: 15px;
                margin: 15px 0;
                border-radius: 5px;
                border-left: 4px solid #3498db;
            }
            .label {
                font-weight: bold;
                color: #2c3e50;
                display: inline-block;
                min-width: 180px;
            }
            .value {
                color: #27ae60;
                font-family: 'Courier New', monospace;
            }
            .sqlite-value {
                color: #e74c3c;
                font-family: 'Courier New', monospace;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }
            th {
                background: #3498db;
                color: white;
                padding: 12px;
                text-align: left;
            }
            td {
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }
            tr:hover {
                background: #f8f9fa;
            }
            .code {
                background: #2c3e50;
                color: #ecf0f1;
                padding: 3px 8px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }
            .warning {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 15px 0;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <h1>SQLite Date String Conversion Examples</h1>

        <div class="warning">
            <strong>📌 Note:</strong> All filters now automatically parse SQLite date strings.
            No need for manual parsing!
        </div>

        <div class="section">
            <h2>1. Working with 'YYYY-MM-DD' Date Strings</h2>
            {% for date_str in dates %}
            <div class="example">
                <div><span class="label">SQLite Value:</span>
                    <span class="sqlite-value">"{{ date_str }}"</span></div>
                <div><span class="label">Formatted:</span>
                    <span class="value">{{ date_str | format_datetime('%B %d, %Y') }}</span></div>
                <div><span class="label">New York Time:</span>
                    <span class="value">{{ date_str | to_local('America/New_York', '%A, %B %d, %Y') }}</span></div>
                <div><span class="label">Relative Time:</span>
                    <span class="value">{{ date_str | humanize }}</span></div>
            </div>
            {% endfor %}
        </div>

        <div class="section">
            <h2>2. Working with 'YYYY-MM-DD HH:MM:SS' DateTime Strings</h2>
            {% for datetime_str in datetimes %}
            <div class="example">
                <div><span class="label">SQLite Value:</span>
                    <span class="sqlite-value">"{{ datetime_str }}"</span></div>
                <div><span class="label">Formatted:</span>
                    <span class="value">{{ datetime_str | format_datetime('%B %d, %Y at %I:%M %p') }}</span></div>
                <div><span class="label">Tokyo Time:</span>
                    <span class="value">{{ datetime_str | to_local('Asia/Tokyo', '%Y-%m-%d %H:%M:%S %Z') }}</span></div>
                <div><span class="label">London Time:</span>
                    <span class="value">{{ datetime_str | to_timezone('Europe/London') | format_datetime('%A, %B %d at %I:%M %p') }}</span></div>
            </div>
            {% endfor %}
        </div>

        <div class="section">
            <h2>3. Direct String Usage (Most Common Pattern)</h2>
            <table>
                <tr>
                    <th>SQLite Date String</th>
                    <th>As US Format</th>
                    <th>As EU Format</th>
                    <th>Relative</th>
                </tr>
                {% for date_str in dates %}
                <tr>
                    <td><span class="sqlite-value">{{ date_str }}</span></td>
                    <td>{{ date_str | format_datetime('%m/%d/%Y') }}</td>
                    <td>{{ date_str | format_datetime('%d/%m/%Y') }}</td>
                    <td>{{ date_str | humanize }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <div class="section">
            <h2>4. Real-World Example: Blog Posts from SQLite</h2>
            {% for datetime_str in datetimes[:2] %}
            <div class="example">
                <h3 style="margin-top: 0;">Sample Blog Post Title</h3>
                <p style="color: #7f8c8d; font-size: 0.9em;">
                    Posted {{ datetime_str | humanize }}
                    ({{ datetime_str | format_datetime('%B %d, %Y') }})
                </p>
                <p>This example shows how you'd display a blog post with a date stored as
                   <span class="sqlite-value">"{{ datetime_str }}"</span> in your SQLite database.</p>
            </div>
            {% endfor %}
        </div>

        <div class="section">
            <h2>5. Filter Usage with SQLite Strings</h2>
            <table>
                <tr>
                    <th>Filter</th>
                    <th>Template Code</th>
                    <th>Example Output</th>
                </tr>
                <tr>
                    <td><span class="code">parse_date</span></td>
                    <td><span class="code">{{ "{{ '2025-10-21' | parse_date }}" }}</span></td>
                    <td>{{ dates[0] | parse_date }}</td>
                </tr>
                <tr>
                    <td><span class="code">format_datetime</span></td>
                    <td><span class="code">{{ "{{ '2025-10-21' | format_datetime('%B %d, %Y') }}" }}</span></td>
                    <td>{{ dates[0] | format_datetime('%B %d, %Y') }}</td>
                </tr>
                <tr>
                    <td><span class="code">to_timezone</span></td>
                    <td><span class="code">{{ "{{ '2025-10-21' | to_timezone('Asia/Tokyo') }}" }}</span></td>
                    <td>{{ dates[0] | to_timezone('Asia/Tokyo') }}</td>
                </tr>
                <tr>
                    <td><span class="code">to_local</span></td>
                    <td><span class="code">{{ "{{ '2025-10-21' | to_local('Europe/Paris', '%d/%m/%Y') }}" }}</span></td>
                    <td>{{ dates[0] | to_local('Europe/Paris', '%d/%m/%Y') }}</td>
                </tr>
                <tr>
                    <td><span class="code">humanize</span></td>
                    <td><span class="code">{{ "{{ '2025-10-15' | humanize }}" }}</span></td>
                    <td>{{ dates[3] | humanize }}</td>
                </tr>
            </table>
        </div>

        <div class="section">
            <h2>6. Common SQLite Query Patterns</h2>
            <div style="background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 4px; font-family: 'Courier New', monospace;">
                <div># In your Flask route:</div>
                <div>cursor.execute("SELECT title, created_at FROM posts")</div>
                <div>posts = cursor.fetchall()</div>
                <div></div>
                <div># In template:</div>
                <div>{% for post in posts %}</div>
                <div>&nbsp;&nbsp;{{ "{{ post.created_at | format_datetime('%B %d, %Y') }}" }}</div>
                <div>{% endfor %}</div>
            </div>
        </div>
    </body>
    </html>
    """

    return render_template_string(template, dates=sqlite_dates, datetimes=sqlite_datetimes)


if __name__ == '__main__':
    # Install with: pip install flask pytz
    app.run(debug=True)