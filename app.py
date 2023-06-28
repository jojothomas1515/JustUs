#!/usr/bin/env python
"""This is the chat entry point for the application."""
import datetime as dt
import os

from flask import Flask
from flask_login import LoginManager
from models.db import sess
from main import auth_views, users_views, home_views
from main import chat_views, socketio
from models.user import User

login_manager = LoginManager()
app = Flask(__name__)
socketio.init_app(app)
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
    return User.get('id', user_id)


app.permanent_session_lifetime = dt.timedelta(days=7)
app.secret_key = 'BAD_SECRET_KEY'
app.register_blueprint(auth_views)
app.register_blueprint(users_views)
app.register_blueprint(chat_views)
app.register_blueprint(home_views)


@app.teardown_appcontext
def cleanup(exception):
    """cleanly closes the session"""
    sess.close()


print(os.getenv('JUSTUS_USER', None))
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)
