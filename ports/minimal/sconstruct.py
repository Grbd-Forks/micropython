import os
import sys
import distutils.spawn
import SCons.Script
from SCons.Environment import Environment

EnsureSConsVersion(3, 0, 0)

# Setup the construction env
toolpaths = [Dir("../../tools/scons/tools").abspath]
tools = ['General', 'Micropython', 'gcc']
env = Environment(tools=tools, toolpath=toolpaths)

#env.Replace(ENV=os.environ)
env.Replace(ENV={'PATH': os.environ['PATH']})
# Needed for windows environments
if sys.platform == 'win32':
    env.AppendUnique(ENV={'SystemDrive': os.environ['SystemDrive']})
# Allow for running commands longer than 8191 characters under windows
env.WinSpawn()

# Global Options
SConscript('../../tools/scons/scons.opts.global.py', {'env': env})
# Local Options
env.SConscript('scons/scons.localopts.py', {'env': env})
# Setup local flags
env.SConscript('scons/scons.flags.py', {'env': env})
# Micropython build scripts
env.SConscript('../../tools/scons/scons.micropython.py', {'env': env})

# Local Sources

# Setup Sources
env.Replace(LIBS='')
env.Replace(LOCAL_C=env.Split("""
    main
    uart_core
    ${BUILD}/_frozen_mpy
"""))

env.Replace(TOP_C=env.Split("""
    lib/utils/printf
    lib/utils/stdout_helpers
    lib/utils/pyexec
    lib/libc/string0
    lib/mp-readline/readline
"""))

# Setup Rules / Alias's

# How to build _frozen_mpy.c
env.Replace(Mpytool_Qstrdefs='${BUILD}/genhdr/qstrdefs.preprocessed.h')
tgt = env.MpytoolFreeze('${BUILD}/_frozen_mpy.c', 'frozentest.mpy')
env.Requires('${BUILD}/_frozen_mpy.c', '${BUILD}/genhdr/qstrdefs.preprocessed.h')

# Specify that we need to build all local C files into objects
tgts = []
for item in env['TOP_C']:
    tgts += env.Object('${BUILD}/' + item, '${TOP}/' + item)
for item in env['LOCAL_C']:
    tgts += env.Object('${BUILD}/' + item, item)
env.Requires(tgts, '${BUILD}/genhdr/qstrdefs.generated.h')


# Build up a list of objects from micropython and locally
env.Replace(OBJ='${PY_CORE_O}')
env.AppendUnique(OBJ=tgts)

# Specify how to build the elf target
cmd1 = '${LD} ${LDFLAGS} -o ${TARGET} ${SOURCES}'
cmd2 = '${SIZE} $TARGET'
act = [SCons.Action.Action(cmd1), SCons.Action.Action(cmd2)]
elftgt = env.Command('${BUILD}/firmware.elf', env.subst_list('$OBJ')[0], act)

# How to Generate bin / dfu from the elf file
env.Elf2Bin('${BUILD}/firmware.bin', '${BUILD}/firmware.elf')
env.Bin2DFU('${BUILD}/firmware.dfu', '${BUILD}/firmware.bin')

# Set default target
if env['ARMBUILD']:
    env.Default('${BUILD}/firmware.dfu')
else:
    env.Default('${BUILD}/firmware.elf')


# TODO
# Alias:    "deploy"
# Depends:  ${BUILD}/firmware.dfu
# $(ECHO) "Writing $< to the board"
# $(Q)$(PYTHON) $(PYDFU) -u $<

# Run emulation build on a POSIX system with suitable terminal settings
# TODO
# Alias:    "run"
# Depends: ""
# stty raw opost -echo
# build/firmware.elf
# stty raw opost -echo
# build/firmware.elf
# @echo Resetting terminal...
# This sleep is useful to spot segfaults
# sleep 1
# reset

# TODO
# Alias:    "test"
# Depends:  ${BUILD}/firmware.elf
# $(Q)/bin/echo -e "print('hello world!', list(x+1 for x in range(10)), end='eol\\\\n')\\r\\n\\x04" | $(BUILD)/firmware.elf | tail -n2 | grep "^hello world! \\[1, 2, 3, 4, 5, 6, 7, 8, 9, 10\\]eol"
