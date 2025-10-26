#===========================================================
# PROJECT NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, render_template, flash, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
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


@app.get("/login-simple")
def login_form_simple():
    return render_template("pages/login_form_simple.jinja")


@app.post("/login-simple")
def login_admin():
    password = request.form.get('password', '').strip()

    load_dotenv()
    ADMIN_PASSWORD = getenv("ADMIN_PASSWORD", "")
    if not ADMIN_PASSWORD:
        flash(f"No admin password set!", "error")
        return redirect("/")

    if password == ADMIN_PASSWORD:
        session["logged_in"] = True
        flash(f"Login successful", "success")
        return redirect("/")
    else:
        session.clear()
        flash(f"Incorrect password", "error")
        return redirect("/")


@app.get("/login")
def login_form():
    return render_template("pages/login_form.jinja")


@app.post("/login")
def login_user():
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '').strip()

    with connect_db() as db:
        sql = """
            SELECT id, forename, surname, pass_hash
            FROM user
            WHERE username=?
        """
        params = (username,)
        user = db.execute(sql, params).fetchone()

        if not user:
            flash(f"Uknown user", "error")
            return redirect("/login")

        if not check_password_hash(user["pass_hash"], password):
            flash(f"Incorrect password", "error")
            return redirect("/login")

        session["logged_in"] = True
        session["user"] = {
            "username": username,
            "forename": user["forename"],
            "surname":  user["surname"],
        }

        flash("Login successful", "success")
        return redirect("/")


@app.get("/logout")
def logout_admin():
    session.clear()
    flash(f"You have been logged out", "success")
    return redirect("/")


@app.get("/admin")
@login_required
def admin_page():
    # Can only access this route if logged in
    return redirect("/")


@app.get("/user/new")
def user_form():
    return render_template("pages/user_form.jinja")


@app.post("/user")
def add_user():
    forename = request.form.get('forename', '').strip()
    surname  = request.form.get('surname',  '').strip()
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '').strip()

    with connect_db() as db:
        sql = "SELECT id FROM user WHERE username=?"
        params = (username,)
        user = db.execute(sql, params).fetchone()

        if user:
            flash(f"Username '{username}' already exists", "error")
            return redirect("/user/new")

        pass_hash = generate_password_hash(password)

        sql = """
            INSERT INTO user (forename, surname, username, pass_hash)
            VALUES (?, ?, ?, ?)
        """
        params = (forename, surname, username, pass_hash)
        db.execute(sql, params)

        flash("Account created. Please login", "success")
        return redirect("/login")



#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

