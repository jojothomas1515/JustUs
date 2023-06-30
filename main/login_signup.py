#!/usr/bin/env python

"""Module for signup views and login views."""

from flask import render_template, request, redirect, url_for
from flask_login import current_user

from controllers.auth_controller import login, signup
from main import auth_views


@auth_views.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login_page():
    """Login page

    Methods:
        GET: return the login page.
        POST: authenticate user and redirect to the chat page
    """
    if current_user.is_authenticated:
        return redirect(url_for("chat.chats_page"))
    if request.method == "POST":
        return login()
    return render_template('login_page.html')


@auth_views.route('/signup', strict_slashes=False, methods=['GET', 'POST'])
def signup_page():
    """Signup page

        Methods:
            GET: return the signup page.
            POST: Register user and redirect to the login page
    """
    if current_user.is_authenticated:
        return redirect(url_for("chat.chats_page"))
    if request.method == 'POST':
        return signup()
    return render_template('signup_page.html')


# todo: implement password reset
@auth_views.route('/reset_password', strict_slashes=False, methods=['GET', 'POST'])
def password_reset():
    pass
