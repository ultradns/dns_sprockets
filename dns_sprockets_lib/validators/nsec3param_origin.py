'''
nsec3param_origin - Zone test: Nsec3paramOrigin

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns_sprockets_lib.validators as validators


class Nsec3paramOrigin(validators.ZoneTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks for an NSEC3PARAM at zone origin for nsec3-type zones.
    '''
    TEST_DNSSECTYPE = 'NSEC3'

    def run(self, context, suggested_tested):

        result = None
        if not context.nsec3param_rdataset:
            result = 'No NSEC3PARAM record at origin.'
        return (suggested_tested, result)

# end of file
