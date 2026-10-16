#!/usr/bin/python3
"""Create an archive of the AirBnB static web files."""

from datetime import datetime
from fabric.api import local


def do_pack():
    """Create and return a timestamped archive of web_static."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    try:
        local("mkdir -p versions")
        print("Packing web_static to {}".format(archive_path))
        result = local(
            "tar -cvzf {} web_static".format(archive_path)
        )

        if result.failed:
            return None

        return archive_path
    except Exception:
        return None
