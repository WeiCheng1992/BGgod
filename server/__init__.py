from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.debug = True

socketio = SocketIO(app)

MAX_PEOPLE = 15

from server import controller



