"""
If the user requests "micropython.tools.scons.MakeQStrPreprocess" then this will call this script as a tool
In which case we include all the builders / methods
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import MakeQStrPreprocess


def generate(env):
    MakeQStrPreprocess.generate(env)


def exists(env):
    if not MakeQStrPreprocess.exists(env):
        return False
    return True
