#!/usr/bin/env python
"""Users route and views"""

from flask import jsonify, render_template, url_for, redirect
from flask_login import current_user, login_required

from controllers.friends_controller import send_friend_request, accept_friend_request, reject_friend_request
from controllers.auth_controller import update_profile, update_profile_image
from main import users_views
from models.db import Session
from models.user import User


@users_views.route("/", strict_slashes=True, methods=["GET"])
def all_users():
    """Get all users"""
    user: User = current_user
    sess = Session()
    sess.add(user)
    all_user = set(sess.query(User).all())
    all_user.discard(user)
    all_user.difference_update(user.exc_friends)
    all_user = list(map(lambda x: x.to_dict(), list(all_user)))
    sess.close()
    return jsonify(all_user), 200


@users_views.route("/friends", strict_slashes=False, methods=["GET"])
def all_friends():
    """Get all friends."""
    user: User = current_user
    sess = Session()
    if user.is_authenticated:
        sess.add(user)
        data = user.friends
        sess.close()
        return jsonify(data), 200
    sess.close()
    return jsonify({'error': 'unauthenticated users'}), 401


@users_views.route("/friends/<string:user_id>", strict_slashes=False, methods=["POST"])
def add_friend(user_id: str):
    """Add a friend with the user id"""
    return send_friend_request(user_id)


@users_views.route("/friends/<string:user_id>", strict_slashes=False, methods=["PUT"])
def accept_friend(user_id: str):
    """Accept a friend request."""
    return accept_friend_request(user_id)


@users_views.route("/friends/<string:user_id>", strict_slashes=False, methods=["DELETE"])
def reject_friend_request(user_id: str):
    """Reject a friend request."""
    return reject_friend_request(user_id)


@users_views.route("/update_profile", strict_slashes=False, methods=["POST"])
def update_user_profile():
    """update profile info"""
    update_profile_image()
    update_profile()
    return redirect(url_for('home.home_page'))
