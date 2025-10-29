---
title: Form Data Processing
parent: Guides
nav_order: 10
---

# Handling Form Data

## Typical Form with a Range of Inputs

```html
<form method="post" action="/note">
    <h3>New Note</h3>

    <label>
        Title
        <input name="title" type="text" required>
    </label>

    <label>
        Body
        <textarea name="body" required></textarea>
    </label>

    <label>
        <input name="pin" type="checkbox">
        Pin note?
    </label>

    <select name="category">
        <option>Home<option>
        <option>Work<option>
    </select>

    <fieldset>
        <legend>Tags</legend>
        <label>
            <input name="tags" value="todo" type="checkbox">
            todo
        </label>
        <label>
            <input name="tags" value="call" type="checkbox">
            call
        </label>
        <label>
            <input name="tags" value="shop" type="checkbox">
            shop
        </label>
    </fieldset>

    <button>Add Note</button>
</form>
```
Giving this form...

<form id="formdemo" method="post" action="/note">
  <h3>New Note</h3>
  <label>Title <input name="title" type="text" required></label>
  <label>Body <textarea name="body" required></textarea></label>
  <label><input name="pin" type="checkbox"> Pin note?</label>
  <label>Category <select name="category">
    <option>Home</option>
    <option>Work</option>
  </select></label>
  <fieldset>
    <legend>Tags</legend>
    <label><input name="tags" value="todo" type="checkbox"> home</label>
    <label><input name="tags" value="call" type="checkbox"> call</label>
    <label><input name="tags" value="shop" type="checkbox"> shop</label>
  </fieldset>
  <button>Add Note</button>
</form>

## Get Values from Form

Get form data via `request.form.get('key').strip()`...
- `.get('key')` gets the form input with the name 'key'
- `.get('key', '')` value will be nothing if the input missing
- `.strip()` removes leading / trailing spaces
- Can also add other text transforms: `.lower()`, `.upper()`, etc.

```python
# Get form text data
title = request.form.get('title', '').strip()
body = request.form.get('body', '').strip()

# Get checkbox state as a boolean
pinned = bool(request.form.get('pin'))   # True/False

# Get all values from checkboxes / selects
tag_list = request.form.getlist('tags')  # ['todo', 'shop']
tags = ", ".join(tag_list)               # "todo, shop"
```

**⚠️ Important Security Issue!**

✅ Always escape text to avoid **cross-site script (XSS) attacks**

❌ Not doing this allows users to exploit your app by entering script commands into form text fields which your app will then run.

```python
# Escape text to avoid XSS exploits
title = html.escape(title)
body = html.escape(body)
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
    flash("Value should be numeric", "error")
    return redirect("/note/new")
```

Check a numeric value is in a **given range** (first converting it to a number)

```python
value = int(value)  # or double(value_str)

if value < 10 or value > 30:
    flash("Value should be between 10 and 30", "error")
    return redirect("/note/new")
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
        flash("Priority should be numeric", "error")
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

<style>
  #formdemo, #formdemo * {
    box-sizing: border-box;
    font-size: inherit;
  }
  #formdemo {
    width: 22rem;
    margin-inline: auto;
    border: 1px solid currentcolor;
    padding: 0 1rem;
    border-radius: 0.5rem;
    background-color: #3692;
  }
  #formdemo > * {
    display:block;
    margin-block: 1rem;
  }
  #formdemo fieldset label {
    display: inline-block;
    margin-inline: 0.5rem;
  }
  #formdemo input[type="text"],
  #formdemo textarea,
  #formdemo select {
    display: block;
    width: 100%;
  }
</style>

