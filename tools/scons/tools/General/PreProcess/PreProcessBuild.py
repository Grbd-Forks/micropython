"""
This tool will call gcc to do the preprocess stage only
typically this is gcc with the -E option
This is the builder form which takes an source / target file
"""

import sys
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder


def exists(env):
    return True


def generate(env):
    cmd = '${CPP} -E ${CFLAGS} ${CCFLAGS} ${_CCCOMCOM} ${SOURCES} >${TARGET}'
    act = [__Output_func, SCons.Action.Action(cmd)]
    bld = env.Builder(
        action=act,
        suffix=".E",
        src_suffix=".c")
    env.AppendUnique(BUILDERS={'PreProcessBuild': bld})


def __Output_func(target, source, env):
    print("PREPROCESS {0}".format(str(target[0])))
