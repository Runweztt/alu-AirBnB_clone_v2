#!/usr/bin/python3
"""Start a Flask application with root and HBNB routes."""

from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Return the HBNB greeting for the root route."""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Return HBNB for the dedicated HBNB route."""
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
