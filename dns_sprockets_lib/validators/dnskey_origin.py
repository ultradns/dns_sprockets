'''
dnskey_origin - Zone test: DnskeyOrigin

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns.rdtypes.ANY.DNSKEY

import dns_sprockets_lib.validators as validators


class DnskeyOrigin(validators.ZoneTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks for a ZSK at zone origin.
    '''
    TEST_DNSSECTYPE = True

    def run(self, context, suggested_tested):

        result = None
        zsk_count = 0
        dnskeys = context.dnskey_rdataset and context.dnskey_rdataset.items or []
        for rdata in dnskeys:
            if rdata.flags & dns.rdtypes.dnskeybase.ZONE:
                zsk_count += 1
        if zsk_count == 0:
            result = 'No ZSK found at origin'
        return (suggested_tested, result)

# end of file
