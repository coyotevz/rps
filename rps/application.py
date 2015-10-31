# -*- coding: utf-8 -*-

import locale
locale.setlocale(locale.LC_ALL, '')


from flask import Flask, request, make_response

from rps.models import configure_db
from rps.views import configure_views


DEFAULT_APPNAME = 'rioplomo-sorteo'


def create_app(config=None, app_name=None):

    if app_name is None:
        app_name = DEFAULT_APPNAME

    #app = Flask(app_name, static_folder=None)
    app = Flask(__name__)

    configure_app(app, config)
    configure_db(app)
    configure_views(app)

    return app

def configure_app(app, config=None):

    if config is not None:
        app.config.from_object(config)
    else:
        try:
            app.config.from_object('localconfig.LocalConfig')
        except ImportError:
            app.config.from_object('rps.config.DevelopmentConfig')
