'''
nsec_chain - Zone test: NsecChain

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns.name

import dns_sprockets_lib.validators as validators


class NsecChain(validators.ZoneTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks for valid NSEC chain.
    '''
    TEST_DNSSECTYPE = 'NSEC'

    def run(self, context, suggested_tested):

        # Get all the NSEC's in a name.upper() -> nsec_rdata dict:
        nsec_dict = dict(
            [(str(nsec[0]).upper(), nsec[1][0]) for nsec
             in context.zone_obj.iterate_rdatasets('NSEC')])

        # Check there's at least one NSEC:
        if len(nsec_dict) == 0:
            return (suggested_tested, 'No NSECs in the zone')

        result = None

        # Pick any one as the first, and follow the chain, should end up on same
        # one after len(nsec_dict) hops.  Also keep track of number of times
        # an NSEC's next value is canonically less than the name[0]; it should
        # be exactly one, for a correctly constructed chain:
        for (first_name, nsec_rdata) in nsec_dict.items():
            break
        # pylint: disable=undefined-loop-variable
        name = first_name
        next_less_than_name_cnt = 0
        for _ in range(len(nsec_dict)):

            # Get the next name upper'd:
            next_name = str(nsec_rdata.next).upper()

            # Count number of times NSEC's next is canonically less than name:
            (_, order, _) = dns.name.from_text(next_name).fullcompare(
                dns.name.from_text(name))
            if order < 0:
                next_less_than_name_cnt += 1

            # Make sure there's an NSEC for the next name:
            if next_name not in nsec_dict:
                result = 'Chain broken at %s (next=%s doesn\'t exist)' % (
                    name, next_name)
                break

            name = next_name
            nsec_rdata = nsec_dict[name]

        if not result and name != first_name:
            result = 'Chain walk didn\'t end up on start item'

        if not result and len(nsec_dict) > 1 and next_less_than_name_cnt != 1:
            result = 'Chain not ordered correctly'

        return (suggested_tested, result)

# end of file
