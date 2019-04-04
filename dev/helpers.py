#!/usr/bin/env python3
# author: Gabriel Auger
# version: 3.3.0
# name: release
# license: MIT
import os, shlex, sys

# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
# import modules.shell_helpers.shell_helpers as shell
# import modules.message.message as msg
# del sys.path[0:2]


from ..modules.shell_helpers import shell_helpers as shell
from ..modules.message import message as msg

def is_pkg_git(path=""):
    start_path=""
    git_directory_found=False

    if path:
        if os.path.exists(path):
            start_path=os.getcwd()
            os.chdir(path)
        else:
            return False

    if shell.cmd_devnull("git rev-parse --git-dir") == 0:
        git_directory_found=True

    if path:
        os.chdir(start_path)

    if not git_directory_found:
        return False
    else:
        return True

def to_be_coded(text=""):
    if not text:
        msg.app_error("To be coded")
    else:
        msg.app_error("To be coded: '{}'".format(text))
    sys.exit(1)