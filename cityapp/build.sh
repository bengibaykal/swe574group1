#!/bin/bash
export WORKSPACE=`pwd`
python3.6 -m venv testenv
source testenv/bin/activate

# Install Requirements
pip3 install -r ../requirements.txt
# Run tests
python3 manage.py test