"""
If the user requests "micropython.tools.scons.ExecutePipe" then this will call this script as a tool
In which case we include all the builders
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import ExecutePipe


def generate(env):
    ExecutePipe.generate(env)


def exists(env):
    if not ExecutePipe.exists(env):
        return False
    return True
