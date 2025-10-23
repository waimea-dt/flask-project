#===========================================================
# PROJECT NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, render_template, flash, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import html

from app.helpers.session import init_session
from app.helpers.log     import init_logging
from app.helpers.db      import init_database, connect_db
from app.helpers.auth    import login_required
from app.helpers.text    import init_text_filters
from app.helpers.date    import init_date_filters
from app.helpers.error   import init_error_handlers


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Home page route - Show all notes
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

        return render_template("pages/home.jinja", notes=notes, name="test")


#-----------------------------------------------------------
# View note route
#-----------------------------------------------------------
@app.get("/note/<int:id>")
def show_note(id):
    return redirect("/")


#-----------------------------------------------------------
# New note route
#-----------------------------------------------------------
@app.post("/note")
def add_note():
    flash("Note added")
    return redirect("/")


#-----------------------------------------------------------
# Delete note route
#-----------------------------------------------------------
@app.get("/note/<int:id>/delete")
def delete_note(id):
    flash("Note deleted")
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


