import datetime
import hashlib
import hmac
import json
import logging
import os
import threading

from flask import abort, Blueprint, jsonify, request

from upgrader import upgrade

meta = Blueprint('meta', __name__)

auto_deploy_method = os.getenv('WS_AUTO_DEPLOY')


@meta.route("/")
def statistics():
    # TODO: Refactor, and if possible, have dynamic status for inprogress updates.

    try:
        last_update_timestamp = os.path.getctime("tmp/restart.txt")
    except OSError:
        last_update_timestamp = 0

    try:
        last_build_timestamp = os.path.getctime("venv")
    except OSError:
        last_build_timestamp = 0

    return jsonify(
        last_update_time=datetime.datetime.fromtimestamp(last_update_timestamp).isoformat(),
        last_build_time=datetime.datetime.fromtimestamp(last_build_timestamp).isoformat()
    )


def queueUpgrade(requirements_required):
    threading.Thread(target=upgrade, args=(requirements_required,)).start()
    if requirements_required:
        return "Upgrade queued, with requirements. Please note this may take several minutes to complete. You can see when the last complete upgrade was at GET /meta."
    else:
        return "Upgrade queued. You can see when the last complete upgrade was at GET /meta."


def verifyGitHubHook(request):
    header_signature = request.headers.get("X-Hub-Signature")
    secret = os.getenv('WS_AUTO_DEPLOY_GITHUB_HOOK_SECRET')
    if header_signature is None or secret is None:
        logging.error("GitHub Hook Secret is not set.")
        abort(403)
    else:
        header_signature = str(header_signature)
        secret = str(secret)

    sha_name, signature = header_signature.split("=")
    mac = hmac.new(secret, msg=request.data, digestmod=hashlib.sha1)

    if hmac.compare_digest(mac.hexdigest(), signature):
        logging.error("Bad GitHub Hook Secret Signature.")
        abort(403)
    else:
        if request.is_json():
            return request.get_json()
        else:
            logging.error("Bad GitHub Hook Post Data.")
            abort(400)


@meta.route("/github_hook", methods=["POST"])
def incomingGitHubHook():
    logging.critical(os.getenv("WS_AUTO_DEPLOY"))
    if auto_deploy_method != "GITHUB_HOOK":
        logging.error("GitHub Hook is not set as the automatic deployment method.")
        abort(403)

    if request.headers.get("X-GitHub-Event") == "ping":
        logging.debug("GitHub Hook Ping Event received. Ponging...")
        return "pong"
    elif request.headers.get("X-GitHub-Event") != "push":
        logging.error("Bad GitHub Hook Event received.")
        abort(501)

    payload = verifyGitHubHook(request)

    try:
        commits = payload['commits']
        requirements_required = False

        for commit in commits:
            if "requirements.txt" in commit['modified']:
                requirements_required = True
                break
    except KeyError:
        logging.error("Bad GitHub Hook Post Data.")
        abort(400)

    logging.debug("Queueing upgrade...")
    return queueUpgrade(requirements_required)
