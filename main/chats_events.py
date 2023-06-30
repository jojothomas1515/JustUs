#!/usr/bin/env python
"""Module for chat events."""

import json
from os import getenv

import redis
from flask import request
from flask_login import current_user
from flask_socketio import emit

from main import socketio
from models.message import Message
from models.user import User

redis_url = getenv("REDIS_URL", "www.jojothomas.tech")
redis_password = getenv("REDIS_PASSWORD", "speed123")

r = redis.StrictRedis(host=redis_url, port=6379, password="speed123", decode_responses=True)


@socketio.on("connect")
def connect():
    """When client connects to the socket."""
    if current_user.is_authenticated:
        user = current_user
        r.hset("chat_sess", f"{user.id}", request.sid)
    else:
        return False


@socketio.on("message")
def message(data):
    """Message event"""
    user: User = current_user
    data = json.loads(data)
    if data["id"] is not None:
        Message(sender_id=user.id, receiver_id=data["id"], message=data["message"]).save()
        target = r.hget("chat_sess", data["id"])
        if target:
            emit("message", json.dumps({"sender": user.to_dict(), "message": data["message"]}), room=target)


@socketio.on("disconnect")
def disconnect():
    """When client disconnect it removes the sid relation."""
    user = current_user
    r.hdel("chat_sess", f"{user.id}")
