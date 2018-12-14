"""
If the user requests "micropython.tools.scons.AddPrefix" then this will call this script as a tool
In which case we include all the builders
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import AddPrefix


def generate(env):
    AddPrefix.generate(env)


def exists(env):
    if not AddPrefix.exists(env):
        return False
    return True
