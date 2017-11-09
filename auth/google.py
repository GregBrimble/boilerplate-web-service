import logging
import os

from flask import abort, current_app, redirect, request, url_for
from flask_dance.contrib.google import google, make_google_blueprint
from oauthlib.oauth2.rfc6749.errors import InvalidClientIdError, TokenExpiredError
import requests

from auth.base import Protection

# TODO: Write the documentation for this
class GoogleAuthentication(Protection):

    # Sets up the Google login blueprint with the flask application
    # Optionally set `oauth_client_id`, `oauth_client_secret`, manually
    # Optionally whitelists every endpoint, other than those marked as exempt (see `login_exempt()`)
    # Optionally restricts access to a certain domain
    def __init__(self, application, oauth_client_id=None, oauth_client_secret=None, whitelist=False, domain=None):

        self.domain = domain
        self.whitelisted = whitelist

        application.register_blueprint(
            make_google_blueprint(
                client_id=(os.getenv("GOOGLE_OAUTH_CLIENT_ID") if oauth_client_id is None else oauth_client_id),
                client_secret=(os.getenv("GOOGLE_OAUTH_CLIENT_SECRET") if oauth_client_secret is None else oauth_client_secret),
                scope=["profile", "email"]
            ),
            url_prefix="/login"
        )

        application.before_request(self.authentication)


    def protected_endpoint(self):
        return request.endpoint in ["google.login", "google.authorized"]


    def is_authorized(self):
        if google.authorized:
            if self.domain is not None:
                response = google.get("/plus/v1/people/me")
                if response.status_code != requests.codes.ok:
                    abort(502)

                try:
                    if response.json()['domain'] != self.domain:
                        abort(403)
                        return False
                except KeyError:
                    abort(403)
                    return False

            return True
        else:
            return False


    def authentication(self):

        if not self.protected_endpoint():
            view = current_app.view_functions.get(request.endpoint)

            # Pretty sure there is a bug in `flask_dance` which isn't expiring and auto-renewing oauth tokens, so...
            try:
                if self.whitelisted:
                    # If view is @login_exempt, or they are logged in, return view
                    if getattr(view, 'login_exempt', False) or self.is_authorized():
                        return
                    else:
                        return redirect(url_for("google.login"))

                else:
                    # If view is @login_required, and they are not logged in, return "google.login"
                    if getattr(view, 'login_required', False) and not self.is_authorized():
                        return redirect(url_for("google.login"))
                    else:
                        return
            except (InvalidClientIdError, TokenExpiredError):
                logging.warning("Token has probably expired...")
                redirect(url_for("google.login"))
