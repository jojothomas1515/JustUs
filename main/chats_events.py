#!/usr/bin/env python
"""Module for chat events."""

import json
from os import getenv

import redis
from flask import request, copy_current_request_context
from flask_login import current_user
from flask_socketio import emit

from main import socketio
from models.message import Message
from models.user import User

redis_url = getenv("REDIS_URL", "www.jojothomas.tech")
redis_password = getenv("REDIS_PASSWORD", "speed123")

r = redis.StrictRedis(host=redis_url, port=6379, password="speed123", decode_responses=True)
id_to_sid = {}


def handler(data):
    """sub handler"""
    data = json.loads(data["data"])
    if data["sid"] == id_to_sid.get(data["receiver_id"]):
        socketio.emit("message", json.dumps({"sender": data["sender"], "message": data["message"]}), room=data["sid"])


def e_handler(err, er, e):
    pass


sub = r.pubsub()
sub.subscribe(chat=handler)
sub.run_in_thread(sleep_time=0.002, exception_handler=e_handler)


@socketio.on("connect")
def connect():
    """When client connects to the socket."""
    if current_user.is_authenticated:
        user = current_user
        r.hset("chat_sess", f"{user.id}", request.sid)
        id_to_sid[user.id] = request.sid
    else:
        pass


@socketio.on("message")
def message(data):
    """Message event"""
    user: User = current_user
    data = json.loads(data)
    if data["id"] is not None:
        Message(sender_id=user.id, receiver_id=data["id"], message=data["message"]).save()
        target = r.hget("chat_sess", data["id"])
        if target:
            if target == id_to_sid.get(data["id"]):
                socketio.emit("message", json.dumps({"sender": user.to_dict(), "message": data["message"]}), to=target)
            else:
                r.publish("chat", json.dumps(
                    {"sender": user.to_dict(), "message": data["message"], "sid": target, "receiver_id": data["id"]}))


@socketio.on("disconnect")
def disconnect():
    """When client disconnect it removes the sid relation."""
    user: User = current_user
    if user.id in id_to_sid.keys():
        id_to_sid.pop(user.id)
    r.hdel("chat_sess", f"{user.id}")


@socketio.on("offer")
def say_offer(data):
    user: User = current_user
    data = json.loads(data)
    if data["id"] is not None:
        target = r.hget("chat_sess", data["id"])
        if target:
            emit("offer", json.dumps(data), room=target)


@socketio.on("answer")
def ans_offer(data):
    user: User = current_user
    data = json.loads(data)
    if data["id"] is not None:
        target = r.hget("chat_sess", data["id"])
        if target:
            emit("answer", json.dumps(data), room=target)


@socketio.on("ice")
def candidate_offer(data):
    user: User = current_user
    data = json.loads(data)
    print(data)
    if data["id"] is not None:
        target = r.hget("chat_sess", data["id"])
        if target:
            emit("ice-candidate", json.dumps(data), room=target)
