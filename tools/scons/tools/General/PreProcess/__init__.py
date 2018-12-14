"""
If the user requests "micropython.tools.scons.PreProcess" then this will call this script as a tool
In which case we include all the builders / methods
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import PreProcessBuild
from . import PreProcessStream


def generate(env):
    PreProcessBuild.generate(env)
    PreProcessStream.generate(env)


def exists(env):
    if not PreProcessBuild.exists(env):
        return False
    if not PreProcessStream.exists(env):
        return False
    return True
