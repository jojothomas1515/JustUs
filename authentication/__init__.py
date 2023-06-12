from flask.blueprints import Blueprint
auth_views = Blueprint('authentication', __name__, url_prefix='/auth',
                       template_folder='templates', static_folder='static', static_url_path='/')
from authentication.login_signup import *
