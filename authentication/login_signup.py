from flask import render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required
from authentication import auth_views
from models.user import User
import datetime as dt


@auth_views.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login_page():
    user = current_user
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('login') is True

        user: User = User.get('email', email)
        if not user:
            flash("Email not associated with any account", "error")
            return render_template('login_page.html')
        if check_password_hash(user.password, password):
            if login_user(user=user, remember=remember, duration=dt.timedelta(days=7)):
                return str(user.__dict__)
            print(login_user(user=user, remember=remember, duration=dt.timedelta(days=7)))
            if not user.is_active:
                flash("Inactive user", "error")
            else:
                flash("Error occurred while trying to log in", "error")
            return render_template("login_page.html")

    return render_template('login_page.html')


@auth_views.route('/signup', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def signup_page():
    if session.get('logged_in'):
        return session.get("username")
    if request.method == 'POST':
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
                    password=generate_password_hash(password=password))
        user.save()
        return redirect(url_for(endpoint='authentication.login_page'))

    return render_template('signup_page.html')


@auth_views.route('/reset_password', strict_slashes=False, methods=['GET', 'POST'])
def password_reset():
    pass
