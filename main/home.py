#!/usr/bin/env python

"""Module for home views."""

from flask import render_template
from flask_login import login_required, current_user

from main import home_views


@home_views.route("/", strict_slashes=False, methods=["GET"])
@login_required
def home_page():
    """View for home."""
    return render_template("home.html", user=current_user)


@home_views.route("/landing_page" ,strict_slashes=False)
def landing_page():
    """landing_page view"""
    return render_template("landing_page.html")

