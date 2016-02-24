from server import app
from server import socketio

if __name__ == '__main__':
    socketio.run(app,port = 12138)
    #app.run(debug = True, port = 12138)

