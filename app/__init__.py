#===========================================================
# PROJECT NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, render_template, flash, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Home page - Show all notes
#-----------------------------------------------------------
@app.get("/")
def show_notes():
    with connect_db() as db:
        sql = """
            SELECT id, title, body, pinned, created
            FROM note
            ORDER BY pinned DESC, created DESC
        """
        params = ()
        notes = db.execute(sql, params).fetchall()

        return render_template("pages/note_list.jinja", notes=notes)


#-----------------------------------------------------------
# View a note
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

        return render_template("pages/note_single.jinja", note=note)


#-----------------------------------------------------------
# View new note form
#-----------------------------------------------------------
@app.get("/note/new")
def show_note_form():
        return render_template("pages/note_form.jinja")


#-----------------------------------------------------------
# New note processing
#-----------------------------------------------------------
@app.post("/note")
def add_note():
    title  = request.form.get('title')
    body   = request.form.get('body')
    pinned = bool(request.form.get('pinned'))

    title = html.escape(title)
    body = html.escape(body)

    with connect_db() as db:
        sql = """
            INSERT INTO note (title, body, pinned) VALUES (?, ?, ?)
        """
        params = (title, body, pinned)
        result = db.execute(sql, params)
        new_note_id = result.lastrowid

        flash(f"Note added (#{new_note_id})")
        return redirect("/")


#-----------------------------------------------------------
# Delete a note - Admin only
#-----------------------------------------------------------
@app.get("/note/<int:id>/delete")
@login_required
def delete_note(id):
    with connect_db() as db:
        # ...
        return redirect("/")



#===========================================================
# Configure the app
#===========================================================
init_session(app)
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()

