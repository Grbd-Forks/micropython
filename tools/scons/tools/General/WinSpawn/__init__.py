"""
If the user requests "micropython.tools.scons.WinSpawn" then this will call this script as a tool
In which case we include all the builders
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import WinSpawn


def generate(env):
    WinSpawn.generate(env)


def exists(env):
    if not WinSpawn.exists(env):
        return False
    return True
