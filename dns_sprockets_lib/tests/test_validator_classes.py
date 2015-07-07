'''
test_validator_classes - Tests zone-validator-class loader functions.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns_sprockets_lib.validator_classes as validator_classes
import dns_sprockets_lib.validators as validators
from dns_sprockets_lib.validators.ns_origin import NsOrigin
from dns_sprockets_lib.validators.soa_origin import SoaOrigin


def test_load_all():

    validator_classes.load_all()
    assert 'ns_origin' in validator_classes.ALL_CLASSES
    assert validator_classes.ALL_CLASSES['ns_origin'] == NsOrigin
    assert 'soa_origin' in validator_classes.ALL_CLASSES
    assert validator_classes.ALL_CLASSES['soa_origin'] == SoaOrigin


def test__get_descriptions():

    got_ns_origin = False
    got_soa_origin = False
    for desc in validator_classes._get_descriptions():
        if desc[0] == 'ns_origin':
            got_ns_origin = True
            assert desc[2] == validators.ZONE_TEST
            assert desc[3] is None
        elif desc[0] == 'soa_origin':
            got_soa_origin = True
            assert desc[2] == validators.ZONE_TEST
            assert desc[3] is None
        assert desc[1] > ''
        assert isinstance(desc[4], dict)
    assert got_ns_origin
    assert got_soa_origin


def test_get_formatted_descriptions():

    desc = validator_classes.get_formatted_descriptions()
    assert 'ns_origin' in desc
    assert 'soa_origin' in desc

# end of file
