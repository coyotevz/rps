# -*- coding: utf-8 -*-

"""
    rps.commands
    ~~~~~~~~~~~~
"""

from flask.ext.script import Manager, Shell, Command, Option, prompt_bool
from flask.ext.script.commands import Clean, ShowUrls

from rps.application import create_app
from rps.models import db


manager = Manager(create_app)

@manager.command
def initdb():
    """Creates all database tables"""
    print("Database:", db.engine.url)
    db.create_all()
    print("All tables created")

@manager.command
def dropdb():
    """Drops all database tables"""
    print("Database:", db.engine.url)
    if prompt_bool("Are you sure ? You will lose all your data!"):
        db.drop_all()
        print("All tables dropped")

def shell_make_context():
    from flask import current_app
    from datetime import datetime
    from decimal import Decimal
    return dict(
        app=current_app,
        db=db,
        Decimal=Decimal,
        datetime=datetime,
    )

manager.add_command("shell", Shell(make_context=shell_make_context))
manager.add_command("clean", Clean())
manager.add_command("show-urls", ShowUrls())

class GunicornServer(Command):
    "Run the app within Gunicorn"

    def __init__(self, host='127.0.0.1', port=8000, workers=4):
        self.port = port
        self.host = host
        self.workers = workers

    def get_options(self):
        return (
            Option('-H', '--host', dest='host', default=self.host),
            Option('-p', '--port', dest='port', default=self.port),
            Option('-w', '--workers', dest='workers', default=self.workers),
        )

    def run(self, host, port, workers):
        from flask import current_app
        try:
            from gunicorn import version_info
        except ImportError:
            import sys
            sys.exit("You must have installed gunicorn to run this command")

        if version_info < (0, 9, 0):
            print("We can't run this yet")
        else:
            from gunicorn.app.base import Application

            class FlaskApplication(Application):
                def init(self, parser, options, args):
                    return {
                        'bind': '{0}:{1}'.format(host, port),
                        'workers': workers,
                    }

                def load(self):
                    return current_app

            FlaskApplication().run()

manager.add_command("gunicorn", GunicornServer())

def main():
    manager.run()
