#!/usr/bin/env bash
# script to configure server for deployment

if ! dpkg -s nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

sudo mkdir -p /data/web_static/{releases/test,shared}

echo "Fake content" | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

nginx_config="
server {
    listen 80;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
    }

    location / {
        return 404;
    }
}
"
sudo bash -c "echo '$nginx_config' > /etc/nginx/sites-available/default"

sudo service nginx restart
