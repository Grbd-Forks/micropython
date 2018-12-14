"""
This tool will call gcc to do the preprocess stage only
typically this is gcc with the -E option
This is the method form which streams a string into gcc's standard input
and streams text out of gcc's standard output
"""

import sys
import subprocess
import SCons.Script
import SCons.Subst
from SCons.Environment import Environment
from SCons.Script import Builder


def exists(env):
    return True


def generate(env):
    env.AddMethod(PreProcessStream, 'PreProcessStream')


def PreProcessStream(env, stdin_str):
    # Handle escaping / quoting variable expansion
    escape = env.get('ESCAPE', lambda x: x)
    escape_list = SCons.Subst.escape_list

    cmdstr = '${CPP} -E ${CFLAGS} ${CCFLAGS} ${_CCCOMCOM} -'
    cmd_list = env.subst_list(cmdstr, SCons.Subst.SUBST_CMD)

    cmd_list = escape_list(cmd_list[0], escape)
    cmd = ' '.join(cmd_list)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=stdin_str.encode())
    return out, err
