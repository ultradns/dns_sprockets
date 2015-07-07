'''
nsec3_missing - RRSet test: Nsec3Missing

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns.rdatatype

import dns_sprockets_lib.dnssec_nsecx as nsecx
import dns_sprockets_lib.validators as validators


class Nsec3Missing(validators.RRSetTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks that all (non-NSEC3/RRSIG, non-delegated) RRSets are covered with an NSEC3.
    '''
    TEST_DNSSECTYPE = 'NSEC3'

    def run(self, context, suggested_tested, name, rdataset):

        tested = None
        result = None

        # Only run test if there's an NSEC3PARAM:
        nsec3param = (len(context.nsec3param_rdataset.items)
            and context.nsec3param_rdataset.items[0] or None)
        if nsec3param:

            # Only run test for non-NSEC3/RRSIG, non-delegated RRSets:
            if (rdataset.rdtype != dns.rdatatype.NSEC3
                and rdataset.rdtype != dns.rdatatype.RRSIG
                and not context.is_delegated(name)):

                tested = suggested_tested

                # Make sure there's an NSEC3 for the rdataset name:
                hashed_name = '%s.%s' % (
                    nsecx.hash_nsec3_name(
                        name,
                        nsec3param.salt,
                        nsec3param.algorithm,
                        nsec3param.iterations),
                    context.zone_name)
                nsec3_rdataset = context.zone_obj.get_rdataset(hashed_name, 'NSEC3')
                if not nsec3_rdataset:
                    result = 'No NSEC3\'s found for name: %s' % (hashed_name)

                if not result:

                    # Look in found nsec3_rdataset for an NSEC3 that covers the
                    # rdataset type:
                    got_one = False
                    for nsec3 in nsec3_rdataset.items:
                        if nsecx.covers(nsec3, rdataset.rdtype):
                            got_one = True
                            break

                    if not got_one:
                        result = 'No NSEC3 that covers type=%s for name: %s' % (
                            dns.rdatatype.to_text(rdataset.rdtype), hashed_name)

        return (tested, result)

# end of file
