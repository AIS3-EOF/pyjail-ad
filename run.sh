#!/bin/sh
(trap - TERM; sleep 1 && poetry run python -m pyjail_ad.flag_worker) &
(trap - TERM; sleep 1 && poetry run python -m pyjail_ad.patch_worker) &
# poetry run flask --app pyjail_ad.app run
(trap - TERM; poetry run gunicorn -k gevent --bind 0.0.0.0:5000 pyjail_ad.app:app) &
trap "kill -TERM 0" TERM
while true; do sleep 1; done
