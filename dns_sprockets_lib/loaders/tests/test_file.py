'''
test_file - Tests dns_sprockets_lib.loaders.file module.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns.rdatatype
import dns.zone

from dns_sprockets_lib.loaders.file import File


def test_File():

    class test_args(object):
        source = 'dns_sprockets_lib/tests/data/001.cst.net.'
        zone = '001.cst.net'

    test_file = File(test_args())
    assert test_file.rdclass == 'IN'
    assert test_file.allow_include == '1'

    zone_obj = test_file.run()
    assert isinstance(zone_obj, dns.zone.Zone)
    assert zone_obj.get_rdataset('001.cst.net.', dns.rdatatype.SOA)

# end of file
