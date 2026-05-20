#!/usr/bin/env bash
set -euo pipefail

DB_HOSTNAME="${DB_HOSTNAME:-db-prod.phishsonar.com}"
DB_LOCAL_PORT="${DB_LOCAL_PORT:-25432}"
SKIP_DB_TUNNEL="${SKIP_DB_TUNNEL:-0}"
CLOUDFLARED_HOME="${CLOUDFLARED_HOME:-/home/nonroot}"
CLOUDFLARED_UID="${CLOUDFLARED_UID:-65532}"
CLOUDFLARED_GID="${CLOUDFLARED_GID:-65532}"

mkdir -p /root/.claude
mkdir -p "$CLOUDFLARED_HOME/.cloudflared"
chown -R "$CLOUDFLARED_UID:$CLOUDFLARED_GID" "$CLOUDFLARED_HOME/.cloudflared" 2>/dev/null || true
chmod 700 "$CLOUDFLARED_HOME/.cloudflared" 2>/dev/null || true

if [ "$SKIP_DB_TUNNEL" != "1" ]; then
  HOME="$CLOUDFLARED_HOME" gosu "$CLOUDFLARED_UID:$CLOUDFLARED_GID" cloudflared access tcp \
    --hostname "$DB_HOSTNAME" \
    --url "localhost:${DB_LOCAL_PORT}" \
    >/tmp/cloudflared-db.log 2>&1 &
  TUNNEL_PID=$!
  trap 'kill $TUNNEL_PID 2>/dev/null || true' EXIT

  for _ in $(seq 1 15); do
    nc -z localhost "$DB_LOCAL_PORT" && break
    sleep 1
  done

  if ! nc -z localhost "$DB_LOCAL_PORT"; then
    echo "skill-runner: DB tunnel to $DB_HOSTNAME failed to come up" >&2
    echo "--- cloudflared log (tail) ---" >&2
    tail -50 /tmp/cloudflared-db.log >&2
    exit 4
  fi
fi

exec "$@"
