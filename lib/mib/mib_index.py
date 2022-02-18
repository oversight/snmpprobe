import json
import os
from .mib import on_mib
from .tc import MIB_TEXTUAL_CONVENTIONS


MIB_JSON_FOLDER = 'mibs/parsed/'


class MibIndex(dict):

    def __init__(self):
        # RFC1213-MIB is obsoleted by SNMPv2-SMI
        # loaded definitions are updated by on_mib, therefore it is important
        # to first load old MIBS
        self.read_mib('RFC1213-MIB')

        for fn in os.listdir(MIB_JSON_FOLDER):
            if fn[:-5] not in self:
                self.read_mib(fn[:-5])

    def read_mib(self, mibname):
        with open(os.path.join(MIB_JSON_FOLDER, mibname + '.json')) as f:
            mib = json.load(f)

        for imibname, _ in mib['IMPORTS']:
            if imibname not in self:
                self.read_mib(imibname)

        # custom TEXTUAL CONVENTIONS
        lk_definitions = MIB_TEXTUAL_CONVENTIONS.get(mibname, {})
        on_mib(mibname, mib, self, lk_definitions)
