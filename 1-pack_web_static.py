#!/usr/bin/python3
"""Create compressed archives of the web_static directory."""

from datetime import datetime
from fabric.api import local


def do_pack():
    """Create a timestamped .tgz archive of the web_static directory."""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    try:
        local("mkdir -p versions")
        result = local(
            "tar -czf {} web_static".format(archive_path)
        )

        if result.failed:
            return None

        return archive_path

    except Exception:
        return None
