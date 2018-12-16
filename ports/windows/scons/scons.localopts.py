# Import the scons environment from the calling script
Import('env')

# Command line option if to use readline
AddOption('--readline', dest='micropy_use_readline', action="store_true", default=0, help='Build for an an ARM CPU')
env.SetDefault(MICROPY_USE_READLINE=GetOption('micropy_use_readline'))

if env['MICROPY_USE_READLINE'] == "1":
    env.MergeFlags('-DMICROPY_USE_READLINE=1')
    env.AppendUnique('SRCS_C', 'lib/mp-readline/readline.c')

elif env['MICROPY_USE_READLINE'] == "2":
    env.MergeFlags('-DMICROPY_USE_READLINE=2')
    env.MergeFlags('-lreadline')

# # TODO where are .P files?
# # If to use gcc's dependency files for rebuilding
# env.Replace(SCANDEPFILES=True)
