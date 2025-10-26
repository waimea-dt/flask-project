# Flask Project Template

This is a simple [Flask](https://flask.palletsprojects.com/en/stable/) project, built using [Python](https://www.python.org/), that using a [SQLite](https://sqlite.org/) database, and [Jinja2](https://jinja.palletsprojects.com/en/stable/) templates

See the [docs](docs) folder for guides to usage.


## Project Structure

```
├── README.md            # Project README
│
├── requirements.txt     # Python modules required
│
├── docs/                # Project documentation
│   └── guides/          # Helpful guides
│
└── app/                 # Flask application
    │
    ├── __init__.py      # Routes and app logic
    │
    ├── .env             # Environment values
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
    │   ├── config.py    # Database schema & seed data
    │   └── data.sqlite  # SQLite database
    │
    └── helpers/         # Helper files (don't modify)

```
