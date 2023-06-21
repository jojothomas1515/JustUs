#!/usr/bin/env python
"""Users route and views"""

from models.user import User
from flask import request, jsonify
from user import users_views
from flask_login import login_required, current_user
from models.db import sess
from models.friend import Friend
import json


@users_views.route("/friends", strict_slashes=False, methods=["GET"])
def all_friends():
    """Get all friends."""
    user: User = current_user
    friends: list = user.friends_req
    friends.extend(user.friends_got)
    friends = list(map(lambda x: x.to_dict(), friends))

    return jsonify({'status': 'ok'}), 200
