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

# Sources
env.Replace(LIBS='')
env.AppendUnique(SRCS_C=env.Split("""
    lib/utils/printf
    ports/unix/main
    ports/unix/file
    ports/unix/input
    ports/unix/modos
    ports/unix/modmachine
    ports/unix/modtime
    ports/unix/gccollect
    windows_mphal
    realpath
    init
    sleep
"""))

# Specify that we need to build all local C files into objects
tgts = []
for item in env['SRCS_C']:
    tgts += env.Object('${BUILD}/' + item, item)
env.Requires(tgts, '${BUILD}/genhdr/qstrdefs.generated.h')

# Add in Micropython targets
env.Replace(OBJ='${PY_O}')
env.AppendUnique(OBJ=tgts)

# default target
env.Program('${BUILD}/micropython.exe', '${OBJ}')
env.Default('${BUILD}/micropython.exe')



# TODO check these
# # compiler settings
# CFLAGS = -Wall -Wpointer-arith -Werror -std=gnu99 -DUNIX -D__USE_MINGW_ANSI_STDIO=1
# LDFLAGS = -lm
# LIB += -lws2_32

# TODO alter qstr base code
# List of sources for qstr extraction
# SRC_QSTR += $(SRC_C)

# TODO not found
# Append any auto-generated sources that are needed by sources listed in SRC_QSTR
# SRC_QSTR_AUTO_DEPS +=


# TODO

# Specify how to build the elf target
#cmd1 = '${LD} ${LDFLAGS} -o ${TARGET} ${SOURCES}'
#cmd2 = '${SIZE} $TARGET'
#act = [SCons.Action.Action(cmd1), SCons.Action.Action(cmd2)]
#elftgt = env.Command('${BUILD}/firmware.elf', env.subst_list('$OBJ')[0], act)
