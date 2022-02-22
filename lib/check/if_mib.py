from collections import Counter

'''
ifSpeed OBJECT-TYPE
    SYNTAX      Gauge32
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
            "An estimate of the interface's current bandwidth in bits
            per second.  For interfaces which do not vary in bandwidth
            or for those where no accurate estimation can be made, this
            object should contain the nominal bandwidth.  If the
            bandwidth of the interface is greater than the maximum value
            reportable by this object then this object should report its
            maximum value (4,294,967,295) and ifHighSpeed must be used
            to report the interace's speed.  For a sub-layer which has
            no concept of bandwidth, this object should be zero."
    ::= { ifEntry 5 }

ifHighSpeed OBJECT-TYPE
    SYNTAX      Gauge32
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION
            "An estimate of the interface's current bandwidth in units
            of 1,000,000 bits per second.  If this object reports a
            value of `n' then the speed of the interface is somewhere in
            the range of `n-500,000' to `n+499,999'.  For interfaces
            which do not vary in bandwidth or for those where no
            accurate estimation can be made, this object should contain
            the nominal bandwidth.  For a sub-layer which has no concept
            of bandwidth, this object should be zero."
    ::= { ifXEntry 15 }
'''


def if_mib(state_data):
    if 'interface' in state_data:
        counts = Counter()
        new = {}
        for item in state_data['interface'].values():
            if 'ifDescr' not in item:
                # this can occur when ifEntry fails but ifXEntry not
                # ignore item
                continue

            name = item['ifDescr']
            idx = counts[name]
            counts[name] += 1
            # compat itemname ('_' instead of '#')
            item['name'] = name_with_suffix = f'{name}_{idx}' if idx else name
            new[name_with_suffix] = item

            if 'ifHCInOctets' in item:
                item['ifInOctets'] = item.pop('ifHCInOctets')
            if 'ifHCOutOctets' in item:
                item['ifOutOctets'] = item.pop('ifHCOutOctets')

            if 'ifSpeed' in item and 'ifHighSpeed' in item:
                # max value for this metric, shown if value is overloading
                if (item['ifSpeed'] == 4294967295
                        and item['ifHighSpeed'] != 4294):
                    # ifspeed is in bits, ifHighSpeed in MBits.
                    item['ifSpeed'] = item['ifHighSpeed'] * 1000000

        state_data['interface'] = new

    return state_data
