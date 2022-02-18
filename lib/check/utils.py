import ipaddress


def addr_ipv4(octets):
    n = octets[0]
    assert len(octets) == n + 1 == 5
    return '.'.join(map(str, octets[1:5]))


def addr_ipv4z(octets):
    # Zone info will just be ignored
    n = octets[0]
    assert len(octets) == n + 1 == 9
    return '.'.join(map(str, octets[1:5]))


def addr_ipv6(octets):
    n = octets[0]
    assert len(octets) == n + 1 == 17
    nr = sum(o * (2 ** ((16 - i - 1) * 8)) for i, o in enumerate(octets[1:17]))
    return str(ipaddress.IPv6Address(nr))


def addr_ipv6z(octets):
    # Zone info will just be ignored
    n = octets[0]
    assert len(octets) == n + 1 == 21
    nr = sum(o * (2 ** ((16 - i - 1) * 8)) for i, o in enumerate(octets[1:17]))
    return str(ipaddress.IPv6Address(nr))


def addr_netmask(addr, n):
    try:
        return str(ipaddress.ip_network(f'{addr}/{n}', strict=False).netmask)
    except ValueError:
        return None


def addr_dns(octets):
    n = octets[0]
    assert len(octets) == n + 1
    return ''.join(map(chr, octets[1:1 + n]))


ADDRESS_TP = {
    0: ('unknown', lambda v: ''),
    1: ('ipv4', addr_ipv4),
    2: ('ipv6', addr_ipv6),
    3: ('ipv4z', addr_ipv4z),
    4: ('ipv6z', addr_ipv6z),
    16: ('dns', addr_dns),
}


def ip_mib_addr(key, item):
    # compat metricnames
    item['address'] = item.get('ipAdEntAddr')
    item['IF_MIB_index'] = item.get('ipAdEntIfIndex')
    item['broadcastAddress'] = item.get('ipAdEntBcastAddr')
    item['netmask'] = item.get('ipAdEntNetMask')
    item['datagram_re-assemlyMaxSize'] = item.get('ipAdEntReasmMaxSize')
    return item


def ip_mib_address(key, item):
    try:
        local_typ = key[0]
        local_typ_name, local_typ_func = ADDRESS_TP[local_typ]
        local_addr = local_typ_func(key[1:])
    except Exception:
        raise Exception(f'Unable to derive address info from oid-part {key}')

    item['ipAddressAddrType'] = local_typ_name
    item['ipAddressAddr'] = local_addr

    # when value is 0.0 or 1.1 ignore
    if 'ipAddressPrefix' in item and item['ipAddressPrefix'] not in (
        'zeroDotZero',  # oid 0.0
        'internet',  # oid 1.1
        None,  # some devices don't follow mib's syntax and return an unparseable int instead of a RowPointer (oid)
    ):
        n = 10  # length of 1.3.6.1.2.1.4.32.1.5 IP-MIB::ipAddressPrefixOrigin
        try:
            prefix_key = tuple(map(int, item['ipAddressPrefix'].split('.')[n:]))
            prefix_ifindex = prefix_key[0]
            prefix_typ = prefix_key[1]
            prefix_typ_name, prefix_typ_func = ADDRESS_TP[prefix_typ]
            prefix_addr = prefix_typ_func(prefix_key[2:-1])
            prefix_len = prefix_key[-1]
        except Exception:
            raise Exception(f'Unable to derive address-prefix info from oid-part {prefix_key}')
        netmask = addr_netmask(prefix_addr, prefix_len)
        item['ipAddressPrefixIfIndex'] = prefix_ifindex
        item['ipAddressPrefixType'] = prefix_typ_name
        item['ipAddressPrefixAddr'] = prefix_addr
        item['ipAddressPrefixLength'] = prefix_len
        item['subnetmask'] = netmask

    # compat metricnames
    item['type'] = item.get('ipAddressType')
    item['prefix'] = item.get('ipAddressPrefix')
    item['origin'] = item.get('ipAddressOrigin')
    item['status'] = item.get('ipAddressStatus')
    item['created'] = item.get('ipAddressCreated')
    item['lastChanged'] = item.get('ipAddressLastChanged')
    return item


def ip_mib_route(key, item):
    # compat metricnames
    item['destination'] = item.get('ipRouteDest')
    item['IFIndex'] = item.get('ipRouteIfIndex')
    item['routingMetric1'] = item.get('ipRouteMetric1')
    item['routingMetric2'] = item.get('ipRouteMetric2')
    item['routingMetric3'] = item.get('ipRouteMetric3')
    item['routingMetric4'] = item.get('ipRouteMetric4')
    item['nextHop'] = item.get('ipRouteNextHop')
    item['type'] = item.get('ipRouteType')
    item['protocol'] = item.get('ipRouteProto')
    item['age'] = item.get('ipRouteAge')
    item['mask'] = item.get('ipRouteMask')
    item['routingMetric5'] = item.get('ipRouteMetric5')
    item['info'] = item.get('ipRouteInfo')
    return item


def tcp_mib_conn(key, item):
    # compat metricnames
    item['localAddress'] = item.get('tcpConnLocalAddress')
    item['localPort'] = item.get('tcpConnLocalPort')
    item['remoteAddress'] = item.get('tcpConnRemAddress')
    item['remotePort'] = item.get('tcpConnRemPort')
    item['state'] = item.get('tcpConnState')
    return item


def tcp_mib_connection(key, item):
    try:
        local_typ = key[0]
        local_typ_len = key[1]
        local_typ_name, local_typ_func = ADDRESS_TP[local_typ]
        local_addr = local_typ_func(key[1: 2 + local_typ_len])
        local_pt = key[2 + local_typ_len]
        remote_typ = key[3 + local_typ_len]
        remote_typ_len = key[4 + local_typ_len]
        remote_typ_name, remote_typ_func = ADDRESS_TP[remote_typ]
        remote_addr = remote_typ_func(key[-remote_typ_len - 2:-1])
        remote_pt = key[-1]
    except Exception:
        raise Exception(f'Unable to derive address info from oid-part {key}')

    item['tcpConnectionLocalAddressType'] = local_typ_name
    item['tcpConnectionLocalAddress'] = local_addr
    item['tcpConnectionLocalPort'] = local_pt
    item['tcpConnectionRemAddressType'] = remote_typ_name
    item['tcpConnectionRemAddress'] = remote_addr
    item['tcpConnectionRemPort'] = remote_pt

    # compat metricnames
    item['localAddressType'] = local_typ_name
    item['localAddress'] = local_addr
    item['localPort'] = local_pt
    item['remoteAddressType'] = remote_typ_name
    item['remoteAddress'] = remote_addr
    item['remotePort'] = remote_pt
    item['state'] = item.get('tcpConnectionState')
    item['process'] = item.get('tcpConnectionProcess')
    return item


def tcp_mib_listener(key, item):
    try:
        local_typ = key[0]
        local_typ_name, local_typ_func = ADDRESS_TP[local_typ]
        local_addr = local_typ_func(key[1: -1])
        local_pt = key[-1]
    except Exception:
        raise Exception(f'Unable to derive address info from oid-part {key}')

    item['tcpListenerLocalAddressType'] = local_typ_name
    item['tcpListenerLocalAddress'] = local_addr
    item['tcpListenerLocalPort'] = local_pt
    return item


def cisco_memory_pool_mib(key, item):
    if 'ciscoMemoryPoolFree' in item and 'ciscoMemoryPoolUsed' in item:
        free = item['ciscoMemoryPoolFree']
        used = item['ciscoMemoryPoolUsed']
        total = free + used
        free_percentage = 100 * free / total if total else None
        used_percentage = 100 * used / total if total else None
        item['ciscoMemoryPoolTotal'] = total
        item['ciscoMemoryPoolFreePercentage'] = free_percentage
        item['ciscoMemoryPoolUsedPercentage'] = used_percentage
    return item


def cisco_process_mib(key, item):
    if 'cpmCPUMemoryFree' in item and 'cpmCPUMemoryUsed' in item:
        free = item['cpmCPUMemoryFree']
        used = item['cpmCPUMemoryUsed']
        total = free + used
        free_percentage = 100 * free / total if total else None
        used_percentage = 100 * used / total if total else None
        item['cpmCPUMemoryTotal'] = total
        item['cpmCPUMemoryFreePercentage'] = free_percentage
        item['cpmCPUMemoryUsedPercentage'] = used_percentage
    return item


def nimble_mib_volume(key, item):
    if 'volSizeHigh' in item and 'volSizeLow' in item:
        item['volSize'] = (item['volSizeHigh'] << 32) + item['volSizeLow'] * 1024 * 1024
    if 'volUsageHigh' in item and 'volUsageLow' in item:
        item['volUsed'] = (item['volUsageHigh'] << 32) + item['volUsageLow'] * 1024 * 1024
    if 'volReserveHigh' in item and 'volReserveLow' in item:
        item['volReserve'] = (item['volReserveHigh'] << 32) + item['volReserveLow'] * 1024 * 1024
    if 'volSize' in item and 'volUsed' in item:
        item['volFree'] = item['volSize'] - item['volUsed']
        item['volFreePercentage'] = 100 * item['volFree'] / item['volSize'] if item['volSize'] else None
        item['volUsedPercentage'] = 100 * item['volUsed'] / item['volSize'] if item['volSize'] else None
    return item


def nimble_mib_status(key, item):
    if 'diskVolBytesUsedHigh' in item and 'diskVolBytesUsedLow' in item:
        item['diskVolBytesUsedInBytes'] = (item['diskVolBytesUsedHigh'] << 32) + item['diskVolBytesUsedLow'] * 1024 * 1024
    if 'diskSnapBytesUsedHigh' in item and 'diskSnapBytesUsedLow' in item:
        item['diskSnapBytesUsedInBytes'] = (item['diskSnapBytesUsedHigh'] << 32) + item['diskSnapBytesUsedLow'] * 1024 * 1024
    return item


def sw_mib(key, item):
    if 'swFCPortRxWords' in item:
        item['swFCPortRxInBytes'] = item['swFCPortRxWords'] * 5
    if 'swFCPortTxWords' in item:
        item['swFCPortTxInBytes'] = item['swFCPortTxWords'] * 5
    return item


def mg_snmp_ups_mib(key, item):
    if 'upsmgBatteryVoltage' in item:
        item['upsmgBatteryVoltage'] = item['upsmgBatteryVoltage'] / 10
    return item


def ucd_snmp_mib(key, item):
    if 'memTotalReal' in item and 'memAvailReal' in item:
        item['memTotalRealInBytes'] = item['memTotalReal'] * 1024
        item['memAvailRealInBytes'] = item['memAvailReal'] * 1024
        item['memUsedRealInBytes'] = item['memTotalRealInBytes'] - item['memAvailRealInBytes']
        item['memUsedRealPercentage'] = 100 * item['memUsedRealInBytes'] / item['memTotalRealInBytes'] if item['memTotalRealInBytes'] else None
        item['memAvialRealPercentage'] = 100 * item['memAvailRealInBytes'] / item['memTotalRealInBytes'] if item['memTotalRealInBytes'] else None

    if 'memTotalSwap' in item and 'memAvailSwap' in item:
        item['memTotalSwapInBytes'] = item['memTotalSwap'] * 1024
        item['memAvailSwapInBytes'] = item['memAvailSwap'] * 1024
        item['memUsedSwapInBytes'] = item['memTotalSwapInBytes'] - item['memAvailSwapInBytes']
        item['memUsedSwapPercentage'] = 100 * item['memUsedSwapInBytes'] / item['memTotalSwapInBytes'] if item['memTotalSwapInBytes'] else None
        item['memFreeSwapPercentage'] = 100 * item['memAvailSwapInBytes'] / item['memTotalSwapInBytes'] if item['memTotalSwapInBytes'] else None

    if 'memTotalFree' in item:
        item['memTotalFreeInBytes'] = item['memTotalFree'] * 1024
    if 'memMinimumSwap' in item:
        item['memMinimumSwapInBytes'] = item['memMinimumSwap'] * 1024

    # UCD-SNMP-MIB says:
    # This object will not be implemented on hosts where the
    # underlying operating system does not distinguish text
    # pages from other uses of physical memory."
    # this rule also applies to memBuffer and memCached
    if 'memShared' in item and 'memBuffer' in item and 'memCached' in item:
        item['memSharedInBytes'] = item['memShared'] * 1024
        item['memBufferInBytes'] = item['memBuffer'] * 1024
        item['memCachedInBytes'] = item['memCached'] * 1024
        item['memUsedHumanInBytes'] = item['memUsedRealInBytes'] - item['memBufferInBytes'] - item['memCachedInBytes']
        item['percentUsedHuman'] = 100 * item['memUsedHumanInBytes'] / item['memTotalRealInBytes'] if item['memTotalRealInBytes'] else None
    return item


def cpqhlth_powersupply(key, item):
    if 'cpqHeFltTolPowerSupplyCapacityMaximum' in item and 'cpqHeFltTolPowerSupplyCapacityUsed' in item:
        total = item['cpqHeFltTolPowerSupplyCapacityMaximum']
        used = item['cpqHeFltTolPowerSupplyCapacityUsed']
        free = total - used
        free_percentage = 100 * free / total if total else None
        used_percentage = 100 * used / total if total else None
        item['cpqHeFltTolPowerSupplyCapacityFree'] = free
        item['cpqHeFltTolPowerSupplyCapacityFreePercentage'] = free_percentage
        item['cpqHeFltTolPowerSupplyCapacityUsedPercentage'] = used_percentage
    return item


def cpqhost_mib(key, item):
    # when no such information available -1 value is returned (CQPHOST-MIB)
    total = item.get('cpqHoFileSysSpaceTotal', -1)
    used = item.get('cpqHoFileSysSpaceUsed', -1)
    if used >= 0 and total >= 0:
        total *= 1048576
        used *= 1048576
        free = total - used
        item['cpqHoFileSysSpaceTotal'] = total
        item['cpqHoFileSysSpaceFree'] = free
        item['cpqHoFileSysSpaceUsed'] = used

    percentused = item.get('cpqHoFileSysPercentSpaceUsed', -1)
    if percentused >= 0:
        item['cpqHoFileSysSpaceFreePercentage'] = 100 - percentused
        item['cpqHoFileSysSpaceUsedPercentage'] = percentused

    return item


def hp_icf_chassis_mib(key, item):
    # compat old lookup is wrong for this value
    if item.get('hpicfSensorStatus') == 'notPresent':
        item['hpicfSensorStatus'] = 'not present'
    return item


MAP_FUNS = {
    'cisco_memory_pool_mib': cisco_memory_pool_mib,
    'cisco_process_mib': cisco_process_mib,
    'cpqhlth_mib_powersupply': cpqhlth_powersupply,
    'cpqhost_mib': cpqhost_mib,
    'hp_icf_chassis_mib': hp_icf_chassis_mib,
    'mg_snmp_ups_mib': mg_snmp_ups_mib,
    'nimble_mib_volume': nimble_mib_volume,
    'nimble_mib_status': nimble_mib_status,
    'sw_mib': sw_mib,
    'ucd_snmp_mib': ucd_snmp_mib,
    'ip_mib_ipaddr': ip_mib_addr,
    'ip_mib_ipaddress': ip_mib_address,
    'ip_mib_iproute': ip_mib_route,
    'tcp_mib_tcpconn': tcp_mib_conn,
    'tcp_mib_tcpconnection': tcp_mib_connection,
    'tcp_mib_tcplistener': tcp_mib_listener,
}

FILTER_FUNS = {

}
