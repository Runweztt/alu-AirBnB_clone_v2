#!/usr/bin/python3
"""Remove obsolete local and remote web_static releases."""

import glob
import os

from fabric.api import env, run, settings


env.hosts = [
    "44.201.123.60",
    "18.233.154.155"
]

env.user = "ubuntu"


def do_clean(number=0):
    """Keep only the requested number of most recent releases."""
    try:
        number = int(number)
    except (TypeError, ValueError):
        number = 0

    if number <= 1:
        keep = 1
    else:
        keep = number

    archives = sorted(
        glob.glob("versions/web_static_*.tgz"),
        reverse=True
    )

    for archive in archives[keep:]:
        try:
            os.remove(archive)
        except OSError:
            pass

    first_to_delete = keep + 1

    command = (
        "ls -1dt /data/web_static/releases/web_static_* "
        "2>/dev/null | tail -n +{} | xargs -r rm -rf"
    ).format(first_to_delete)

    with settings(warn_only=True):
        run(command)
