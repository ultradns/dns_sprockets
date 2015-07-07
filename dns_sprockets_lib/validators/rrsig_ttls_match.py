'''
rrsig_ttls_match - Record test: RrsigTtlsMatch

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns_sprockets_lib.validators as validators


class RrsigTtlsMatch(validators.RecTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks RRSIG TTL's match original and covered TTL's.
    '''
    TEST_DNSSECTYPE = True
    TEST_RRTYPE = 'RRSIG'

    def run(self, context, suggested_tested, name, ttl, rdata):
        # pylint: disable=too-many-arguments

        result = None

        if ttl != rdata.original_ttl:
            result = 'TTL doesn\'t match original TTL'

        rdataset = context.zone_obj.get_rdataset(name, rdata.type_covered)
        if rdataset and ttl != rdataset.ttl:
            if result:
                result += ', and '
            else:
                result = ''
            result += 'TTL doesn\'t match covered TTL'

        return (suggested_tested, result)

# end of file
