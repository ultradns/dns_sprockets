'''
__init__.py - Loaders for "dns_sprockets" zone validator.
---------------------------------------------------------

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns_sprockets_lib.utils as utils


#
# For validator classes, use short docstrings, which will be used for the actual
# test descriptions!
#


class ZoneLoader(object):
    # pylint: disable=too-few-public-methods
    '''
    [Base class for zone loaders]
    '''
    LOADER_NAME = None  # Automatically set in __init__.
    LOADER_OPTARGS = {}  # Override possible!  e.g.: {'now': (None, 'Time to use for now')}

    def __init__(self, args):
        '''
        Ctor, caches the arguments used to run the application, and grabs any
        optional test arguments.
        '''
        # pylint: disable=invalid-name
        self.LOADER_NAME = utils.camelcase_to_underscores(self.__class__.__name__)
        self.args = args

        utils.process_optargs(self.LOADER_OPTARGS, self.LOADER_NAME, self)

    def run(self):
        '''
        Runs the zone loader -- must override!

        :return: A dns.zone.Zone instance.
        '''
        pass

# end of file
