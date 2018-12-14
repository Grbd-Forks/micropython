"""
This tool will generate a bin file from an elf file
"""

import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder


def exists(env):
    return True


def generate(env):
    env.SetDefault(OBJCOPY='objcopy')
    cmd = '${OBJCOPY} -O binary -j .isr_vector -j .text -j .data ${SOURCE} ${TARGET}'
    act = [__Output_func, SCons.Action.Action(cmd)]
    bld = env.Builder(
        action=act,
        suffix=".bin",
        src_suffix=".elf")
    env.AppendUnique(BUILDERS={'Elf2Bin': bld})


def __Output_func(target, source, env):
    print("LINK {0}".format(str(target[0])))
