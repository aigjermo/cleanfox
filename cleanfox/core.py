#!/usr/bin/env python3
"""
Manage a set of disposable firefox profiles
"""

import os
import sys
import shutil
import tempfile
import subprocess
import xdg.BaseDirectory as bd

_APP_NAME = 'cleanfox'
_BROWSER_CMD = 'firefox'

_XDG_DATA = bd.save_data_path(_APP_NAME)
_BASE_PROFILE = os.path.join(_XDG_DATA, 'base-profile')

def _init_base_profile():
    """
    Create the profile to use as a basis for all others
    """
    args = [_BROWSER_CMD, '-CreateProfile', 'cleanfox '+_BASE_PROFILE]
    subprocess.call(args)

def _spawn_base_profile():
    """
    launch the base profile for setup purposes
    """
    args = [_BROWSER_CMD, '-no-remote', '-profile', _BASE_PROFILE]
    subprocess.call(args)

def _get_profile_path(name=None):
    """
    Load a profile path

    Unnamed profiles are initialized in a temporary directory
    Named profiles are created unless they already exist
    """
    if name:
        path = os.path.join(_XDG_DATA, 'profile-'+name)
        directory = None
    else:
        directory = tempfile.TemporaryDirectory(prefix=_APP_NAME + "-")
        path = os.path.join(directory.name, 'profile')

    if not os.path.exists(path):
        shutil.copytree(_BASE_PROFILE, path)

    return path, directory

def _get_profiles():
    """
    get a list of all named profiles
    """
    return [a[8:] for a in os.listdir(path=_XDG_DATA) if a[0:8] == 'profile-']


class Profile:
    """
    profile object
    """
    def __init__(self, name=None):

        self.name = name
        self.path, self.directory = _get_profile_path(self.name)

    def __enter__(self):
        return self

    def __exit__(self, _type, value, traceback):
        if self.directory:
            self.directory.cleanup()

    def spawn(self):
        """
        launch the browser with this profile
        """
        args = [_BROWSER_CMD, '-no-remote', '-profile', self.path]
        subprocess.call(args)
        return self

    def destroy(self):
        """
        delete the profile
        """
        shutil.rmtree(self.path)

def action(args):
    """
    Parse arguments and trigger appropriate action
    """
    cmd = args[1] if len(args) > 1 else "spawn"
    arg = args[2] if len(args) > 2 else None

    if cmd in ['base', 'template']:
        _spawn_base_profile()
        return

    if cmd in ['spawn', 'launch', 'open']:
        with Profile(arg) as prf:
            prf.spawn()
        return

    if cmd == 'list':
        for entry in _get_profiles():
            print(entry)
        return

    if cmd == 'delete' and arg:
        with Profile(arg) as prf:
            prf.destroy()
            print("deleted profile: {:s}".format(prf.name))
        return

    #default
    print("usage: {:s} [cmd] [name]".format(args[0]))

def script_entry():
    """
    Run action with args from command line
    """
    action(sys.argv)

if not os.path.exists(_BASE_PROFILE):
    _init_base_profile()

if __name__ == '__main__':
    script_entry()
