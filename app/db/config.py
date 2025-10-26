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

# Add other table schema here...


#----------------------------------------------------------------------------
# Table seeding queries and data (optional)
#----------------------------------------------------------------------------

NOTE_SEED_SQL = """
    INSERT INTO note (title, body, pinned)
    VALUES
        ("Welcome!", "This is a demo application using Flask, Jinja and SQLite.", 1),
        ("Shopping List", "Milk\nBread\nEggs\nCheese", 0),
        ("Meeting Notes", "Discussed project timeline.\n\nAction items:\n- Review design\n- Update docs", 0),
        ("Recipe: Pasta", "Ingredients:\n- 500g pasta\n- Tomato sauce\n- Garlic\n\nCook pasta, add sauce, enjoy!", 0),
        ("Important!", "Remember to backup your database regularly.", 1)
"""

# Add other table seed data SQL here...


#----------------------------------------------------------------------------
# Tables List - Add your tables here
#
# Format: (table_name, schema, seed_sql),
#     or: (table_name, schema, None),
#
#   Note: The order is important - Create the tables that have foreign keys
#         *after* the linked table has been created
#----------------------------------------------------------------------------

TABLES = [
    ('note', NOTE_SCHEMA, NOTE_SEED_SQL),
    # Add more table rows here...
]

