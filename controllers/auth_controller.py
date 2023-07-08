#!/usr/bin/env python
"""Login controller."""
import datetime as dt

from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from models.db import Session
from models.user import User
from os import mkdir, path


def login():
    """Login user."""

    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember-me')

    sess = Session()
    user: User = sess.query(User).filter(User.email == email).first()
    if not user:
        flash("Email not associated with any account", "error")
    if check_password_hash(user.password, password):
        if login_user(user=user, remember=remember, duration=dt.timedelta(days=7)):
            sess.close()
            return redirect(url_for("home.home_page"))
        if not user.is_active:
            flash("Inactive user", "error")
        else:
            flash("Error occurred while trying to log in", "error")
    else:
        flash("Incorrect password", "error")
    sess.close()
    return render_template("login_page.html")


def signup():
    """Signup user."""
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    middle_name = request.form.get('middlename')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('c-password')

    sess = Session()
    if password != password2:
        flash("Passwords do not match", "error")
        sess.close()
        return render_template('signup_page.html')
    elif sess.query(User).filter(User.email == email).first():
        flash('Email already taken by another user', 'error')
        sess.close()
        return render_template('signup_page.html')

    user = User(first_name=first_name, last_name=last_name, middle_name=middle_name, email=email,
                password=generate_password_hash(password=password), is_active=True)
    sess.add(user)
    sess.commit()
    sess.close()
    return redirect(url_for(endpoint='auth.login_page'))


def update_profile():
    """Update Profile."""
    user: User = current_user
    user.first_name = request.form.get("first_name")
    user.last_name = request.form.get("last_name")
    user.middle_name = request.form.get("middle_name")
    sess = Session()
    sess.add(user)
    sess.commit()
    sess.close()
    return user


def update_profile_image():
    """Update profile image"""
    file = request.files.get("profile_img")
    if file:
        user: User = current_user
        if not user.is_authenticated:
            return jsonify(error="Unauthorized User")
        if not path.exists(f"./files/profile_images"):
            mkdir(f"./files/profile_images")
        filename = f"/files/profile_images/{user.id}.jpg"
        file.save(f".{filename}")
        # requests.post(url="http://web-02.jojothomas.tech/upload", files=file)
        user.profile_img = filename
        sess = Session()
        sess.add(user)
        sess.commit()
        sess.close()
        return user