import re
import subprocess
from os import path

# Import the scons environment from the calling script
Import('env')


# Just to give a bit a bit of detail on typically how qstr works
# https://forum.micropython.org/viewtopic.php?t=3211
# QSTR is a mechanism for string interning. It basically lets you replace a string with a number.
# it saves some flash size, saves memory, it speeds up comparisons

#  * Read in source files from SRC_MOD, PY_CORE_SRCS, PY_EXTMOD_SRCS
#    Parse them to a file ./build/genhdr/qstr.i.last

#  * Take the file ./build/genhdr/qstr.i.last
#    Parse it to the ./build/genhdr/qstr directory as a bunch of files

#  * Take the files from the ./build/genhdr/qstr directory
#    Parse them into ./build/genhdr/qstrdefs.collected.h

#  * Read in ./build/genhdr/qstrdefs.collected.h, ${QSTR_DEFS}, ${TOP}/py/qstrdefs.h
#    Parse into ./build/genhdr/qstrdefs.preprocessed.h

#  * Read in ./build/genhdr/qstrdefs.preprocessed.h
#    Parse to ./build/genhdr/qstrdefs.generated.h

# When building the final micropython exe
# qstrdefs.generated.h is used to reference system strings (not specific to the port)
# Also qstrdefs.preprocessed.h is used by the mpy tool when generating mpy files
# (python files precompiled down to bytecode)

# Default options
env.SetDefault(QSTR_AUTOGEN_DISABLE='0')

# If qstr autogeneration is not disabled we specify the output header
# for all collected qstrings.
if env['QSTR_AUTOGEN_DISABLE'] != "1":
    env.Replace(QSTR_DEFS_COLLECTED='${HEADER_BUILD}/qstrdefs.collected.h')

# Any files listed by this variable will cause a full regeneration of qstrs
env.AppendUnique(QSTR_GLOBAL_DEPENDENCIES=
    env.Split("${PY_SRC}/mpconfig.h mpconfigport.h"))

# file containing qstr defs for the core Python bit
env.Replace(PY_QSTR_DEFS='${PY_SRC}/qstrdefs.h')

# Setup SRC_QSTR, the builder will add in any missing extensions
srclist = env['SRC_MOD']
srclist += env['PY_CORE_SRCS']
srclist += env['PY_EXTMOD_SRCS']

# Filter out 'py/nlr'
srclist_copy = list(srclist)
for item in srclist_copy:
    if str(item).startswith(path.normpath('py/nlr')):
        srclist.remove(item)
env.Replace(SRC_QSTR=srclist)

# Build qstr.i.last
env.AppendUnique(QSTR_GEN_EXTRA_CFLAGS='-DNO_QSTR')
srcs = env.AddPrefix('${TOP}/', env['SRC_QSTR'])
qstr_env = env.Clone()
qstr_env.AppendUnique(CFLAGS='${QSTR_GEN_EXTRA_CFLAGS}')

tgt = qstr_env.PreProcessBuild('${HEADER_BUILD}/qstr.i.last', srcs)
env.Requires(tgt, ['${QSTR_GLOBAL_DEPENDENCIES}', '${HEADER_BUILD}/mpversion.h'])
# This is picked up from qstr.h but results in a circular depend
env.Ignore(tgt, '${HEADER_BUILD}/qstrdefs.generated.h')


# split qstr.i.last into the qstr directory
tgt = env.MakeQStrDefs_Split(env.Dir('${HEADER_BUILD}/qstr'), '${HEADER_BUILD}/qstr.i.last')

# Build ${QSTR_DEFS_COLLECTED} / qstrdefs.collected.h
tgt = env.MakeQStrDefs_Join('${QSTR_DEFS_COLLECTED}', env.Dir('${HEADER_BUILD}/qstr'))


# qstr data
# Note: we need to protect the qstr names from the preprocessor, so we wrap
# the lines in "" and then unwrap after the preprocessor is finished.
tgt = env.MakeQStrPreprocess('${HEADER_BUILD}/qstrdefs.preprocessed.h',
    ['${PY_QSTR_DEFS}', '${QSTR_DEFS}', '${QSTR_DEFS_COLLECTED}'])
env.Requires(tgt, ['mpconfigport.h', '${PY_SRC}/mpconfig.h'])

# Generate qstrdefs.generated.h from qstrdefs.preprocessed.h
tgt = env.MakeQStrData('${HEADER_BUILD}/qstrdefs.generated.h', '${HEADER_BUILD}/qstrdefs.preprocessed.h')
