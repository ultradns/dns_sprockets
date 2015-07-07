'''
rrsig_covers - Record test: RrsigCovers

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns.rdatatype

import dns_sprockets_lib.validators as validators


class RrsigCovers(validators.RecTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks RRSIG's don't cover RRSIG's.
    '''
    TEST_DNSSECTYPE = True
    TEST_RRTYPE = 'RRSIG'

    def run(self, context, suggested_tested, name, ttl, rdata):
        # pylint: disable=too-many-arguments

        result = None
        if rdata.type_covered == dns.rdatatype.RRSIG:
            result = 'Covers another RRSIG'
        return (suggested_tested, result)

# end of file
