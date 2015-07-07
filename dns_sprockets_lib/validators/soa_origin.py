'''
soa_origin - Zone test: SoaOrigin

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns_sprockets_lib.validators as validators


class SoaOrigin(validators.ZoneTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks for an SOA at zone origin.
    '''

    def run(self, context, suggested_tested):

        result = None
        if not context.soa_rdataset:
            result = 'No SOA record at origin.'
        return (suggested_tested, result)

# end of file
