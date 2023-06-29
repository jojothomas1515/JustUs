#!/usr/bin/env python
"""Users route and views"""

import json

from flask import jsonify
from flask import render_template, request
from flask_login import login_required, current_user
from flask_socketio import emit

from main import chat_views, socketio, users_views, home_views
from models.friend import Friend, FriendshipStatus
from models.message import Message
from models.user import User


@users_views.route("/", strict_slashes=True, methods=["GET"])
def all_users():
    """Get all users"""
    user: User = current_user
    all_user = set(User.all())
    all_user.discard(user)
    all_user.difference_update(user.exc_friends)
    all_user = list(map(lambda x: x.to_dict(), list(all_user)))

    return jsonify(all_user), 200


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
    return jsonify(success="request sent successfully"), 201


@users_views.route("/friends/<string:user_id>", strict_slashes=False, methods=["PUT"])
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
    print(friend.to_dict())
    return jsonify(success="request accepted successfully"), 201


@users_views.route("/friends/<string:user_id>", strict_slashes=False, methods=["DELETE"])
def reject_friend_request(user_id: str):
    """Reject a friend request."""
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

    friend.status = FriendshipStatus.rejected
    friend.save()
    return jsonify(success="request rejected successfully"), 201


# todo: orginize

user_id_to_sid = {}


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
        return jsonify({"error": "User Not found"}), 404
    print(chat_user)
    return render_template("chats.html", chat_user=chat_user)


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
        target = user_id_to_sid.get(data['id'])
        if target:
            emit("message", json.dumps({"sender": user.to_dict(), "message": data['message']}), room=target)


@socketio.on('disconnect')
def disconnect():
    """When client disconnect it removes the sid relation."""
    user = current_user
    user_id_to_sid.pop(f'{user.id}')


@home_views.route("/", strict_slashes=False, methods=["GET"])
@login_required
def home_page():
    """View for home."""
    return render_template("home.html", user=current_user)
