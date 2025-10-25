# Flask Cheatsheet

## Defining Routes

### Simple Route to a Page

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
        params = ()
        rows = db.execute(sql, params).fetchall()
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

## Protected Routes

```python
@app.get("/admin")
@login_required
def admin_page():
    # Only accessible if session['logged_in'] is True
    return render_template("pages/admin.jinja")
```

## Redirects

```python
return redirect("/")
return redirect(f"/note/{id}")
```

## Forms

```python
# Get form data
value = request.form.get('field_name', '').strip()
value = request.form.get('field_name', 'default').strip()

# Get checkbox state as a boolean
checked = bool(request.form.get('checkbox_name'))

# Get all values for a field
values = request.form.getlist('field_name')
```

### Validation of Input Data

```python
# Check if a value has been given
if not title:
    flash("Title is required", "error")
    return redirect("/note/new")

# Check length of a value
if len(title) > 200:
    flash("Title is too long (max 200 characters)", "error")
    return redirect("/note/new")

# Check a value is in a given range
if value < 10 or value > 30:
    flash("Value shouod be between 10 and 30", "error")
    return redirect("/note/new")
```

### Escaping Potential HTML Tag / JS Script Injection

```python
# HTML escape for safety
title = html.escape(title)
body = html.escape(body)
```

## Session Management

```python
# Set a value
session['key'] = value

# Get a value
value = session.get('key')
# Get a value with a default if missing
value = session.get('key', 'default')

# Delete a value
session.pop('key', None)

# Clear all values
session.clear()
```

## Flash Messages

```python
flash("Message")
flash("Success message", "success")
flash("Error message", "error")
```
### Display in template:
```jinja
{% for message in get_flashed_messages() %}
    <p>{{ message }}</p>
{% endfor %}
```

