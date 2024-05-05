#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers using the function do_deploy.
"""

from fabric import task
from os import path

env.hosts = ['107.22.66.180', '34.232.65.109']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


@task
def do_deploy(c, archive_path):
    """
    Distributes an archive to web servers.
    """
    if not path.exists(archive_path):
        print("Archive doesn't exist.")
        return False

    archive_name = path.basename(archive_path)
    remote_archive_path = f'/tmp/{archive_name}'
    c.put(archive_path, remote_archive_path)

    folder_name = archive_name.split('.')[0]
    release_path = f'/data/web_static/releases/{folder_name}'
    c.run(f'mkdir -p {release_path}')
    c.run(f'tar -xzf {remote_archive_path} -C {release_path}')

    c.run(f'rm {remote_archive_path}')

    c.run('rm -rf /data/web_static/current')

    c.run(f'ln -s {release_path} /data/web_static/current')

    return True
