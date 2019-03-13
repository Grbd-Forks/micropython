# Import the scons environment from the calling script
Import('env')

env.SetDefault(MICROPY_PY_LWIP='0')

# A port should add an include path where lwipopts.h can be found
# (eg extmod/lwip-include) or '-I${TOP}/extmod/lwip-include'

# TODO
# $(BUILD)/$(LWIP_DIR)/core/ipv4/dhcp.o: CFLAGS_MOD += -Wno-address

# TCP/IP Stack
if env['MICROPY_PY_LWIP'] == "1":
    env.Replace(LWIP_DIR='lib/lwip/src')
    env.AppendUnique(INC=
        ['-I${TOP}/${LWIP_DIR}/include'])

    env.AppendUnique(CFLAGS_MOD='-DMICROPY_PY_LWIP=1')

    env.AppendUnique(SRC_MOD=
    env.Split("extmod/modlwip.c lib/netutils/netutils.c"))
    env.AppendUnique(SRC_MOD=
        env.AddPrefix('${LWIP_DIR}/',
            env.Split("""
        core/def.c
        core/dns.c
        core/inet_chksum.c
        core/init.c
        core/ip.c
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
        core/timeouts.c
        core/udp.c
        core/ipv4/autoip.c
        core/ipv4/dhcp.c
        core/ipv4/etharp.c
        core/ipv4/icmp.c
        core/ipv4/igmp.c
        core/ipv4/ip4_addr.c
        core/ipv4/ip4.c
        core/ipv4/ip4_frag.c
        core/ipv6/dhcp6.c
        core/ipv6/ethip6.c
        core/ipv6/icmp6.c
        core/ipv6/inet6.c
        core/ipv6/ip6_addr.c
        core/ipv6/ip6.c
        core/ipv6/ip6_frag.c
        core/ipv6/mld6.c
        core/ipv6/nd6.c
        netif/ethernet.c
            """)))

    if env['MICROPY_PY_LWIP_SLIP'] == "1":
        env.AppendUnique(CFLAGS_MOD='-DMICROPY_PY_LWIP_SLIP=1')
        env.AppendUnique(SRC_MOD='${LWIP_DIR}/netif/slipif.c')
