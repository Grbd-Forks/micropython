import os
import shutil

# Import the scons environment from the calling script
Import('env')


# Print Defines within GCC
def print_def(env, target, source):
    print(env.subst("The following defines are built into the ${CC} compiler"))
    empty_file = env.File('${BUILD}/__empty__.c')
    env.Execute(Mkdir('${BUILD}'), chdir=env.GetLaunchDir())
    env.Execute(Touch(empty_file.abspath))
    env.Execute('${CC} -E -Wp,-dM ' + empty_file.abspath)
    empty_file.remove()

tgt = env.Command('#print_def_dummy.c', [], print_def)
env.Alias('print-def', tgt)


# Print scons env variables
def print_env(env, target, source):
    print(env.Dump())

tgt = env.Command('#print_env_dummy.c', [], print_env)
env.Alias('print-env', tgt)


# Alias for clean
def do_clean(env, target, source):
    builddir = env.Dir('${BUILD}').abspath
    if os.path.exists(builddir):
        shutil.rmtree(builddir)

tgt = env.Command('#do_clean_dummy.c', [], do_clean)
env.Alias('clean', tgt)
