from os import environ
from flask import Flask, render_template, flash, redirect, session

from app.helpers.log import init_logging, log_routes, log_exception
from app.helpers.db import connect_db, init_db, init_db_table

# Create the app
app = Flask(__name__)

# Initialize logging
app_logger, sql_logger = init_logging(app)


#-----------------------------------------------------------
@app.get("/")
def show_all_notes():
    with connect_db() as db:
        sql = """
            SELECT id, title, body, pinned, created
            FROM note
            ORDER BY pinned DESC, created DESC
        """
        params = ()
        notes = db.execute(sql, params).fetchall()

        return render_template("pages/home.jinja", notes=notes)


#-----------------------------------------------------------
@app.get("/note/<int:id>")
def show_note(id):
    with connect_db() as db:
        sql = """
            SELECT id, title, body, pinned, created
            FROM note
            WHERE id=?
        """
        params = (id,)
        note = db.execute(sql, params).fetchone()

        return render_template("pages/home.jinja", note=note)
    pass


#-----------------------------------------------------------
@app.get("/test")
def test():
    return redirect("/")


#-----------------------------------------------------------
@app.post("/note")
def add_note():
    pass


#-----------------------------------------------------------
@app.delete("/note/<int:id>")
def delete_note(id):
    pass


#-----------------------------------------------------------
@app.errorhandler(404)
def page_not_found(error):
    return render_template("pages/404.jinja"), 404


#-----------------------------------------------------------
@app.errorhandler(Exception)
def handle_exception(error):
    log_exception(error)
    return render_template("pages/500.jinja"), 500


#-----------------------------------------------------------
# Now all the routes are defined, announce them
log_routes(app)


#-----------------------------------------------------------
# Initialize the database

NOTE_SCHEMA = """
    CREATE TABLE note (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT,
        pinned INTEGER DEFAULT 0,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

NOTE_SEED_INSERT = """
    INSERT INTO note (title, body, pinned)
    VALUES (?, ?, ?)
"""

NOTE_SEED_DATA = [
    ("Welcome to Notes", "This is your first note. You can edit or delete it.", 1),
    ("Getting Started",  "Create new notes by clicking the 'New Note' button.", 0),
    ("Pinned Notes",     "Pinned notes always appear at the top of your list.", 1),
    ("Sample Note",      "This is just a sample note with some content.",       0),
]

if environ.get('WERKZEUG_RUN_MAIN') == 'true':
    init_db()
    init_db_table('note', NOTE_SCHEMA, NOTE_SEED_INSERT, NOTE_SEED_DATA)


