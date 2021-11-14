#! /usr/bin/env bash
set -e

python /app/app/consumers/systemworker_wait_for_db.py

faust -A app.consumers.system_worker worker -l info
