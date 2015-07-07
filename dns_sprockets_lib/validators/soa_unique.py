'''
soa_unique - Zone test: SoaUnique

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns_sprockets_lib.validators as validators


class SoaUnique(validators.ZoneTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks for a single SOA in the zone.
    '''

    def run(self, context, suggested_tested):

        result = None

        # Insure there's only one SOA in the whole zone:
        soa_cnt = 0
        for (_, rdataset) in context.zone_obj.iterate_rdatasets(rdtype='SOA'):
            soa_cnt += len(rdataset)
        if soa_cnt == 0:
            result = 'No SOA in the zone'
        elif soa_cnt > 1:
            result = 'More than one SOA in the zone (count=%d)' % (soa_cnt)

        return (suggested_tested, result)

# end of file
