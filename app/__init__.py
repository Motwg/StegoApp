from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_navbar import Nav
from flask_navbar.elements import View, Navbar
from flask_socketio import SocketIO

# Import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy

mod_home = Blueprint('home', __name__, url_prefix='/')
from . import controllers

socket_io = SocketIO(async_mode='threading')


def create_app():
    app = Flask(__name__)
    # registers the "top" menu bar
    top_bar = Navbar(
        View('Home', 'home.get_home'),
        View('Demo', 'demo.get_demo')
    )
    nav = Nav(app)
    nav.register_element('top', top_bar)
    Bootstrap(app)

    # Configurations
    app.config.from_object('config')

    from app.demo.stego.progress_callback import ProgressCallback
    app.config['progress_cb'] = ProgressCallback()

    # Define the database object which is imported
    # by modules and controllers
    # db = SQLAlchemy(app)

    # Register blueprint(s)
    from app.demo import mod_demo
    app.register_blueprint(mod_home)
    app.register_blueprint(mod_demo)

    # Build the database:
    # This will create the database file using SQLAlchemy
    # db.create_all()
    socket_io.init_app(app)
    return app
