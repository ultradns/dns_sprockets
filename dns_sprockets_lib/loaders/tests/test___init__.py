'''
test___init__ - Tests dns_sprockets_lib.loaders package.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns_sprockets_lib.loaders as loaders


def test_ZoneLoader():

    class TestZoneLoader(loaders.ZoneLoader):
        LOADER_OPTARGS = {'now': ('20150101000000', 'Time to use for now')}

    class test_args(object):
        verbose = True
        test_zone_loader_now = '20151231000000'

    loader = TestZoneLoader(test_args())
    assert loader.LOADER_NAME == 'test_zone_loader'
    assert not hasattr(loader, 'verbose')
    assert loader.now == test_args.test_zone_loader_now

# end of file
