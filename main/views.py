#!/usr/bin/env python
"""Users route and views"""

import json

from flask import jsonify
from flask import render_template, request
from flask_login import login_required, current_user
from flask_socketio import emit

from main import chat_views, socketio
from main import users_views
from models.friend import Friend, FriendshipStatus
from models.message import Message
from models.user import User


@users_views.route("/friends", strict_slashes=False, methods=["GET"])
def all_friends():
    """Get all friends."""
    user: User = current_user
    if user.is_authenticated:
        data = user.friends
        return jsonify(data), 200
    else:
        return jsonify({'error': 'unauthenticated users'}), 401


@users_views.route("/friends/<string:user_id>", strict_slashes=False, methods=["POST"])
def add_friend(user_id: str):
    """Add a friend with the user id"""
    user: User = current_user
    if not user.is_authenticated:
        return jsonify({'error': 'unauthenticated user'}), 401
    if not User.get('id', user_id):
        return jsonify({"error": "User Not found"}), 404
    if user_id == user.id:
        return jsonify({"error": "Cannot send friend request to yourself"}), 400
    friend = Friend.filter_one(((Friend.requester_id == user.id) & (Friend.requested_id == user_id)) | (
            (Friend.requester_id == user_id) & (Friend.requested_id == user.id)))
    if friend:
        if friend.status.value == "accepted":
            return jsonify({"error": "You are already friends with this user "}), 400
        elif friend.status.value == "pending":
            return jsonify({"error": "You have a pending friend requested with this user "}), 400
        elif friend.status.value == "rejected":
            return jsonify({"error": "You cannot send this user a friend request"}), 400
    friend = Friend(requester_id=user.id, requested_id=user_id, status=FriendshipStatus.pending, )
    friend.save()
    return jsonify(friend.to_dict()), 201


@users_views.route("/friends/<string:user_id>", strict_slashes=False, methods=["POST"])
def accept_friend_request(user_id: str):
    """Accept a friend request."""
    user: User = current_user
    if not user.is_authenticated:
        return jsonify({'error': 'unauthenticated user'}), 401
    if not User.get('id', user_id):
        return jsonify({"error": "User Not found"}), 404
    if user_id == user.id:
        return jsonify({"error": "Bad request"}), 400
    friend = Friend.filter_one((Friend.requester_id == user_id) & (Friend.requested_id == user.id))
    if friend:
        if friend.status.value == "accepted":
            return jsonify({"error": "You are already friends with this user "}), 400
        elif friend.status.value == "rejected":
            return jsonify({"error": "You already rejected this user a friend request"}), 400

    friend.status = FriendshipStatus.accepted
    friend.save()
    return jsonify(friend.to_dict()), 201


# todo: orginize

user_id_to_sid = {}


@chat_views.route("/", strict_slashes=False, methods=["GET"])
@login_required
def chats_page():
    """View for chats."""
    return render_template("chats.html")


@chat_views.route("/messages/<string:user_id>", strict_slashes=False, methods=["GET"])
def chat_message(user_id):
    """api for messages."""
    user: User = current_user
    if not user.is_authenticated:
        return jsonify({'error': 'unauthenticated user'}), 401
    messages = user.messages_with(user_id)
    return jsonify(messages), 200


@socketio.on('connect')
def connect():
    """When client connects to the socket."""
    if current_user.is_authenticated:
        user = current_user
        user_id_to_sid[f'{user.id}'] = request.sid

    else:
        return False


@socketio.on('message')
def message(data):
    """Message event"""
    user: User = current_user
    data = json.loads(data)
    if data['id'] is not None:
        Message(sender_id=user.id, receiver_id=data['id'], message=data['message']).save()
        emit("message", json.dumps({"message": data['message']}), room=user_id_to_sid[data['id']])


@socketio.on('disconnect')
def disconnect():
    """When client disconnect it removes the sid relation."""
    user = current_user
    user_id_to_sid.pop(f'{user.id}')
