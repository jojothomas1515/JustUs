#!/usr/bin/env python

"""Module for chat controllers."""

from flask import jsonify
from flask_login import current_user

from models.db import Session
from models.message import Message
from models.user import User


def get_chats(user_id: str):
    """Get chats."""
    user: User = current_user
    if not user.is_authenticated:
        return jsonify({'error': 'unauthenticated user'}), 401
    sess = Session()
    data = sess.query(Message).filter(((Message.sender_id == user.id) & (Message.receiver_id == user_id)) | (
            (Message.sender_id == user_id) & (Message.receiver_id == user.id)))
    messages = list(map(lambda message: message.to_dict(), data))
    sess.close()
    return jsonify(messages), 200


def recent_chats():
    """Get recent chats."""
    user: User = current_user
    # if not user.is_authenticated:
    #     return jsonify({'error': 'unauthenticated user'}), 401
    sess = Session()
    sess.add(user)
    res = []
    for i in user.exc_friends:
        data = sess.query(Message).filter(((Message.sender_id == user.id) & (Message.receiver_id == i.id)) | (
                (Message.sender_id == i.id) & (Message.receiver_id == user.id))).all()
        messages = list(map(lambda message: message.to_dict(), data))
        if messages:
            res.append({"user": i.to_dict(), "data": messages[-1]})
    sess.close()
    # return jsonify(messages), 200
    return res
