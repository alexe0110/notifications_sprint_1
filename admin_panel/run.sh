#!/usr/bin/env bash

gunicorn --bind 0.0.0.0:8000  --log-level INFO --access-logfile=- 'main:app'