"""
This tool will change the file extension on a string or an array of strings/file/entry

There are 2 ways to use this tool

1. val = env.ReplaceExtension('.o', '.c', 'test1.o')
   val = env.ReplaceExtension('.o', '.c', ['test1.o', 'test2', 'test3.exe'])

2. env.ReplaceExtension(TEST=['.o', '.c'])

the parameters are old extension, new extension, string or list of items
the old extension is optional in which case all items will have they're extension set
to the new extension parameter
"""


import sys
from os import path
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder
from SCons.Node.FS import Entry, Dir, File


def exists(env):
    return True


def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    env.AddMethod(ReplaceExtension, 'ReplaceExtension')


def ReplaceExtension(env, oldext=None, newext=None, source=None, **kw):

    # Handle ReplaceExtension in the form val = env.ReplaceExtension('oldext', 'newext', files)
    # In this form kw is empty, and prefix / source are used
    if newext is not None and source is not None:
        return __parse_param(env, oldext, newext, source)

    # Handle ReplaceExtension in the form env.ReplaceExtension(VAR={'oldext', 'newext'}})
    # In this form only kw is used
    __parse_kw(env, kw)
    return


def __parse_param(env, oldext, newext, source):
    ret = []
    if type(source) is not list:
        source = [source]
    for item in source:
        ret += [__parse_item(env, oldext, newext, item)]
    if len(ret) == 1:
        ret = ret[0]
    return ret


def __parse_kw(env, kw):
    for item in kw.items():
        envname = item[0]
        extensions = item[1]
        oldval = env[envname]

        if len(extensions) > 1:
            oldext = extensions[0]
            newext = extensions[1]
        else:
            oldext = None
            newext = extensions[0]

        if type(oldval) is list:
            newval = []
            for listitem in oldval:
                newval += [__parse_item(env, oldext, newext, listitem)]
        else:
            newval = __parse_item(env, oldext, newext, oldval)
        env.Replace(**{envname: newval})
    return


def __parse_item(env, oldext, newext, source):
    newext = str(newext)
    ret = str(source)
    pathsplit = path.splitext(ret)

    if oldext is not None:
        oldext = str(oldext)
        if len(pathsplit) > 1:
            if pathsplit[1] == oldext:
                ret = pathsplit[0] + newext
    else:
        ret = pathsplit[0] + newext

    if type(source) is Entry:
        ret = env.Entry(ret)
    elif type(source) is File:
        ret = env.File(ret)
    elif type(source) is Dir:
        ret = env.Dir(ret)
    return ret
