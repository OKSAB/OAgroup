#!/usr/bin/env bash
# Stop Gunicorn + Nginx
echo "→ Stopping Gunicorn …"
kill "$(cat /tmp/oagroup_gunicorn.pid 2>/dev/null)" 2>/dev/null && echo "  stopped" || echo "  (not running)"

echo "→ Stopping Nginx …"
sudo /opt/homebrew/bin/nginx -s stop 2>/dev/null && echo "  stopped" || echo "  (not running)"
