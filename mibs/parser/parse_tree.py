V_FUNS = {
    's_val_textualconvention': lambda n: {
        'tp': n.children[0].string,
        'syntax': parse_syntax(n.children[5]),
        'display_hint': parse_display_hint(n.children[1]),
    },
    's_val_objectidentifier': lambda n: {
        'tp': n.children[0].string,
    },
    's_val_octetstring': lambda n: {
        'tp': n.children[0].string,
    },
    's_val_int': lambda n: {
        'tp': n.children[0].string,
    },
    's_val_int_map': lambda n: {
        'tp': n.children[0].string,
        'values': parse_map(n)
    },
    's_val_bit_map': lambda n: {
        'tp': n.children[0].string,
        'values': parse_map(n)
    },
    's_val_other': lambda n: {
        'tp': n.children[0].string,
    },
    's_val_sequence': lambda n: {
        'tp': n.children[0].string,
    },
    's_val_sequenceof': lambda n: {
        'tp': n.string,
    },
}
KV_FUNS = {
    's_objtyp': lambda n: {
        'tp': 'OBJECT-TYPE',
        # 'description': parse_description(n.children[5],
        'syntax': parse_syntax(n.children[1]),
        'index': parse_index(n.children[-5]) or parse_augments(n.children[-4]),
        'value': parse_oid(n.children[-1]),
    },
    's_objtyp_': lambda n: {
        'tp': 'OBJECT-TYPE',
        # 'description': n.children[5].children else n.children[3]),
        'syntax': parse_syntax(n.children[1]),
        'index': parse_index(n.children[-5]) or parse_augments(n.children[-4]),
        'value': parse_oid(n.children[-1]),
    },
    's_objidentity': lambda n: {
        'tp': 'OBJECT-IDENTITY',
        # 'description': parse_description(n.children[2]),
        'value': parse_oid(n.children[-1]),
    },
    's_objidentifier': lambda n: {
        'tp': 'OBJECT IDENTIFIER',
        'value': parse_oid(n.children[-1]),
    },
    's_moduleidentity': lambda n: {
        'tp': 'MODULE-IDENTITY',
        'value': parse_oid(n.children[-1]),
    },
    's_objgroup': lambda n: {
        'tp': 'OBJECT-GROUP',
        'value': parse_oid(n.children[-1]),
    },
}


def parse_map(node):
    lu = {}
    for i, n in enumerate(node.children[1].children[1].children):
        if i % 2 == 0:
            k = int(n.children[2].string)
            v = n.children[0].string
            lu[k] = v
    return lu


def parse_augments(node):
    if node.children:
        return node.children[0].children[2].string


def parse_index(node):
    if node.children:
        columns = []
        for i, n in enumerate(node.children[0].children[2].children):
            if i % 2 == 0:
                columns.append(n.string)
        return columns


def parse_display_hint(node):
    if node.children:
        return node.children[0].children[-1].string[1:-1]


def parse_description(node):
    if node.children:
        return node.children[1].string.strip()


def parse_oid(node):
    if len(node.children[1].children) < 2:
        raise Exception('! oid length: {}'.format(node.string))
    path = []
    for i, a in enumerate(node.children[1].children):
        if a.children[0].element.name == 'r_dec':
            path += (int(a.string), )
        elif a.children[0].element.name == 's_value_key':
            path += (int(a.children[0].children[2].string), )
        elif not i and a.children[0].element.name == 'r_objname':
            path += (a.string, )
        else:
            raise Exception('! oid: {}'.format(node.string))
    return path


def parse_syntax(node):
    a = node.children[-1].children[0]
    tp = a.element.name
    return V_FUNS[tp](a)


def parse_tree(node):
    lk_definitions = {
        'Counter',
        'Counter32',
        'Counter64',
        'Gauge',
        'Gauge32',
        'Integer32',
        'IpAddress',
        'NetworkAddress',
        'Opaque',
        'TimeTicks',
        'Unsigned32',
    }

    mib = {}
    mib['IMPORTS'] = [
        [a.children[2].string, [n.string for i, n in enumerate(a.children[0].children) if i % 2 == 0]]
        for a in node.children[5].children[0].children[1].children
    ] if node.children[5].children else []

    for a in node.children[6].children:
        if a.children[0].element.name == 'mib_v':
            name = a.children[0].children[0].string
            node_ = a.children[0].children[-1].children[0]
            tp = node_.element.name
            # skip predefined type assignments
            if name in lk_definitions:
                continue
            if tp in V_FUNS:
                mib[name] = V_FUNS[tp](node_)

        elif a.children[0].element.name == 'mib_kv':
            name = a.children[0].children[0].string
            node_ = a.children[0].children[-1].children[0]
            tp = a.children[0].children[-1].children[0].element.name
            if tp in KV_FUNS:
                mib[name] = KV_FUNS[tp](node_)

    return node.children[0].string, mib
