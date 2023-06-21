#!/usr/bin/env python
from flask.blueprints import Blueprint

auth_views = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates', static_folder='static',
                       static_url_path='/')
users_views = Blueprint('user', __name__, url_prefix='/users', template_folder='templates', static_folder='static',
                        static_url_path='/')
from user.login_signup import *
from user.views import *
