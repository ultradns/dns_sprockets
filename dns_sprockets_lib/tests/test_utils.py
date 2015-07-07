'''
test_utils - Tests dns_sprockets utils functions.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns_sprockets_lib.utils as utils
import dns_sprockets_lib.tests


def test_public_modules_in_package():

    mods = utils.public_modules_in_package(dns_sprockets_lib.tests)
    assert 'test_utils' in mods
    assert '__init__' not in mods


def test_camelcase_to_underscores():

    tests = [
        ('', ''),
        ('test_me', 'test_me'),
        ('testMe', 'test_me'),
        ('TestMe', 'test_me'),
        ('Test4Me', 'test4_me')]

    for test in tests:
        assert utils.camelcase_to_underscores(test[0]) == test[1]


def test_underscores_to_camelcase():

    tests = [
        ('', ''),
        ('test_me', 'TestMe'),
        ('Test_Me', 'TestMe'),
        ('test4_me', 'Test4Me'),
        ('test_4me', 'Test4me'),
        ('test_4_me', 'Test4Me')]

    for test in tests:
        assert utils.underscores_to_camelcase(test[0]) == test[1]

# end of file
