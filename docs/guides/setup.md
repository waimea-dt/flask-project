# Flask App Setup

## Create and Configure a Virtual Environment

### 1. Create a virtual environment:

   A virtual environment (venv) is used to create an isolated Python install, just for this app...

   ```bash
   python -m venv venv
   ```

   Activate the new virtual environment...

   On Windows:
   ```ps
   venv\Scripts\activate
   ```
   On Linux / Mac:
   ```bash
   source venv/bin/activate
   ```

### 2. Install dependencies:

   Install the required Python modules into the new virtual environment...

   ```bash
   pip install -r requirements.txt
   ```

### 3. Configure environment:

   Setup the environment variable file that define key values for the app...

   Copy `.env.example` to `.env`

   Customize `.env` if needed. At the least, change the secret string (used to encrypt session cookies)


## Setup the Database

### 1. Define Database Schema and Seed Data:

   Modify `app/db/config.py` to change database schema and define sample seed data.

   Database schema examples can be found in [schema.md](schema.md)

### 2. Create Database:

   The database is automatically created and seeded on **first run**...


## Launch the App

### 1. Run the app:

   In a terminal...

   ```bash
   flask run
   ```

### 2. View in browser:

   Open http://localhost:5000 in a browser


### 3. View Logs:

   Watch the console to see logs for:
   - Database configuration
   - HTTP requests and responses
   - SQL queries and results
   - Traceback of errors


## Command-Line DB Management Commands

A number of command-line commands are available to help you manage your database:

```bash
flask db-reset   # Delete and recreate database
flask db-seed    # Reseed with sample data
flask db-clear   # Clear all data (with confirmation)
flask db-show    # Shows the DB schema and data
flask db-schema  # Shows the DB schema
flask db-data    # Shows the DB data
```
