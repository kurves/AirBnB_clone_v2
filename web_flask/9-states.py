#!/usr/bin/python3
"""Script to start a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

@app.route('/states', strict_slashes=False)
def states_list():
    """Display a HTML of all State objects"""
    states = storage.all(State).values()
    return render_template('9-states.html', states=sorted(states, key=lambda x: x.name))

@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Display a HTML  of cities of a specific state"""
    states = storage.all(State).values()
    state = None
    for st in states:
        if st.id == id:
            state = st
            break
    if state:
        return render_template('9-states.html', state=state)
    else:
        return render_template('not_found.html')

@app.teardown_appcontext
def teardown_db(exception):
    """Close the current SQLAlchemy Session"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
