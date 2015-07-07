'''
nsec_orphan - Record test: NsecOrphan

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns.rdatatype

import dns_sprockets_lib.dnssec_nsecx as nsecx
import dns_sprockets_lib.validators as validators


class NsecOrphan(validators.RecTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks for orphan or invalid-covers NSECs.
    '''
    TEST_DNSSECTYPE = 'NSEC'
    TEST_RRTYPE = 'NSEC'

    def run(self, context, suggested_tested, name, ttl, rdata):
        # pylint: disable=too-many-arguments

        result = None

        # Get the types covered by the NSEC and those in the node:
        covered_types = nsecx.get_covered_types(rdata)
        node = context.zone_obj.get_node(name)
        node_rdatasets = node and node.rdatasets or []
        node_types = [rdataset.rdtype for rdataset in node_rdatasets]

        # Check for any node types not covered:
        not_covered = [t for t in node_types if t not in covered_types]
        if not_covered:
            result = 'Doesn\'t cover types: %s' % (
                ' '.join([dns.rdatatype.to_text(t) for t in not_covered]))

        # Check for any extra covered types not needed:
        extra_covered = [t for t in covered_types if t not in node_types]
        if extra_covered:
            if not result:
                result = ''
            else:
                result += ' and '
            result += 'Covers non-existent RRSet types: %s' % (
                ' '.join([dns.rdatatype.to_text(t) for t in extra_covered]))

        return (suggested_tested, result)

# end of file
