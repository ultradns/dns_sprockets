'''
dnssectype_ambiguous - Zone test: DnssectypeAmbiguous

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns_sprockets_lib.validators as validators


class DnssectypeAmbiguous(validators.ZoneTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks for existence of both NSEC and NSEC3 in the zone.
    '''

    def run(self, context, suggested_tested):

        result = None

        # Insure there's just NSEC's or just NSEC3's in the zone:
        has_nsec = next(context.zone_obj.iterate_rdatasets('NSEC'), None)
        has_nsec3 = next(context.zone_obj.iterate_rdatasets('NSEC3'), None)
        if has_nsec and has_nsec3:
            result = 'Zone has both NSEC and NSEC3 records'

        # If that's ok, see if there's an NSEC3PARAM and NSEC's:
        if not result and has_nsec and context.nsec3param_rdataset:
            result = 'Zone has NSEC3PARAM and NSEC records'

        return (suggested_tested, result)

# end of file
