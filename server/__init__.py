from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

socketio = SocketIO(app)

from server import viewhandlers



