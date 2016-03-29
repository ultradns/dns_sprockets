'''
test_loader_classes - Tests dns_sprockets zone-loader-class loader functions.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns_sprockets_lib.loader_classes as loader_classes
from dns_sprockets_lib.loaders.file import File
from dns_sprockets_lib.loaders.xfr import Xfr


def test_load_all():

    loader_classes.load_all()
    assert 'file' in loader_classes.ALL_CLASSES
    assert loader_classes.ALL_CLASSES['file'] == File
    assert 'xfr' in loader_classes.ALL_CLASSES
    assert loader_classes.ALL_CLASSES['xfr'] == Xfr


def test__get_descriptions():

    got_file = False
    got_xfr = False
    for desc in loader_classes._get_descriptions():
        if desc[0] == 'file':
            got_file = True
        elif desc[0] == 'xfr':
            got_xfr = True
        assert desc[1] > ''
        assert isinstance(desc[2], dict)
    assert got_file
    assert got_xfr


def test_get_formatted_descriptions():

    desc = loader_classes.get_formatted_descriptions()
    assert 'file' in desc
    assert '(file_)allow_include' in desc
    assert 'xfr' in desc
    assert '(xfr_)timeout' in desc

# end of file
