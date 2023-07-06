#!/usr/bin/env python
"""Initialization module """
from flask.blueprints import Blueprint
from flask_socketio import SocketIO

auth_views = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates', static_folder='../static',
                       static_url_path='/static/')
serve_file = Blueprint('serve_files', __name__, url_prefix='/files', template_folder='templates',
                       static_folder='../files', static_url_path='/')
users_views = Blueprint('user', __name__, url_prefix='/users', template_folder='templates', static_folder='../static',
                        static_url_path='/static/')
home_views = Blueprint('home', __name__, url_prefix='/', template_folder='templates', static_folder='../static',
                       static_url_path='/static/')

socketio = SocketIO()
chat_views = Blueprint('chat', __name__, url_prefix='/chats', template_folder='templates', static_folder='../static',
                       static_url_path='/static/')

from main.users import *
from main.login_signup import *
from main.chats_events import *
from main.home import *
from main.chats import *
from main.serve_files import *
