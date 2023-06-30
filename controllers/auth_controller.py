#!/usr/bin/env python
"""Login controller."""

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User

import datetime as dt


def login():
    """Login user."""

    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember-me')

    user: User = User.get('email', email)
    if not user:
        flash("Email not associated with any account", "error")
        return render_template('login_page.html')
    if check_password_hash(user.password, password):
        if login_user(user=user, remember=remember, duration=dt.timedelta(days=7)):
            return redirect(url_for("home.home_page"))
        if not user.is_active:
            flash("Inactive user", "error")
        else:
            flash("Error occurred while trying to log in", "error")
        return render_template("login_page.html")
    else:
        flash("Incorrect password", "error")
        return render_template("login_page.html")

def signup():
    """Signup user."""
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    middle_name = request.form.get('middlename')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('c-password')

    if password != password2:
        flash("Passwords do not match", "error")
        return render_template('signup_page.html')
    elif User.get('email', email):
        flash('Email already taken by another user', 'error')
        return render_template('signup_page.html')

    user = User(first_name=first_name, last_name=last_name, middle_name=middle_name, email=email,
                password=generate_password_hash(password=password), is_active=True)
    user.save()
    return redirect(url_for(endpoint='auth.login_page'))
