# Flask Route Handling

## Defining Routes

### Simple Route to a Page - No Data

```python
@app.get("/about")
def example_route():
    return render_template("pages/about.jinja")
```

### Route to a Page with Data

```python
@app.get("/example")
def example_route():
    with connect_db() as db:
        sql = "SELECT * FROM table_name"
        rows = db.execute(sql).fetchall()
    return render_template("pages/example.jinja", data=rows)
```

### Route with a Paramater in URL (e.g. an ID)

```python
@app.get("/example/<int:id>")
def example_route(id):
    with connect_db() as db:
        sql = "SELECT * FROM table_name WHERE id=?"
        params = (id,)
        row = db.execute(sql, params).fetchone()
    return render_template("pages/example.jinja", data=row)
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

Immediately load a different route...

```python
return redirect("/")
return redirect(f"/note/{id}")
```

