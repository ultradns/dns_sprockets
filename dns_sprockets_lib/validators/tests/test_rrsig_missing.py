'''
test_rrsig_missing - Tests rrsig_missing validator.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns_sprockets_lib.validators.tests.harness as harness


def test_rrsig_missing():

    (tests, errs) = harness.test_validator(
        test_name='rrsig_missing',
        zone_name='example',
        file_name='rfc4035_example.',
        extra_defines=['rrsig_missing_now=20040501000000'])
    assert tests == 23
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='rrsig_missing',
        zone_name='example',
        file_name='rfc5155_example.',
        extra_defines=['rrsig_missing_now=20100101000000'])
    assert tests == 29
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='rrsig_missing',
        zone_name='001.cst.net',
        file_name='001.cst.net.',
        extra_defines=['rrsig_missing_now=20150701000000'])
    assert tests == 11
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='rrsig_missing',
        zone_name='001.cst.net',
        file_name='001.cst.net.',
        extra_defines=['rrsig_missing_now=20150801000000'])  # expired now
    assert tests == 11
    assert errs == 11

    (tests, errs) = harness.test_validator(
        test_name='rrsig_missing',
        zone_name='001.cst.net',
        file_name='001.cst.net._rrsig_missing',
        extra_defines=['rrsig_missing_now=20150701000000'])
    assert tests == 11
    assert errs == 1

    (tests, errs) = harness.test_validator(
        test_name='rrsig_missing',
        zone_name='001.cst.net',
        file_name='001.cst.net._rrsig_bad_algo',
        extra_defines=['rrsig_missing_now=20150701000000'])
    assert tests == 11
    assert errs == 1

# end of file

