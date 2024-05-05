#!/usr/bin/python3
from fabric import task
from datetime import datetime
import os
from fabric.api import local, run, env, mkdir

def do_pack():
  """
  Generates a .tgz archive of the web_static folder content.

  Returns:
      str: Path to the generated archive or None on failure.
  """
  now = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
  archive_name = f"versions/web_static_{now}.tgz"
  run("mkdir -p versions", quiet=True)

  with local.capture("tar -czf {archive_name} ./web_static") as output:
    if output.failed:
      print(f"Error creating archive: {output}")
      return None
    return archive_name

