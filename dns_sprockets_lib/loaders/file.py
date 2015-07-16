'''
file - Zone loader: File
------------------------

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns.rdataclass
import dns.zone

import dns_sprockets_lib.loaders as loaders


class File(loaders.ZoneLoader):
    # pylint: disable=too-few-public-methods
    '''
    Loads a zone from a file in AXFR-type or Bind host-type format.
    '''
    LOADER_OPTARGS = {
        'rdclass': ('IN', 'Class of records to pull'),
        'allow_include': ('1', 'Allow file to include other files')}

    def __init__(self, args):
        '''
        Ctor.

        :param obj args: The application's command-line arguments object.
        '''
        self.rdclass = None
        self.allow_include = None
        super(File, self).__init__(args)

    def run(self):
        '''
        :return: A dns.zone.Zone instance.
        '''
        other_args = {
            'origin': self.args.zone,
            'relativize': False,
            'filename': self.args.source,
            'check_origin': False,
            'rdclass': dns.rdataclass.from_text(self.rdclass),
            'allow_include': bool(int(self.allow_include))}

        return dns.zone.from_file(self.args.source, **other_args)

# end of file
