#!/usr/bin/python3
"""Display all states or one selected state and its cities."""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def close_storage(error):
    """Close the active storage session after each Flask request."""
    storage.close()


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states(id=None):
    """Render all states or one state selected by its identifier."""
    if id is None:
        all_states = sorted(
            storage.all(State).values(),
            key=lambda state: state.name
        )

        return render_template(
            "9-states.html",
            states=all_states,
            state=None,
            single=False
        )

    state = storage.all(State).get(
        "State.{}".format(id)
    )

    return render_template(
        "9-states.html",
        states=None,
        state=state,
        single=True
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
