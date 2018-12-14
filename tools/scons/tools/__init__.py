"""
If the user requests "micropython.tools.scons" then this will call this script as a tool
In which case we include all the builders
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import General
from . import Micropython


def generate(env):
    General.generate(env)
    Micropython.generate(env)


def exists(env):
    if not General.exists(env):
        return False
    if not Micropython.exists(env):
        return False
    return True
