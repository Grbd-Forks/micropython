# Import the scons environment from the calling script
Import('env')

# Top Level Micropython build scipt
# Pull in all other global scripts from here

env.SConscript('scons.lib.micropy.py', {'env': env})
env.SConscript('scons.lib.qstr.py', {'env': env})
env.SConscript('scons.lib.frozen.py', {'env': env})

# Optional Libs
env.SConscript('scons.lib.btree.py', {'env': env})
env.SConscript('scons.lib.lwip.py', {'env': env})
env.SConscript('scons.lib.ussl.py', {'env': env})

# Util targets
env.SConscript('scons.util.py', {'env': env})
