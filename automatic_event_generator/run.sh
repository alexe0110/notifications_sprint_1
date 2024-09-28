#!/usr/bin/env bash

gunicorn -w 4 --bind 0.0.0.0:5000  --log-level INFO --access-logfile=- 'src.app:app'