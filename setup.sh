#!/bin/bash
git pull
rm -rf venv tmp
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
deactivate
mkdir tmp
touch tmp/restart.txt
