#!/usr/bin/env python
"""Module for chat views."""

from flask import render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user

from main import chat_views
from models.user import User
from controllers.chats_controller import get_chats


@chat_views.route("/", strict_slashes=False, methods=["GET"])
@login_required
def chats_page():
    """View for chats."""
    return render_template("chats.html")


@chat_views.route("/<string:user_id>", strict_slashes=False, methods=["GET"])
@login_required
def chats(user_id: str):
    """View for chats."""
    chat_user = User.get('id', user_id)
    if not chat_user:
        return redirect(url_for("chat.chats_page"))
    return render_template("chats.html", chat_user=chat_user, recent_chats=current_user.recent_messages())


@chat_views.route("/messages/<string:user_id>", strict_slashes=False, methods=["GET"])
def chat_message(user_id):
    """api for messages."""
    return get_chats(user_id)
