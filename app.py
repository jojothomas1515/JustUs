#!/usr/bin/env python
"""This is the main entry point for the application."""
from flask import Flask
from authentication import auth_views

import os
app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
app.register_blueprint(auth_views)
print(os.getenv('JUSTUS_USER', None))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
