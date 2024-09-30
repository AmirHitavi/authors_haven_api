#!/bin/bash

set -o errexit

set -o nounset

set -o pipefail

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

exec python manage.py runserver 0.0.0.0:8000