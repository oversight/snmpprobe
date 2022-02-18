MIB_TEXTUAL_CONVENTIONS = {
    'RFC1155-SMI': {
        'Counter': {'tp': 'INTEGER'},
        'Gauge': {'tp': 'INTEGER'},
        'TimeTicks': {'tp': 'CUSTOM', 'func': 'TimeTicks'},
        'Opaque': {'tp': 'OCTET STRING'},
        'IpAddress': {'tp': 'CUSTOM', 'func': 'IpAddress'},
        'NetworkAddress': {'tp': 'CUSTOM', 'func': 'IpAddress'},
    },
    'RFC1213-MIB': {
        'DisplayString': {'tp': 'CUSTOM', 'func': 'DisplayString'},
        'PhysAddress': {'tp': 'CUSTOM', 'func': 'PhysAddress'},
    },
    'SNMPv2-SMI': {
        'Counter32': {'tp': 'INTEGER'},
        'Gauge32': {'tp': 'INTEGER'},
        'Integer32': {'tp': 'INTEGER'},
        'Unsigned32': {'tp': 'INTEGER'},
        'Counter64': {'tp': 'INTEGER'},
        'TimeTicks': {'tp': 'CUSTOM', 'func': 'TimeTicks'},
        'Opaque': {'tp': 'OCTET STRING'},
        'IpAddress': {'tp': 'CUSTOM', 'func': 'IpAddress'},
    },
    'SNMPv2-TC': {
        'DateAndTime': {'tp': 'CUSTOM', 'func': 'DateAndTime'},
        'DisplayString': {'tp': 'CUSTOM', 'func': 'DisplayString'},
        'MacAddress': {'tp': 'CUSTOM', 'func': 'MacAddress'},
        'PhysAddress': {'tp': 'CUSTOM', 'func': 'PhysAddress'},
        'TruthValue': {'tp': 'CUSTOM', 'func': 'TruthValue'},
    },

    'HOST-RESOURCES-MIB': {
        'InternationalDisplayString': {'tp': 'CUSTOM', 'func': 'DisplayString'},
    },
    'SNMP-FRAMEWORK-MIB': {
        'SnmpAdminString': {'tp': 'CUSTOM', 'func': 'DisplayString'},
    },
    'AH-SMI-MIB': {
        'AhString': {'tp': 'CUSTOM', 'func': 'DisplayString'},
    },
    'IDRAC-MIB-SMIv2': {
        'DateName': {'tp': 'CUSTOM', 'func': 'IDRAC-MIB-SMIv2::DateName'},
    },
    'CPQSTDEQ-MIB': {
        'TruthValue': {'tp': 'CUSTOM', 'func': 'CPQSTDEQ-MIB::TruthValue'},
    },
    'STATISTICS-MIB': {
        'MacAddress': {'tp': 'CUSTOM', 'func': 'MacAddress'},
    },
    'SYNOLOGY-RAID-MIB': {
        'Counter64': {'tp': 'INTEGER'},  # import missing in mib
    },
    'PAN-COMMON-MIB': {
        'Counter64': {'tp': 'INTEGER'},  # import missing in mib
        'Unsigned32': {'tp': 'INTEGER'},  # import missing in mib
        'FloatValue': {'tp': 'CUSTOM', 'func': 'PAN-COMMON-MIB::FloatValue'},
    },
    'AH-INTERFACE-MIB': {
        'Counter32': {'tp': 'INTEGER'},  # import missing in mib
        'Counter64': {'tp': 'INTEGER'},  # import missing in mib
        'Integer32': {'tp': 'INTEGER'},  # import missing in mib
    },
}
