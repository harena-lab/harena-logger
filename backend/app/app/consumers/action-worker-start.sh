#! /usr/bin/env bash
set -e

python /app/app/consumers/actionworker_wait_for_db.py

faust -A app.consumers.action_worker worker -l info
