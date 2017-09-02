import subprocess


# Helpers

def touchTmpRestart():
    # TODO: Add error catching
    subprocess.check_call(['mkdir', '-p', 'tmp'])
    subprocess.call(['touch', 'tmp/restart.txt'])
    return True


def gitFetchOriginAndPull():
    # TODO: Add error catching
    subprocess.call(['git', 'fetch', 'origin'])
    subprocess.call(['git', 'pull'])
    return True


def removeTemporaryFiles():
    # TODO: Add error catching
    subprocess.call(['rm', '-rf', 'venv', 'tmp'])
    return True


def buildVirtualEnv():
    # TODO: Add error catching
    subprocess.call(['./virtualenv_setup.sh'])      # TODO: Extract out
    return True


def removeGitUpstream():
    # TODO: Add error catching
    # TODO: Check if required first
    subprocess.call(['git', 'remote', 'rm', 'upstream'])
    return True


def addGitUpstream():
    # TODO: Add error catching
    subprocess.call(['git', 'remote', 'add', 'upstream', 'git@github.com:GregBrimble/boilerplate-web-service.git'])
    return True


# Public functions

def update():
    """
    Simply fetches origin/master, pulls the latest changes, and restarts the server.
    If any big changes have been made, it might not work (e.g. added a new dependancy).
    """
    gitFetchOriginAndPull()
    touchTmpRestart()
    return True


def build():
    """
    Fetches origin/master, pulls the latest changes, rebuilds the virtual environment (collecting new dependancies), and re-adds the upstream repo.
    """
    gitFetchOriginAndPull()
    removeTemporaryFiles()
    buildVirtualEnv()
    removeGitUpstream()
    addGitUpstream()
    return True
