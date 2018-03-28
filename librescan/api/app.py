from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO, emit

app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app, async_mode='threading')


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
