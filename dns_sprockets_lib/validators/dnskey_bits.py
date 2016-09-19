'''
dnskey_bits - Record test: DnskeyBits

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns.rdtypes.ANY.DNSKEY

import dns_sprockets_lib.validators as validators


class DnskeyBits(validators.RecTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks DNSKEY flags and protocol.
    '''
    TEST_DNSSECTYPE = True
    TEST_RRTYPE = 'DNSKEY'

    def run(self, context, suggested_tested, name, ttl, rdata):
        # pylint: disable=too-many-arguments

        result = None
        if (rdata.flags & dns.rdtypes.dnskeybase.ZONE) and name != context.zone_name:
            result = 'Zone signing key not at zone apex'
        if rdata.protocol != 3:
            if result:
                result += ', and '
            else:
                result = ''
            result += 'Protocol not 3'
        return (suggested_tested, result)

# end of file
