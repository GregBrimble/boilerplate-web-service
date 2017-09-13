# Must be run as venv/bin/python

import logging
from os import getenv, makedirs, utime
from os.path import dirname
from shutil import rmtree
from subprocess import check_call, CalledProcessError

import git


# Variables
# TODO: Document

restarting_file_location = getenv('RESTARTING_FILE_LOCATION', 'tmp/restart.txt')
github_remote_origin_name = getenv('GITHUB_REMOTE_ORIGIN_NAME', 'origin')
github_remote_upstream_name = getenv('GITHUB_REMOTE_UPSTREAM_NAME', 'upstream')

try:
    repository = git.Repo('.')
    repository.remotes[github_remote_origin_name]
except git.exc.InvalidGitRepositoryError as e:
    logging.error("Git repository `%s` does not exist." % e)
except IndexError:
    logging.error("Git remote `%s` does not exist." % github_remote_origin_name)


# Helpers

def _restart_server():
    logging.info('Restarting server...')
    makedirs(dirname(restarting_file_location), exist_ok=True)
    with open(restarting_file_location, 'a'):
        utime(restarting_file_location, None)
    return True

def _install_requirements():
    try:
        check_call(['pip', 'install', '-r', 'requirements.txt'])
    except CalledProcessError:
        logging.warning("Could not install requirements.")
        return False
    return True

def _git_pull():
    try:
        repository.remotes[github_remote_origin_name].pull()
    except git.exc.GitCommandError:
        logging.error("Could not pull from git remote `%s`" % repository.remotes[github_remote_origin_name].url)
        return False
    return True


# Public functions

def upgrade(requirements_required=False):
    """
    Pull from `origin/master`, and restart the server. Optionally, install requirements as well.
    """
    if requirements_required:
        logging.info("Upgrading with requirements...")
    else:
        logging.info("Upgrading without requirements...")

    _git_pull()
    if requirements_required:
        _install_requirements()
    _restart_server()

    logging.info("Upgrade complete.")
    return True
