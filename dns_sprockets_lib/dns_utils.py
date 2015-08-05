'''
dns_utils - Misc. DNS utility functions not present in dnspython.
-----------------------------------------------------------------

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns.name


def is_delegated(delegated_names, name):
    '''
    Tests a name to see if it is in a delegated zone.

    :param list delegated_names: List of non-apex dns.name.Names in zone with NS RRSets.
    :param obj name: The dns.name.Name to test.
    :return: True if name is delegated, False otherwise.
    '''
    for deleg_name in delegated_names:
        if name.is_subdomain(deleg_name):
            return True
    return False


def dns_name_cmp_to_key():
    '''
    Convert dns.name.Name.fullcompare method into a key= "function", which is a
    class suitable for the key= argument for sort/sorted.

    :return: Class that uses fullcompare() on dns.name.Name's.
    '''
    class Key(object):
        # pylint: disable=too-few-public-methods
        '''
        Wraps a dns.name.Name object with comparison operators that use the
        dns.name.Name.fullcompare() method.
        '''

        def __init__(self, obj, *_args):
            # pylint: disable=unused-argument
            ''' Ctor, initializes a Key instance. '''
            self.obj = obj

        def __lt__(self, other):
            ''' Less-than operator. '''
            return self.obj.fullcompare(other.obj)[1] < 0

        def __gt__(self, other):
            ''' Greater-than operator. '''
            return self.obj.fullcompare(other.obj)[1] > 0

        def __eq__(self, other):
            ''' Equality operator. '''
            return self.obj.fullcompare(other.obj)[1] == 0

        def __le__(self, other):
            ''' Less-than-or-equal operator. '''
            return self.obj.fullcompare(other.obj)[1] <= 0

        def __ge__(self, other):
            ''' Greater-than-or-equal operator. '''
            return self.obj.fullcompare(other.obj)[1] >= 0

        def __ne__(self, other):
            ''' Non-equality operator. '''
            return self.obj.fullcompare(other.obj)[1] != 0

    return Key


def dnssec_sort_names(names, reverse=False):
    '''
    Sorts names to DNSSEC sorted order.

    :param names: Container of dns.name.Names.
    :return: List of DNSSEC-sorted order dns.name.Names.
    '''
    return sorted(names, key=dns_name_cmp_to_key(), reverse=reverse)


def calc_node_names(node_names, ents_too, zone_name):
    '''
    Calculates list of node names in a zone (including any Empty Non-Terminals
    if 'ents_too' is True), ordered in DNSSEC name order.

    :param list node_names: The list of name objects from Zone.nodes.keys().
    :param bool ents_too: Set True to generate ENT names too.
    :param obj zone_name: Name of zone (used when 'ents_too' is True).
    :return: Sorted list of all node names.
    '''

    # Generate set of names (for lookups):
    names = frozenset(node_names)

    # If we want ENT's too, spin through names (in DNSSEC-order) and add them:
    ent_names = set()
    if ents_too:
        for name in dnssec_sort_names(node_names):

            # Chop-off most specific label and see if it is accounted for:
            pot_ent_name = dns.name.Name(name.labels[1:])
            while pot_ent_name.is_subdomain(zone_name):

                if pot_ent_name not in names:
                    ent_names.add(pot_ent_name)

                # Chop off next most specific lable and continue:
                pot_ent_name = dns.name.Name(pot_ent_name.labels[1:])

    # Gather all names and sort in DNSEC name order:
    return dnssec_sort_names(names | ent_names)

# end of file
