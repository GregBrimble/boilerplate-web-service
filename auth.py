import os

from flask import abort, current_app, g, redirect, request, url_for
from flask_dance.contrib.google import google, make_google_blueprint

# Exemption from `require_authentication()`
def login_exempt(f):
    f.login_exempt = True
    return f

def require_api_authentication():

    # Exempt from requiring authentication
    view = current_app.view_functions.get(request.endpoint)
    if getattr(view, 'login_exempt', False) or request.endpoint in ["google.login", "google.authorized"]:
        return

    if not google.authorized:
        abort(403)

    return

def require_browser_authentication():

    # Exempt from requiring authentication
    view = current_app.view_functions.get(request.endpoint)
    if getattr(view, 'login_exempt', False) or request.endpoint in ["google.login", "google.authorized"]:
        return

    if not google.authorized:
        return redirect(url_for("google.login"))

    return


def register_google_blueprint(application, whitelist=False, api_mode=False):
    application.register_blueprint(
        make_google_blueprint(
            client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
            scope=["profile", "email"]
        ),
        url_prefix="/login"
    )

    if whitelist:
        if api_mode:
            application.before_request(require_api_authentication)
        else:
            application.before_request(require_browser_authentication)
