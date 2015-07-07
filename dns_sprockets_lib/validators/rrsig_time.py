'''
rrsig_time - Record test: RrsigTime

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns_sprockets_lib.validators as validators


class RrsigTime(validators.RecTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks RRSIG's inception <= expiration.
    '''
    TEST_DNSSECTYPE = True
    TEST_RRTYPE = 'RRSIG'

    def run(self, context, suggested_tested, name, ttl, rdata):
        # pylint: disable=too-many-arguments

        result = None
        if rdata.inception > rdata.expiration:
            result = 'Inception time greater than expiration time'
        return (suggested_tested, result)

# end of file
