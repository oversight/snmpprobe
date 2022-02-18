from configparser import ConfigParser, NoSectionError, NoOptionError
from .snmp.v3.auth import AUTH_PROTO
from .snmp.v3.encr import PRIV_PROTO


def read_asset_config(config: ConfigParser, key, decrypt):
    try:
        section = config['credentials']
    except NoSectionError:
        # credentials are currently only needed for snmpv3
        return {}

    try:
        user_name = section.get('user_name')
    except NoOptionError:
        raise Exception(f'Missing user_name')

    auth_type = section.get('auth_type', 'USM_AUTH_NONE')
    if auth_type != 'USM_AUTH_NONE':
        if auth_type not in AUTH_PROTO:
            raise Exception(f'Invalid auth_type')

        try:
            auth_passwd = section.get('auth_passwd')
        except NoOptionError:
            raise Exception(f'Missing required auth_passwd')

        try:
            auth_passwd = decrypt(key, auth_passwd)
        except Exception:
            raise Exception(f'Failed to decrypt auth_passwd')

        priv_type = section.get('priv_type', 'USM_PRIV_NONE')
        if priv_type != 'USM_PRIV_NONE':
            if priv_type not in PRIV_PROTO:
                raise Exception(f'Invalid priv_type')

            try:
                priv_passwd = section.get('priv_passwd')
            except NoOptionError:
                raise Exception(f'Missing required priv_passwd')

            try:
                priv_passwd = decrypt(key, priv_passwd)
            except Exception:
                raise Exception(f'Failed to decrypt priv_passwd')

            cred = {
                'username': user_name,
                'auth_proto': auth_type,
                'auth_passwd': auth_passwd,
                'priv_proto': priv_type,
                'priv_passwd': priv_passwd,
            }
        else:
            cred = {
                'username': user_name,
                'auth_proto': auth_type,
                'auth_passwd': auth_passwd,
            }
    else:
        cred = {
            'username': user_name,
        }

    return {
        'credentials': cred
    }
