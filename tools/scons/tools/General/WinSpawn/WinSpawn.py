"""
In some cases when running a windows command shell with a command string longer than 8191 characters
This can cause issues with windows platforms

This tool will modify the default spawn process function called by scons
to use subprocess directly without a shell.

Basic redirection is supported such as > >> and < for standard input and output.
Although more advanced redirection such as 1>stdout 2>stderr etc is not supported

Based on code from:
https://github.com/SCons/scons/wiki/LongCmdLinesOnWin32
"""

import sys
import subprocess
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder
from random import randint


def exists(env):
    return True


def generate(env):
    env.AddMethod(WinSpawn, 'WinSpawn')


def WinSpawn(env):
    if sys.platform == 'win32':
        env['SPAWN'] = __winspawn
    return


def __winspawn(sh, escape, cmd, args, env):

    # Handle redirections without the shell
    # This is mostly for windows environments that have limited size on the command line shell
    # So we don't need to implement 1>out etc just basic >, >>, < redirection

    args1 = args[1:]

    # Used to get around the following error when launching python 3.7 as an executable
    # b'Fatal Python error: _Py_HashRandomization_Init: failed to get random numbers to initialize Python\n\n'
    if 'PYTHONHASHSEED' not in env:
        env['PYTHONHASHSEED'] = str(randint(0, 4294967294))

    args1, stdout_file = __popredirect(args1, '>', 'wb')
    if not stdout_file:
        args1, stdout_file = __popredirect(args1, '>>', 'wb')
    args1, stdin_file = __popredirect(args1, '<', 'rb')
    argstr = ' '.join(args1)
    cmdline = cmd + ' ' + argstr

    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        proc = subprocess.Popen(cmdline, stdin=stdin_file, stdout=stdout_file,
            stderr=subprocess.PIPE, startupinfo=startupinfo, shell = False, env = env)
        data, err = proc.communicate()
        rv = proc.wait()

    finally:
        if stdout_file:
            stdout_file.close()
        if stdin_file:
            stdin_file.close()

    if rv:
        print("=====")
        print(err)
        print("=====")
    return rv


def __popredirect(args, symbl, mode):
    fhandle = None
    retargs = list(args)
    for idx, val in enumerate(args):
        if val == symbl:
            file_name = args[idx + 1].strip('\"')
            fhandle = open(file_name, mode)
            del retargs[idx:(idx + 2)]
            break
    return retargs, fhandle
