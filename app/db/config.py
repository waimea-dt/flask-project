#============================================================================
# Database schema and seed data configuration
#============================================================================

#----------------------------------------------------------------------------
# Table schema
#----------------------------------------------------------------------------

NOTE_SCHEMA = """
    CREATE TABLE note (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT,
        pinned INTEGER DEFAULT 0,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

# Add other schema here...


#----------------------------------------------------------------------------
# Table seeding queries and data
#----------------------------------------------------------------------------

NOTE_SEED_SQL = """
    INSERT INTO note (title, body, pinned)
    VALUES ("Welcome!",        "This is a demo application using Flask, Jinja and SQLite.",  1),
           ("Getting Started", "Use this template as a starting point for your app.",        0),
           ("Pinned Note",     "Pinned notes always appear at the start of the note list.",  1),
           ("Sample Note 1",   "This is just a sample note with some sample text.",          0),
           ("Sample Note 2",   "This notes has multiple paragraphs.\n\nHere is the second.", 0),
           ("Sample Note 3",   "Multiple lines:\n- Item 1\n- Item 2\n- Item 3\n- Item 4",    0)
"""

# Add other seed data SQL here...


#----------------------------------------------------------------------------
# Tables List - Add your tables here
# Format: (table_name, schema, seed_sql),
#----------------------------------------------------------------------------

TABLES = [
    ('note', NOTE_SCHEMA, NOTE_SEED_SQL),
    # Add more tables here...
]

