#============================================================================
# Database schema and seed data configuration
#============================================================================


#----------------------------------------------------------------------------
# Table definitions
#
# One per table, in this format:
#
# class TableName:
#     NAME   = ""
#     SCHEMA = "..."
#     SEED   = "..." or None
#----------------------------------------------------------------------------

class NoteTable:

    NAME = "note"

    SCHEMA = """
        CREATE TABLE note (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            title   TEXT NOT NULL,
            body    TEXT,
            pinned  INTEGER DEFAULT 0,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

    SEED = """
        INSERT INTO note (title, pinned, body)
        VALUES
            ("Welcome!",      1, "This is a demo application using Flask, Jinja and SQLite."),
            ("Shopping List", 0, "Milk\nBread\nEggs\nCheese"),
            ("Meeting Notes", 0, "Discussed project timeline.\n\nAction items:\n- Review design\n- Update docs"),
            ("Recipe: Pasta", 0, "Ingredients:\n- 500g pasta\n- Tomato sauce\n- Garlic\n\nCook pasta, add sauce, enjoy!"),
            ("Important!",    1, "Remember to backup your database regularly.")
    """

# Add more table classes here...



#----------------------------------------------------------------------------
# Table registry
#
# Format: (Table.NAME, Table.SCHEMA, Table.SEED),

# Note: The order is important - Create the tables that have foreign keys
#       *after* the linked table has been created
#----------------------------------------------------------------------------

TABLES = [
    (NoteTable.NAME, NoteTable.SCHEMA, NoteTable.SEED),
    # Add more tables here...
]

