'''
nsecx_ttls_match - Record test: NsecxTtlsMatch

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns_sprockets_lib.validators as validators


class NsecxTtlsMatch(validators.RecTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks that NSECx TTL's match SOA's minimum.
    '''
    TEST_DNSSECTYPE = True
    TEST_RRTYPE = 'NSEC,NSEC3'

    def run(self, context, suggested_tested, name, ttl, rdata):
        # pylint: disable=too-many-arguments

        tested = None
        result = None

        # Only run TTL test if there's an SOA:
        soa = (len(context.soa_rdataset.items)
            and context.soa_rdataset.items[0] or None)
        if soa:
            tested = suggested_tested

            # Check the NSECx's TTL is same as SOA minimum TTL:
            if ttl != soa.minimum:
                result = 'NSECx TTL=%d doesn\'t match SOA minimum=%d' % (
                    ttl, soa.minimum)

        return (tested, result)

# end of file
