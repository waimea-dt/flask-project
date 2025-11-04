# What is Flask?

[Flask](https://flask.palletsprojects.com/) is a lightweight Python web framework that provides routing and HTTP request / response handling. It uses [Jinja](https://jinja.palletsprojects.com/templates/) as its templating engine and connects easily to [SQLite](https://sqlite.org/) databases.

### A typical Flask web application:
1. Receives **HTTP requests** (GET / POST / PUT / DELETE)
2. **Routes** the request URLs to Python 'handler' functions
3. Requests SQLite database data via **SQL queries** if needed
4. Passes data to **Jinja templates** as variables
5. **Renders HTML**, using control logic and variables
6. Serves up the resulting HTML web page as an **HTTP response**


![Flask flow diagram](../assets/images/flask.png)


