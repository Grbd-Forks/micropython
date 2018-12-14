"""
This tool will freeze the bytecode?
"""

import sys
import SCons.Script
from . import common_opts
from SCons.Environment import Environment
from SCons.Script import Builder


def exists(env):
    return True


def generate(env):
    common_opts.setupopts(env)
    cmd = '"' + sys.executable + '" ${Mpytool_Script} -f '
    if 'Mpytool_Qstrdefs' in env:
        cmd += '-q "${Mpytool_Qstrdefs}" '

    cmd += '-mlongint-impl=none ${SOURCE} >${TARGET}'
    act = [__Output_func, SCons.Action.Action(cmd)]
    bld = env.Builder(
        action=act,
        suffix=".c",
        src_suffix=".mpy")
    env.AppendUnique(BUILDERS={'MpytoolFreeze': bld})


def __Output_func(target, source, env):
    print("Mpytool freezing bytecode {0}".format(str(target[0])))
