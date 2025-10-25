# Handling Form Data

## Get Values from Form

```python
# Get form data
value = request.form.get('field_name', '').strip()
value = request.form.get('field_name', 'default').strip()

# Get checkbox state as a boolean
checked = bool(request.form.get('checkbox_name'))

# Get all values for multiple checkboxes / selects
values = request.form.getlist('field_name')
```

## Validation of Input Data

Check that a value is **present**:

```python
title = request.form.get('title', '').strip()

if not title:
    flash("Title is required", "error")
    return redirect("/note/new")
```

### Text Values

Check that a text value is **not too long**:

```python
if len(title) > 200:
    flash("Title is too long (max 200 characters)", "error")
    return redirect("/note/new")
```

### Numeric Values

Check a value is **numeric** using `isdigit()`:

```python
value = request.form.get('value', '').strip()

if not value.isdigit():
    flash("Value shouod be numeric", "error")
    return redirect("/note/new")
```

Check a numeric value is in a **given range** (first converting it to a number)

```python
value = int(value)  # or double(value_str)

if value < 10 or value > 30:
    flash("Value shouod be between 10 and 30", "error")
    return redirect("/note/new")
```

## Escaping HTML Tag / JS Script Injection

```python
title = html.escape(title)
body = html.escape(body)
```

## Full Example

```python
@app.post("/note")
def add_note():
    # Get form data
    title    = request.form.get('title', '').strip()
    body     = request.form.get('body', '').strip()
    priority = request.form.get('priority', '3').strip()
    pinned   = bool(request.form.get('pinned'))

    # Validate data
    if not title:
        flash("Title is required", "error")
        return redirect("/note/new")

    if len(title) > 40:
        flash("Title is too long (max 40 chars)", "error")
        return redirect("/note/new")

    if not priority.isdigit():
        flash("Priority shouod be numeric", "error")
        return redirect("/note/new")

    priority = int(priority)
    if priority < 1 or priority > 5:
        flash("Priority should be between 1 and 5", "error")
        return redirect("/note/new")

    # Escape text inputs
    title = html.escape(title)
    body = html.escape(body)

    # Add to the database
    with connect_db() as db:
        sql = """
            INSERT INTO note (title, body, priority, pinned)
            VALUES (?, ?, ?, ?)
        """
        params = (title, body, priority, pinned)
        db.execute(sql, params)

        flash(f"Note added")
        return redirect("/")
```



