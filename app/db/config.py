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

#----------------------------------------------------------------------------
# Table seeding queries and data
#----------------------------------------------------------------------------

NOTE_SEED_SQL = """
    INSERT INTO note (title, body, pinned)
    VALUES ("Welcome!",        "This is a demo application using Flask, Jinja and SQLite.", 1),
           ("Getting Started", "Use this template as a starting point for your app.",       1),
           ("Pinned Note",     "Pinned notes always appear at the top of your list.",       1),
           ("Sample Note",     "This is just a sample note.\n\nIt has some sample text.",   0),
           ("Sample Note",     "This is just a sample note.\n\nIt has some sample text.",   0),
           ("Sample Note",     "This is just a sample note.\n\nIt has some sample text.",   0)
"""


#----------------------------------------------------------------------------
# Tables List - One row per table
#----------------------------------------------------------------------------

TABLES = [
    ('note', NOTE_SCHEMA, NOTE_SEED_SQL),
]

