from os import environ, getenv
from sys import exc_info
from dotenv import load_dotenv
from flask import request, session
from flask.signals import before_render_template
from rich.logging import RichHandler
from rich.console import Console
from rich.table import Table
import logging

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

REQUEST  = "[yellow][APP] Request:[/yellow]"
RESPONSE = "[yellow][APP] Response:[/yellow]"
RENDER   = "[magenta][JIN] Render:[/magenta]"


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
        log_time_format="[%X]",
        omit_repeated_times=True,
    )

    # Flask's app logger
    app.logger.name = "app"
    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # SQL logger
    sql_logger = logging.getLogger('sql')
    sql_logger.handlers.clear()
    sql_logger.addHandler(handler)
    sql_logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

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
            route_name = "unknown route"
            func_name = ""

        query_text = '?' + request.query_string.decode('utf-8') if request.query_string else ''
        path_text = f"{request.path}{query_text}"

        console.rule()
        app.logger.debug(f"{REQUEST}  {request.method} {path_text} --→ {route_name} {func_name}")

        if request.form:
            form_data = dict(request.form)
            app.logger.debug(f"[cyan][APP] Form:[/cyan]     {form_data}")

        if request.files and any(file.filename for file in request.files.values()):
            filenames = [file.filename for file in request.files.values()]
            app.logger.debug(f"[cyan][APP] Files:[/cyan]    {filenames}")

        if session:
            session_data = dict(session)
            app.logger.debug(f"[blue][APP] Session:[/blue] {session_data}")

    @app.after_request
    def log_request_end(response):
        status_code = response.status_code
        status_name = STATUS_INFO.get(status_code, "")
        status_text = f"{RESPONSE} {request.method} {request.path} --→ {status_code} [dim]({status_name})[/dim]"
        if request.endpoint == STATIC:
            app.logger.debug(f"[dim]{status_text}[/dim]")
        else:
            app.logger.debug(f"{status_text}")

        return response


    # Log the start of Jinja template rendering
    @before_render_template.connect_via(app)
    def log_before_render(sender, template, context, **extra):
        if app.debug:
            app.logger.debug(f"{RENDER}   {template.name}")


    # Announce the server is up
    if environ.get('WERKZEUG_RUN_MAIN') == 'true':
        console.rule("[bold cyan]Flask Application Starting[/bold cyan]")
        console.print(f"🚀 [green]Server running at[/green] [link=http://{FLASK_HOST}:{FLASK_PORT}]http://{FLASK_HOST}:{FLASK_PORT}[/link]")
        if app.debug:
            console.print("🔧 [yellow]Debug mode enabled[/yellow]")

    return app.logger, sql_logger


def get_sql_logger():
    """Get the SQL logger (call after init_logging)"""
    return logging.getLogger('sql')


def log_exception(error):
    """Log exception with Rich formatting"""
    exc_type, exc_value, exc_traceback = exc_info()
    app_logger = logging.getLogger('app')

    app_logger.error(
        f"[red bold][APP] {exc_type.__name__}:[/red bold] {str(error)}",
        exc_info=True
    )


def log_routes(app):
    """Log all registered routes as a Rich table"""
    if environ.get('WERKZEUG_RUN_MAIN') == 'true':
        table = Table(
            title="Registered Routes",
            show_header=True,
            header_style="magenta",
        )
        table.add_column("Method", style="cyan")
        table.add_column("Route Pattern", style="yellow")
        table.add_column("Endpoint Function", style="green")

        for rule in app.url_map.iter_rules():
            methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            table.add_row(methods, rule.rule, rule.endpoint + ("()" if rule.endpoint != "static" else ""))

        console.print(table)
        console.rule()


