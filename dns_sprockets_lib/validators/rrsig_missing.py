'''
rrsig_missing - RRSet test: RrsigMissing

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import time

import dns.rdatatype
import dns.rdtypes.ANY.RRSIG
import dns.dnssec

import dns_sprockets_lib.validators as validators


class RrsigMissing(validators.RRSetTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks that all (non-RRSIG, non-delegated) RRSets are covered with an RRSIG.
    '''
    TEST_DNSSECTYPE = True
    TEST_OPTARGS = {
        'now': (None, 'Time to use for validating RRSIG time windows, e.g. 20150101123000'),
        'now_offset': (None, 'Number of seconds to offset the "now" value, e.g. -86400)')}

    def __init__(self, args):

        self.now = None
        self.now_offset = None
        super(RrsigMissing, self).__init__(args)

        self.posix_now = (self.now
            and dns.rdtypes.ANY.RRSIG.sigtime_to_posixtime(self.now)
            or int(time.time()))
        if self.now_offset:
            self.posix_now += int(self.now_offset)

    def run(self, context, suggested_tested, name, rdataset):

        tested = None
        result = None

        # Only do this test for non-RRSIG, non-delegated RRSets:
        if (rdataset.rdtype != dns.rdatatype.RRSIG
            and not context.is_delegated(name)):

            tested = suggested_tested

            # Make sure there's a valid RRSIG for the rdataset:
            rrsigset = context.zone_obj.get_rdataset(
                name, 'RRSIG', covers=rdataset.rdtype)
            if not rrsigset:
                result = 'No RRSIG for name: %s' % (name)
            else:
                # Use dnspython's RRSIG validator:
                try:
                    dns.dnssec.validate(
                        (name, rdataset),
                        (name, rrsigset),
                        {context.zone_name: context.dnskey_rdataset},
                        now=self.posix_now)
                except dns.dnssec.UnsupportedAlgorithm as err:
                    result = str(err)
                except dns.dnssec.ValidationFailure as err:
                    result = str(err)

        return (tested, result)

# end of file
