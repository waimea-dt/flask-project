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

