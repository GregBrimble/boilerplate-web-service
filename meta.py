import datetime
import hashlib
import hmac
import json
import os
import threading

from flask import abort, Blueprint, request

from upgrader import build, update
from config import config

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


def verifyGitHubHook(request):
    header_signature = request.headers.get("X-Hub-Signature")
    if header_signature is None:
        abort(403)

    secret = config.get("github_hook", "secret")

    sha_name, signature = header_signature.split("=")
    mac = hmac.new(str(secret), msg=request.data, digestmod=hashlib.sha1)

    if str(mac.hexdigest()) != str(signature):
        abort(403)
    else:
        try:
            return request.get_json()
        except:     # TODO: Be more specific
            abort(400)


@meta.route("/github_hook", methods=["POST"])
def incomingGitHubHook():
    if request.headers.get("X-GitHub-Event") != "push":
        abort(501)

    payload = verifyGitHubHook(request)

    buildRequired = False

    commits = payload['commits']
    for commit in commits:
        if "requirements.txt" in commit['modified']:
            buildRequired = True

    if buildRequired:
        return queueBuild()
    else:
        return queueUpdate()
