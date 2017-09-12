#!/bin/bash
rm -rf venv tmp
virtualenv -p python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
git remote add upstream git@github.com:GregBrimble/boilerplate-web-service.git
