#!/usr/bin/env python
"""Initialization module """
from flask import Blueprint
from flask_socketio import SocketIO

socketio = SocketIO()
chat_views = Blueprint('chat', __name__,
                       url_prefix='/chats',
                       template_folder='templates',
                       static_folder='static',
                       static_url_path='/')

from chat.views import *
