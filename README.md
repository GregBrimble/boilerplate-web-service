# Boilerplate Web Service
A bare minimum web service deployment by [Greg Brimble](https://gregbrimble.com).

## Dependencies
* Python3.6.3
* pip3

## Setup
1. Clone this repository to wherever you want to deploy.
2. `$ pip3 install virtualenv`
3. Run `./setup.sh` to build dependencies into `venv`, set `git remote upstream` to point to this repository.

## Features

### Authentication
This service can be protected by the following services:

#### Google
In `passenger_wsgi.py`, protect the application by doing the following:
```python
from flask import Flask
from auth.google import GoogleAuthentication

application = Flask(__name__)

my_google_authenticator = GoogleAuthentication(application)
```

Optionally, in `GoogleAuthentication()`, pass in:
* `whitelist=True` to protect all endpoints by default.
* `domain=gregbrimble.com` for example, to restrict the authenticated Google account domain.

Use the following to protect an endpoint:
```python
@application.route("/secret")
@my_google_authenticator.login_required
def secret():
  return "You're authenticated!"
```

and when using `whitelist=True`, the following to make an endpoint exempt from authentication:
```python
@application.route("/")
@my_google_authenticator.login_exempt
def index():
  return "Hello, world!"
```

#### Sentinel ([flask-sentinel](https://github.com/pyeve/flask-sentinel))
In `passenger_wsgi.py`, protect the application by doing the following:
```python
from flask import Flask
from auth.sentinel import SentinelAuthentication

application = Flask(__name__)

my_sentinel_authenticator = SentinelAuthentication(application)
```

Just as with `GoogleAuthentication()`, optionally pass in `whitelist=True` to protect all endpoints by default.

And again, similarly to `GoogleAuthentication()`, use the following to protect an endpoint:
```python
@application.route("/secret")
@my_sentinel_authenticator.login_required
def secret():
  return "You're authenticated!"
```

and when using `whitelist=True`, the following to make an endpoint exempt from authentication:
```python
@application.route("/")
@my_sentinel_authenticator.login_exempt
def index():
  return "Hello, world!"
```
