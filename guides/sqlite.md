# SQLite Cheetsheet

## Example Queries

### Fetch All Rows - fetchall()

```python
sql = "SELECT * FROM note"
params = ()
rows = db.execute(sql, params).fetchall()
```

### Fetch a Single Row - fetchone()

```python
sql = "SELECT * FROM note WHERE id = ?"
params = (id,)
row = db.execute(sql, params).fetchone()
```

### Add a New Row

```python
sql = "INSERT INTO note (title, body) VALUES (?, ?)"
params = (title, body)
result = db.execute(sql, params)
new_id = result.lastrowid
```

### Update a Row

```python
sql = "UPDATE note SET title = ? WHERE id = ?"
params = (title, id)
db.execute(sql, params)
```

### Delete a Row

```python
sql = "DELETE FROM note WHERE id = ?"
params = (id,)
db.execute(sql, params)
```

## Tips

- Always use parameterized queries (`?` placeholders) to prevent SQL injection
- NEVER use f-strings or string concatenation with user input

Good:
```python
sql = "SELECT * FROM note WHERE id=?"
params = (id,)
db.execute(sql, params)
```
Bad:
```python
sql = f"SELECT * FROM note WHERE id={id}"
db.execute(sql)
```

