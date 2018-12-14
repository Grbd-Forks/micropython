"""
This tool will preprocess the qstr data
"""

import sys
import re
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder


def exists(env):
    return True


def generate(env):
    bld = env.Builder(
        action=__Build_func,
        suffix=".h")
    env.AppendUnique(BUILDERS={'MakeQStrPreprocess': bld})


# qstr data
# Note: we need to protect the qstr names from the preprocessor, so we wrap
# the lines in "" and then unwrap after the preprocessor is finished.
def __Build_func(env, target, source):
    print("GEN: {0}".format(str(target[0])))
    # Read / cat all sources
    tmpstr = ""
    for src in source:
        with open(src.abspath, 'r') as f:
            tmpstr += f.read()

    # sed replace
    regex = re.compile(r"(^Q\(.*\))", re.MULTILINE)
    tmpstr = regex.sub(r'"\1"', tmpstr)

    # pipe through the compiler
    tmpstr, errstr = env.PreProcessStream(tmpstr)

    # sed replace
    regex = re.compile(r'^"(Q\(.*\))"', re.MULTILINE)
    tmpstr = regex.sub(r'\1', tmpstr)

    # Output to target
    with open(target[0].abspath, "w") as f:
        f.write(tmpstr)
