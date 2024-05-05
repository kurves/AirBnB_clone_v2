#!/usr/bin/python3
"""sscript to configure server"""


from fabric import task
from datetime import datetime
import os

@task
def do_pack(c):
    """script to configure server"""
    c.run('mkdir -p versions')

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    archive_name = f"web_static_{timestamp}.tgz"

    archive_path = os.path.join("versions", archive_name)

    result = c.local(f'tar -czvf {archive_path} web_static')

    if result.failed:
        return None
    else:
        return archive_path
