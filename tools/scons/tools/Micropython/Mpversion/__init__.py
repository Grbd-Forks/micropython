"""
If the user requests "micropython.tools.scons.Mpversion" then this will call this script as a tool
In which case we include all the builders / methods
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import Mpversion


def generate(env):
    Mpversion.generate(env)


def exists(env):
    if not Mpversion.exists(env):
        return False
    return True
