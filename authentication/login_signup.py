from flask import render_template, request
from werkzeug.security import generate_password_hash, check_password_hash

from authentication import auth_views


@auth_views.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login_page():
    email = request.form.get('email')
    password = request.form.get('password')
    ans = generate_password_hash(password)
    print(request.form)
    print(ans)
    print(check_password_hash(ans, password))
    return render_template('login_page.html')


@auth_views.route('/signup', strict_slashes=False, methods=['GET', 'POST'])
def signup_page():
    return render_template('signup_page.html')


@auth_views.route('/reset_password', strict_slashes=False, methods=['GET', 'POST'])
def password_reset():
    pass
