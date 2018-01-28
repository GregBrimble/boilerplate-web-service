import binascii
import os
import sys

from flask import Flask
from flask_sslify import SSLify

from auth.google import GoogleAuthentication
from auth.sentinel import SentinelAuthentication


app = Flask(__name__)

# Load the environment variables into application configuration dictionary
app.secret_key = os.getenv("SECRET_KEY", binascii.hexlify(os.urandom(24)))
app.config['SENTINEL_MONGO_URI'] = os.getenv("SENTINEL_MONGO_URI")
app.config['SENTINEL_REDIS_URL'] = os.getenv("SENTINEL_REDIS_URL")
app.config['REDIS_URL'] = os.getenv("SENTINEL_REDIS_URL")

sslify = SSLify(app)

# my_google_authenticator = GoogleAuthentication(application, whitelist=True)
# my_sentinel_authenticator = SentinelAuthentication(application, whitelist=True)

# client = OAuth2Session(client=LegacyApplicationClient(os.getenv("OAUTH_CLIENT_ID")))
# token = client.fetch_token(token_url=os.getenv("OAUTH_TOKEN_URL", username=os.getenv("OAUTH_USERNAME"), password=os.getenv("OAUTH_PASSWORD"), client_id=os.getenv("OAUTH_CLIENT_ID")))


@app.route("/")
# @my_google_authenticator.login_exempt
# @my_sentinel_authenticator.login_exempt
def index():
    return "Hello, world!"


@app.route("/secret")
# @my_google_authenticator.login_required
# @my_sentinel_authenticator.login_required
def secret():
    return "Hello, secret!"


if __name__ == "__main__":
    app.run()
