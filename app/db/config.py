#============================================================================
# Database schema and seed data configuration
#============================================================================


#----------------------------------------------------------------------------
# Table definitions
#----------------------------------------------------------------------------
# Define your tables with a name, a schema and optional seed/sample data,
# using this format, and then add the tables to the Table Registry below:
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
#----------------------------------------------------------------------------
# Register all of your tables by adding them to the TABLES list here:
#
# TABLES = [
#     (Table1.NAME, Table1.SCHEMA, Table1.SEED),
#     (Table2.NAME, Table2.SCHEMA, Table2.SEED),
#     etc.
# ]
#
# Note: The table order is important - Create the tables that have
# foreign keys *after* the tables they link to have been created
#----------------------------------------------------------------------------

TABLES = [
    (NoteTable.NAME, NoteTable.SCHEMA, NoteTable.SEED),
    # Add more tables here...
]

