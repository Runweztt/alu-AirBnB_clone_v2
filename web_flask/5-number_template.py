#!/usr/bin/python3
"""Start a Flask application that renders a number template."""

from flask import Flask, render_template


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Return the HBNB greeting for the root route."""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Return HBNB for the dedicated HBNB route."""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """Return C followed by text with underscores replaced by spaces."""
    return "C {}".format(text.replace("_", " "))


@app.route(
    "/python/",
    defaults={"text": "is cool"},
    strict_slashes=False
)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text):
    """Return Python followed by the supplied text value."""
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def number_route(n):
    """Return a message identifying the supplied integer as a number."""
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """Render an HTML page containing the supplied integer."""
    return render_template("5-number.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
