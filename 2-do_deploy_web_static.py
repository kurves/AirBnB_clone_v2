#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers using the function do_deploy.
"""

from fabric import task
from os import path

# Define web server IPs
env.hosts = ['xx.xx.xx.xx', 'xx.xx.xx.xx']  # Replace xx.xx.xx.xx with actual IPs

@task
def do_deploy(c, archive_path):
    """
    Distributes an archive to web servers.

    Parameters:
        c: Connection object to run remote commands using Fabric.
        archive_path: Path to the archive to be deployed.

    Returns:
        True if all operations are successful, otherwise False.
    """
    # Check if the archive exists
    if not path.exists(archive_path):
        print("Archive doesn't exist.")
        return False

    # Upload the archive to the /tmp/ directory of the web server
    archive_name = path.basename(archive_path)
    remote_archive_path = f'/tmp/{archive_name}'
    c.put(archive_path, remote_archive_path)

    # Uncompress the archive to /data/web_static/releases/<archive filename without extension>
    folder_name = archive_name.split('.')[0]
    release_path = f'/data/web_static/releases/{folder_name}'
    c.run(f'mkdir -p {release_path}')
    c.run(f'tar -xzf {remote_archive_path} -C {release_path}')

    # Delete the archive from the web server
    c.run(f'rm {remote_archive_path}')

    # Delete the symbolic link /data/web_static/current
    c.run('rm -rf /data/web_static/current')

    # Create a new symbolic link /data/web_static/current linked to the new version
    c.run(f'ln -s {release_path} /data/web_static/current')

    return True

