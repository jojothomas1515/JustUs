#!/usr/bin/env python
"""This is the chat entry point for the application."""
import datetime as dt
import os

from flask import Flask
from flask_login import LoginManager
from main import auth_views, users_views, home_views, serve_file
from main import chat_views, socketio
from models.user import User
from models.db import Session
from flask_cors import CORS

login_manager = LoginManager()
app = Flask(__name__)
socketio.init_app(app)
CORS(app=app, resources={"/*": {"origins": "*"}})
login_manager.init_app(app)
login_manager.login_view = 'auth.login_page'


# todo: fix things
@login_manager.user_loader
def load_user(user_id: str):
    """Loads the user when ever its making a request

    Args:
        user_id: id  of the logged-in user
    Returns:
          User (object)
    """
    sess = Session()
    user = sess.get(User, user_id)
    sess.close()
    return user



app.permanent_session_lifetime = dt.timedelta(days=7)
app.secret_key = 'BAD_SECRET_KEY'
app.register_blueprint(auth_views)
app.register_blueprint(users_views)
app.register_blueprint(chat_views)
app.register_blueprint(home_views)
app.register_blueprint(serve_file)


# @app.teardown_appcontext
# def cleanup(exception):
#     """cleanly closes the session"""
#     sess = Session()
#     sess.close()

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
