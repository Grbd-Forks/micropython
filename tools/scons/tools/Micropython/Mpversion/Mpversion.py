"""
This tool will generate a micropython version header
"""

import sys
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder


def exists(env):
    return True


def generate(env):
    cmd = '"' + sys.executable + '" ${PY_SRC}/makeversionhdr.py ${TARGET}'
    act = [__Output_func, SCons.Action.Action(cmd)]
    bld = env.Builder(
        action=act,
        suffix=".E",
        src_suffix=".c")
    env.AppendUnique(BUILDERS={'Mpversion': bld})


def __Output_func(target, source, env):
    print("Make Version Header {0}".format(str(target[0])))
