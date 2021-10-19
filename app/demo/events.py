from flask import current_app
from flask_socketio import emit

from app import socket_io


@socket_io.on('check_progress_bar', namespace='/events')
def check_progress():
    cb = current_app.config['progress_cb']
    emit('progress', cb.progress)


@socket_io.on('reset_progress_bar', namespace='/events')
def reset_progress():
    cb = current_app.config['progress_cb']
    cb.reset()
    emit('progress', cb.progress)


@socket_io.on_error_default
def default_error_handler(e):
    pass
