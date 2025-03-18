import os

from flask import Flask, render_template, jsonify, Response
from .agent_runner import get_latest_data

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', '..', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', '..', 'static')
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    data_to_send = get_latest_data()
    print("Sending to frontend:", data_to_send)
    response = jsonify(data_to_send)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response