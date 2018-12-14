# Import the scons environment from the calling script
Import('env')

# qstr definitions
env.Replace(QSTR_DEFS='#qstrdefsport.h',)

# Include dirs
env.AppendUnique(CPPPATH=[
    env.GetLaunchDir(),
    '${TOP}',
    '${BUILD}',
])

# If we're compiling for the local arch or cross compiling for an ARM based arch
if env['ARMBUILD']:
    env.Replace(CROSS_COMPILE='arm-none-eabi-')
    env.Replace(PYDFU='${TOP}/tools/pydfu.py')

    env.MergeFlags('-mthumb -mtune=cortex-m4 -mabi=aapcs-linux -mcpu=cortex-m4 -mfpu=fpv4-sp-d16')
    env.MergeFlags('-mfloat-abi=hard -fsingle-precision-constant -Wdouble-promotion')
    env.MergeFlags('-Wall -Werror -std=c99 -nostdlib')
    env.Replace(LDFLAGS=env.Split('-nostdlib -T stm32f405.ld --cref --gc-sections'))
    env.AppendUnique(LDFLAGS='-Map=${TARGET.base}.map')

else:
    env.Replace(LD='gcc')
    env.MergeFlags('-m32 $(INC) -Wall -Werror -std=c99')
    env.Replace(LDLAGS=env.Split('-m32 -Wl,--gc-sections'))
    env.AppendUnique(LDFLAGS='-Wl,-Map=${TARGET.base}.map,--cref')

# Tune for Debugging or Optimization
if env['DEBUG'] == "1":
    env.MergeFlags('-O0 -ggdb')
else:
    env.MergeFlags('-Os -DNDEBUG')
    env.MergeFlags('-fdata-sections -ffunction-sections')
