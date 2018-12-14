# Import the scons environment from the calling script
Import('env')

env.SetDefault(MICROPY_PY_LWIP='0')

# TCP/IP Stack
if env['MICROPY_PY_LWIP'] == "1":
    env.Replace(LWIP_DIR='lib/lwip/src')
    env.AppendUnique(INC=
        ['-I${TOP}/lib/lwip/src/include',
         '-I${TOP}/lib/lwip/src/include/ipv4',
         '-I${TOP}/extmod/lwip-include'])

    env.AppendUnique(CFLAGS_MOD='-DMICROPY_PY_LWIP=1')

    env.AppendUnique(SRC_MOD=
    env.Split("extmod/modlwip.c lib/netutils/netutils.c"))
    env.AppendUnique(SRC_MOD=
        env.AddPrefix('${LWIP_DIR}/',
            env.Split("""
        core/def.c
        core/dns.c
        core/init.c
        core/mem.c
        core/memp.c
        core/netif.c
        core/pbuf.c
        core/raw.c
        core/stats.c
        core/sys.c
        core/tcp.c
        core/tcp_in.c
        core/tcp_out.c
        core/timers.c
        core/udp.c
        core/ipv4/autoip.c
        core/ipv4/icmp.c
        core/ipv4/igmp.c
        core/ipv4/inet.c
        core/ipv4/inet_chksum.c
        core/ipv4/ip_addr.c
        core/ipv4/ip.c
        core/ipv4/ip_frag.c
            """)))

    if env['MICROPY_PY_LWIP_SLIP'] == "1":
            env.AppendUnique(CFLAGS_MOD='-DMICROPY_PY_LWIP_SLIP=1')
            env.AppendUnique(SRC_MOD='${LWIP_DIR}/netif/slipif.c')
