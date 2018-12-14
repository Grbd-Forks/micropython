"""
If the user requests "micropython.tools.scons.BinDFU" then this will call this script as a tool
In which case we include all the builders
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import BinDFU

def generate(env):
    BinDFU.generate(env)

def exists(env):
    if not BinDFU.exists(env):
        return False
    return True
