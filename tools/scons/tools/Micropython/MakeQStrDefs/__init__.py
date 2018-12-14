"""
If the user requests "micropython.tools.scons.MakeQStrDefs" then this will call this script as a tool
In which case we include all the builders / methods
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import MakeQStrDefs_Split
from . import MakeQStrDefs_Join


def generate(env):
    MakeQStrDefs_Split.generate(env)
    MakeQStrDefs_Join.generate(env)


def exists(env):
    if not MakeQStrDefs_Split.exists(env):
        return False
    if not MakeQStrDefs_Join.exists(env):
        return False
    return True
