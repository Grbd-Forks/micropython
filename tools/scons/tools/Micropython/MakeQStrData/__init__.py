"""
If the user requests "micropython.tools.scons.MakeQStrData" then this will call this script as a tool
In which case we include all the builders / methods
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import MakeQStrData


def generate(env):
    MakeQStrData.generate(env)


def exists(env):
    if not MakeQStrData.exists(env):
        return False
    return True
