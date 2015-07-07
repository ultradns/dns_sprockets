'''
test_dnskey_origin - Tests dnskey_origin validator.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns_sprockets_lib.validators.tests.harness as harness


def test_dnskeys():

    (tests, errs) = harness.test_validator(
        test_name='dnskey_origin',
        zone_name='example',
        file_name='rfc4035_example.')
    assert tests == 1
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='dnskey_origin',
        zone_name='example',
        file_name='rfc5155_example.')
    assert tests == 1
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='dnskey_origin',
        zone_name='001.cst.net',
        file_name='001.cst.net.')
    assert tests == 1
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='dnskey_origin',
        zone_name='001.cst.net',
        file_name='001.cst.net._zsk_not_origin')
    assert tests == 1
    assert errs == 1

# end of file

