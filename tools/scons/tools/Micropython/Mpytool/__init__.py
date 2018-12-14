"""
If the user requests "micropython.tools.scons.Mpytool" then this will call this script as a tool
In which case we include all the builders
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import MpytoolDump
from . import MpytoolFreeze

def generate(env):
    MpytoolDump.generate(env)
    MpytoolFreeze.generate(env)

def exists(env):
    if not MpytoolDump.exists(env):
        return False
    if not MpytoolFreeze.exists(env):
        return False
    return True
