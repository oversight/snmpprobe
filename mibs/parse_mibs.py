import json
import os
from parser.grammar import MibsGrammar
from parser.parse_tree import parse_tree
from parser.utils import remove_comments_from_mib


MIBS_FOLDER = 'orig/'
MIB_JSON_FOLDER = 'parsed/'

GRAMMAR = MibsGrammar()


def read_mib_folder():
    for mib_name in os.listdir(MIBS_FOLDER):
        if os.path.exists(os.path.join(MIB_JSON_FOLDER, mib_name + '.json')):
            continue
        read_mib_file(mib_name)


def read_mib_file(mib_name):
    if os.path.exists(os.path.join(MIB_JSON_FOLDER, mib_name + '.json')):
        raise Exception('mib already parsed')

    with open(os.path.join(MIBS_FOLDER, mib_name)) as f:
        try:
            line = f.read()
        except UnicodeDecodeError:
            raise Exception('invalid mib')

    line = remove_comments_from_mib(line)
    res = GRAMMAR.parse(line)
    if not res.is_valid:
        raise Exception('invalid mib')

    node = res.tree.children[0]
    if node.children[5].children:
        for a in node.children[5].children[0].children[1].children:
            imib_name = a.children[2].string
            if not os.path.exists(os.path.join(MIBS_FOLDER, imib_name)):
                raise Exception(f'invalid mib: missing import {imib_name}')

    mibname, mib = parse_tree(node)
    if mibname != mib_name:
        raise Exception(f'invalid mib: filename != {mibname}')

    with open(os.path.join(MIB_JSON_FOLDER, mib_name + '.json'), 'w') as f:
        f.write(json.dumps(mib, indent=2))


if __name__ == '__main__':
    assert os.path.exists(MIBS_FOLDER)
    assert os.path.exists(MIB_JSON_FOLDER)
    read_mib_folder()
