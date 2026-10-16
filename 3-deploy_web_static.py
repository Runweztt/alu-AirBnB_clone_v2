#!/usr/bin/python3
"""Create and deploy web_static archives to the web servers."""

import os
from datetime import datetime

from fabric.api import env, local, put, run, settings


env.hosts = [
    "44.201.123.60",
    "18.233.154.155"
]

env.user = "ubuntu"


def do_pack():
    """Create a timestamped archive of the web_static directory."""
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


def do_deploy(archive_path):
    """Deploy an archive to every configured web server."""
    if not os.path.exists(archive_path):
        return False

    archive_name = os.path.basename(archive_path)
    release_name = archive_name[:-4]

    remote_archive = "/tmp/{}".format(archive_name)
    release_path = "/data/web_static/releases/{}".format(
        release_name
    )

    with settings(warn_only=True):
        result = put(
            archive_path,
            remote_archive
        )

        if result.failed:
            return False

        result = run(
            "mkdir -p {}".format(release_path)
        )

        if result.failed:
            return False

        result = run(
            "tar -xzf {} -C {}".format(
                remote_archive,
                release_path
            )
        )

        if result.failed:
            return False

        result = run(
            "cp -a {0}/web_static/. {0}/ && "
            "rm -rf {0}/web_static".format(
                release_path
            )
        )

        if result.failed:
            return False

        result = run(
            "rm -f {}".format(remote_archive)
        )

        if result.failed:
            return False

        result = run(
            "rm -f /data/web_static/current"
        )

        if result.failed:
            return False

        result = run(
            "ln -s {} /data/web_static/current".format(
                release_path
            )
        )

        if result.failed:
            return False

    return True


def deploy():
    """Create a new archive and deploy it to all web servers."""
    archive_path = do_pack()

    if archive_path is None:
        return False

    return do_deploy(archive_path)
