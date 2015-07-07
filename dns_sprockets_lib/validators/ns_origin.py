'''
ns_origin - Zone test: NsOrigin

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns_sprockets_lib.validators as validators


class NsOrigin(validators.ZoneTest):
    # pylint: disable=too-few-public-methods
    '''
    Checks for at least one NS at zone origin.
    '''

    def run(self, context, suggested_tested):

        result = None
        if not context.zone_obj.get_rdataset(context.zone_name, 'NS'):
            result = 'No NS records at origin.'
        return (suggested_tested, result)

# end of file
