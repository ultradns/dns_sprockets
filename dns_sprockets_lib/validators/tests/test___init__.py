'''
test___init__ - Tests dns_sprockets_lib.validators package.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns.rdatatype

from dns_sprockets_lib.loaders.file import File
import dns_sprockets_lib.validators as validators


def test_test_type_to_str():

    tests = {
        ((validators.ZONE_TEST, None), 'ZONE_TEST'),
        ((validators.ZONE_TEST, ''), 'ZONE_TEST'),
        ((validators.ZONE_TEST, 'SOA'), 'ZONE_TEST[SOA]'),
        ((validators.ZONE_TEST, 'SOA,NS'), 'ZONE_TEST[SOA,NS]'),
        ((validators.NODE_TEST, 'A,AAAA'), 'NODE_TEST[A,AAAA]'),
        ((validators.RRSET_TEST, None), 'RRSET_TEST'),
        ((validators.REC_TEST, None), 'REC_TEST')}

    for test in tests:
        assert validators.test_type_to_str(test[0][0], test[0][1]) == test[1]


def test_dnssec_filter_tests_by_context():

    class test1(object):
        TEST_NAME = 'test1'
        TEST_DNSSECTYPE = None

    class test2(object):
        TEST_NAME = 'test2'
        TEST_DNSSECTYPE = True

    class test3(object):
        TEST_NAME = 'test3'
        TEST_DNSSECTYPE = 'NSEC'

    class test4(object):
        TEST_NAME = 'test4'
        TEST_DNSSECTYPE = 'NSEC3'

    class context1(object):
        dnssec_type = 'unsigned'

    class context2(object):
        dnssec_type = 'NSEC'

    class context3(object):
        dnssec_type = 'NSEC3'

    tests = {
        ((test1(), context1()), 1),
        ((test1(), context2()), 1),
        ((test1(), context3()), 1),
        ((test2(), context1()), 0),
        ((test2(), context2()), 1),
        ((test2(), context3()), 1),
        ((test3(), context1()), 0),
        ((test3(), context2()), 1),
        ((test3(), context3()), 0),
        ((test4(), context1()), 0),
        ((test4(), context2()), 0),
        ((test4(), context3()), 1)}

    for test in tests:
        valis = [test[0][0]]
        context = test[0][1]
        count = test[1]
        validators.dnssec_filter_tests_by_context(valis, context)
        assert len(valis) == count


def test_filter_node():

    class test_args(object):
        source = 'dns_sprockets_lib/tests/data/001.cst.net.'
        zone = '001.cst.net'

    test_file = File(test_args())
    zone_obj = test_file.run()
    node = zone_obj.get_node('001.cst.net.')

    tests = {
        (None, 8),
        ('', 8),
        ('SOA', 1),
        ('A', 0),
        ('SOA,NS', 2),
        ('SOA,NS,DNSKEY', 3),
        ('SOA,NS,DNSKEY,A', 3)}

    for test in tests:
        assert len(validators.filter_node(node, test[0]).rdatasets) == test[1]


def test_test_covers_type():

    class TestInst(object):
        TEST_RRTYPE = None

    tests = {
        ((None, 'SOA'), True),
        (('', 'SOA'), True),
        (('SOA', 'SOA'), True),
        (('SOA', 'A'), False),
        (('SOA,NS', 'A'), False),
        (('SOA,NS', 'SOA'), True),
        (('SOA,NS', 'NS'), True)}

    for test in tests:
        test_inst = TestInst()
        test_inst.TEST_RRTYPE = test[0][0]
        rec_type = dns.rdatatype.from_text(test[0][1])
        assert validators.test_covers_type(test_inst, rec_type) is test[1]


def test_Context():

    class test_args(object):
        source = 'dns_sprockets_lib/tests/data/001.cst.net.'
        zone = '001.cst.net'
        force_dnssec_type = 'detect'

    test_args_inst = test_args()
    test_file = File(test_args_inst)
    zone_obj = test_file.run()
    context = validators.Context(test_args_inst, zone_obj)

    node_names = [
        dns.name.from_text('001.cst.net.'),
        dns.name.from_text('001.001.cst.net.'),
        dns.name.from_text('06ES9CGGDRORFDD4NS9AHOCAIKLDRRP8.001.cst.net.'),
        dns.name.from_text('AL016ABKH6LVDIG6503FS92KDMOTQH4V.001.cst.net.'),
        dns.name.from_text('KQGPU8I0AI43NEM212BD0079J5SI5R3K.001.cst.net.'),
        dns.name.from_text('test.001.cst.net.'),
        dns.name.from_text('test2.001.cst.net.'),
        dns.name.from_text('UQML1AM96TFTFMLKAGTBS82ISR050SH0.001.cst.net.')]

    assert context.zone_name == dns.name.from_text(test_args_inst.zone)
    assert context.zone_obj == zone_obj
    assert context.node_names == node_names
    assert len(context.soa_rdataset.items) == 1
    assert len(context.dnskey_rdataset) == 2
    assert len(context.nsec3param_rdataset) == 1
    assert context.delegated_names == []
    assert context.dnssec_type == 'NSEC3'
    assert context.is_delegated('test.001.cst.net.') is False


def test__Validator():

    class test_args(object):
        test_validator_verbose = True
        test_validator_now = '20150101000000'

    class TestValidator(validators._Validator):
        TEST_OPTARGS = {'now': (None, 'Time to use for now')}

    val = TestValidator(test_args())
    assert val.TEST_TYPE is None
    assert val.TEST_DNSSECTYPE is None
    assert val.TEST_RRTYPE is None
    assert val.TEST_NAME == 'test_validator'
    assert not hasattr(val, 'verbose')
    assert val.now == test_args().test_validator_now


def test_ZoneTest():

    class TestZoneTest(validators.ZoneTest):
        TEST_OPTARGS = {'now': ('20150101000000', 'Time to use for now')}

    class test_args(object):
        verbose = True
        test_zone_test_now = '20151231000000'

    test = TestZoneTest(test_args())
    assert test.TEST_TYPE == validators.ZONE_TEST
    assert test.TEST_NAME == 'test_zone_test'
    assert not hasattr(test, 'verbose')
    assert test.now == test_args.test_zone_test_now


def test_NodeTest():

    class TestNodeTest(validators.NodeTest):
        TEST_OPTARGS = {'now': ('20150101000000', 'Time to use for now')}

    class test_args(object):
        verbose = True
        test_node_test_now = '20151231000000'

    test = TestNodeTest(test_args())
    assert test.TEST_TYPE == validators.NODE_TEST
    assert test.TEST_NAME == 'test_node_test'
    assert not hasattr(test, 'verbose')
    assert test.now == test_args.test_node_test_now


def test_RRSetTest():

    class TestRrsetTest(validators.RRSetTest):
        TEST_OPTARGS = {'now': ('20150101000000', 'Time to use for now')}

    class test_args(object):
        verbose = True
        test_rrset_test_now = '20151231000000'

    test = TestRrsetTest(test_args())
    assert test.TEST_TYPE == validators.RRSET_TEST
    assert test.TEST_NAME == 'test_rrset_test'
    assert not hasattr(test, 'verbose')
    assert test.now == test_args.test_rrset_test_now


def test_RecTest():

    class TestRecTest(validators.RecTest):
        TEST_OPTARGS = {'now': ('20150101000000', 'Time to use for now')}

    class test_args(object):
        verbose = True
        test_rec_test_now = '20151231000000'

    test = TestRecTest(test_args())
    assert test.TEST_TYPE == validators.REC_TEST
    assert test.TEST_NAME == 'test_rec_test'
    assert not hasattr(test, 'verbose')
    assert test.now == test_args.test_rec_test_now

# end of file
