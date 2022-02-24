import asyncio
import logging
from collections import Counter
from .utils import FILTER_FUNS, MAP_FUNS
from ..mib_check.syntax_funs import SYNTAX_FUNS
from ..snmp.asn1 import Number
from ..snmp.client import Snmp, SnmpV1, SnmpV3
from ..snmp.exceptions import SnmpErrorStatus, SnmpVendorOidError, \
    SnmpNoConnection, SnmpNoAuthParams


DEFAULT_INTERVAL = 300

ENUM_UNKNOWN = 'unknown'

FLAGS_SEPERATOR = ','


class Base:

    interval = DEFAULT_INTERVAL
    required = False

    @classmethod
    async def run(cls, data, asset_config):
        try:
            asset_id = data['hostUuid']
            config = data['hostConfig']['probeConfig']['snmpProbe']
            ip4 = config['ip4']
            version = config.get('snmpVersion', '2c')
            community = config.get('snmpCommunity', 'public')
            interval = data.get('checkConfig', {}).get('metaConfig', {}).get(
                'checkInterval')
            assert interval is None or isinstance(interval, int)
            # assert check_name in NEW_CHECK_DEFINITIONS
        except Exception:
            logging.error('invalid check configuration')
            return

        if version == '2c':
            cl = Snmp(
                host=ip4,
                community=community,
                # max_rows=cls.snmp_max_rows,
            )
        elif version == '3':
            cred = asset_config['credentials']
            if cred is None:
                logging.warning(f'missing credentials for {ip4}')
                return
            try:
                cl = SnmpV3(
                    host=ip4,
                    **cred,
                    # max_rows=cls.snmp_max_rows,
                )
            except Exception as e:
                logging.warning(f'invalid snmpv3 client config for {ip4}')
                return
        elif version == '1':
            cl = SnmpV1(
                host=ip4,
                community=community,
                # max_rows=cls.snmp_max_rows,
            )
        else:
            logging.warning(f'unsupported snmpVersion {version}')
            return

        try:
            await cl.connect()
        except SnmpNoConnection:
            logging.error(f'unable to connect to {asset_id} {ip4}')
            return
        except SnmpNoAuthParams:
            logging.error(f'unable to set auth params for {asset_id} {ip4}')
            cl.close()
            return

        max_runtime = .9 * (interval or cls.interval)

        try:
            state_data = await asyncio.wait_for(
                cls.get_data(cl),
                timeout=max_runtime
            )
        except SnmpVendorOidError:
            pass
        except asyncio.TimeoutError:
            raise Exception('Check timed out.')
        except Exception as e:
            raise Exception(f'Check error: {e.__class__.__name__}: {e}')
        else:
            return state_data
        finally:
            cl.close()


def on_oid_map(oid, map_):
    if not isinstance(oid, tuple):
        # some devices don't follow mib's syntax
        # for example ipAddressTable.ipAddressPrefix returns an int in case of
        # old ups firmware version
        # possible solution is to take tag.nr into account while choosing
        # translation func (make_column)
        return
    return map_.get(oid, {}).get('name', '.'.join(map(str, oid)))


def on_value_map(value, map_):
    return map_.get(value, ENUM_UNKNOWN)


def on_value_map_b(value, map_):
    return FLAGS_SEPERATOR.join(
        v for k, v in map_.items() if value[k // 8] & (1 << k % 8))


def make_column(mi, mib_name, column_name, metric_func=None):
    mib_objects, _ = mi[mib_name]
    oid = mib_objects[column_name]
    syntax = mi[oid]['syntax']
    if metric_func:
        return oid, column_name, SYNTAX_FUNS[metric_func]
    elif syntax['tp'] == 'CUSTOM':
        return oid, column_name, SYNTAX_FUNS[syntax['func']]
    elif syntax['tp'] == 'OCTET STRING':
        return oid, column_name, lambda v: v.decode('ascii', 'ignore')
    elif syntax['tp'] == 'OBJECT IDENTIFIER':
        return oid, column_name, lambda v: on_oid_map(v, mi)
    elif syntax['tp'] == 'INTEGER' and syntax.get('values'):
        return oid, column_name, lambda v: on_value_map(v, syntax['values'])
    elif syntax['tp'] == 'INTEGER':
        return oid, column_name, lambda v: v
    elif syntax['tp'] == 'BITS':
        return oid, column_name, lambda v: on_value_map_b(v, syntax['values'])
    else:
        raise Exception(f'Invalid syntax {syntax}')


def make_typ(mi, typ_info):

    async def func(snmp):
        results = await snmp.walk(base_oid, recursive=recursive)
        return dict(on_results(results))

    def on_results(results):
        item = {}
        for oid, value in results:
            prefix = oid[:prefixlen]
            if prefix not in translations:
                continue
            _, name, fun = translations[prefix]
            try:
                item[name] = fun(value)
            except Exception as e:
                raise Exception('Something went wrong in the metric processor:'
                                f' {e.__class__.__name__}: {e}')

        if item:
            prefix = typ_info['type_name']
            name = f'{prefix}-0'
            try:
                item = mfun((0, ), item)
            except Exception as e:
                raise Exception('Something went wrong in the item processor:'
                                f' {e.__class__.__name__}: {e}')
            item['name'] = name
            yield name, item

    mib, obj = typ_info['mib_obj'].split('::')
    base_oid = mi[mib][0][obj]
    prefixlen = len(base_oid) + 1
    metric_funcs = typ_info.get('metric_funcs', {})
    translations = {
        oid: make_column(mi, mib, name, metric_funcs.get(name))
        for name, oid in mi[mib][0].items()
        if (oid in mi and mi[oid]['tp'] == 'OBJECT-TYPE' and
            not mi[oid]['syntax']['tp'].startswith('SEQUENCE OF') and
            mi[oid]['value'][0] == obj)
    }
    assert translations

    mfun = MAP_FUNS[typ_info['item_func']] \
        if 'item_func' in typ_info else lambda k, v: v
    recursive = typ_info.get('is_recursive', False)

    return (
        typ_info['type_name'],
        False,
        [oid for oid in translations],
        func,
    )


def make_typ_table(mi, typ_info):

    async def func(snmp):
        results = await snmp.walk(base_oid)
        return dict(on_results(results))

    def on_item_named(key, item, counts):
        name = typ_info['name_template'].format_map(item)
        idx = counts[name]
        counts[name] += 1
        return f'{name}#{idx}' if idx else name

    def on_item(key, item, counts):
        prefix = typ_info['type_name']
        key_str = '.'.join(map(str, key))
        return f'{prefix}-{key_str}'

    def on_results(results):
        table = {}
        for oid, value in results:
            idx = oid[prefixlen:]
            prefix = oid[:prefixlen]
            if prefix not in translations:
                continue
            _, name, fun = translations[prefix]
            if idx not in table:
                table[idx] = {}
            try:
                table[idx][name] = fun(value)
            except Exception as e:
                raise Exception('Something went wrong in the metric processor:'
                                f' {e.__class__.__name__}: {e}')

        counts = Counter()
        for key, item in table.items():
            name = nfun(key, item, counts)
            try:
                valid = ffun(key, item)
            except Exception as e:
                raise Exception('Something went wrong in the item filter'
                                f' function: {e.__class__.__name__}: {e}')
            if valid:
                try:
                    item = mfun(key, item)
                except Exception as e:
                    raise Exception('Something went wrong in the item'
                                    f' processor: {e.__class__.__name__}: {e}')
                item['name'] = name
                yield name, item

    mib, obj = typ_info['mib_obj'].split('::')
    base_oid = mi[mib][0][obj]
    prefixlen = len(base_oid) + 1
    metric_funcs = typ_info.get('metric_funcs', {})
    assert mi[base_oid]['tp'] == 'OBJECT-TYPE' \
        and mi[base_oid]['syntax']['tp'] == 'SEQUENCE'
    translations = {
        oid: make_column(mi, mib, name, metric_funcs.get(name))
        for name, oid in mi[mib][0].items()
        if (oid in mi and mi[oid]['tp'] == 'OBJECT-TYPE' and
            mi[oid]['value'][0] == obj)
    }
    assert translations

    nfun = on_item_named if 'name_template' in typ_info else on_item
    mfun = MAP_FUNS[typ_info['item_func']] \
        if 'item_func' in typ_info else lambda k, v: v
    ffun = FILTER_FUNS[typ_info['item_filter_func']] \
        if 'item_filter_func' in typ_info else lambda k, v: True

    return (
        typ_info['type_name'],
        True,
        [base_oid],
        func,
    )


def make_vendor_test(mi, check_name, check_info):

    async def func(snmp):
        oid, tag, _ = await snmp.get_next(test_oid)

        if tag.cls + tag.nr == Number.EndOfMibView or oid[:7] != test_oid:
            logging.warning(f'{snmp.host} {check_name} vendor oid mismatch')
            raise SnmpVendorOidError

    needs_vendor_test = False
    if check_info.get('types'):
        typ_info = check_info['types'][0]
        mib, obj = typ_info['mib_obj'].split('::')
        test_oid = mi[mib][0][obj][:7]
        needs_vendor_test = test_oid[:6] == (1, 3, 6, 1, 4, 1)

    return needs_vendor_test, func


def make_check(mi, check_name, check_info):

    async def func(snmp):
        # raises when err or oid mismatch
        is_vendor_check and (await vendor_test(snmp))

        state_data = {}
        for typ_name, _, _, func in types:
            try:
                itms = await func(snmp)
            except SnmpErrorStatus as e:
                logging.warning(f'{snmp.host} {check_name} {typ_name} {e}')
                # resume other types no raise
                # set to empty to clear previous data
                if typ_name not in state_data:
                    state_data[typ_name] = {}
            except Exception as e:
                raise e
            else:
                current = state_data.get(typ_name)
                if current:
                    for name, item in itms.items():
                        if name in current:
                            current[name].update(item)
                        else:
                            current[name] = item
                else:
                    state_data[typ_name] = itms

        if on_state_data:
            try:
                state_data = on_state_data(state_data)
            except Exception as e:
                raise Exception('Something went wrong in the check processor:'
                                f' {e.__class__.__name__}: {e}')
        return state_data

    types = [
        make_typ_table(mi, typ_info)
        if typ_info.get('is_table') else make_typ(mi, typ_info)
        for typ_info in check_info['types']]
    on_state_data = check_info['check_func'] \
        if 'check_func' in check_info else lambda v: v
    is_vendor_check, vendor_test = make_vendor_test(mi, check_name, check_info)

    return type(check_name, (Base,), {
        'interval': check_info.get('interval', DEFAULT_INTERVAL),
        'get_data': check_info.get('snmp_func', func),
        'required': check_info.get('required', False),
    })
