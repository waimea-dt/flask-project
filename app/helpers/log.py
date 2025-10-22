from os import environ, getenv
from sys import exc_info
from dotenv import load_dotenv
from flask import request, session, render_template
from flask.signals import before_render_template
from rich.logging import RichHandler
from rich.console import Console
from rich.table import Table
import logging
import re

# Load Flask environment config
load_dotenv()
FLASK_HOST = getenv("FLASK_RUN_HOST", "localhost")
FLASK_PORT = getenv("FLASK_RUN_PORT", "5000")

# Rich console
console = Console()

STATUS_INFO = {
    200: "OK",
    201: "created",
    204: "no content",
    301: "redirect",
    302: "redirect",
    304: "from cache",
    400: "bad request",
    401: "unauthorised",
    403: "forbidden",
    404: "not found",
    405: "bad method",
    500: "server error",
}

STATIC = "static"

APP_LOG_PREFIX   = "[FLASK]"
JINJA_LOG_PREFIX = "[JINJA]"


def init_logging(app):
    """Initialize Rich logging"""

    import flask
    import jinja2
    import werkzeug

    # Configure Rich handler
    handler = RichHandler(
        console=console,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        tracebacks_extra_lines=5,
        tracebacks_suppress=[
            flask,
            jinja2,
            werkzeug,
            "app/helpers/db.py",
            "app/helpers/log.py",
            "app/helpers/date.py",
        ],
        tracebacks_max_frames=3,
        markup=True,
        show_path=False,
        show_level=False,
        log_time_format="[%X]",
        omit_repeated_times=True,
    )

    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # Disable Werkzeug
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.CRITICAL)

    @app.before_request
    def log_request_start():
        endpoint = request.endpoint
        if endpoint == STATIC:
            return

        view_func = app.view_functions.get(endpoint) if endpoint else None
        if view_func and hasattr(view_func, '__name__'):
            route_name = f"{request.url_rule}" if request.url_rule else ""
            func_name = f"--→ {view_func.__name__}()"
        else:
            route_name = "[red][bold]✗[/bold] unknown route[/red]"
            func_name = ""

        query_text = '?' + request.query_string.decode('utf-8') if request.query_string else ''
        path_text = f"{request.path}{query_text}"

        console.rule()
        app.logger.debug(
            f"[yellow]{APP_LOG_PREFIX} Request:[/yellow] " +
            f"{request.method} {path_text} --→ {route_name} {func_name}"
        )

        if request.view_args:
            app.logger.debug(f"[yellow]{APP_LOG_PREFIX}  Params:[/yellow] {request.view_args}")

        if request.args:
            query_params = dict(request.args)
            app.logger.debug(f"[yellow]{APP_LOG_PREFIX}   Query:[/yellow] {query_params}")

        if request.form:
            form_data = dict(request.form)
            app.logger.debug(f"[yellow]{APP_LOG_PREFIX}    Form:[/yellow] {form_data}")

        if request.files and any(file.filename for file in request.files.values()):
            filenames = [file.filename for file in request.files.values()]
            app.logger.debug(f"[yellow]{APP_LOG_PREFIX}   Files:[/yellow] {filenames}")

        if session:
            session_data = dict(session)
            app.logger.debug(f"[yellow]{APP_LOG_PREFIX} Session:[/yellow] {session_data}")


    @app.after_request
    def log_request_end(response):
        status_code = response.status_code
        status_name = STATUS_INFO.get(status_code, "")
        status_text = f"[yellow]{APP_LOG_PREFIX}  Status:[/yellow] "
        status_text += f"{request.method} {request.path} --→ "
        status_text += f"{status_code} [dim]({status_name})[/dim]"

        if request.endpoint == STATIC:
            app.logger.debug(f"[dim]{status_text}[/dim]")
        else:
            app.logger.info(f"{status_text}")

        return response


    # Log the start of Jinja template rendering
    @before_render_template.connect_via(app)
    def log_before_render(sender, template, context, **extra):
        if app.debug:
            app.logger.debug(f"[cyan]{JINJA_LOG_PREFIX}  Render:[/cyan] {template.name}")

            template_data = [
                item for item in context.keys()
                if not item.startswith('_') and item not in ['request', 'session', 'g', 'config', 'url_for', 'get_flashed_messages']
            ]
            app.logger.debug(f"[cyan]{JINJA_LOG_PREFIX}    Data:[/cyan] {template_data}")

    # Announce the server is up
    if environ.get('WERKZEUG_RUN_MAIN') == 'true':
        console.clear()
        console.rule()
        console.print(f"🚀 [green]Server running at[/green] [link=http://{FLASK_HOST}:{FLASK_PORT}]http://{FLASK_HOST}:{FLASK_PORT}[/link]")
        if app.debug:
            console.print("🔧 [yellow]Debug mode enabled[/yellow]")


def get_logger():
    """Get the app logger (call after init_logging)"""
    return logging.getLogger('app')


def truncate(text, width=80):
    text = str(text).replace('\n', ' ').replace('\r', '')

    if len(text) > width:
        truncated_text = text[:width]

        # Remove complete quoted strings, leaving only unmatched quotes
        no_doubles = re.sub(r'"[^"]*"', '', truncated_text)
        no_singles = re.sub(r"'[^']*'", '', truncated_text)

        # Count remaining (unmatched) quotes
        closing = ""
        if no_singles.count("'") % 2:
            closing += "'"
        if no_doubles.count('"') % 2:
            closing += '"'

        return truncated_text + closing + "...}"
    return text




def log_exception(error):
    """Log exception with Rich formatting"""
    exc_type, exc_value, exc_traceback = exc_info()
    app_logger = logging.getLogger('app')

    app_logger.error(
        f"[red bold]{APP_LOG_PREFIX}   Error:[/red bold] {exc_type.__name__} → {str(error)}",
        exc_info=True
    )


def log_routes(app):
    """Log all registered routes as a Rich table"""
    if environ.get('WERKZEUG_RUN_MAIN') == 'true':
        table = Table(
            show_header=False,
        )
        table.add_column("Method", style="yellow")
        table.add_column("Route Pattern", style="cyan")
        table.add_column("Endpoint Function", style="green")

        for rule in app.url_map.iter_rules():
            methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            table.add_row(methods, rule.rule, rule.endpoint + ("()" if rule.endpoint != "static" else ""))

        console.print("🧭 [cyan]Registered routes:[/cyan]")
        console.print(table)
        console.rule()


