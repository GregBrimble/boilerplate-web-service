import os
import subprocess
import sys

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


@application.route("/")
def index():
    return "Hello, world!"


@application.route("/update")
def update():
    subprocess.call(['git', 'fetch', 'origin'])
    subprocess.call(['git', 'pull'])
    try:
        subprocess.check_call(['mkdir', 'tmp'])
    except subprocess.CalledProcessError, e:
        pass
    subprocess.call(['touch', 'tmp/restart.txt'])
    return "Please restart."


@application.route("/big_update")
def bigUpdate():
    subprocess.call(['./setup.sh'])


if __name__ == "__main__":
    application.run()
