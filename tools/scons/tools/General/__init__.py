"""
If the user requests "micropython.tools.scons" then this will call this script as a tool
In which case we include all the builders
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)
from . import AddPrefix
from . import Bin2DFU
from . import Elf2Bin
from . import ExecutePipe
from . import PreProcess
from . import ReplaceExtension
from . import WinSpawn


def generate(env):
    AddPrefix.generate(env)
    Bin2DFU.generate(env)
    Elf2Bin.generate(env)
    ExecutePipe.generate(env)
    PreProcess.generate(env)
    ReplaceExtension.generate(env)
    WinSpawn.generate(env)

def exists(env):
    if not AddPrefix.exists(env):
        return False
    if not Bin2DFU.exists(env):
        return False
    if not Elf2Bin.exists(env):
        return False
    if not ExecutePipe.exists(env):
        return False
    if not PreProcess.exists(env):
        return False
    if not ReplaceExtension.exists(env):
        return False
    if not WinSpawn.exists(env):
        return False
    return True
