import binascii
import logging
import os
import subprocess
import sys
import threading

# Try to import all requirements
try:
    from flask import Flask, abort, current_app, request, redirect, url_for
    import flask_login
    from flask_restless import APIManager
    from flask_sslify import SSLify
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from flask_wtf import FlaskForm
    import wtforms_components

    import requests

    from meta import meta
    from auth.google import google, GoogleAuthentication
    from auth.sentinel import SentinelAuthentication
except ImportError:
    # If it fails, we must not be in the virtual environment. Let's move there...
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
sslify = SSLify(application)

application.register_blueprint(meta, url_prefix="/meta")

# my_google_authenticator = GoogleAuthentication(application, whitelist=True)
# my_sentinel_authenticator = SentinelAuthentication(application, whitelist=True)


@application.route("/")
# @my_google_authenticator.login_exempt
# @my_sentinel_authenticator.login_exempt
def index():
    return "Hello, world!"


@application.route("/secret")
# @my_google_authenticator.login_required
# @my_sentinel_authenticator.login_required
def secret():
    return "Hello, secret!"

if __name__ == "__main__":
    application.run()
