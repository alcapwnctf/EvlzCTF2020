#!/usr/bin/env sh
caddy start --config /Caddyfile
python /app/create_admin.py
python /app/admin_visit.py &
