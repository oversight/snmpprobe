import asyncio
import unittest
from lib.check import CHECKS
from lib.check.base import make_check
from lib.mib.mib_index import MibIndex
from mibs.parser.grammar import MibsGrammar
from mibs.parser.parse_tree import parse_tree
from mibs.parser.utils import remove_comments_from_mib


mi = MibIndex()
NEW_CHECK_DEFINITIONS = {
    check_name: make_check(mi, check_name, check_info)
    for check_name, check_info in CHECKS.items()
}


TEST_HOSTCONFIG = {
    'probeConfig': {
        'snmpProbe': {
            'ip4': 'localhost',
            'snmpCommunity': 'public'
        }
    }
}

TEST_HOSTCONFIG_V3 = {
    'probeConfig': {
        'snmpProbe': {
            'ip4': 'localhost',
            'snmpVersion': '3',
        }
    }
}

TEST_CREDENTIALS = {
    'username': 'user_md5_des',
    'auth_proto': 'USM_AUTH_HMAC96_MD5',
    'auth_passwd': 'password',
    'priv_proto': 'USM_PRIV_CBC56_DES',
    'priv_passwd': 'password',
}


GRAMMAR = MibsGrammar()


class TestMibs(unittest.TestCase):
    def test_(self):
        line = open('mibs/orig/IF-MIB').read()
        line = remove_comments_from_mib(line)
        res = GRAMMAR.parse(line)
        self.assertTrue(res.is_valid)

        node = res.tree.children[0]
        mibname, mib = parse_tree(node)
        self.assertEqual(mibname, 'IF-MIB')
        self.assertIsNotNone(mib)


class TestProbe(unittest.TestCase):
    def test_check(self):
        check_name = 'RFC1213_MIB ASN.1 MIB'
        check = NEW_CHECK_DEFINITIONS[check_name]

        data = {
            'hostUuid': '',
            'checkName': check_name,
            'hostConfig': TEST_HOSTCONFIG,
        }
        asyncio.run(check.run(data, {}))

    def test_check_snmpv3(self):
        check_name = 'RFC1213_MIB ASN.1 MIB'
        check = NEW_CHECK_DEFINITIONS[check_name]

        data = {
            'hostUuid': '',
            'checkName': check_name,
            'hostConfig': TEST_HOSTCONFIG_V3,
        }
        asyncio.run(check.run(data, {'credentials': TEST_CREDENTIALS}))

    def test_check_func(self):
        check_name = 'IF_MIB ASN.1 MIB'
        check = NEW_CHECK_DEFINITIONS[check_name]

        data = {
            'hostUuid': '',
            'checkName': check_name,
            'hostConfig': TEST_HOSTCONFIG,
        }
        asyncio.run(check.run(data, {}))

    def test_snmp_func(self):
        check_name = 'CheckSnmpPing'
        check = NEW_CHECK_DEFINITIONS[check_name]

        data = {
            'hostUuid': '',
            'checkName': check_name,
            'hostConfig': TEST_HOSTCONFIG,
        }
        asyncio.run(check.run(data, {}))

    def test_my_check(self):
        check_name = 'MyCheck'
        check_conf = {'types': []}
        check = make_check(mi, check_name, check_conf)

        data = {
            'hostUuid': '',
            'checkName': check_name,
            'hostConfig': TEST_HOSTCONFIG,
        }
        asyncio.run(check.run(data, {}))

    def test_my_check_1(self):
        check_name = 'MyCheck'
        check_conf = {'types': [
            {'mib_obj': 'RFC1213-MIB::system', 'type_name': ''}
        ]}
        check = make_check(mi, check_name, check_conf)

        data = {
            'hostUuid': '',
            'checkName': check_name,
            'hostConfig': TEST_HOSTCONFIG,
        }
        asyncio.run(check.run(data, {}))


if __name__ == '__main__':
    suite = unittest.TestSuite()

    suite.addTest(TestMibs('test_'))

    suite.addTest(TestProbe('test_check'))
    suite.addTest(TestProbe('test_check_snmpv3'))
    suite.addTest(TestProbe('test_check_func'))
    suite.addTest(TestProbe('test_snmp_func'))
    suite.addTest(TestProbe('test_my_check'))
    suite.addTest(TestProbe('test_my_check_1'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
