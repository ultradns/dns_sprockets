'''
test_rrsig_orphan - Tests rrsig_orphan validator.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns_sprockets_lib.validators.tests.harness as harness


def test_rrsig_orphan():

    (tests, errs) = harness.test_validator(
        test_name='rrsig_orphan',
        zone_name='example',
        file_name='rfc4035_example.',
        extra_defines=['rrsig_orphan_now=20040501000000'])
    assert tests == 27
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='rrsig_orphan',
        zone_name='example',
        file_name='rfc5155_example.',
        extra_defines=['rrsig_orphan_now=20100101000000'])
    assert tests == 30
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='rrsig_orphan',
        zone_name='001.cst.net',
        file_name='001.cst.net.',
        extra_defines=['rrsig_orphan_now=20150701000000'])
    assert tests == 11
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='rrsig_orphan',
        zone_name='001.cst.net',
        file_name='001.cst.net.',
        extra_defines=['rrsig_orphan_now=20150801000000'])  # expired now
    assert tests == 11
    assert errs == 11

    (tests, errs) = harness.test_validator(
        test_name='rrsig_orphan',
        zone_name='001.cst.net',
        file_name='001.cst.net._rrsig_orphan',
        extra_defines=['rrsig_orphan_now=20150701000000'])
    assert tests == 11
    assert errs == 1

    (tests, errs) = harness.test_validator(
        test_name='rrsig_orphan',
        zone_name='001.cst.net',
        file_name='001.cst.net._rrsig_bad_algo',
        extra_defines=['rrsig_orphan_now=20150701000000'])
    assert tests == 11
    assert errs == 1

# end of file

