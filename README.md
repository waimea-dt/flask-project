# Flask Project Template

> [!IMPORTANT]
> Replace this file with the README template in the docs folder

---

A simple Flask template for web development with Python.

## Project Structure

```
├── README.md            # Project README
├── docs/                # Project documentation
├── guides/              # Helpful guides
├── .gitignore           # Files not be be pushed to GH
├── requirements.txt     # Python modules required
│
└── app/                 # Flask application
    │
    ├── .env             # Environment values
    │
    ├── __init__.py      # Routes and app logic go here
    │
    ├── templates/       # Jinja2 templates
    │   ├── pages/       # Full page templates
    │   └── partials/    # Reusable template parts
    │
    ├── static/          # Files to be served directly
    │   ├── css/         # CSS stylesheets
    │   ├── images/      # Images
    │   └── js/          # Javascript files
    │
    ├── db/              # Database files
    │   ├── data.sqlite  # SQLite database
    │   ├── config.py    # Database schema & seed data
    │   └── example.py   # Example database schema
    │
    └── helpers/         # Helper funcs (don't modify)

```
