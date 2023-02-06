#!/bin/sh
sleep 1 && poetry run python -m pyjail_ad.flag_worker &
sleep 1 && poetry run python -m pyjail_ad.patch_worker &
# poetry run flask --app pyjail_ad.app run
poetry run gunicorn -k gevent --bind 0.0.0.0:5000 pyjail_ad.app:app
trap "kill 0" EXIT
