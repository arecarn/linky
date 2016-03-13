"""
Sets up the dotfiles in this repository

Requires python 3
"""

import sys
import os
import shutil

from dploy.util import resolve_abs_path

def link_file(target, dest):
    dest_dir = os.path.dirname(dest)
    # get a relative path to the target from the destination location of
    # the file, this way we will have a relative symlink
    target_relative = os.path.relpath(target, start=dest_dir)

    try:
        os.symlink(target_relative, dest)
        print("Link: {dest} => {target}".format(target=target, dest=dest))
    except Exception as exception_message:
        print(exception_message)

def deploy_files(target, dest):
    target_absolute = resolve_abs_path(target)
    dest_absolute = resolve_abs_path(dest)

    if os.path.islink(dest_absolute):
        link_location = os.readlink(dest_absolute)
        if resolve_abs_path(os.readlink(dest_absolute)) == target_absolute:
            print("Link: Already Linked {dest} => {target}".format(target=target,
                                                                   dest=dest))
        else:
            print("Abort: Dest Is A Link That Points To {link_location}".format(
                link_location=resolve_abs_path(link_location)))
    elif os.path.isfile(dest_absolute):
        print("Abort: file Already Exists")
    elif os.path.isdir(dest_absolute):
        for file in os.listdir(target_absolute):
            link_file(os.path.join(target_absolute, file),
                      os.path.join(dest_absolute, file))
    else:
        os.makedirs(os.path.dirname(dest_absolute), exist_ok=True)
        link_file(target_absolute, dest_absolute)
