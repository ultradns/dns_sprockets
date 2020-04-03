'''
rrsig_orphan - Record test: RrsigOrphan

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import time

import dns.rdtypes.ANY.RRSIG
import dns.dnssec

import dns_sprockets_lib.validators as validators


class RrsigOrphan(validators.RecTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks for orphan RRSIGs.
    '''
    TEST_DNSSECTYPE = True
    TEST_RRTYPE = 'RRSIG'
    TEST_OPTARGS = {
        'now': (None, 'Time to use for validating RRSIG time windows, e.g. 20150101123000'),
        'now_offset': (None, 'Number of seconds to offset the "now" value, e.g. -86400)')}

    def __init__(self, args):

        self.now = None
        self.now_offset = None
        super(RrsigOrphan, self).__init__(args)

        self.posix_now = (self.now
            and dns.rdtypes.ANY.RRSIG.sigtime_to_posixtime(self.now)
            or int(time.time()))
        if self.now_offset:
            self.posix_now += int(self.now_offset)

    def run(self, context, suggested_tested, name, ttl, rdata):
        # pylint: disable=too-many-arguments

        result = None

        # Make sure there's a covered RRSet for the RRSIG rdata:
        rdataset = context.zone_obj.get_rdataset(name, rdata.type_covered)
        if not rdataset:
            result = 'No RRSet for name: %s type: %s' % (
                name, dns.rdatatype.to_text(rdata.type_covered))
        else:
            try:
                dns.dnssec.validate_rrsig(
                    (name, rdataset),
                    rdata,
                    {context.zone_name: context.dnskey_rdataset},
                    now=self.posix_now)
            except dns.dnssec.UnsupportedAlgorithm as err:
                result = str(err)
            except dns.dnssec.ValidationFailure as err:
                result = str(err)

        return (suggested_tested, result)

# end of file
