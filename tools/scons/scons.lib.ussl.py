# Import the scons environment from the calling script
Import('env')

env.SetDefault(MICROPY_PY_USSL='0')

# USSL – SSL/TLS module
if env['MICROPY_PY_USSL'] == "1":
    env.AppendUnique(CFLAGS_MOD='-DMICROPY_PY_USSL=1')

    # AXTLS - USSL Module
    if env['MICROPY_SSL_AXTLS'] == "1":
            env.AppendUnique(CFLAGS_MOD=
                ['-DMICROPY_SSL_AXTLS=1',
                 '-I' + '${TOP}/lib/axtls/ssl',
                 '-I' + '${TOP}/lib/axtls/crypto',
                 '-I' + '${TOP}/lib/axtls/config'])
            env.AppendUnique(LDFLAGS_MOD=env.Split("-L${BUILD} -laxtls"))

    # Mbed / TLS - USSL Module
    elif env['MICROPY_SSL_MBEDTLS'] == "1":
        # Can be overridden by ports which have "builtin" mbedTLS
        env.SetDefault(MICROPY_SSL_MBEDTLS_INCLUDE='${TOP}/lib/mbedtls/include')
        env.AppendUnique(CFLAGS_MOD=env.Split("-DMICROPY_SSL_MBEDTLS=1 -I${MICROPY_SSL_MBEDTLS_INCLUDE}"))
        env.AppendUnique(LDFLAGS_MOD=
            env.Split("-L${TOP}/lib/mbedtls/library -lmbedx509 -lmbedtls -lmbedcrypto"))
