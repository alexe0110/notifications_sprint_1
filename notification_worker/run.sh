#!/usr/bin/env bash

exec gunicorn -w 4 --bind 0.0.0.0:8008 --worker-class uvicorn.workers.UvicornWorker  --log-level INFO --access-logfile=- 'main:app'