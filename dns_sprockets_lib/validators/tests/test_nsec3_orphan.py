'''
test_nsec3_orphan - Tests nsec3_orphan validator.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns_sprockets_lib.validators.tests.harness as harness


def test_nsec3_orphan():

    (tests, errs) = harness.test_validator(
        test_name='nsec3_orphan',
        zone_name='001.cst.net',
        file_name='001.cst.net.')
    assert tests == 4
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='nsec3_orphan',
        zone_name='example',
        file_name='rfc5155_example.')
    assert tests == 12
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='nsec3_orphan',
        zone_name='example',
        file_name='rfc5155_example._bad_nsec3_covers')
    assert tests == 12
    assert errs == 1

    (tests, errs) = harness.test_validator(
        test_name='nsec3_orphan',
        zone_name='example',
        file_name='rfc5155_example._extra_nsec3_covers')
    assert tests == 12
    assert errs == 1

# end of file

