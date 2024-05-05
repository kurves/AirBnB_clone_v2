#!/usr/bin/env bash
# script to configure server for deployment
from fabric import task

@task
def setup_web_static(c):
    # Install Nginx if not already installed
    c.sudo('apt-get update')
    c.sudo('apt-get install -y nginx')

    # Create necessary directories if they don't exist
    directories = [
        '/data/',
        '/data/web_static/',
        '/data/web_static/releases/',
        '/data/web_static/shared/',
        '/data/web_static/releases/test/'
    ]
    for directory in directories:
        c.sudo(f'mkdir -p {directory}')

    # Create fake HTML file
    c.sudo('echo "Fake content" | sudo tee /data/web_static/releases/test/index.html')

    # Create symbolic link
    c.sudo('rm -rf /data/web_static/current')
    c.sudo('ln -s /data/web_static/releases/test/ /data/web_static/current')

    # Give ownership of /data/ folder to ubuntu user and group
    c.sudo('chown -R ubuntu:ubuntu /data/')

    # Update Nginx configuration
    nginx_config = """
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
    """
    with c.sudo('bash -c "echo \'{}\' > /etc/nginx/sites-available/default"'.format(nginx_config)):
        pass

    # Restart Nginx
    c.sudo('service nginx restart')
