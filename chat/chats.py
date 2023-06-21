#!/usr/bin/env python
"""Chat views"""
from flask import render_template, request

from flask_login import login_required, current_user
from chat import chat_views, socketio

user_id_to_sid = {}


@chat_views.route("/", strict_slashes=False, methods=["GET"])
@login_required
def chats_page():
    """View for chats."""
    return render_template("chats.html")


@socketio.on('connect')
def connect():
    """When client connects to the socket."""
    if current_user.is_authenticated:
        user = current_user
        user_id_to_sid[f'{user.id}'] = request.sid
        print(user_id_to_sid)

    else:
        return False


@socketio.on('disconnect')
def disconnect():
    """When client disconnect it removes the sid relation."""
    user = current_user
    user_id_to_sid.pop(f'{user.id}')
