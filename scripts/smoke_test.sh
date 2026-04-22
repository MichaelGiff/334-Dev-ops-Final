#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"
PORT="${PORT:-5050}"
HOST="127.0.0.1"
HEALTH_URL="http://${HOST}:${PORT}/health"
LOG_FILE="${TMPDIR:-/tmp}/recipe-recommender-smoke.log"

cleanup() {
    if [[ -n "${SERVER_PID:-}" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
        kill "$SERVER_PID"
        wait "$SERVER_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT

"$PYTHON_BIN" -m flask --app app run --host "$HOST" --port "$PORT" > "$LOG_FILE" 2>&1 &
SERVER_PID="$!"

for _ in {1..20}; do
    if curl -fsS "$HEALTH_URL"; then
        echo
        echo "Smoke test passed: ${HEALTH_URL}"
        exit 0
    fi
    sleep 1
done

echo "Smoke test failed: ${HEALTH_URL} did not respond."
echo "Server log:"
cat "$LOG_FILE"
exit 1
