# SQLite Queries

## Query Parameters

### Query with No Parameters

```python
with connect_db() as db:
    sql = "SELECT * FROM note"
    notes = db.execute(sql).fetchall()
```

### Query with Parameters

```python
with connect_db() as db:
    sql = "SELECT * FROM note WHERE user_id=?"
    params = (id,)
    notes = db.execute(sql, params).fetchall()
```

```python
with connect_db() as db:
    sql = "INSERT INTO note (title, body) VALUES (?, ?)"
    params = (title, body)
    db.execute(sql, params)
```

## Example Queries

### `SELECT` to Fetch All Rows with`fetchall()`

```python
with connect_db() as db:
    sql = "SELECT * FROM note WHERE pinned=1"
    notes = db.execute(sql).fetchall()
```

### `SELECT` to Fetch a Single Row with `fetchone()`

```python
with connect_db() as db:
    sql = "SELECT * FROM note WHERE id = ?"
    params = (id,)
    note = db.execute(sql, params).fetchone()
```

### `INSERT` to Add a New Row

```python
with connect_db() as db:
    sql = "INSERT INTO note (title, body) VALUES (?, ?)"
    params = (title, body)
    db.execute(sql, params)
```

#### ... and get the id of the new row

```python
with connect_db() as db:
    sql = "INSERT INTO note (title, body) VALUES (?, ?)"
    params = (title, body)
    result = db.execute(sql, params)
    new_id = result.lastrowid
```

### `UPDATE` to Update a Row

```python
with connect_db() as db:
    sql = "UPDATE note SET title = ? WHERE id = ?"
    params = (title, id)
    db.execute(sql, params)
```

### `DELETE` to Delete a Row

```python
with connect_db() as db:
    sql = "DELETE FROM note WHERE id = ?"
    params = (id,)
    db.execute(sql, params)
```

## Tips

- Always use parameterized queries (`?` placeholders) to prevent SQL injection
- NEVER use f-strings or string concatenation with user input

Good:
```python
with connect_db() as db:
    sql = "SELECT * FROM note WHERE id=?"
    params = (id,)
    db.execute(sql, params)
```
Bad:
```python
with connect_db() as db:
    sql = f"SELECT * FROM note WHERE id={id}"
    db.execute(sql)
```

