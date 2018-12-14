import os.path as path
import sys

# Import the scons environment from the calling script
Import('env')

# Global Options
# Command Line / Default options, can be overridden within the script

# If to do a debug build of the code
AddOption('--debugbuild', dest='debugbuild', action="store_true", default=False, help='Do a debug build')
if GetOption('debugbuild'):
    env.SetDefault(DEBUG='1')
else:
    env.SetDefault(DEBUG='0')

# Top level source directory for micropython
AddOption('--topdir', dest='topdir', action="store", default='../..', help='Top level micropython source directory')
topdir = GetOption('topdir')
topdir = Dir(topdir)
env.SetDefault(TOP=topdir)

# If to give verbose output - TODO default value
AddOption('--verbose', dest='verbose', action="store_true", default=True, help='verbose output for build')
if GetOption('verbose'):
    env.SetOption('silent', False)
    env.SetDefault(BUILD_VERBOSE='1')
else:
    env.SetOption('silent', True)
    env.SetDefault(BUILD_VERBOSE='0')

# Build Directory output
AddOption('--builddir', dest='builddir', action="store", default='build', help='Build Directory')
builddir = GetOption('builddir')
builddir = Dir(builddir, directory = '#')
env.SetDefault(BUILD=builddir)

# If to force 32bit
AddOption('--force32bit', dest='force32bit', action="store_true", default=False, help='Force micropy to use 32bit')
if GetOption('force32bit'):
    env.SetDefault(MICROPY_FORCE_32BIT='1')
else:
    env.SetDefault(MICROPY_FORCE_32BIT='0')

# Overridable Script options
env.SetDefault(SRC_MOD=[])
env.SetDefault(CROSS_COMPILE='')
env.SetDefault(PROG='')

# Scons has it's own inbuilt system for scanning dependencies for .c / .h files
# However as an alternative we can use the dependency files outputed by gcc
# By setting SCANDEPFILES to True
# This can result in more rebuilding than is needed however
env.SetDefault(SCANDEPFILES=False)
if env['SCANDEPFILES']:
    env.MergeFlags('-MD')


# Compiler commands
env.Replace(AS='${CROSS_COMPILE}as')
env.Replace(CC='${CROSS_COMPILE}gcc')
env.Replace(CPP='${CROSS_COMPILE}gcc')
env.Replace(CXX='${CROSS_COMPILE}g++')
env.Replace(LD='${CROSS_COMPILE}ld')
env.Replace(OBJCOPY='${CROSS_COMPILE}objcopy')
env.Replace(SIZE='${CROSS_COMPILE}size')
env.Replace(STRIP='${CROSS_COMPILE}strip')
env.Replace(AR='${CROSS_COMPILE}ar')

if env['MICROPY_FORCE_32BIT'] == '1':
    env.MergeFlags('-m32')

# TODO
# Look into Alias function
# https://scons.org/doc/3.0.1/HTML/scons-user.html#app-functions
