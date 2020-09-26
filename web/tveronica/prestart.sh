#!/usr/bin/env sh
caddy start --config /Caddyfile
/opt/scripts/ingest-redis.sh
