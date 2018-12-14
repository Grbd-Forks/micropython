"""
This tool will generate QString Data
Typically qstrdefs.generated.h which is included into the main source of the firmware
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
    env.SetDefault(MakeQStrData_Script="${TOP}/py/makeqstrdata.py")
    cmd = '"' + sys.executable + '" ${MakeQStrData_Script} ${SOURCE} >${TARGET}'
    act = [__Output_func, SCons.Action.Action(cmd)]
    bld = env.Builder(
        action=act,
        suffix=".h",
        src_suffix=".h")
    env.AppendUnique(BUILDERS={'MakeQStrData': bld})


def __Output_func(target, source, env):
    print("GEN {0}".format(str(target[0])))
