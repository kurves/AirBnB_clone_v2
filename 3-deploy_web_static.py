#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers using the function deploy.
"""

from fabric import task
from os import path

# Define web server IPs
env.hosts = ['xx.xx.xx.xx', 'xx.xx.xx.xx']  # Replace xx.xx.xx.xx with actual IPs

@task
def deploy(c):
    """
    Creates and distributes an archive to web servers.

    Parameters:
        c: Connection object to run remote commands using Fabric.

    Returns:
        Returns the return value of do_deploy if successful, otherwise False.
    """
    # Call the do_pack() function and store the path of the created archive
    archive_path = do_pack()

    # Return False if no archive has been created
    if not archive_path:
        print("Failed to create archive.")
        return False

    # Call the do_deploy(archive_path) function
    return do_deploy(c, archive_path)

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        If the archive is generated successfully, returns the path to the archive.
        Otherwise, returns None.
    """
    # Import required modules here
    from datetime import datetime
    import os

    # Create the versions directory if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Get the current date and time
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # Name of the archive
    archive_name = f"web_static_{timestamp}.tgz"

    # Path to the archive
    archive_path = os.path.join("versions", archive_name)

    # Compress web_static folder into a .tgz archive
    result = os.system(f'tar -czvf {archive_path} web_static')

    # Check if the archive has been correctly generated
    if result != 0:
        return None
    else:
        return archive_path

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
