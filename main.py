from server import app
from server import socketio
import logging

if __name__ == '__main__':
    log = logging.FileHandler('log')
    log.setLevel(logging.INFO)
    app.logger.addHandler(log)
    log.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s'
        '[%(filename)s(%(funcName)s:%(lineno)d)]'
        ': %(message)s'))
    socketio.run(app, port=12138)

