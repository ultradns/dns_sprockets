'''
rrsig_signer_match - Record test: RrsigSignerMatch

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns_sprockets_lib.validators as validators


class RrsigSignerMatch(validators.RecTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks RRSIG signers match the zone.
    '''
    TEST_DNSSECTYPE = True
    TEST_RRTYPE = 'RRSIG'

    def run(self, context, suggested_tested, name, ttl, rdata):
        # pylint: disable=too-many-arguments

        result = None
        if rdata.signer != context.zone_name:
            result = 'Signer not zone name'
        return (suggested_tested, result)

# end of file
