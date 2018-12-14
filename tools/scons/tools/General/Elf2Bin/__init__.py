"""
If the user requests "micropython.tools.scons.Elf2Bin" then this will call this script as a tool
In which case we include all the builders
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import Elf2Bin

def generate(env):
    Elf2Bin.generate(env)

def exists(env):
    if not Elf2Bin.exists(env):
        return False
    return True
