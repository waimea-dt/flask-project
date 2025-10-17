from flask import Flask, render_template, flash, redirect, session
from dotenv import load_dotenv
from os import getenv

from app.helpers.log import init_logging, log_routes, DIVIDER
from app.helpers.db import connect_db, init_db

# Create the app
app = Flask(__name__)
# Initialize logging
app_logger, sql_logger = init_logging(app)
# Initialize the database
init_db(app)


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
@app.post("/note")
def add_note(id):
    pass


#-----------------------------------------------------------
@app.delete("/note/<int:id>")
def delete_note(id):
    pass


#-----------------------------------------------------------
# Now all the routes are defined, announce them
log_routes(app)

