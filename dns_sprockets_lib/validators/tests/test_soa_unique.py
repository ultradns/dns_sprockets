'''
test_soa_unique - Tests soa_unique validator.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns_sprockets_lib.validators.tests.harness as harness


def test_soa_unique():

    (tests, errs) = harness.test_validator(
        test_name='soa_unique',
        zone_name='example',
        file_name='rfc4035_example.')
    assert tests == 1
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='soa_unique',
        zone_name='example',
        file_name='rfc5155_example.')
    assert tests == 1
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='soa_unique',
        zone_name='001.cst.net',
        file_name='001.cst.net.')
    assert tests == 1
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='soa_unique',
        zone_name='001.cst.net',
        file_name='001.cst.net._no_soa')
    assert tests == 1
    assert errs == 1

    (tests, errs) = harness.test_validator(
        test_name='soa_unique',
        zone_name='001.cst.net',
        file_name='001.cst.net._mult_soa')
    assert tests == 1
    assert errs == 1

# end of file

