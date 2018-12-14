# Import the scons environment from the calling script
Import('env')

env.SetDefault(FROZEN_DIR='')
env.SetDefault(FROZEN_MPY_DIR='')


def AddPrefix(arr, prefix):
    for i in range(len(arr)):
        arr[i] = prefix + arr[i]
    return arr

# object file for frozen files
if env['FROZEN_DIR'] != "":
    env.AppendUnique(PY_O='${BUILD}/${BUILD}/frozen.o')

# object file for frozen bytecode (frozen .mpy files)
if env['FROZEN_MPY_DIR'] != "":
    env.AppendUnique(PY_O='${BUILD}/${BUILD}/frozen_mpy.o')

if env['FROZEN_DIR'] != "":
    print("TODO rules for Frozen Dir")
    # Rule:    ${BUILD}/frozen.c
    # Depends:  ' TODO Unhandled expression definition '<class 'make2scons.pymake.functions.WildcardFunction'> ${HEADER_BUILD} ${FROZEN_EXTRA_DEPS}

    #TODO CONVERSION: statement type: <class 'make2scons.pymake.parserdata.Command'>
    #TODO CONVERSION: statement type: <class 'make2scons.pymake.parserdata.Command'>

if env['FROZEN_MPY_DIR'] != "":
    # Rule:    ${TOP}/mpy-cross/mpy-cross
    # Depends:  ${TOP}/py/*.[ch] ${TOP}/mpy-cross/*.[ch] ${TOP}/ports/windows/fmode.c

    #TODO CONVERSION: statement type: <class 'make2scons.pymake.parserdata.Command'>
    #TODO env.subst may be required, := token used below
    env.Replace(FROZEN_MPY_PY_FILES="$(shell find -L $(FROZEN_MPY_DIR) -type f -name '*.py' | $(SED) -e 's=^$(FROZEN_MPY_DIR)/==')")

    #TODO env.subst may be required, := token used below
    prefix = '${BUILD}/frozen_mpy/${FROZEN_MPY_PY_FILES:.py=.mpy}}'
    __FROZEN_MPY_MPY_FILES = env.Split("""
    """)
    __FROZEN_MPY_MPY_FILES = AddPrefix(__FROZEN_MPY_MPY_FILES, prefix)
    env.Replace(FROZEN_MPY_MPY_FILES=__FROZEN_MPY_MPY_FILES)
    
    # Rule:    ${BUILD}/frozen_mpy/%.mpy
    # Depends:  ${FROZEN_MPY_DIR}/%.py ${TOP}/mpy-cross/mpy-cross
    
    #TODO CONVERSION: statement type: <class 'make2scons.pymake.parserdata.Command'>
    #TODO CONVERSION: statement type: <class 'make2scons.pymake.parserdata.Command'>
    #TODO CONVERSION: statement type: <class 'make2scons.pymake.parserdata.Command'>
    # Rule:    ${BUILD}/frozen_mpy.c
    # Depends:  ${FROZEN_MPY_MPY_FILES} ${BUILD}/genhdr/qstrdefs.generated.h
    
    #TODO CONVERSION: statement type: <class 'make2scons.pymake.parserdata.Command'>
    #TODO CONVERSION: statement type: <class 'make2scons.pymake.parserdata.Command'>


# TODO seperate into tools
env.Replace(MAKE_FROZEN=env.Split("""
    ${PYTHON}
    ${TOP}/tools/make-frozen.py
"""))

env.Replace(MPY_CROSS='${TOP}/mpy-cross/mpy-cross')

env.Replace(MPY_TOOL=env.Split("""
    ${PYTHON}
    ${TOP}/tools/mpy-tool.py
"""))
