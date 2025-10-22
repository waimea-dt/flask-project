# ============================================================================
# Jinja2 Filters for DateTime using Arrow
# ============================================================================

from os import getenv
from dotenv import load_dotenv
import arrow


load_dotenv()
DEFAULT_TIMEZONE = getenv("DEFAULT_TIMEZONE", "Pacific/Auckland")

NICE_DATE_FORMAT = 'ddd, DD MMM YYYY'
NICE_TIME_FORMAT = 'h:mmA'


def init_date_filters(app):
    """Register Arrow-based date/time filters with the Flask app"""

    @app.template_filter('timezone')
    def to_timezone(dt, tz=DEFAULT_TIMEZONE):
        """Convert to specific timezone."""
        if not dt:
            return None
        return arrow.get(dt).to(tz)

    @app.template_filter('local')
    def to_local(dt):
        """Convert to default local timezone."""
        if not dt:
            return None
        return arrow.get(dt).to(DEFAULT_TIMEZONE)

    @app.template_filter('format')
    def format_date(dt, fmt=NICE_DATE_FORMAT):
        """Format datetime. Uses Arrow tokens: YYYY, MM, DD, HH, mm, ss, etc."""
        if not dt:
            return ''
        return arrow.get(dt).format(fmt)

    @app.template_filter('format_human')
    def format_date_humanize(dt, tz=DEFAULT_TIMEZONE, granularity='auto'):
        """Human-readable relative time like '2 hours ago'."""
        if not dt:
            return ''
        arr = arrow.get(dt).to(tz)
        return arr.humanize(granularity=granularity)

    # Global function for current time
    app.jinja_env.globals['now'] = lambda tz=DEFAULT_TIMEZONE: arrow.now(tz)

