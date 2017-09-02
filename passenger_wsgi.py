import os
import subprocess
import sys
import threading

from meta import meta

try:
    from flask import Flask
    import flask_login
    from flask_restless import APIManager
    from flask_sqlalchemy import SQLAlchemy
    import requests
except ImportError:
    INTERP = "venv/bin/python"

    if os.path.relpath(sys.executable, os.getcwd()) != INTERP:
        try:
            os.execl(INTERP, INTERP, *sys.argv)
        except OSError:
            sys.exit("Could not find virtual environment. Run `:~$ ./setup.sh`")
    else:
        sys.exit("Could not find requirements. Are they all included in requirements.txt? Run `:~$ ./setup.sh`")


application = Flask(__name__)
application.register_blueprint(meta, url_prefix="/meta")


@application.route("/")
def index():
    return "Hello, world!"




@application.route("/meta/big_update")
def bigUpdate():
    subprocess.call(['./setup.sh'])
    return "Please restart."


if __name__ == "__main__":
    application.run()
