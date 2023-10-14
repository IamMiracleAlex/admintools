#!/bin/bash
set -x
set -eu
set -o pipefail

pip3 install virtualenv
virtualenv ve
source ve/bin/activate
pip3 install -r requirements.txt
export ENVIRONMENT="staging_deployment"
python manage.py check
python manage.py test
npm install
npm run build
