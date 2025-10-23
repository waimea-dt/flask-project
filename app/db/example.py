#============================================================================
# Example Database Schema
#============================================================================


#----------------------------------------------------------------------------
# Simple, single table schema
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
# Typical two-table schema with a single foreign key
#----------------------------------------------------------------------------

USER_SCHEMA = """
    CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        forename TEXT NOT NULL,
        surname TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        pass_hash TEXT NOT NULL
    )
"""

NOTE_SCHEMA = """
    CREATE TABLE note (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT,
        pinned INTEGER DEFAULT 0,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER NOT NULL,

        FOREIGN KEY(user_id) REFERENCES user(id)
    )
"""


#----------------------------------------------------------------------------
# Two table, many-to-many schema with a linking table, having a composite PK
#----------------------------------------------------------------------------

USER_SCHEMA = """
    CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        forename TEXT NOT NULL,
        surname TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        pass_hash TEXT NOT NULL
    )
"""

CLUB_SCHEMA = """
    CREATE TABLE club (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
"""

MEMBER_SCHEMA = """
    CREATE TABLE member (
        user_id INTEGER NOT NULL,
        club_id INTEGER NOT NULL,

        PRIMARY KEY(user_id, club_id),

        FOREIGN KEY(user_id) REFERENCES user(id),
        FOREIGN KEY(club_id) REFERENCES club(id)
    )
"""


#----------------------------------------------------------------------------
# Example table seeding queries and data
#----------------------------------------------------------------------------

# test password is 'test'
USER_SEED_SQL = """
    INSERT INTO user (forename, surname, username, pass_hash)
    VALUES ("Test", "User", "test", "scrypt:32768:8:1$n7eJTucLbaGmUpAM$c1776374a8d456a6eaf61bccc08db5e1fcc4ff3b3983d364c45ab13074255eeae0a393afb11f99a9fe63fb1d980992ace17a72ba70324523b11e92e36cbe4252")
"""

NOTE_SEED_SQL = """
    INSERT INTO note (title, body, pinned, user_id)
    VALUES ("Welcome!",        "This is a demo application using Flask, Jinja and SQLite.", 1, 1),
           ("Getting Started", "Use this template as a starting point for your app.",       1, 1),
           ("Pinned Note",     "Pinned notes always appear at the top of your list.",       1, 1),
           ("Sample Note",     "This is just a sample note.\n\nIt has some sample text.",   0, 1),
           ("Sample Note",     "This is just a sample note.\n\nIt has some sample text.",   0, 1),
           ("Sample Note",     "This is just a sample note.\n\nIt has some sample text.",   0, 1)
"""


#----------------------------------------------------------------------------
# Example tables List - One row per table
#----------------------------------------------------------------------------

TABLES = [
    ('user', USER_SCHEMA, USER_SEED_SQL),
    ('note', NOTE_SCHEMA, NOTE_SEED_SQL),
]

