#!/usr/bin/env bash
# Start OA Group in production mode (Gunicorn + Nginx)
set -e

PROJECT="/Users/School/Desktop/Omarwebsite/OAgroup"
cd "$PROJECT"

echo "→ Starting Gunicorn on 127.0.0.1:8001 …"
venv/bin/gunicorn oagroup.wsgi:application \
  --config deploy/gunicorn.conf.py \
  --daemon \
  --pid /tmp/oagroup_gunicorn.pid

echo "→ Starting Nginx …"
sudo /opt/homebrew/bin/nginx

echo ""
echo "✓ OA Group is live at https://oalamoudi.com"
echo "  (Make sure oalamoudi.com is in /etc/hosts → see deploy/README.md)"
