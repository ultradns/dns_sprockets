'''
test_nsec3_chain - Tests nsec3_chain validator.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns_sprockets_lib.validators.tests.harness as harness


def test_nsec_chain():

    (tests, errs) = harness.test_validator(
        test_name='nsec3_chain',
        zone_name='001.cst.net',
        file_name='001.cst.net.')
    assert tests == 1
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='nsec3_chain',
        zone_name='example',
        file_name='rfc5155_example.')
    assert tests == 1
    assert errs == 0

    (tests, errs) = harness.test_validator(
        test_name='nsec3_chain',
        zone_name='example',
        file_name='rfc5155_example._no_nsec3')
    assert tests == 1
    assert errs == 1

    (tests, errs) = harness.test_validator(
        test_name='nsec3_chain',
        zone_name='example',
        file_name='rfc5155_example._chain_broke')
    assert tests == 1
    assert errs == 1

    (tests, errs) = harness.test_validator(
        test_name='nsec3_chain',
        zone_name='example',
        file_name='rfc5155_example._chain_short')
    assert tests == 1
    assert errs == 1

    (tests, errs) = harness.test_validator(
        test_name='nsec3_chain',
        zone_name='example',
        file_name='rfc5155_example._chain_misorder')
    assert tests == 1
    assert errs == 1

    (tests, errs) = harness.test_validator(
        test_name='nsec3_chain',
        zone_name='signerendtoendtest.com',
        file_name='signerendtoendtest.com.')
    assert tests == 1
    assert errs == 0

# end of file

