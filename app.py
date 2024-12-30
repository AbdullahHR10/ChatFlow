""" Entry point to initialize and run the Flask application. """
import eventlet
eventlet.monkey_patch()

from website import create_app, Config, socketio
from flask_socketio import SocketIO


app = create_app()
app.config.from_object(Config)


if __name__ == '__main__':
    socketio.run(app, debug=True)
