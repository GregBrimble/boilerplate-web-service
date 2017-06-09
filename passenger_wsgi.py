import os
import sys

try:
    from flask import Flask, render_template, send_file, Response    
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
