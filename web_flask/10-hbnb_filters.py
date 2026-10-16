#!/usr/bin/python3
"""Display dynamic HBNB filters using data from storage."""

from flask import Flask, render_template
from models import storage
from models.amenity import Amenity
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def close_storage(error):
    """Close the active storage session after each Flask request."""
    storage.close()


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Render states, cities, and amenities in the HBNB filters."""
    states = sorted(
        storage.all(State).values(),
        key=lambda state: state.name
    )

    amenities = sorted(
        storage.all(Amenity).values(),
        key=lambda amenity: amenity.name
    )

    return render_template(
        "10-hbnb_filters.html",
        states=states,
        amenities=amenities
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
