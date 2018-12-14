"""
This tool will generate a dfu file from a bin file
"""

import sys
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder


def exists(env):
    return True


def generate(env):
    env.SetDefault(DFU_Script="${TOP}/tools/dfu.py")
    cmd = '"' + sys.executable + '" ${DFU_Script} -b 0x08000000:${SOURCE} ${TARGET}'
    act = [__Output_func, SCons.Action.Action(cmd)]
    bld = env.Builder(
        action=act,
        suffix=".dfu",
        src_suffix=".bin")
    env.AppendUnique(BUILDERS={'Bin2DFU': bld})


def __Output_func(target, source, env):
    print("DFU {0}".format(str(target[0])))
