'''
test_nsec_missing - Tests nsec_missing validator.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns_sprockets_lib.validators.tests.harness as harness


def test_nsec_missing():

    (tests, errs) = harness.test_validator(
        test_name='nsec_missing',
        zone_name='example',
        file_name='rfc4035_example.')
    assert tests == 15
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='nsec_missing',
        zone_name='example',
        file_name='rfc4035_example._nsec_missing')
    assert tests == 15
    assert errs == 3

    (tests, errs) = harness.test_validator(
        test_name='nsec_missing',
        zone_name='example',
        file_name='rfc4035_example._bad_nsec_covers')
    assert tests == 15
    assert errs == 1

# end of file

