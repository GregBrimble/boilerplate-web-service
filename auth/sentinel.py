import logging

from flask import abort, current_app, jsonify, redirect, request, url_for
from flask_sentinel import ResourceOwnerPasswordCredentials, oauth

from auth.base import Protection

# TODO: Write the documentation for this
class SentinelAuthentication(Protection):

    # Sets up the Sentinel login blueprint with the flask application
    # Optionally whitelists every endpoint, other than those marked as exempt (see `login_exempt()`)
    def __init__(self, application, whitelist=False):

        self.whitelisted = whitelist

        ResourceOwnerPasswordCredentials(application)

        application.before_request(self.authentication)


    def protected_endpoint(self):
        return (request.endpoint in ["management"]) or (request.path in ["/oauth/token"])


    def authentication(self):

        if not self.protected_endpoint():
            view = current_app.view_functions.get(request.endpoint)

            if self.whitelisted:
                # If view is @login_exempt, or they are logged in, return view
                if not getattr(view, 'login_exempt', False):
                    current_app.view_functions[request.endpoint] = oauth.require_oauth()(view)

            else:
                # If view is @login_required, and they are not logged in, return "google.login"
                if getattr(view, 'login_required', False):
                    current_app.view_functions[request.endpoint] = oauth.require_oauth()(view)

        return
