#! /usr/bin/env bash
set -e

python /app/app/celeryworker_pre_start.py

faust -A app.worker worker -l info
