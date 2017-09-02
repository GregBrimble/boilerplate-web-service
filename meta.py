import datetime
import json
import os

from flask import Blueprint

from upgrader import build, update

meta = Blueprint('meta', __name__)


@meta.route("/")
def stats():
    # TODO: Refactor, and if possible, have dynamic status for inprogress updates.

    try:
        last_update_timestamp = os.path.getctime("tmp/restart.txt")
    except OSError:
        last_update_timestamp = 0

    try:
        last_build_time = os.path.getctime("venv")
    except OSError:
        last_build_time = 0

    meta_info = {
        "last_update_time": datetime.datetime.fromtimestamp(last_update_timestamp).isoformat(),
        "last_build_time": datetime.datetime.fromtimestamp(last_build_time).isoformat()
    }
    return json.dumps(meta_info)


def queueUpdate():
    threading.Thread(target=update).start()
    return "Update queued. You can see when the last complete update was at GET /meta."


def queueBuild():
    threading.Thread(target=build).start()
    return "Build queued. Please note this takes many minutes to complete. Get yourself some tea. You can see when the last complete update was at GET /meta."
