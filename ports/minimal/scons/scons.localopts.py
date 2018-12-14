# Import the scons environment from the calling script
Import('env')

# Command line option if to do an ARM build or local build
AddOption('--armbuild', dest='armbuild', action="store_true", default=True, help='Build for an an ARM CPU')
env.SetDefault(ARMBUILD=GetOption('armbuild'))

# TODO where are .P files?
# If to use gcc's dependency files for rebuilding
env.Replace(SCANDEPFILES=True)
