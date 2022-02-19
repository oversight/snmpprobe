[![CI](https://github.com/oversight/snmpprobe/workflows/CI/badge.svg)](https://github.com/oversight/snmpprobe/actions)
[![Release Version](https://img.shields.io/github/release/oversight/snmpprobe)](https://github.com/oversight/snmpprobe/releases)

# Oversight SNMP probe


## Configuration Options
Variable           | Default     | Description
-------------------|-------------|------------------------------------
`AGENTCORE_IP`     | localhost   | Agentcore ip
`AGENTCORE_PORT`   | 7211        | Agentcore port
`SNMP_MAX_ROWS`    | 50000       | Max number of snmp objects (metrics * items). The default is chosen based on the old value `55000`.
`OS_CONFIG_FOLDER` | /etc        | Location of the config files
`OS_LOG_LEVEL`     | warning     | Log level

## Create a check

1. Put mib file(s) into `mibs/orig` folder. The filename should be the same as specified in mib, without a file-extension.
2. Run `python3 parse_mibs.py` from within `mibs/` folder. The parsed mib(s) should appear in the `mibs/parsed` folder.
3. Add check definition to `CHECKS` in `lib/checks/__init__.py`
```
CHECKS = {
    ...

    'MY_CHECK': {
        'interval': 900,
        'types': [
            {
                'type_name': 'my_type',
                'mib_obj': 'HOST-RESOURCES-MIB::hrSystem',
            },
            {
                'type_name': 'my_type_table',
                'mib_obj': 'HOST-RESOURCES-MIB::hrProcessorEntry',
                'is_table': True,
                'name_template': 'processor {hrProcessorFrwID}',
                'item_func': 'MY_ITEM_FUNC',
                'filter_func': 'MY_FILTER_FUNC',
                'metric_funcs': {
                    'hrProcessorLoad': 'MY_METRIC_FUNC'
                },
            },
        ],
    },
}
```
`MY_CHECK` is the name of the check as shown in oversight.

(optionally) a check `interval` can be configured (seconds). This defaults to 300 seconds.

a check can have one of objects to query, specified in the `types` list

`type_name` is the name of the type as shown in oversight.

`mib_obj` should be `<MIB name>::<MIB object name>`: which object to query.

`is_table` needs to be set `True` when an object has multiple items. These objects always end with `Entry`.

(optionally) a `name_template` can be specified in case of a table. This defaults to `type_name-{idx}`

(optionally) an `item_func` can be specified (see 4).

(optionally) a `filter_func` can be specified in case of a table (see 5).

(optionally) `metric_funcs` can be specified (see 6). This should be an object with keys for the metric which should be formatted and values for the function name which should be called for this metric.

4. Create a item function if needed and add definition to `MAP_FUNS` in `lib/checks/utils.py`.
```
def my_item_func(key, item):
    # do something with key or item here
    return item

MAP_FUNS = {
    ...

    'MY_ITEM_FUNC': my_item_func,
}
```

5. Create a filter function if needed and add definition to `FILTER_FUNS` in `lib/checks/utils.py`.
```
def my_filter_func(key, item):
    # return boolean whether or not this item should be kept in the resulting table
    return True

FILTER_FUNS = {
    ...

    'MY_FILTER_FUNC': my_filter_func,
}
```

6. Create a metric function if needed and add definition to `SYNTAX_FUNS` in `lib/mib_check/syntax_funs.py`.
```
def my_metric_func(value):
    # do something with value here
    return value

SYNTAX_FUNS = {
    ...

    'MY_METRIC_FUNC': my_metric_func,
}
```


## SNMP v3

**Supported auth protocols**
- `USM_AUTH_HMAC96_MD5`
- `USM_AUTH_HMAC96_SHA`
- `USM_AUTH_NONE`

**Supported encryption protocols**
- `USM_PRIV_CBC56_DES`
- `USM_PRIV_CFB128_AES`
- `USM_PRIV_NONE`
