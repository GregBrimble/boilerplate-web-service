import os
import subprocess
import sys
import threading

try:
    from flask import Flask
    import flask_login
    from flask_restless import APIManager
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from flask_wtf import FlaskForm

    import requests

    from celery import Celery

    from meta import meta
except ImportError:
    interpreter_location = "venv/bin/python"

    if os.path.relpath(sys.executable, os.getcwd()) != interpreter_location:
        try:
            print("Switching interpreter to `%s`..." % interpreter_location)
            os.execl(interpreter_location, interpreter_location, *sys.argv)
        except OSError:
            sys.exit("Virtual environment `%s` not found." % interpreter_location)
    else:
        sys.exit("Requirements not found in virtual environment `%s`" % interpreter_location)


application = Flask(__name__)
application.register_blueprint(meta, url_prefix="/meta")


@application.route("/")
def index():
    return "Hello, world!"


if __name__ == "__main__":
    application.run()
