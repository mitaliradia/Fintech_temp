import os

from flask import Flask, render_template, jsonify, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Babes!"


if __name__ == "__main__":
    app.run(debug=True)