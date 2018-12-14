"""
This tool will add a prefix to a string or an array of strings/dir/file/entry

There are 2 ways to use this tool

1. value = env.AddPrefix('prefixtest/', 'testpath3')
   value = env.AddPrefix('prefixtest/', ['testpath2', 'testpath3'])

returns a string with the prefix added
the first parameter represents the prefix, the second can be an array or single item.

With this variant of the tool no path seperator is added automatically.
This way this can be used for non path values.

2. env.AddPrefix(VAR='prefix/')
adds a prefix to each item within env['VAR'] and replaces the value within env.
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
    env.AddMethod(AddPrefix, 'AddPrefix')


def AddPrefix(env, prefix=None, source=None, **kw):

    # Handle AddPrefix in the form val = env.AddPrefix('prefix', files)
    # In this form kw is empty, and prefix / source are used
    if prefix is not None and source is not None:
        return __parse_param(env, prefix, source)

    # Handle AddPrefix in the form env.AddPrefix(VAR='prefix')
    # In this form only kw is used
    __parse_kw(env, kw)
    return


def __parse_param(env, prefix, source):
    ret = []
    if type(source) is not list:
        source = [source]
    for item in source:
        ret += [__parse_item(env, prefix, item)]
    if len(ret) == 1:
        ret = ret[0]
    return ret


def __parse_kw(env, kw):
    for item in kw.items():
        envname = item[0]
        prefix = item[1]
        oldval = env[envname]
        if type(oldval) is list:
            newval = []
            for listitem in oldval:
                newval += [__parse_item(env, prefix, listitem)]
        else:
            newval = __parse_item(env, prefix, oldval)
        env.Replace(**{envname: newval})
    return


def __parse_item(env, prefix, source):
    ret = str(prefix) + str(source)
    if type(source) is Entry:
        ret = env.Entry(ret)
    elif type(source) is File:
        ret = env.File(ret)
    elif type(source) is Dir:
        ret = env.Dir(ret)
    return ret
