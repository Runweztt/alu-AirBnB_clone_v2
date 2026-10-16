#!/usr/bin/env bash
# Configure Nginx and folders required to serve AirBnB static content.

sudo apt-get update -y >/dev/null 2>&1 || true
sudo apt-get install -y nginx >/dev/null 2>&1 || true

sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

printf '%s\n' "Holberton School" | \
    sudo tee /data/web_static/releases/test/index.html >/dev/null

sudo rm -f /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

NGINX_CONF="/etc/nginx/sites-available/default"

if ! sudo grep -q "location /hbnb_static/" "$NGINX_CONF"; then
    sudo sed -i '/server_name _;/a\
        location /hbnb_static/ {\
            alias /data/web_static/current/;\
        }' "$NGINX_CONF"
fi

sudo nginx -t >/dev/null 2>&1 && \
    sudo service nginx restart >/dev/null 2>&1 || true

exit 0
