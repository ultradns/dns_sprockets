'''
nsec3_orphan - Record test: Nsec3Orphan

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns.rdatatype

import dns_sprockets_lib.dnssec_nsecx as nsecx
import dns_sprockets_lib.validators as validators


class Nsec3Orphan(validators.RecTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks for orphan or invalid-covers NSEC3s.
    '''
    TEST_DNSSECTYPE = 'NSEC3'
    TEST_RRTYPE = 'NSEC3'

    def __init__(self, args):
        '''
        Ctor, initializes NSEC3-hashed names cache of all node names in zone.
        '''
        super(Nsec3Orphan, self).__init__(args)
        self.hashed_node_names = None

    def run(self, context, suggested_tested, name, ttl, rdata):
        # pylint: disable=too-many-arguments

        tested = None
        result = None

        # Only run test if there's an NSEC3PARAM:
        nsec3param = (len(context.nsec3param_rdataset.items) and
                      context.nsec3param_rdataset.items[0] or None)
        if nsec3param:
            tested = suggested_tested

            # Check and build hashed node names cache if necessary:
            if self.hashed_node_names is None:
                self.hashed_node_names = {}
                if self.args.verbose:
                    print('#  DICTIONARY OF HASHED NODE NAMES TO NODE NAMES:')
                for node_name in context.node_names:
                    hashed_node_name = nsecx.hash_nsec3_name(
                        node_name,
                        nsec3param.salt,
                        nsec3param.algorithm,
                        nsec3param.iterations)
                    self.hashed_node_names[hashed_node_name] = node_name
                    if self.args.verbose:
                        print('#  %s -> %s' % (hashed_node_name.upper(), node_name))

            # Get the NSEC3's lowercased hashed label from owner name:
            hashed_label = name.labels[0].lower().decode()

            # Insure the NSEC3 covers a node name in the zone:
            if hashed_label in self.hashed_node_names:
                node_name = self.hashed_node_names[hashed_label]

                # Get the types covered by those in the node:
                node = context.zone_obj.get_node(node_name)
                node_rdatasets = node and node.rdatasets or []
                node_types = [
                    rdataset.rdtype for rdataset in node_rdatasets
                    if rdataset.rdtype != dns.rdatatype.NSEC3]

                # Get the types covered by the NSEC3:
                covered_types = nsecx.get_covered_types(rdata)

                # Check for any node types not covered:
                not_covered = [t for t in node_types
                               if t not in covered_types]
                if not_covered:
                    result = 'Doesn\'t cover types: %s' % (
                        ' '.join([dns.rdatatype.to_text(t)
                                  for t in not_covered]))

                # Check for any extra covered types not needed:
                extra_covered = [t for t in covered_types
                                 if t not in node_types]
                if extra_covered:
                    if not result:
                        result = ''
                    else:
                        result += ' and '
                    result += 'Covers non-existent RRSet types: %s' % (
                        ' '.join([dns.rdatatype.to_text(t)
                                  for t in extra_covered]))
            else:
                result = 'Doesn\'t cover any RRSet in the zone'

        return (tested, result)

# end of file
