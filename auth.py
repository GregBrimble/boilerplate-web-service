import os

from flask import abort, current_app, g, redirect, request, url_for
from flask_dance.contrib.google import google, make_google_blueprint
import requests

g_api_mode = False
g_domain = None


def require_domain():
    global g_domain

    response = google.get("/plus/v1/people/me")
    if response.status_code != requests.codes.ok:
        abort(502)

    # Assert the user is a part of Administrate
    try:
        if response.json()['domain'] != g_domain:
            abort(403)
    except KeyError:
        abort(403)

    return


# Exemption from `require_authentication()`
def login_exempt(f):
    f.login_exempt = True
    return f


def require_authentication():
    global g_api_mode

    # Exempt from requiring authentication
    view = current_app.view_functions.get(request.endpoint)
    if getattr(view, 'login_exempt', False) or request.endpoint in ["google.login", "google.authorized"]:
        return

    if not google.authorized:
        if g_api_mode:
            abort(403)
        else:
            return redirect(url_for("google.login"))

    return


def register_google_blueprint(application, whitelist=False, api_mode=False, domain=None):

    application.register_blueprint(
        make_google_blueprint(
            client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
            scope=["profile", "email"]
        ),
        url_prefix="/login"
    )

    if whitelist:
        global g_api_mode
        g_api_mode = api_mode

        application.before_request(require_authentication)

        global g_domain
        g_domain = domain

        if g_domain:
            application.before_request(require_domain)
