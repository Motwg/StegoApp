from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_navbar import Nav
from flask_navbar.elements import View, Navbar
from flask_socketio import SocketIO
from flask_cors import CORS

mod_home = Blueprint('home', __name__, url_prefix='/')
from . import controllers

# used with eventlet module
socket_io = SocketIO(async_mode='eventlet')
import eventlet
eventlet.monkey_patch()

# used without eventlet
# socket_io = SocketIO(async_mode='threading')


def create_app():
    print('[INFO] Starting loading')
    app = Flask(__name__)
    # registers the "top" menu bar
    top_bar = Navbar(
        View('Background', 'home.get_home'),
        View('Watermarking Demo', 'demo.get_demo')
    )
    nav = Nav(app)
    nav.register_element('top', top_bar)
    Bootstrap(app)

    # Configurations
    print('[INFO] Loading configuration')
    app.config.from_object('config')

    from app.demo.stego.progress_callback import ProgressCallback
    app.config['progress_cb'] = ProgressCallback()

    # Register blueprint(s)
    print('[INFO] Loading blueprints')
    from app.demo import mod_demo
    app.register_blueprint(mod_home)
    app.register_blueprint(mod_demo)

    # Wrap app in flask socket-io
    CORS(app)
    socket_io.init_app(app)

    print('[INFO] Loading complete')
    return app
