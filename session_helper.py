import logging

from flask import session
import git

logging.basicConfig(level=logging.DEBUG)

def check_session_version():

    app_version = git.Repo(search_parent_directories=True).head.object.hexsha

    try:
        assert session.get('app_version') == app_version
    except (KeyError, AssertionError):
        logging.info("Session is out of date with app version. Clearing...")
        session.clear()
        session['app_version'] = app_version
