#!/usr/bin/env bash

uvicorn src.main:app --reload  --port 8000 --workers 2