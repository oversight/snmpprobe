from pyleri.grammar import Grammar
from pyleri.repeat import Repeat
from pyleri.sequence import Sequence
from pyleri.regex import Regex
from pyleri.choice import Choice
from pyleri.optional import Optional
from pyleri.keyword import Keyword
from pyleri.list import List


class MibsGrammar(Grammar):
    # RE_KEYWORDS = re.compile('^[A-Z-]+')
    # tk = Token('::=')
    r_dec = Regex(r'[\d-]+')
    r_hex = Regex("'.*?'[hH]")
    r_bin = Regex("'.*?'[bB]")
    r_objname = Regex(r'[\w\-]+')
    r_objname2 = Regex(r'[A-Z][\w\-]+')
    r_quotes = Regex('\"(.|\n)*?\"')

    s_value_key = Sequence(r_objname, '(', r_dec, ')')
    s_accolades_map_itm = Sequence(
        r_objname, '(', Choice(r_dec, r_hex, most_greedy=False), ')')
    s_accolades_map = Sequence('{', List(s_accolades_map_itm), '}')
    s_accolades_list = Sequence('{', List(r_objname), '}')
    s_oid = Sequence('{', Repeat(Choice(r_dec, r_objname, s_value_key)), '}')
    s_sub_types_int = Sequence(
        '(',
        List(
            List(Choice(r_dec, r_hex, r_bin, most_greedy=False), '..', 1, 2),
            '|',
            1), ')')
    s_sub_types_octetstring = Sequence(
        '(', 'SIZE', '(', List(
            List(Choice(r_dec, r_hex, r_bin, most_greedy=False), '..', 1, 2),
            '|',
            1), ')', ')')

    s_val_int = Sequence('INTEGER', Optional(s_sub_types_int))
    s_val_int_map = Sequence('INTEGER', s_accolades_map)
    s_val_bit_map = Sequence('BITS', s_accolades_map)
    s_val_octetstring = Sequence(
        'OCTET STRING', Optional(s_sub_types_octetstring))
    s_val_objectidentifier = Sequence('OBJECT IDENTIFIER')
    s_val_sequenceof = Sequence('SEQUENCE OF', r_objname2)
    s_val_other_map = Sequence(r_objname2, s_accolades_map)
    s_val_other = Sequence(r_objname2, Repeat(
        Choice(s_sub_types_octetstring, s_sub_types_int, most_greedy=False),
        0,
        1))
    s_val_sequence = Sequence(
        'SEQUENCE',
        '{',
        List(Sequence(
            r_objname,
            Choice(
                s_val_octetstring,
                s_val_objectidentifier,
                s_val_int_map,
                s_val_int,
                s_val_other,
                most_greedy=False))), '}')  # s_accolades map ok?

    c_syntax = Choice(
        s_val_sequenceof,
        s_val_int_map,
        s_val_int,
        s_val_bit_map,
        s_val_octetstring,
        s_val_objectidentifier,
        s_val_other_map,
        s_val_other,
        most_greedy=False)

    s_status = Sequence('STATUS', Choice(
        'current',
        'deprecated',
        'obsolete',
        most_greedy=False))
    s_status_ = Sequence('STATUS', Choice(
        'mandatory',
        'optional',
        'obsolete',
        'deprecated',
        most_greedy=False))
    s_description = Sequence('DESCRIPTION', r_quotes)
    s_access_ = Sequence('ACCESS', Choice(
        'read-only', 'read-write', 'write-only', 'not-accessible', most_greedy=False))
    s_access = Sequence('MAX-ACCESS', Choice(
        'not-accessible',
        'accessible-for-notify',
        'read-only',
        'read-write',
        'read-create',
        most_greedy=False))
    s_index = Sequence(
        'INDEX',
        '{',
        List(Sequence(Optional('IMPLIED'), r_objname)),
        '}')
    s_defval = Sequence(
        'DEFVAL',
        Sequence(
            '{',
            Choice(
                r_quotes,
                r_hex,
                r_bin,
                s_accolades_list,
                Sequence('{', Repeat(r_dec, 1), '}'),
                r_objname,
                most_greedy=False), '}'))
    s_units = Sequence('UNITS', r_quotes)
    s_reference = Sequence('REFERENCE', r_quotes)
    s_augments = Sequence('AUGMENTS', '{', r_objname, '}')
    s_objects = Sequence('OBJECTS', s_accolades_list)
    s_displayhint = Sequence('DISPLAY-HINT', r_quotes)
    s_notifications = Sequence('NOTIFICATIONS', s_accolades_list)
    s_lastupdated = Sequence('LAST-UPDATED', r_quotes)  # rfc5878 ExtUTCTime
    s_organization = Sequence('ORGANIZATION', r_quotes)
    s_contactinfo = Sequence('CONTACT-INFO', r_quotes)
    s_revision = Sequence('REVISION', r_quotes, 'DESCRIPTION', r_quotes)
    s_productrelease = Sequence('PRODUCT-RELEASE', r_quotes)
    s_enterprice = Sequence('ENTERPRISE', r_objname)
    s_variables = Sequence('VARIABLES', s_accolades_list)
    s_syntax = Sequence('SYNTAX', c_syntax)
    s_val_textualconvention = Sequence(
        'TEXTUAL-CONVENTION',
        Repeat(s_displayhint, 0, 1),
        s_status,
        s_description,
        Repeat(s_reference, 0, 1),
        s_syntax)

    s_objidentifier = Sequence('OBJECT', 'IDENTIFIER', '::=', s_oid)

    # rfc1212
    s_objtyp_ = Sequence(
        'OBJECT-TYPE',
        s_syntax,  #
        s_access_,
        s_status_,
        Repeat(s_description, 0, 1),
        Repeat(s_reference, 0, 1),
        Repeat(s_index, 0, 1),  #
        Repeat(s_augments, 0, 1),  #
        Repeat(s_defval, 0, 1),  #
        '::=',
        s_oid,
    )

    # rfc1215
    s_traptyp = Sequence(
        'TRAP-TYPE',
        s_enterprice,
        Repeat(s_variables, 0, 1),
        Repeat(s_description, 0, 1),
        Repeat(s_reference, 0, 1),
        '::=',
        r_dec,
    )

    # rfc2578
    s_moduleidentity = Sequence(
        'MODULE-IDENTITY',
        s_lastupdated,
        s_organization,
        s_contactinfo,
        s_description,
        Repeat(s_revision),
        '::=',
        s_oid,
    )

    s_objidentity = Sequence(
        'OBJECT-IDENTITY',
        s_status,
        s_description,
        Repeat(s_reference, 0, 1),
        '::=',
        s_oid,
    )

    s_objtyp = Sequence(
        'OBJECT-TYPE',
        s_syntax,  #
        Repeat(s_units, 0, 1),
        s_access,
        s_status,
        s_description,
        Repeat(s_reference, 0, 1),
        Repeat(s_index, 0, 1),  #
        Repeat(s_augments, 0, 1),  #
        Repeat(s_defval, 0, 1),  #
        '::=',
        s_oid,
    )

    s_notificationtyp = Sequence(
        'NOTIFICATION-TYPE',
        Repeat(s_objects, 0, 1),  #
        s_status,
        s_description,
        Repeat(s_reference, 0, 1),
        '::=',
        s_oid,
    )

    # rfc2580
    s_objgroup = Sequence(
        'OBJECT-GROUP',
        s_objects,
        s_status,
        s_description,
        Repeat(s_reference, 0, 1),
        '::=',
        s_oid,
    )

    s_notificationgroup = Sequence(
        'NOTIFICATION-GROUP',
        s_notifications,
        s_status,
        s_description,
        Repeat(s_reference, 0, 1),
        '::=',
        s_oid,
    )

    s_modulecompliance = Sequence(
        'MODULE-COMPLIANCE',
        s_status,
        s_description,
        Repeat(s_reference, 0, 1),
        Sequence('MODULE', Repeat(Choice(
            Sequence(
                'OBJECT',
                r_objname,
                Repeat(Sequence('SYNTAX', c_syntax), 0, 1),
                Repeat(Sequence('WRITE-SYNTAX', c_syntax), 0, 1),
                Repeat(Sequence(
                    'MIN-ACCESS',
                    Choice(
                        'not-accessible',
                        'accessible-for-notify',
                        'read-only',
                        'read-write',
                        'read-create',
                        most_greedy=False)), 0, 1),
                s_description,
            ),
            Sequence('GROUP', r_objname, s_description),
            Sequence('MANDATORY-GROUPS', s_accolades_list),
            r_objname2,  # modulename
        ))),
        '::=',
        s_oid,
    )

    s_agentcapabilities = Sequence(
        'AGENT-CAPABILITIES',
        s_productrelease,
        Sequence('STATUS', Choice('current', 'obsolete', most_greedy=False)),
        s_description,
        Repeat(s_reference, 0, 1),
        Repeat(Sequence(
            Sequence('SUPPORTS', r_objname),
            Sequence('INCLUDES', s_accolades_list),
            Repeat(Sequence(
                'VARIATION', r_objname,
                Repeat(Sequence('SYNTAX', c_syntax), 0, 1),
                Repeat(Sequence('WRITE-SYNTAX', c_syntax), 0, 1),
                Repeat(Sequence(
                    'ACCESS',
                    Choice(
                        'not-implemented',
                        'accessible-for-notify',
                        'read-only',
                        'read-write',
                        'read-create',
                        'write-only',
                        most_greedy=False)), 0, 1),
                Repeat(Sequence('CREATION-REQUIRES', s_accolades_list), 0, 1),
                Repeat(s_defval, 0, 1),
                Sequence('DESCRIPTION', r_quotes)
            )),
        )),
        '::=',
        s_oid,
    )

    mib_kv = Sequence(r_objname, Choice(
        # KV-types
        s_agentcapabilities,
        s_moduleidentity,
        s_modulecompliance,
        s_notificationtyp,
        s_notificationgroup,
        s_objidentifier,
        s_objidentity,
        s_objgroup,
        s_objtyp,
        s_objtyp_,
        s_traptyp,
        most_greedy=False))

    s_val_choice = Sequence('CHOICE', Regex('{(.|\n)*?}'))
    s_val_implicit = Sequence(
        Regex(r'\[.*?\]'),
        'IMPLICIT',
        Choice(s_val_int, s_val_octetstring, most_greedy=False))

    mib_v = Sequence(r_objname2, '::=', Choice(
        # V-types
        s_val_sequence,
        s_val_textualconvention,
        s_val_octetstring,
        s_val_int_map,
        s_val_int,
        s_val_choice,  # smi
        s_val_objectidentifier,  # smi
        s_val_other,
        s_val_implicit,  # smi
        most_greedy=False))

    s_macro = Sequence(
        Regex(r'[A-Z\-]+'), 'MACRO', '::=', Regex('BEGIN(.|\n)*?END'))

    mib_imports = Repeat(Sequence(
        'IMPORTS',
        Repeat(Sequence(List(r_objname), 'FROM', r_objname)), ';'), 0, 1)
    mib_exports = Repeat(Sequence('EXPORTS', List(r_objname), ';'), 0, 1)

    rp_obj_def = Repeat(Choice(
        mib_v,
        mib_kv,
        s_macro,
        most_greedy=False))

    START = Sequence(
        r_objname,
        'DEFINITIONS',
        '::=',
        'BEGIN',
        mib_exports,
        mib_imports,
        rp_obj_def,
        'END'
    )
