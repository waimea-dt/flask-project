import logging
from os import getenv
from colorama import init, Fore, Back, Style
from dotenv import load_dotenv
from flask import request

LOG_COLOURS = {
    'APP':      Fore.YELLOW,
    'SQL':      Fore.BLUE,
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
    '200':    Fore.GREEN,
    '400':    Fore.YELLOW,
    '500':    Fore.RED,
}

DIVIDER = "┄" * 80


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        logger_name = record.name.upper()
        name_colour  = LOG_COLOURS.get(logger_name, Fore.WHITE)
        level_colour = LOG_COLOURS.get(record.levelname, Fore.WHITE)
        record.name      = f"{name_colour}[{logger_name}]{Style.RESET_ALL}"
        record.levelname = f"{level_colour}{record.levelname:<8}{Style.RESET_ALL}"
        return super().format(record)


def init_logging(app):
    """Initialize all loggers with colored formatting"""

    # Load Flask environment config
    load_dotenv()
    FLASK_HOST = getenv("FLASK_RUN_HOST", "localhost")
    FLASK_PORT = getenv("FLASK_RUN_PORT", "5000")

    # Initialize colorama for Windows
    init(autoreset=True)

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

    # Werkzeug's logger
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.CRITICAL)

    @app.before_request
    def log_request_start():
        method_colour = METHOD_COLOURS.get(request.method, Fore.WHITE)
        app.logger.debug(DIVIDER)
        app.logger.info(f"Request: {method_colour}{request.method.upper():<6}{Style.RESET_ALL} {request.path}")

    @app.after_request
    def log_request_end(response):
        if response.status_code < 300:
            response_colour = STATUS_COLOURS.get('200')
        elif response.status_code < 500:
            response_colour = STATUS_COLOURS.get('400')
        elif response.status_code < 600:
            response_colour = STATUS_COLOURS.get('500')
        else:
            response_colour = Fore.WHITE

        method_colour = METHOD_COLOURS.get(request.method, Fore.WHITE)
        app.logger.info(f" Result: {method_colour}{request.method.upper():<6}{Style.RESET_ALL} {Fore.WHITE}{request.path:<58}{Style.RESET_ALL} [{response_colour}{response.status_code}{Style.RESET_ALL}]")
        return response

    # Announce the server is up
    app.logger.debug(DIVIDER)
    app.logger.info(f"🚀 Server running at http://{FLASK_HOST}:{FLASK_PORT}")

    return app.logger, sql_logger


def get_sql_logger():
    """Get the SQL logger (call after init_logging)"""
    return logging.getLogger('sql')


def log_routes(app):
    """Log all registered routes (call after routes are defined)"""
    from os import environ

    if environ.get('WERKZEUG_RUN_MAIN') == 'true':
        app.logger.debug(DIVIDER)
        app.logger.debug("Registered Routes:")
        for rule in app.url_map.iter_rules():
            methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            method_colour = METHOD_COLOURS.get(methods, Fore.WHITE)
            app.logger.debug(f"▪ {method_colour}{methods:8}{Style.RESET_ALL} {rule.rule:30} → {rule.endpoint}")

