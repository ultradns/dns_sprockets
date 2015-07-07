'''
test_nsecx_ttls_match - Tests nsecx_ttls_match validator.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns_sprockets_lib.validators.tests.harness as harness


def test_nsecx_ttls_match():

    (tests, errs) = harness.test_validator(
        test_name='nsecx_ttls_match',
        zone_name='example',
        file_name='rfc4035_example.')
    assert tests == 10
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='nsecx_ttls_match',
        zone_name='example',
        file_name='rfc5155_example.')
    assert tests == 12
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='nsecx_ttls_match',
        zone_name='001.cst.net',
        file_name='001.cst.net.')
    assert tests == 4
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='nsecx_ttls_match',
        zone_name='001.cst.net',
        file_name='001.cst.net._bad_nsec3_ttl')
    assert tests == 4
    assert errs == 2

# end of file

