"""
If the user requests "micropython.tools.scons" then this will call this script as a tool
In which case we include all the builders
"""
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)

from . import MakeQStrData
from . import MakeQStrDefs
from . import MakeQStrPreprocess
from . import Mpversion
from . import Mpytool


def generate(env):
    MakeQStrData.generate(env)
    MakeQStrDefs.generate(env)
    MakeQStrPreprocess.generate(env)
    Mpversion.generate(env)
    Mpytool.generate(env)


def exists(env):
    if not MakeQStrData.exists(env):
        return False
    if not MakeQStrDefs.exists(env):
        return False
    if not MakeQStrPreprocess.exists(env):
        return False
    if not Mpversion.exists(env):
        return False
    if not Mpytool.exists(env):
        return False
    return True
