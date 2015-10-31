# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template


## Front End

frontend = Blueprint('fontend', __name__)

@frontend.route('/')
def index():
    return render_template('base.html')


## Admin

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('')
def index_admin():
    return "Admin"


## Configure

def configure_views(app):
    app.register_blueprint(frontend)
    app.register_blueprint(admin)

    @app.context_processor
    def template_helpers():

        def static(filename):
            return url_for('static', filename=filename)

        return dict(static=static)
