import argparse
import asyncio
import os
from agentcoreclient import AgentCoreClient
from setproctitle import setproctitle
from lib.check import CHECKS
from lib.check.base import make_check
from lib.config import read_asset_config
from lib.mib.mib_index import MibIndex


# Migrate the snmp configuration and credentials
def migrate_config_folder():
    if os.path.exists('/data/config/OsSnmpProbe'):
        os.rename('/data/config/OsSnmpProbe', '/data/config/snmpprobe')
    if os.path.exists('/data/config/snmpprobe/defaultCredentials.ini'):
        os.rename('/data/config/snmpprobe/defaultCredentials.ini',
                  '/data/config/snmpprobe/defaultAssetConfig.ini')


if __name__ == '__main__':
    setproctitle('snmpprobe')

    migrate_config_folder()

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-l', '--log-level',
        default='warning',
        help='set the log level',
        choices=['debug', 'info', 'warning', 'error'])

    parser.add_argument(
        '--log-colorized',
        action='store_true',
        help='use colorized logging')

    args = parser.parse_args()

    mi = MibIndex()

    NEW_CHECK_DEFINITIONS = {
        check_name: make_check(mi, check_name, check_info)
        for check_name, check_info in CHECKS.items()
    }

    cl = AgentCoreClient(
        'probe',
        '0.0.1',
        NEW_CHECK_DEFINITIONS,
        read_asset_config,
        '/data/config/wmiprobe/snmpProbe-config.json'
    )

    cl.setup_logger(args.log_level, args.log_colorized)

    asyncio.get_event_loop().run_until_complete(cl.connect_loop())
