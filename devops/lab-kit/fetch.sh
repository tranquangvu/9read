#!/usr/bin/env bash
# Download the lab kit into ./clinic-app:   bash fetch.sh https://<this-site>/devops/lab-kit
set -euo pipefail
BASE="${1:?usage: fetch.sh <base-url-of-lab-kit>}"
FILES="README.md compose.yaml booking-api/package.json booking-api/server.js booking-api/healthcheck.js booking-api/Dockerfile
booking-worker/package.json booking-worker/worker.js booking-worker/Dockerfile
booking-web/index.html booking-web/nginx.conf booking-web/Dockerfile"
for f in $FILES; do mkdir -p "clinic-app/$(dirname "$f")"; curl -fsSL "$BASE/$f" -o "clinic-app/$f"; echo "got $f"; done
echo "done: cd clinic-app && docker compose up --build"
