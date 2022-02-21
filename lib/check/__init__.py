from .host_resources_mib import host_resources_mib
from .if_mib import if_mib
from .snmpping import snmpping


CHECKS = {
    'CheckSnmpPing': {
        'types': [],
        'snmp_func': snmpping,
    },
    'RFC1213_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'RFC1213-MIB::system', 'type_name': 'system'},
        ],
        'required': True,
    },
    'IF_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'IF-MIB::ifEntry', 'type_name': 'interface', 'is_table': True},
            {'mib_obj': 'IF-MIB::ifXEntry', 'type_name': 'interface', 'is_table': True},
        ],
        'check_func': if_mib,
    },
    'HOST_RESOURCES_MIB': {
        'types': [
            {'mib_obj': 'HOST-RESOURCES-MIB::hrSystem', 'type_name': 'system'},
            {'mib_obj': 'HOST-RESOURCES-MIB::hrStorageEntry', 'type_name': 'storage', 'is_table': True, 'name_template': '{hrStorageDescr}'},
            {'mib_obj': 'HOST-RESOURCES-MIB::hrDeviceEntry', 'type_name': 'device', 'is_table': True},
            {'mib_obj': 'HOST-RESOURCES-MIB::hrFSEntry', 'type_name': 'fs', 'is_table': True},
            {'mib_obj': 'HOST-RESOURCES-MIB::hrSWRunEntry', 'type_name': 'process', 'is_table': True},
            {'mib_obj': 'HOST-RESOURCES-MIB::hrProcessorEntry', 'type_name': 'processor', 'is_table': True},
        ],
        'check_func': host_resources_mib,
    },
    'ipAddrTable': {
        'types': [
            {'mib_obj': 'RFC1213-MIB::ipAddrEntry', 'type_name': 'IPaddress', 'is_table': True, 'item_func': 'ip_mib_ipaddr'},
        ],
        'interval': 600,
    },
    'ipAddressTable': {
        'types': [
            {'mib_obj': 'IP-MIB::ipAddressEntry', 'type_name': 'IPaddress', 'is_table': True, 'item_func': 'ip_mib_ipaddress'},
        ],
        'interval': 600,
    },
    'ipRouteTable': {
        'types': [
            {'mib_obj': 'RFC1213-MIB::ipRouteEntry', 'type_name': 'ipRoute', 'is_table': True, 'item_func': 'ip_mib_iproute'},
        ],
        'interval': 82800,
    },
    'tcpConnTable': {
        'types': [
            {'mib_obj': 'RFC1213-MIB::tcpConnEntry', 'type_name': 'TCPConnections', 'is_table': True, 'item_func': 'tcp_mib_tcpconn'},
        ],
    },
    'tcpConnectionsTable': {
        'types': [
            {'mib_obj': 'TCP-MIB::tcpConnectionEntry', 'type_name': 'TCPConnections', 'is_table': True, 'item_func': 'tcp_mib_tcpconnection'},
        ],
    },
    'tcpListenerTable': {
        'types': [
            {'mib_obj': 'TCP-MIB::tcpListenerEntry', 'type_name': 'TCPListeners', 'is_table': True, 'item_func': 'tcp_mib_tcplistener'},
        ],
    },
    'MIB ENTITY_MIB': {
        'types': [
            {'mib_obj': 'ENTITY-MIB::entPhysicalEntry', 'type_name': 'system', 'is_table': True},
        ],
        'interval': 3600,
    },
    'SENSOR_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'ENTITY-SENSOR-MIB::entPhySensorEntry', 'type_name': 'sensor', 'is_table': True},
        ],
    },
    'POWER_ETHERNET_MIB': {
        'types': [
            {'mib_obj': 'POWER-ETHERNET-MIB::pethPsePortEntry', 'type_name': 'pethObjects', 'is_table': True},
            {'mib_obj': 'POWER-ETHERNET-MIB::pethMainPseEntry', 'type_name': 'pethMainPseObjects', 'is_table': True},
        ],
    },
    'HP_ICF_CHASSIS ASN.1 MIB': {
        'types': [
            {'mib_obj': 'HP-ICF-CHASSIS::hpicfSensorEntry', 'type_name': 'sensor', 'is_table': True, 'item_func': 'hp_icf_chassis_mib'},
        ],
    },
    'hpSwitchSystemPerformance': {
        'types': [
            {'mib_obj': 'STATISTICS-MIB::hpSwitchMiscStat', 'type_name': 'system'},
        ],
    },
    'SW_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'SW-MIB::swSensorEntry', 'type_name': 'system', 'is_table': True},
            {'mib_obj': 'SW-MIB::swFCPortEntry', 'type_name': 'fcPort', 'is_table': True, 'item_func': 'sw_mib', 'metric_funcs': {'swFCPortLipLastAlpa': 'BROCADE-SYSTEM-MIB::swFCPortLipLastAlpa', 'swFCPortWwn': 'BROCADE-SYSTEM-MIB::swFCPortWwn', }},
            {'mib_obj': 'SW-MIB::swEventEntry', 'type_name': 'event', 'is_table': True},
            {'mib_obj': 'SW-MIB::swSystem', 'type_name': 'system', 'is_recursive': True},
        ],
    },
    'UCD_DISKIO_MIB': {
        'types': [
            {'mib_obj': 'UCD-DISKIO-MIB::diskIOEntry', 'type_name': 'diskio', 'is_table': True, 'name_template': '{diskIODevice}'},
        ],
    },
    'UCD_SNMP_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'UCD-SNMP-MIB::memory', 'type_name': 'memory', 'item_func': 'ucd_snmp_mib'},
        ],
    },
    'CPQHLTH_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'CPQSTDEQ-MIB::cpqSeCpuEntry', 'type_name': 'processor', 'is_table': True},
            {'mib_obj': 'CPQHLTH-MIB::cpqHeFltTolFanEntry', 'type_name': 'thermalFan', 'is_table': True},
            {'mib_obj': 'CPQHLTH-MIB::cpqHeTemperatureEntry', 'type_name': 'thermalTerminal', 'is_table': True},
            {'mib_obj': 'CPQHLTH-MIB::cpqHeFltTolPowerSupplyEntry', 'type_name': 'powersupply', 'is_table': True, 'item_func': 'cpqhlth_mib_powersupply'},
            {'mib_obj': 'CPQHLTH-MIB::cpqHeEventLogEntry', 'type_name': 'eventlog', 'is_table': True, 'metric_funcs': {'cpqHeEventLogInitialTime': 'CPQHLTH-MIB::cpqHeEventLogInitialTime', 'cpqHeEventLogUpdateTime': 'CPQHLTH-MIB::cpqHeEventLogUpdateTime', }},
            {'mib_obj': 'CPQHLTH-MIB::cpqHeResMem2ModuleEntry', 'type_name': 'memory', 'is_table': True},
            {'mib_obj': 'CPQHLTH-MIB::cpqHeResilientMemory', 'type_name': 'memoryglobal'},
            {'mib_obj': 'CPQHLTH-MIB::cpqHeResMemModuleEntry', 'type_name': 'memory', 'is_table': True},
        ],
    },
    'CPQHOST_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'CPQHOST-MIB::cpqHoFileSysEntry', 'type_name': 'system', 'is_table': True, 'item_func': 'cpqhost_mib'},
        ],
    },
    'CPQIDA_MIB_ASN_1_MIB_CTRL': {
        'types': [
            {'mib_obj': 'CPQIDA-MIB::cpqDaCntlrEntry', 'type_name': 'controller', 'is_table': True, 'name_template': '{cpqDaCntlrSerialNumber}'},
        ],
    },
    'CPQIDA_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'CPQIDA-MIB::cpqDaLogDrvEntry', 'type_name': 'logicalDrive', 'is_table': True, 'name_template': '{cpqDaLogDrvOsName}'},
            {'mib_obj': 'CPQIDA-MIB::cpqDaPhyDrvEntry', 'type_name': 'physicalDrive', 'is_table': True, 'name_template': '{cpqDaPhyDrvSerialNum}'},
        ],
    },
    'PAN_COMMON_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'PAN-COMMON-MIB::panSys', 'type_name': 'system'},
            {'mib_obj': 'PAN-COMMON-MIB::panSession', 'type_name': 'session'},
            {'mib_obj': 'PAN-COMMON-MIB::panChassis', 'type_name': 'system'},
        ],
    },
    'PAN_COMMON_MIB EXTENDED': {
        'types': [
            {'mib_obj': 'PAN-COMMON-MIB::panGlobalCounters', 'type_name': 'panGlobalCounters'},
            {'mib_obj': 'PAN-COMMON-MIB::panGlobalCountersDOSCounters', 'type_name': 'panGlobalCountersDOSCounters'},
            {'mib_obj': 'PAN-COMMON-MIB::panGlobalCountersDropCounters', 'type_name': 'panGlobalCountersDropCounters'},
            {'mib_obj': 'PAN-COMMON-MIB::panGlobalCountersIPFragmentationCounters', 'type_name': 'panGlobalCountersIPFragmentationCounters'},
            {'mib_obj': 'PAN-COMMON-MIB::panGlobalCountersTCPState', 'type_name': 'panGlobalCountersTCPState'},
            {'mib_obj': 'PAN-COMMON-MIB::panGlobalCountersTunnelInspect', 'type_name': 'panGlobalCountersTunnelInspect'},
            {'mib_obj': 'PAN-COMMON-MIB::panVsysEntry', 'type_name': 'panVsysEntry', 'is_table': True, 'name_template': '{panVsysName}'},
            {'mib_obj': 'PAN-COMMON-MIB::panZoneEntry', 'type_name': 'panZoneEntry', 'is_table': True, 'name_template': '{panZoneName}'},
            {'mib_obj': 'PAN-COMMON-MIB::panIfEntry', 'type_name': 'panIfEntry', 'is_table': True, 'name_template': '{ifDescr}'},
            {'mib_obj': 'PAN-COMMON-MIB::panMgmt', 'type_name': 'panMgmt'},
            {'mib_obj': 'PAN-COMMON-MIB::panGPGatewayUtilization', 'type_name': 'panGPGatewayUtilization'},
            {'mib_obj': 'PAN-COMMON-MIB::panLcStat', 'type_name': 'panLcStat'},
            {'mib_obj': 'PAN-COMMON-MIB::panLcLogDuration', 'type_name': 'panLcLogDuration'},
            {'mib_obj': 'PAN-COMMON-MIB::panLcDiskUsageEntry', 'type_name': 'panLcDiskUsageEntry', 'is_table': True},
            {'mib_obj': 'PAN-COMMON-MIB::panLcLogUsageEntry', 'type_name': 'panLcLogUsageEntry', 'is_table': True},
            {'mib_obj': 'PAN-COMMON-MIB::panLocalLogUsageEntry', 'type_name': 'panLocalLogUsageEntry', 'is_table': True},
            {'mib_obj': 'PAN-COMMON-MIB::panLcDiskIOPSEntry', 'type_name': 'panLcDiskIOPSEntry', 'is_table': True},
            {'mib_obj': 'PAN-COMMON-MIB::panLcLogFwdStatsEntry', 'type_name': 'panLcLogFwdStatsEntry', 'is_table': True},
            {'mib_obj': 'PAN-COMMON-MIB::panLcLoggingConnectedDeviceEntry', 'type_name': 'panLcLoggingConnectedDeviceEntry', 'is_table': True},
            {'mib_obj': 'PAN-COMMON-MIB::panLcLoggingDeviceEntry', 'type_name': 'panLcLoggingDeviceEntry', 'is_table': True},
            {'mib_obj': 'PAN-COMMON-MIB::panDeviceLoggingLogRate', 'type_name': 'panDeviceLoggingLogRate'},
            {'mib_obj': 'PAN-COMMON-MIB::panDeviceLoggingLogTypeStatEntry', 'type_name': 'panDeviceLoggingLogTypeStatEntry', 'is_table': True},
            {'mib_obj': 'PAN-COMMON-MIB::panDeviceLoggingLogUsageEntry', 'type_name': 'panDeviceLoggingLogUsageEntry', 'is_table': True},
            {'mib_obj': 'PAN-COMMON-MIB::panDeviceLoggingExtFwd', 'type_name': 'panDeviceLoggingExtFwd'},
            {'mib_obj': 'PAN-COMMON-MIB::panDeviceLoggingExtFwdStatsEntry', 'type_name': 'panDeviceLoggingExtFwdStatsEntry', 'is_table': True},
            {'mib_obj': 'PAN-COMMON-MIB::panDeviceLoggingCollectorConnectionEntry', 'type_name': 'panDeviceLoggingCollectorConnectionEntry', 'is_table': True},
            {'mib_obj': 'PAN-COMMON-MIB::panSSLBrokerStatsEntry', 'type_name': 'panSSLBrokerStatsEntry', 'is_table': True},
        ],
    },
    'AEROHIVE_MIB': {
        'types': [
            {'mib_obj': 'AH-INTERFACE-MIB::ahXIfEntry', 'type_name': 'ahXIfTable', 'is_table': True},
            {'mib_obj': 'AH-INTERFACE-MIB::ahAssociationEntry', 'type_name': 'ahAssociationTable', 'is_table': True},
            {'mib_obj': 'AH-INTERFACE-MIB::ahRadioStatsEntry', 'type_name': 'ahRadioStatsTable', 'is_table': True},
            {'mib_obj': 'AH-INTERFACE-MIB::ahVIfStatsEntry', 'type_name': 'ahVIfStatsTable', 'is_table': True},
            {'mib_obj': 'AH-INTERFACE-MIB::ahRadioAttributeEntry', 'type_name': 'ahRadioAttributeTable', 'is_table': True},
            {'mib_obj': 'AH-SYSTEM-MIB::ahSystem', 'type_name': 'ahSystem'},
        ],
    },
    'PowerNet_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'PowerNet-MIB::iemStatusProbesEntry', 'type_name': 'temperature', 'is_table': True},
            {'mib_obj': 'PowerNet-MIB::rPDU2SensorTempHumidityStatusEntry', 'type_name': 'rPDU2SensorTempHumidityStatus', 'is_table': True, 'metric_funcs': {'rPDU2SensorTempHumidityStatusTempF': 'PowerNet-MIB::rPDU2SensorTempHumidityStatusTempF', 'rPDU2SensorTempHumidityStatusTempC': 'PowerNet-MIB::rPDU2SensorTempHumidityStatusTempC'}},
            {'mib_obj': 'PowerNet-MIB::rPDUIdent', 'type_name': 'pdu'},
            {'mib_obj': 'PowerNet-MIB::rPDUPowerSupplyDevice', 'type_name': 'pdu'},
            {'mib_obj': 'PowerNet-MIB::sPDUIdent', 'type_name': 'system'},
            {'mib_obj': 'PowerNet-MIB::upsAdvBattery', 'type_name': 'ups'},
            {'mib_obj': 'PowerNet-MIB::upsAdvIdent', 'type_name': 'system'},
            {'mib_obj': 'PowerNet-MIB::upsAdvInput', 'type_name': 'ups'},
            {'mib_obj': 'PowerNet-MIB::upsAdvOutput', 'type_name': 'ups'},
            {'mib_obj': 'PowerNet-MIB::upsBasicBattery', 'type_name': 'ups'},
            {'mib_obj': 'PowerNet-MIB::upsBasicIdent', 'type_name': 'system'},
            {'mib_obj': 'PowerNet-MIB::upsBasicInput', 'type_name': 'ups'},
            {'mib_obj': 'PowerNet-MIB::upsBasicOutput', 'type_name': 'ups'},
        ],
    },
    'NIMBLE_MIB': {
        'types': [
            {'mib_obj': 'NIMBLE-MIB::volEntry', 'type_name': 'volume', 'is_table': True, 'name_template': '{volName}', 'item_func': 'nimble_mib_volume'},
            {'mib_obj': 'NIMBLE-MIB::globalStats', 'type_name': 'status', 'item_func': 'nimble_mib_status'},
        ],
    },
    'UNIFI_MIB': {
        'types': [
            {'mib_obj': 'UBNT-UniFi-MIB::unifiRadioEntry', 'type_name': 'unifiRadioTable', 'is_table': True},
            {'mib_obj': 'UBNT-UniFi-MIB::unifiVapEntry', 'type_name': 'unifiVapTable', 'is_table': True},
            {'mib_obj': 'UBNT-UniFi-MIB::unifiApSystem', 'type_name': 'unifiApSystem'},
        ],
    },
    'NETBOTZ300_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'NETBOTZ300-MIB::tempSensorEntry', 'type_name': 'temperature', 'is_table': True},
            {'mib_obj': 'NETBOTZ300-MIB::humiSensorEntry', 'type_name': 'humidity', 'is_table': True},
            {'mib_obj': 'NETBOTZ300-MIB::dewPointSensorEntry', 'type_name': 'dewPoint', 'is_table': True},
            {'mib_obj': 'NETBOTZ300-MIB::audioSensorEntry', 'type_name': 'audio', 'is_table': True},
            {'mib_obj': 'NETBOTZ300-MIB::airFlowSensorEntry', 'type_name': 'airFlow', 'is_table': True},
            {'mib_obj': 'NETBOTZ300-MIB::dryContactSensorEntry', 'type_name': 'dryContact', 'is_table': True},
            {'mib_obj': 'NETBOTZ300-MIB::doorSwitchSensorEntry', 'type_name': 'doorSwitch', 'is_table': True},
        ],
    },
    'NShardwareConfig': {
        'types': [
            {'mib_obj': 'NS-ROOT-MIB::nsSysGroup', 'type_name': 'hardwareConfig'},
        ],
    },
    'NSfeatures': {
        'types': [
            {'mib_obj': 'NS-ROOT-MIB::nsFeatureInfo', 'type_name': 'NSfeature'},
        ],
    },
    'NShighAvailability': {
        'types': [
            {'mib_obj': 'NS-ROOT-MIB::nsHighAvailabilityGroup', 'type_name': 'NS_HA'},
        ],
    },
    'NSserviceGroup': {
        'types': [
            {'mib_obj': 'NS-ROOT-MIB::serviceEntry', 'type_name': 'NSservice', 'is_table': True, 'name_template': '{svcServiceName}'},
        ],
    },
    'NSserver': {
        'types': [
            {'mib_obj': 'NS-ROOT-MIB::serverEntry', 'type_name': 'NSserver', 'is_table': True, 'name_template': '{serverName}'},
        ],
    },
    'NSVserver': {
        'types': [
            {'mib_obj': 'NS-ROOT-MIB::vserverEntry', 'type_name': 'NSvserver', 'is_table': True, 'name_template': '{vsvrName}'},
        ],
    },
    'NSvserverAdvanceSslConfig': {
        'types': [
            {'mib_obj': 'NS-ROOT-MIB::vserverAdvanceSslConfigEntry', 'type_name': 'vserverAdvanceSslConfig', 'is_table': True},
        ],
    },
    'SYNOLOGY_MIB': {
        'types': [
            {'mib_obj': 'SYNOLOGY-SYSTEM-MIB::synoSystem', 'type_name': 'system'},
            {'mib_obj': 'SYNOLOGY-SYSTEM-MIB::fan', 'type_name': 'fan'},
            {'mib_obj': 'SYNOLOGY-SYSTEM-MIB::dsmInfo', 'type_name': 'dsmInfo'},
            {'mib_obj': 'SYNOLOGY-DISK-MIB::diskEntry', 'type_name': 'disk', 'is_table': True, 'name_template': '{diskID}'},
            {'mib_obj': 'SYNOLOGY-RAID-MIB::raidEntry', 'type_name': 'raid', 'is_table': True, 'name_template': '{raidName}'},
            {'mib_obj': 'SYNOLOGY-SMART-MIB::diskSMARTEntry', 'type_name': 'diskSMART', 'is_table': True},
            {'mib_obj': 'SYNOLOGY-SERVICES-MIB::serviceEntry', 'type_name': 'service', 'is_table': True, 'name_template': '{serviceName}'},
            {'mib_obj': 'SYNOLOGY-STORAGEIO-MIB::storageIOEntry', 'type_name': 'storageIO', 'is_table': True, 'name_template': '{storageIODevice}'},
            {'mib_obj': 'SYNOLOGY-SPACEIO-MIB::spaceIOEntry', 'type_name': 'spaceIO', 'is_table': True, 'name_template': '{spaceIODevice}'},
            {'mib_obj': 'SYNOLOGY-FLASHCACHE-MIB::flashCacheEntry', 'type_name': 'flashCache', 'is_table': True},
            {'mib_obj': 'SYNOLOGY-ISCSILUN-MIB::iSCSILUNEntry', 'type_name': 'iSCSILUN', 'is_table': True},
            {'mib_obj': 'SYNOLOGY-EBOX-MIB::eboxEntry', 'type_name': 'ebox', 'is_table': True},
            {'mib_obj': 'SYNOLOGY-SHA-MIB::synologyHA', 'type_name': 'ha'},
        ]
    },
    'MIB DELL_RAC_MIB': {
        'types': [
            {'mib_obj': 'DELL-RAC-MIB::drsProductInfoGroup', 'type_name': 'system'},
            {'mib_obj': 'DELL-RAC-MIB::drsStatusNowGroup', 'type_name': 'globalStatus'},
            {'mib_obj': 'DELL-RAC-MIB::drsCMCPowerTableEntry', 'type_name': 'globalPsu', 'is_table': True},
            {'mib_obj': 'DELL-RAC-MIB::drsCMCPSUTableEntry', 'type_name': 'psu', 'is_table': True},
            {'mib_obj': 'DELL-RAC-MIB::drsCMCServerTableEntry', 'type_name': 'slotInfo', 'is_table': True},
            {'mib_obj': 'DELL-RAC-MIB::drsFirmwareGroup', 'type_name': 'drsFirmwareGroup'},
        ],
    },
    'IDRAC_MIB': {
        'types': [
            {'mib_obj': 'IDRAC-MIB-SMIv2::systemStateTableEntry', 'type_name': 'systemStateTable', 'is_table': True},
            {'mib_obj': 'IDRAC-MIB-SMIv2::eventLogTableEntry', 'type_name': 'eventLogTable', 'is_table': True, 'metric_funcs': {'eventLogDateName': 'IDRAC-MIB-SMIv2::eventLogDateName'}},
            {'mib_obj': 'IDRAC-MIB-SMIv2::firmwareTableEntry', 'type_name': 'firmwareTable', 'is_table': True},
        ],
    },
    'MG_SNMP_UPS_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'MG-SNMP-UPS-MIB::upsmgIdent', 'type_name': 'system'},
            {'mib_obj': 'MG-SNMP-UPS-MIB::upsmgBattery', 'type_name': 'battery', 'item_func': 'mg_snmp_ups_mib'},
            {'mib_obj': 'MG-SNMP-UPS-MIB::upsmgOutput', 'type_name': 'output', 'is_recursive': True},
            {'mib_obj': 'MG-SNMP-UPS-MIB::upsmgOutputPhaseEntry', 'type_name': 'output', 'is_table': True},
        ],
    },
    'CISCO_PROCESS_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'CISCO-PROCESS-MIB::cpmCPUTotalEntry', 'type_name': 'cpu', 'is_table': True, 'item_func': 'cisco_process_mib'},
        ],
    },
    'CISCO_ENVMON_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'CISCO-ENVMON-MIB::ciscoEnvMonTemperatureStatusEntry', 'type_name': 'temperatureSensor', 'is_table': True},
            {'mib_obj': 'CISCO-ENVMON-MIB::ciscoEnvMonFanStatusEntry', 'type_name': 'fanSensor', 'is_table': True},
            {'mib_obj': 'CISCO-ENVMON-MIB::ciscoEnvMonSupplyStatusEntry', 'type_name': 'powerSupplySensor', 'is_table': True},
        ],
    },
    'CISCO_FIREWALL_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'CISCO-FIREWALL-MIB::cfwHardwareStatusEntry', 'type_name': 'failover', 'is_table': True},
        ],
    },
    'CISCO_FIREWALL_ConnectionStatTable': {
        'types': [
            {'mib_obj': 'CISCO-FIREWALL-MIB::cfwConnectionStatEntry', 'type_name': 'connectionStat', 'is_table': True},
        ],
    },
    'CISCO_SYSLOG_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'CISCO-SYSLOG-MIB::clogHistoryEntry', 'type_name': 'log', 'is_table': True},
        ],
    },
    'CISCO_MEMORY_POOL_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'CISCO-MEMORY-POOL-MIB::ciscoMemoryPoolEntry', 'type_name': 'memoryPool', 'is_table': True, 'name_template': '{ciscoMemoryPoolName}', 'item_func': 'cisco_memory_pool_mib'},
        ],
    },
    'CISCO_LWAPP_WLAN_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'CISCO-LWAPP-WLAN-MIB::cLWlanConfigEntry', 'type_name': 'wlan', 'is_table': True},
        ],
        'interval': 3600,
    },
    'CISCO_ENTITY_SENSOR_MIB ASN.1 MIB': {
        'types': [
            {'mib_obj': 'CISCO-ENTITY-SENSOR-MIB::entSensorValueEntry', 'type_name': 'sensor', 'is_table': True},
        ]
    },
    'XG_FIREWALL_MIB': {
        'types': [
            {'mib_obj': 'XG-FIREWALL-MIB::sysInstall', 'type_name': 'sysInstall'},
            {'mib_obj': 'XG-FIREWALL-MIB::sysStatus', 'type_name': 'sysStatus'},
            {'mib_obj': 'XG-FIREWALL-MIB::cpuStatus', 'type_name': 'cpuStatus'},
            {'mib_obj': 'XG-FIREWALL-MIB::diskStatus', 'type_name': 'diskStatus'},
            {'mib_obj': 'XG-FIREWALL-MIB::memoryStatus', 'type_name': 'memoryStatus'},
            {'mib_obj': 'XG-FIREWALL-MIB::mailHits', 'type_name': 'mailHits'},
            {'mib_obj': 'XG-FIREWALL-MIB::serviceStats', 'type_name': 'serviceStats'},
            {'mib_obj': 'XG-FIREWALL-MIB::liAppliance', 'type_name': 'liAppliance'},
            {'mib_obj': 'XG-FIREWALL-MIB::liSupport', 'type_name': 'liSupport'},
            {'mib_obj': 'XG-FIREWALL-MIB::liAntivirus', 'type_name': 'liAntivirus'},
            {'mib_obj': 'XG-FIREWALL-MIB::liAntispam', 'type_name': 'liAntispam'},
            {'mib_obj': 'XG-FIREWALL-MIB::liIdp', 'type_name': 'liIdp'},
            {'mib_obj': 'XG-FIREWALL-MIB::liWebcat', 'type_name': 'liWebcat'},
        ]
    },
    'XUPS_MIB': {
        'types': [
            {'mib_obj': 'XUPS-MIB::xupsIdent', 'type_name': 'xupsIdent'},
            {'mib_obj': 'XUPS-MIB::xupsBattery', 'type_name': 'xupsBattery'},
            {'mib_obj': 'XUPS-MIB::xupsInput', 'type_name': 'xupsInput', 'metric_funcs': {'xupsInputFrequency': 'XUPS-MIB::xupsInputFrequency', }},
            {'mib_obj': 'XUPS-MIB::xupsInputEntry', 'type_name': 'xupsInputEntry', 'is_table': True},
            {'mib_obj': 'XUPS-MIB::xupsOutput', 'type_name': 'xupsOutput', 'metric_funcs': {'xupsOutputFrequency': 'XUPS-MIB::xupsInputFrequency', }},
            {'mib_obj': 'XUPS-MIB::xupsOutputEntry', 'type_name': 'xupsOutputEntry', 'is_table': True},
            {'mib_obj': 'XUPS-MIB::xupsBypass', 'type_name': 'xupsBypass', 'metric_funcs': {'xupsBypassFrequency': 'XUPS-MIB::xupsInputFrequency', }},
            {'mib_obj': 'XUPS-MIB::xupsBypassEntry', 'type_name': 'xupsBypassEntry', 'is_table': True},
            {'mib_obj': 'XUPS-MIB::xupsEnvironment', 'type_name': 'xupsEnvironment'},
            {'mib_obj': 'XUPS-MIB::xupsAlarm', 'type_name': 'xupsAlarm'},
            {'mib_obj': 'XUPS-MIB::xupsAlarmEntry', 'type_name': 'xupsAlarmEntry', 'is_table': True},
            {'mib_obj': 'XUPS-MIB::xupsAlarmEventEntry', 'type_name': 'xupsAlarmEventEntry', 'is_table': True},
            {'mib_obj': 'XUPS-MIB::xupsTest', 'type_name': 'xupsTest'},
            {'mib_obj': 'XUPS-MIB::xupsControl', 'type_name': 'xupsControl'},
            {'mib_obj': 'XUPS-MIB::xupsConfig', 'type_name': 'xupsConfig', 'metric_funcs': {'xupsConfigOutputFreq': 'XUPS-MIB::xupsInputFrequency', }},
            {'mib_obj': 'XUPS-MIB::xupsTrapControl', 'type_name': 'xupsTrapControl'},
            {'mib_obj': 'XUPS-MIB::xupsRecep', 'type_name': 'xupsRecep'},
            {'mib_obj': 'XUPS-MIB::xupsRecepEntry', 'type_name': 'xupsRecepEntry', 'is_table': True},
            {'mib_obj': 'XUPS-MIB::xupsTopology', 'type_name': 'xupsTopology'},
        ]
    },
    'BDTMIB': {
        'types': [
            {'mib_obj': 'BDTMIB::bDTAgentInfo', 'type_name': 'bDTAgentInfo'},
            {'mib_obj': 'BDTMIB::bDTGlobalData', 'type_name': 'bDTGlobalData'},
            {'mib_obj': 'BDTMIB::bDTDeviceInfo', 'type_name': 'bDTDeviceInfo'},
        ]
    },
}
