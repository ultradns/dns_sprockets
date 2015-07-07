'''
nsec_missing - RRSet test: NsecMissing

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns.rdatatype

import dns_sprockets_lib.dnssec_nsecx as nsecx
import dns_sprockets_lib.validators as validators


class NsecMissing(validators.RRSetTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks that all (non-NSEC/RRSIG, non-delegated) RRSets are covered with an NSEC.
    '''
    TEST_DNSSECTYPE = 'NSEC'

    def run(self, context, suggested_tested, name, rdataset):

        tested = None
        result = None

        # Only run test for non-NSEC/RRSIG, non-delegated RRSets:
        if (rdataset.rdtype != dns.rdatatype.NSEC
            and rdataset.rdtype != dns.rdatatype.RRSIG
            and not context.is_delegated(name)):

            tested = suggested_tested

            # Make sure there's an NSEC for the rdataset name:
            nsec_rdataset = context.zone_obj.get_rdataset(name, 'NSEC')
            if not nsec_rdataset:
                result = 'No NSEC\'s found for name: %s' % (name)

            if not result:

                # Look in found nsec_rdataset for an NSEC that covers the
                # rdataset type:
                got_one = False
                for nsec in nsec_rdataset.items:
                    if nsecx.covers(nsec, rdataset.rdtype):
                        got_one = True
                        break

                if not got_one:
                    result = 'No NSEC that covers type=%s for name: %s' % (
                        dns.rdatatype.to_text(rdataset.rdtype), name)

        return (tested, result)

# end of file
