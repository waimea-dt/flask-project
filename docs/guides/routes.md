# Flask Route Handling

## Naming Routes

Try to be consistent when naming routes. A good pattern to use is:

**Fetching Data:**
- `GET  /notes` - for a page that has multiple items
- `GET  /note/<int:id>` - for a page that shows a single thing by ID
- `GET  /notes/pinned` - for a page that has multiple, specific items

**New Data:**
- `GET  /note/new` - for a page with a form for a new item
- `POST /note` - to process the new item form data

**Updating Data:**
- `GET  /note/<int:id>/edit` - for a page with a form to edit an item
- `POST /note/<int:id>` - to process updated data for an item

**Deleting Data:**
- `GET  /note/<int:id>/delete` - to process an item deletion

*Note: within routes, **numeric** parameters use `<int:value>`, whilst **text** parameters use `<value>`*


## Defining Routes

### Simple Route to a Page - No Data

```python
@app.get("/about")
def example_route():
    return render_template("pages/about.jinja")
```

```python
@app.get("/note/new")
def example_route():
    return render_template("pages/note_form.jinja")
```

### Route for a Page with Multiple Items

```python
@app.get("/notes")
def show_note_list():
    with connect_db() as db:
        sql = "SELECT * FROM note"
        notes = db.execute(sql).fetchall()
    return render_template("pages/note_list.jinja", notes=notes)
```

### Route for a Page with Multiple, Specific Items

```python
@app.get("/notes/pinned")
def show_pinned_note_list():
    with connect_db() as db:
        sql = "SELECT * FROM note WHERE pinned=1"
        notes = db.execute(sql).fetchall()
    return render_template("pages/note_list.jinja", notes=notes, title="Pinned Notes")
```

### Route for a Single Item using a Parameter (e.g. an ID)

```python
@app.get("/note/<int:id>")
def show_note(id):
    with connect_db() as db:
        sql = "SELECT * FROM note WHERE id=?"
        params = (id,)
        note = db.execute(sql, params).fetchone()
    return render_template("pages/note_info.jinja", note=note)
```

### Route for Multiple Items using a Parameter (e.g. a category)

```python
@app.get("/notes/<category>")
def show_note(category):
    with connect_db() as db:
        sql = "SELECT * FROM note WHERE category=?"
        params = (category,)
        note = db.execute(sql, params).fetchone()
    return render_template("pages/note_info.jinja", note=note)
```

### Route for a Search Query

This would filter notes via a search URL of the form `/notes/search?query=...`. Typically this URL would be from filter links on the notes page, or from a search form, using the `GET` method...

```python
@app.get("/notes/search")
def search_notes():
    # Get search query and add wildcards
    query = request.args.get('query')
    query = f"%{query}%"

    with connect_db() as db:
        sql = """
            SELECT * FROM note
            WHERE title LIKE ? OR body LIKE ?
        """
        params = (query, query)
        notes = db.execute(sql, params).fetchall()
    return render_template("pages/note_list.jinja", notes=notes)
```

### Protected Routes

Add the `@login_required` decorator...

```python
@app.get("/admin")
@login_required
def admin_page():
    # Only accessible if session['logged_in'] is True
    return render_template("pages/admin.jinja")
```

## Redirects

Immediately loads a different route...

```python
return redirect("/")
return redirect(f"/note/{id}")
```

