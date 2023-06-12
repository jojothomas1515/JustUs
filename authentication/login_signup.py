from flask import render_template
from authentication import auth_views


@auth_views.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login_page():
    return render_template('login_page.html')

@auth_views.route('/signup', strict_slashes=False, methods=['GET', 'POST'])
def signup_page():
    return render_template('signup_page.html')


@auth_views.route('/reset_password', strict_slashes=False, methods=['GET', 'POST'])
def password_reset():
    pass
