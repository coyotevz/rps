# -*- coding: utf-8 -*-

from flask import Blueprint, url_for


## Front End

frontend = Blueprint('fontend', __name__)

@frontend.route('/')
def index():
    return "Working"


## Admin

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('')
def index_admin():
    return "Admin"


## Configure

def configure_views(app):
    app.register_blueprint(frontend)
    app.register_blueprint(admin)
