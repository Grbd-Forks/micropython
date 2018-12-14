# Import the scons environment from the calling script
Import('env')

env.SetDefault(MICROPY_PY_BTREE='0')

# BTree - simple key-value database
if env['MICROPY_PY_BTREE'] == "1":
    env.Replace(BTREE_DIR='lib/berkeley-db-1.xx')
    env.Replace(BTREE_DEFS=
    env.Split("""
        -D__DBINTERFACE_PRIVATE=1
        -Dmpool_error=printf
        -Dabort=abort_
        "-Dvirt_fd_t=void*"
        ${BTREE_DEFS_EXTRA}
    """))
    env.AppendUnique(INC='-I${TOP}/${BTREE_DIR}/PORT/include')
    env.AppendUnique(SRC_MOD='extmod/modbtree.c')

    env.AppendUnique(SRC_MOD=
        env.AddPrefix('${BTREE_DIR}/',
            env.Split("""
        btree/bt_close.c
        btree/bt_conv.c
        btree/bt_debug.c
        btree/bt_delete.c
        btree/bt_get.c
        btree/bt_open.c
        btree/bt_overflow.c
        btree/bt_page.c
        btree/bt_put.c
        btree/bt_search.c
        btree/bt_seq.c
        btree/bt_split.c
        btree/bt_utils.c
        mpool/mpool.c
            """)))

    env.AppendUnique(CFLAGS_MOD='-DMICROPY_PY_BTREE=1')

    # we need to suppress certain warnings to get berkeley-db to compile cleanly
    # and we have separate BTREE_DEFS so the definitions don't interfere with other source code

    # TODO Variable assignment is for targets: ${BUILD}/${BTREE_DIR}/%.o
    #env.AppendUnique(CFLAGS=
    #    env.Split("-Wno-old-style-definition -Wno-sign-compare -Wno-unused-parameter ${BTREE_DEFS}"))

    # TODO Variable assignment is for targets: ${BUILD}/extmod/modbtree.o
    #env.AppendUnique(CFLAGS='${BTREE_DEFS}')
