"""
This tool will Split a header into QStr files
Typically from qstr.i.last
"""

import sys
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder


def exists(env):
    return True


def generate(env):
    # Because of the way the called script is written for split mode
    # we just need a dummy entry for the last parameter
    # only the first two parameters are used for split
    env.SetDefault(MakeQStrDefs_Script="${TOP}/py/makeqstrdefs.py")
    cmd = '"' + sys.executable + '" ${MakeQStrDefs_Script} split ${SOURCE} ${TARGET} None'
    act = [__Output_func, SCons.Action.Action(cmd)]
    bld = env.Builder(
        action=act,
        suffix=".E",
        src_suffix=".c")
    env.AppendUnique(BUILDERS={'MakeQStrDefs_Split': bld})


def __Output_func(target, source, env):
    print("SPLIT {0} into {1}".format(str(source[0]), str(target[0])))
