"""
This tool will Join QStr files into a single header
Typically into qstrdefs.collected.h
"""

import sys
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder


def exists(env):
    return True


def generate(env):
    # Because of the way the called script is written for join / cat mode
    # we just need a dummy entry for the first parameter - None
    # only the last two parameters are used for join / cat
    env.SetDefault(MakeQStrDefs_Script="${TOP}/py/makeqstrdefs.py")
    cmd = '"' + sys.executable + '" ${MakeQStrDefs_Script} cat None ${SOURCE} ${TARGET}'
    act = [__Output_func, SCons.Action.Action(cmd)]
    bld = env.Builder(
        action=act,
        emitter = modify_targets)
    env.AppendUnique(BUILDERS={'MakeQStrDefs_Join': bld})


def __Output_func(target, source, env):
    print("JOIN {0} into {1}".format(str(source[0]), str(target[0])))


def modify_targets(target, source, env):
    target.append(env.File(target[0].abspath + '.hash'))
    return target, source
