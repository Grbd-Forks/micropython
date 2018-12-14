"""
This tool is similar to env.Execute
however it can return the output from stdout / stderr and feed a stdin to the called exe

There are 2 ways to use this tool

1. out, err = env.ExecutePipe('dir/something.exe')
   out, err = env.ExecutePipe('dir/something.exe', stdin='stream this to stdin')
   # For use in a builder for source / target substitution
   out, err = env.ExecutePipe('dir/something.exe $SOURCES $TARGET', stdin='stream this to stdin', target, source)

The out / err represent the stdout / stderr returned from the called command

2. env.ExecutePipe(VAR='dir/something.exe')

In this form the stdout is stored within the VAR variable inside scons construction environment
"""

import subprocess
import SCons.Script
import SCons.Subst
from SCons.Environment import Environment
from SCons.Script import Builder


def exists(env):
    return True


def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    env.AddMethod(ExecutePipe, 'ExecutePipe')


def ExecutePipe(env, cmdobj=None, stdin=None, target=None, source=None, **kw):

    # Handle ExecutePipe in the form val = env.ExecutePipe('cmdstr', target, source)
    # In this form kw is empty, and cmdobj / target / source are used
    if cmdobj is not None:
        return __executepipe(env, cmdobj, stdin, target, source)

    # Handle ExecutePipe in the form env.ExecutePipe(VAR='cmdstr')
    # In this form only kw is used
    __parse_kw(env, kw)
    return


def __executepipe(env, cmdstr, stdin=None, target=None, source=None):

    # Handle escaping / quoting variable expansion for paths with spaces in
    escape = env.get('ESCAPE', lambda x: x)
    escape_list = SCons.Subst.escape_list
    cmdarr = env.subst_list(cmdstr, SCons.Subst.SUBST_CMD)
    cmdarr = escape_list(cmdarr[0], escape)
    cmd = ' '.join(cmdarr)

    if isinstance(stdin, basestring):
        stdin = stdin.encode()

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=stdin)
    return out, err


def __parse_kw(env, kw):
    for item in kw.items():
        envname = item[0]
        cmdobj = item[1]
        out, err = __executepipe(env, cmdobj)
        env.Replace(**{envname: out})
    return
