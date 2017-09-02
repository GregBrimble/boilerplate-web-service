import os
import subprocess
import sys
import threading

try:
    from flask import Flask
    import flask_login
    from flask_restless import APIManager
    from flask_sqlalchemy import SQLAlchemy
    import requests

    from meta import meta
except ImportError:
    INTERP = "venv/bin/python"

    if os.path.relpath(sys.executable, os.getcwd()) != INTERP:
        try:
            os.execl(INTERP, INTERP, *sys.argv)
        except OSError:
            sys.exit("Environment not build. Run the following `:~$ python -c 'from upgrader import build; build();'`")
    else:
        sys.exit("Environment not build. Run the following `:~$ python -c 'from upgrader import build; build();'`")


application = Flask(__name__)
application.register_blueprint(meta, url_prefix="/meta")


@application.route("/")
def index():
    return "Hello, world!"


if __name__ == "__main__":
    application.run()
