"""
If the user requests "micropython.tools.scons.ReplaceExtension" then this will call this script as a tool
In which case we include all the builders
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import ReplaceExtension


def generate(env):
    ReplaceExtension.generate(env)


def exists(env):
    if not ReplaceExtension.exists(env):
        return False
    return True
