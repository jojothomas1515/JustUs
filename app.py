#!/usr/bin/env python
"""This is the chat entry point for the application."""
import datetime as dt
import os

from flask import Flask, redirect
from flask_login import LoginManager

from authentication import auth_views
from chat import chat_views
from models.user import User

login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)
login_manager.login_view = 'authentication.login_page'



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
app.register_blueprint(chat_views)


@app.route("/", strict_slashes=True)
def index():
    """This route redirect to chat"""
    return redirect('/chats')


print(os.getenv('JUSTUS_USER', None))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
