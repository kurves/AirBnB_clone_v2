#!/usr/bin/python3

"""script to create flask app"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>HGHhHHello HBNB!</p>"
