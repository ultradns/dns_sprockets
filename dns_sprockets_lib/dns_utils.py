'''
dns_utils - Misc. DNS utility functions not present in dnspython.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns.name


def is_delegated(delegated_names, name):
    '''
    Tests a name to see if it is in a delegated zone.
    @param delegated_names List of non-apex dns.name.Names in zone with NS RRSets.
    @param name The dns.name.Name to test.
    @return True if name is delegated, False otherwise.
    '''
    for deleg_name in delegated_names:
        if name.is_subdomain(deleg_name):
            return True
    return False


def dns_name_cmp_to_key():
    '''
    Convert dns.name.Name.fullcompare method into a key= "function", which is a
    class suitable for the key= argument for sort/sorted.
    @return Class that uses fullcompare() on dns.name.Name's.
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
    @param names Container of dns.name.Names.
    @return List of DNSSEC-sorted order dns.name.Names.
    '''
    return sorted(names, key=dns_name_cmp_to_key(), reverse=reverse)


def calc_node_names(node_names):
    '''
    Calculates list of node names in a zone, including any Empty Non-Terminals
    implied by wildcard records, ordered in DNSSEC name order.
    @param node_names The list of names from Zone.nodes.keys().
    @return Sorted list of all node names.
    '''

    # Split explicit node names into wildcard and non-wildcard lists:
    names = []
    wc_names = []
    for name in node_names:
        if name.labels[0] == '*':
            wc_names.append(name)
        else:
            names.append(name)

    # Get list of wildcard base names:
    base_wc_names = [dns.name.Name(list(n.labels[1:])) for n in wc_names]

    # Add wildcard base names to names if not already accounted for:
    for base_wc_name in base_wc_names:
        if base_wc_name not in names:
            names.append(base_wc_name)

    # Sort wildcard base names most-specific to least:
    base_wc_names.sort(key=lambda n: len(n.labels), reverse=True)

    # For each non-wildcard name, look for any Empty Non-Terminals:
    ent_names = []
    for name in names:

        # Compare against all wildcard base names:
        for base_wc_name in base_wc_names:

            # If the name is a (non-equal) subdomain of the base wild card name,
            # then there are potential ENT's present:
            if name != base_wc_name and name.is_subdomain(base_wc_name):

                # First potential ENT is parent of name:
                pot_ent_name = dns.name.Name(list(name.labels[1:]))

                # While potential ENT is not equal to the base wildcard name:
                while pot_ent_name != base_wc_name:

                    # Add potential name if not already accounted for:
                    if pot_ent_name not in names + ent_names:
                        ent_names.append(pot_ent_name)

                    # Proceed to it's parent:
                    # pylint: disable=no-member
                    pot_ent_name = dns.name.Name(list(pot_ent_name.labels[1:]))

    # Gather all names and sort in DNSEC name order:
    return dnssec_sort_names(names + wc_names + ent_names)

# end of file
