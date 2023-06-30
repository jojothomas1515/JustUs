#!/usr/bin/env python

"""Module for chat controllers."""

from flask import jsonify
from flask_login import current_user

from models.user import User


def get_chats(user_id: str):
    """Get chats."""
    user: User = current_user
    if not user.is_authenticated:
        return jsonify({'error': 'unauthenticated user'}), 401
    messages = user.messages_with(user_id)
    return jsonify(messages), 200

def recent_chats():
    """Get recent chats."""
    user: User = current_user
    if not user.is_authenticated:
        return jsonify({'error': 'unauthenticated user'}), 401
    messages = user.recent_messages()
    return jsonify(messages), 200
