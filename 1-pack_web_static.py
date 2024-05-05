from fabric import task
from datetime import datetime
import os

@task
def do_pack(c):
    # Create the versions directory if it doesn't exist
    c.run('mkdir -p versions')

    # Get the current date and time
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # Name of the archive
    archive_name = f"web_static_{timestamp}.tgz"

    # Path to the archive
    archive_path = os.path.join("versions", archive_name)

    # Compress web_static folder into a .tgz archive
    result = c.local(f'tar -czvf {archive_path} web_static')

    # Check if the archive has been correctly generated
    if result.failed:
        return None
    else:
        return archive_path
