# Quick Start

## First Run

### 1. Setup virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
*(use `source venv/bin/activate` on Mac/Linux)*


### 2. Configure environment vars:

- Copy `.env-example` to `.env`, and edit as needed


### 3. Run server:

```bash
flask run
```

### 4. Browse site

- Visit: [http://localhost:5000](http://localhost:5000)


---

## Create Your App

### 1. Define database schema in `db/config.py`

- *See [schema](schema.md) doc for more details*


### 2. Define routes and handlers in `__init__.py`

- *See [CRUD example](crud.md) doc for examples*

- Design Patterns to Follow...

    - **Route** Pattern *(See [routes](routes.md) guide)*

        ```python
        @app.get("/path")
        def handler():
            return render_template("page.jinja")
        ```

    - **Database Query** Pattern *(see [sqlite](sqlite.md) guide)*

        ```python
        with connect_db() as db:
            sql = "SELECT * FROM table WHERE col=?"
            params = (value,)
            rows = db.execute(sql, params).fetchall()
        ```

    - **Form Processing** Pattern *(see [forms](forms.md) guide)*

        ```python
        @app.post("/path")
        def handler():
            value = request.form.get('field', '').strip()
            value = html.escape(value)
            # ... validate, then save
        ```


### 3. Edit / create page templates

- *See [jinja](jinja.md) doc for more details*


---
### 😀 That's it!


