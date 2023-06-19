#!/usr/bin/env python
"""Chat views"""
from flask import render_template

from chat import chat_views
from flask_login import login_required


@chat_views.route("/", strict_slashes=False,
                  methods=["GET"])
@login_required
def chats_page():
    """View for chats."""
    return render_template("chats.html")
