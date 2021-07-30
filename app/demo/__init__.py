from flask import Blueprint

MOD_NAME = 'demo'
mod_demo = Blueprint(MOD_NAME, __name__, url_prefix=f'/{MOD_NAME}')

from . import controllers, events
