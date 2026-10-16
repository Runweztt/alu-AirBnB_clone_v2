#!/usr/bin/python3
"""Create and deploy an archive of AirBnB static web files."""

import os
from datetime import datetime
from fabric.api import env, local, put, run, settings


env.hosts = [
    "44.201.123.60",
    "18.233.154.155"
]

env.user = "ubuntu"


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


def do_deploy(archive_path):
    """Deploy an archive to both configured AirBnB web servers."""
    if not os.path.isfile(archive_path):
        return False

    archive_name = os.path.basename(archive_path)
    release_name = archive_name[:-4]
    remote_archive = "/tmp/{}".format(archive_name)
    release_path = "/data/web_static/releases/{}/".format(
        release_name
    )

    with settings(warn_only=True):
        result = put(archive_path, remote_archive)
        if result.failed:
            return False

        result = run("mkdir -p {}".format(release_path))
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

        result = run("rm -f {}".format(remote_archive))
        if result.failed:
            return False

        result = run(
            "cp -a {0}web_static/. {0}".format(
                release_path
            )
        )
        if result.failed:
            return False

        result = run(
            "rm -rf {}web_static".format(
                release_path
            )
        )
        if result.failed:
            return False

        result = run("rm -rf /data/web_static/current")
        if result.failed:
            return False

        result = run(
            "ln -s {} /data/web_static/current".format(
                release_path
            )
        )
        if result.failed:
            return False

    print("New version deployed!")
    return True


def deploy():
    """Create a new archive and deploy it to both web servers."""
    archive_path = do_pack()

    if archive_path is None:
        return False

    return do_deploy(archive_path)
