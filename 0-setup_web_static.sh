#!/usr/bin/env bash
# Configure a web server for deployment of AirBnB static files.

sudo apt-get update -y
sudo apt-get install -y nginx

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

echo '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>' | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo rm -f /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

if ! sudo grep -q "location /hbnb_static/" \
    /etc/nginx/sites-available/default; then
    sudo sed -i '/server_name _;/a\
        location /hbnb_static/ {\
            alias /data/web_static/current/;\
        }' /etc/nginx/sites-available/default
fi

sudo service nginx restart

exit 0
