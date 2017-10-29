import binascii
import logging
import os
import subprocess
import sys
import threading

try:
    from flask import Flask, abort, current_app, request, redirect, url_for
    import flask_login
    from flask_restless import APIManager
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from flask_wtf import FlaskForm

    import requests

    from celery import Celery

    from meta import meta
    from auth import login_exempt, register_google_blueprint
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
application.secret_key = os.getenv("SECRET_KEY", binascii.hexlify(os.urandom(24)))

application.register_blueprint(meta, url_prefix="/meta")

register_google_blueprint(application, whitelist=True, api_mode=False, domain="administrate.co")


@application.route("/")
def index():
    return "Hello, world!"


if __name__ == "__main__":
    application.run()
