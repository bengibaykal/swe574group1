#!/bin/bash
export WORKSPACE=`pwd`
virtualenv venv
source venv/bin/activate

# Install Requirements
pip install -r requirements.txt
# Run tests
python manage.py test