from flask import Flask
from flask_socketio import SocketIO

application = app = Flask(__name__)
socketio = SocketIO(app)

from application import views