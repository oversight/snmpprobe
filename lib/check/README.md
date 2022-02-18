```
new checks
SYNOLOGY_MIB
HP_DOT1X_EXTENSIONS_MIB
HP_SYSTEM_MIB
HP_IF_EXT_MIB
HP_MEMPROC_MIB
PAN_COMMON_MIB EXTENDED
XG_FIREWALL_MIB
XUPS_MIB
BDTMIB
```

```
removed (netapp) checks
NETWORK_APPLIANCE_MIB ASN.1 MIB
NETWORK_APPLIANCE_MIB ASN.1 MIB_ctrl
clusterEnclosureTable
clusterHAtable
clusterIfTable
clusterNetportTable
clusterIfGRPtable
clusterLogicalInterfaceTable
clusterNodeTable
clusterVserverTable
```

```
removed checks
CheckLldp
```

```
changed itemname
tcpConnTable
    no type_name prefix
ipAddrTable.IPaddress
    no type_name prefix
NShardwareConfig.hardwareConfig
    type is not a table
    ! widgets (requires extra "sysHardwareSerialNumber" metric and must be used in "Hardware" widget)
NShighAvailability.NS_HA
    type is not a table
    ! conditions
    ! widgets (name is but can be disabled in widget because data is not a table)
NSvserverAdvanceSslConfig.vserverAdvanceSslConfig
    no idx suffix
POWER_ETHERNET_MIB.pethObjects
    no type_name prefix
    ! conditions
POWER_ETHERNET_MIB.pethMainPseObjects
    no type_name prefix
    ! conditions
    ! widgets
CPQHLTH_MIB ASN.1 MIB.thermalFan
    itemname uses wrong index cpqHeFltTolFanIndex != cpqHeFltTolFanChassis.cpqHeFltTolFanIndex
    conditions
    widgets
CPQHLTH_MIB ASN.1 MIB.thermalTerminal
    itemname uses wrong index cpqHeTemperatureIndex != cpqHeTemperatureChassis.cpqHeTemperatureIndex
    ! performance data
    conditions
    widgets
CPQHLTH_MIB ASN.1 MIB.powersupply
    itemname uses wrong index cpqHeFltTolPowerSupplyBay != cpqHeFltTolPowerSupplyChassis.cpqHeFltTolPowerSupplyBay
    ! performance data
    conditions
    widgets
```

```
removed metric
IF_MIB ASN.1 MIB.interface.intStatus
    this is a concatenation of 2 other metrics
    ! conditions

HOST_RESOURCES_MIB.device.hrProcessorLoad
    separate type processor has this metric now (issue #13)
    performance data
    widgets
```

```
changed metric (no conditions, performance data)
CPQHLTH_MIB ASN.1 MIB.memory.cpqHeResMem2ModuleSize
    ! change display function
CPQHLTH_MIB ASN.1 MIB.memoryglobal.cpqHeResilientMemTotalMemSize
    ! change display function
```
