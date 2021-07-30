import os

from flask import render_template, send_from_directory, current_app

from . import mod_home


@mod_home.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@mod_home.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'favicon.svg'
    )


@mod_home.route('/', methods=['GET'])
@mod_home.route('/home/', methods=['GET'])
def get_home():
    return render_template('home.html')
