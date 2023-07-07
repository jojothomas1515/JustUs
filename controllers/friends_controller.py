#!/usr/bin/env python

"""Controller for adding friends."""

from flask import jsonify
from flask_login import current_user

from models.friend import Friend, FriendshipStatus
from models.user import User
from models.db import Session


def send_friend_request(user_id: str):
    """Send a friend request to a user.

    Args:
        user_id (str): The id of the user to send the friend request to.
    """
    user: User = current_user
    sess: Session = Session()
    if not user.is_authenticated:
        sess.close()
        return jsonify({'error': 'unauthenticated user'}), 401
    if not sess.query(User).filter_by(id=user_id).first():
        sess.close()
        return jsonify({"error": "User Not found"}), 404
    if user_id == user.id:
        sess.close()
        return jsonify({"error": "Cannot send friend request to yourself"}), 400
    friend = sess.query(Friend).filter(((Friend.requester_id == user.id) & (Friend.requested_id == user_id)) | (
            (Friend.requester_id == user_id) & (Friend.requested_id == user.id))).first()
    if friend:
        sess.close()
        if friend.status.value == "accepted":
            return jsonify({"error": "You are already friends with this user "}), 400
        elif friend.status.value == "pending":
            return jsonify({"error": "You have a pending friend requested with this user "}), 400
        elif friend.status.value == "rejected":
            return jsonify({"error": "You cannot send this user a friend request"}), 400
    friend = Friend(requester_id=user.id, requested_id=user_id, status=FriendshipStatus.pending, )
    sess.add(friend)
    sess.commit()
    sess.close()
    return jsonify(success="request sent successfully"), 201


def accept_friend_request(user_id: str):
    """Accept a friend request."""
    user: User = current_user
    sess: Session = Session()
    if not user.is_authenticated:
        sess.close()
        return jsonify({'error': 'unauthenticated user'}), 401
    if not sess.query(User).filter_by(id=user_id).first():
        sess.close()
        return jsonify({"error": "User Not found"}), 404
    if user_id == user.id:
        sess.close()
        return jsonify({"error": "Bad request"}), 400
    friend = sess.query(Friend).filter((Friend.requester_id == user_id) & (Friend.requested_id == user.id)).first()
    if friend:
        if friend.status.value == "accepted":
            sess.close()
            return jsonify({"error": "You are already friends with this user "}), 400
        elif friend.status.value == "rejected":
            sess.close()
            return jsonify({"error": "You already rejected this user a friend request"}), 400

    friend.status = FriendshipStatus.accepted
    sess.commit()
    sess.close()
    return jsonify(success="request accepted successfully"), 201


def reject_friend_request(user_id: str):
    """Reject a friend request."""
    user: User = current_user
    sess: Session = Session()
    if not user.is_authenticated:
        sess.close()
        return jsonify({'error': 'unauthenticated user'}), 401
    if not sess.query(User).filter_by(id=user_id).first():
        sess.close()
        return jsonify({"error": "User Not found"}), 404
    if user_id == user.id:
        sess.close()
        return jsonify({"error": "Bad request"}), 400
    friend = sess.query(Friend).filter((Friend.requester_id == user_id) & (Friend.requested_id == user.id)).first()
    if friend:
        if friend.status.value == "accepted":
            sess.close()
            return jsonify({"error": "You are already friends with this user "}), 400
        elif friend.status.value == "rejected":
            sess.close()
            return jsonify({"error": "You already rejected this user a friend request"}), 400

    friend.status = FriendshipStatus.rejected
    sess.commit()
    sess.close()
    return jsonify(success="request rejected successfully"), 201