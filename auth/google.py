import os

from flask import abort, current_app, redirect, request, url_for
from flask_dance.contrib.google import google, make_google_blueprint
import requests


class GoogleAuthentication:

    domain = None
    application = None

    # Sets up the Google login blueprint with the flask application
    # Optionally set `oauth_client_id`, `oauth_client_secret`, `redirect_url`, manually
    # Optionally whitelists every endpoint
    # Optionally restricts access to a certain domain
    def __init__(self, application, oauth_client_id=None, oauth_client_secret=None, redirect_url=None, whitelist=False, domain=None):

        self.domain = domain
        self.application = application

        application.register_blueprint(
            make_google_blueprint(
                client_id=(os.getenv("GOOGLE_OAUTH_CLIENT_ID") if oauth_client_id is None else oauth_client_id),
                client_secret=(os.getenv("GOOGLE_OAUTH_CLIENT_SECRET") if oauth_client_secret is None else oauth_client_secret),
                redirect_url=redirect_url,
                scope=["profile", "email"]
            ),
            url_prefix="/login"
        )

        if whitelist:
            application.before_request(self.whitelist_authentication)

        if domain:
            application.before_request(self.require_domain)


    # Exemption from `require_authentication()`
    def login_exempt(self, f):
        f.login_exempt = True
        return f


    def whitelist_authentication(self):

        # Exempt from requiring authentication
        view = current_app.view_functions.get(request.endpoint)
        if getattr(view, 'login_exempt', False) or request.endpoint in ["google.login", "google.authorized"]:
            return

        if not google.authorized:
            return redirect(url_for("google.login"))

        return


    def require_domain(self):

        # Exempt from requiring authentication
        view = current_app.view_functions.get(request.endpoint)
        if getattr(view, 'login_exempt', False) or request.endpoint in ["google.login", "google.authorized"]:
            return

        response = google.get("/plus/v1/people/me")
        if response.status_code != requests.codes.ok:
            abort(502)

        # Assert the user has the domain
        # TODO: Prompt to re-login with a different user.
        try:
            if response.json()['domain'] != self.domain:
                abort(403)
        except KeyError:
            abort(403)

        return
