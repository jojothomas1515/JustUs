#!/usr/bin/env python
"""Users route and views"""
import datetime

from flask import jsonify
from flask_login import current_user

from models.friend import Friend, FriendshipStatus
from models.user import User
from user import users_views


@users_views.route("/friends", strict_slashes=False, methods=["GET"])
def all_friends():
    """Get all friends."""
    user: User = current_user
    if user.is_authenticated:
        data = user.friends
        return jsonify(data), 200
    else:
        return jsonify({'error': 'unauthenticated users'}), 401


@users_views.route("/friends/<user_id:string>", strict_slashes=False, methods=["POST"])
def add_friend(user_id: str):
    """Add a friend with the user id"""
    user: User = current_user
    if not user.is_authenticated:
        return jsonify({'error': 'unauthenticated users'}), 401
    if User.get('id', user_id):
        return jsonify({"error": "User Not found"}), 404
    friend = Friend.filter_one(
        ((Friend.requester_id == user.id) &
         (Friend.requested_id == user_id)) |
        ((Friend.requester_id == user_id) &
         (Friend.requested_id == user.id)))
    if friend:
        if friend.status.value == "accepted":
            return jsonify({"error": "You are already friends with this user "}), 200
        elif friend.status.value == "pending":
            return jsonify({"error": "You have a pending friend requested with this user "}), 200
        elif friend.status.value == "rejected":
            return jsonify({"error": "You cannot send this user a friend request"})
    friend = Friend(user.id, user_id, FriendshipStatus.pending, datetime.datetime.now())
    friend.save()
    return jsonify(friend.to_dict()), 201
