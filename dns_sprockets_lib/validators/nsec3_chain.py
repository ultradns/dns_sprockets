'''
nsec3_chain - Zone test: Nsec3Chain

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import base64

import dns.rdtypes.ANY.NSEC3

import dns_sprockets_lib.validators as validators


class Nsec3Chain(validators.ZoneTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks for valid NSEC3 chain.
    '''
    TEST_DNSSECTYPE = 'NSEC3'

    def run(self, context, suggested_tested):

        # Get all the NSEC3's in a name[0].upper() -> nsec3_rdata dict:
        nsec3_dict = dict(
            [(nsec3[0].labels[0].upper(), nsec3[1][0])
             for nsec3 in context.zone_obj.iterate_rdatasets('NSEC3')])

        # Check there's at least one NSEC3:
        if len(nsec3_dict) == 0:
            return (suggested_tested, 'No NSEC3s in the zone')

        result = None

        # Pick any one as the first, and follow the chain, should end up on same
        # one after len(nsec3_dict) hops.  Also keep track of number of times
        # an NSEC3's next value is less than the name[0]; it should be exactly
        # one, for a correctly constructed chain:
        for (first_name, nsec3_rdata) in nsec3_dict.items():
            break
        # pylint: disable=undefined-loop-variable
        name = first_name
        next_less_than_name_cnt = 0
        for _ in range(len(nsec3_dict)):

            # Encode the next name:
            next_name = base64.b32encode(nsec3_rdata.next).translate(
                dns.rdtypes.ANY.NSEC3.b32_normal_to_hex)

            # Count number of times NSEC3's next is less than name:
            if next_name < name:
                next_less_than_name_cnt += 1

            # Make sure there's an NSEC3 for the next name:
            if next_name not in nsec3_dict:
                result = 'Chain broken at %s (next=%s doesn\'t exist)' % (
                    name, next_name)
                break

            name = next_name
            nsec3_rdata = nsec3_dict[name]

        if not result and name != first_name:
            result = 'Chain walk didn\'t end up on start item'

        if not result and len(nsec3_dict) > 1 and next_less_than_name_cnt != 1:
            result = 'Chain not ordered correctly'

        return (suggested_tested, result)

# end of file
