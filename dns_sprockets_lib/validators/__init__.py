'''
__init__.py - Validators library for dns_sprockets zone validator.
------------------------------------------------------------------

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''

import time

import dns.rdatatype
import dns.name
import dns.rdata
import dns.rdtypes
import dns.rdtypes.ANY
import dns.node

import dns_sprockets_lib.utils as utils
import dns_sprockets_lib.dns_utils as dns_utils


# Test types:
(ZONE_TEST,   # A test type that validates entire zone.
 NODE_TEST,   # A test type that validates nodes in the zone.
 RRSET_TEST,  # A test type that validates RRSets in the zone.
 REC_TEST     # A test type that validates individual records in the zone.
) = list(range(4))


def test_type_to_str(test_type, test_rrtype=None):
    '''
    Convert a test_type and test_rrtype to a string for output purposes.

    :param int test_type: The TEST_TYPE attribute from the test.
    :param str test_rrtype: The string describing record type(s) covered by the test.
    :return: Description string for test.
    '''
    specific = test_rrtype and '[%s]' % (test_rrtype) or ''
    if test_type == ZONE_TEST:
        return 'ZONE_TEST' + specific
    elif test_type == NODE_TEST:
        return 'NODE_TEST' + specific
    elif test_type == RRSET_TEST:
        return 'RRSET_TEST' + specific
    elif test_type == REC_TEST:
        return 'REC_TEST' + specific


def rec_to_abbrev_text(name, ttl, klass, rdata):
    '''
    Translates a record to abbreviated text.  For most records, this is the
    same as the to_text(); for others (such as RRSIG), it is truncated to
    attempt to fit on a single terminal line.

    :param str name: The owner name of the record.
    :param int ttl: The TTL for the record.
    :param int/str klass: The class of the record.
    :param obj rdata: The rdata of the record.
    :return: Text description of the record.
    '''
    if isinstance(rdata, dns.rdtypes.ANY.RRSIG.RRSIG):
        # pylint: disable=protected-access
        sig = dns.rdata._base64ify(rdata.signature)
        rdata_txt = '%s %d %d %d %s %s %d %s %s' % (
            dns.rdatatype.to_text(rdata.type_covered),
            rdata.algorithm,
            rdata.labels,
            rdata.original_ttl,
            dns.rdtypes.ANY.RRSIG.posixtime_to_sigtime(rdata.expiration),
            dns.rdtypes.ANY.RRSIG.posixtime_to_sigtime(rdata.inception),
            rdata.key_tag,
            rdata.signer,
            '%s...%s' % (sig[:6], sig[len(sig) - 6:]))
    else:
        rdata_txt = rdata.to_text(relativize=False)

    klass_txt = (isinstance(klass, str)
        and klass or dns.rdataclass.to_text(klass))
    return '%s %d %s %s %s' % (
        name, ttl, klass_txt, rdata.__class__.__name__, rdata_txt)


def dnssec_filter_tests_by_context(tests, context):
    '''
    Removes any tests from the tests list that do not apply to the context.

    :param list tests: List of tests to filter.
    :param obj context: The context being used.
    '''
    remove_tests = []

    for test in tests:
        rem_test = None
        if context.dnssec_type == 'unsigned':
            if test.TEST_DNSSECTYPE is not None:
                rem_test = test
        elif context.dnssec_type == 'NSEC':
            if test.TEST_DNSSECTYPE == 'NSEC3':
                rem_test = test
        elif context.dnssec_type == 'NSEC3':
            if test.TEST_DNSSECTYPE == 'NSEC':
                rem_test = test

        if rem_test:
            remove_tests.append(rem_test)
            print('# Skipping test: %s  (DNSSEC type for zone: %s, for test: %s)' % (
                rem_test.TEST_NAME,
                context.dnssec_type,
                test.TEST_DNSSECTYPE))

    for test in remove_tests:
        tests.remove(test)


def filter_node(node, test_rrtype):
    '''
    Returns a node that has rdatasets that match the test RR types.  If the
    test_rrtype is specified, a new, temporary node for use by the validator
    will be generated, which only has those rdatasets mentioned.

    :param obj node: The dns.node.Node to inspect.
    :param str test_rrtype: The string description of RR type(s) that the test covers.
    :return: The dns.node.Node for the validator to examine.
    '''
    if not test_rrtype:
        return node
    rrtypes_txt = test_rrtype.split(',')
    rrtypes = [dns.rdatatype.from_text(t) for t in rrtypes_txt]
    new_node = dns.node.Node()
    new_node.rdatasets = [rds for rds in node.rdatasets
                          if rds.rdtype in rrtypes]
    return new_node


def test_covers_type(test, rdtype):
    '''
    Checks to see if a test covers a RR type.

    :param obj test: The test to examine.
    :param int rdtype: The dns.rdatatype for the rdataset/record under consideration.
    :return: True if the test covers the type; False if not.
    '''
    if not test.TEST_RRTYPE:
        return True
    rrtypes_txt = test.TEST_RRTYPE.split(',')
    rrtypes = [dns.rdatatype.from_text(t) for t in rrtypes_txt]
    return rdtype in rrtypes


def make_suggested_tested(test, context, **kwargs):
    '''
    Generates a description for the test being run.  A test description is
    printed for each test instance being run against zone, node, rrset, or
    record, and this is the suggested description.  Usually, specific test
    instances will use this value for 'tested' return variable, but are free
    to ignore this description in favor of their own if desired.

    :param obj test: The test being run.
    :param obj context: The testing context.
    :param dict kwargs: Optional, test-type-specific parameters.
    :return: A string describing the test instance being run.
    '''
    if test.TEST_TYPE == ZONE_TEST:
        suggested_tested = 'ZONE(%s %s)' % (
            context.zone_name,
            dns.rdataclass.to_text(context.zone_obj.rdclass))
    elif test.TEST_TYPE == NODE_TEST:
        suggested_tested = 'NODE(%s %s)' % (
            kwargs['name'],
            dns.rdataclass.to_text(context.zone_obj.rdclass))
    elif test.TEST_TYPE == RRSET_TEST:
        suggested_tested = 'RRSET(%s %s %s)' % (
            kwargs['name'],
            dns.rdataclass.to_text(context.zone_obj.rdclass),
            dns.rdatatype.to_text(kwargs['rdataset'].rdtype))
    elif test.TEST_TYPE == REC_TEST:
        suggested_tested = 'REC(%s)' % (
            rec_to_abbrev_text(
                kwargs['name'],
                kwargs['ttl'],
                context.zone_obj.rdclass,
                kwargs['rdata']))
    return suggested_tested


class Context(object):
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    '''
    A testing context containing the zone name, zone_obj, etc.
    '''
    def __init__(self, args, zone_obj):
        '''
        Ctor.

        :param obj args: The application arguments.
        :param obj zone_obj: The dns.zone.Zone instance.
        '''
        self.zone_name = dns.name.from_text(args.zone)
        self.zone_obj = zone_obj

        # Get SOA if available:
        self.soa_rdataset = self.zone_obj.get_rdataset(
            self.zone_name, dns.rdatatype.SOA)

        # Get DNSKEY(s) if available:
        self.dnskey_rdataset = self.zone_obj.get_rdataset(
            self.zone_name, dns.rdatatype.DNSKEY)

        # Get NSEC3PARAM(s) if available:
        self.nsec3param_rdataset = self.zone_obj.get_rdataset(
            self.zone_name, dns.rdatatype.NSEC3PARAM)

        # Get delegated zones if any:
        self.delegated_names = [
            name for (name, _) in self.zone_obj.iterate_rdatasets('NS')
            if name != self.zone_name]

        # Force or detect zone's DNSSEC type:
        if args.force_dnssec_type != 'detect':
            self.dnssec_type = args.force_dnssec_type
        else:
            # See if there are any NSEC or NSEC3's:
            has_nsec = next(self.zone_obj.iterate_rdatasets(dns.rdatatype.NSEC), None)
            has_nsec3 = (self.nsec3param_rdataset or
                next(self.zone_obj.iterate_rdatasets(dns.rdatatype.NSEC3), None))

            # See if this appears to be a signed zone (note: can't seem to
            # practically check all RRSIG's since they "cover" other records,
            # which would require us to iterate all possible "covers" values,
            # so just try a few obvious ones):
            seems_signed = (
                self.dnskey_rdataset or
                has_nsec or
                has_nsec3 or
                next(self.zone_obj.iterate_rdatasets(
                    dns.rdatatype.DS), None) or
                next(self.zone_obj.iterate_rdatasets(
                    dns.rdatatype.RRSIG, dns.rdatatype.SOA), None) or
                next(self.zone_obj.iterate_rdatasets(
                    dns.rdatatype.RRSIG, dns.rdatatype.NS), None) or
                next(self.zone_obj.iterate_rdatasets(
                    dns.rdatatype.RRSIG, dns.rdatatype.A), None) or
                next(self.zone_obj.iterate_rdatasets(
                    dns.rdatatype.RRSIG, dns.rdatatype.AAAA), None))

            self.dnssec_type = (
                has_nsec3 and 'NSEC3' or
                has_nsec and 'NSEC' or
                seems_signed and 'NSEC3' or  # assume NSEC3-type
                'unsigned')

        # Get DNSSEC-ordered list of names in zone (including any Empty Non-
        # Terminals if NSEC3-style zone):
        self.node_names = dns_utils.calc_node_names(
            list(zone_obj.nodes),
            self.dnssec_type == 'NSEC3', self.zone_name)

    def is_delegated(self, name):
        '''
        :return: True if name is delegated w.r.t. the context.
        '''
        return dns_utils.is_delegated(self.delegated_names, name)

#
# For validator classes, use short docstrings, which will be used for the actual
# test descriptions!
#


class _Validator(object):
    # pylint: disable=too-few-public-methods
    '''
    [Base class for validator classes]
    '''
    TEST_NAME = None  # Automatically set in __init__.
    TEST_TYPE = None  # Override expected!  e.g.: ZONE_TEST
    TEST_DNSSECTYPE = None  # Override possible!  one of: None, True, 'NSEC' or 'NSEC3'
    TEST_RRTYPE = None  # Override possible!  e.g.: 'A', or 'RRSIG,NSEC3PARAM'
    TEST_OPTARGS = {}  # Override possible!  e.g.: {'now': (None, 'Time to use for now')}

    def __init__(self, args):
        '''
        Ctor, caches the arguments used to run the application, and grabs any
        optional test arguments.
        '''
        # pylint: disable=invalid-name
        self.TEST_NAME = utils.camelcase_to_underscores(self.__class__.__name__)
        self.args = args

        utils.process_optargs(self.TEST_OPTARGS, self.TEST_NAME, self)

        # For accumulating run times:
        self.total_time = 0
        self.start_time = 0
        
        # For accumulating number of runs:
        self.total_runs = 0

    def start_timer(self):
        '''
        Starts the validator timer.
        '''
        self.start_time = time.time()

    def stop_timer(self):
        '''
        Stops the validator timer and adds to accumulator.
        '''
        self.total_time += time.time() - self.start_time


class ZoneTest(_Validator):
    # pylint: disable=too-few-public-methods
    '''
    [Base class for zone-type validators]
    '''
    TEST_TYPE = ZONE_TEST

    def run(self, suggested_tested, context):
        # pylint: disable=unused-argument
        '''
        Runs the zone-type validator.

        :param str suggested_tested: A suggested tested value.
        :param obj context: The testing context.
        :return: A 2-tuple (tested, result)
        '''
        return ('OOPS!', 'ERROR: run() not overridden for %s' % (self.TEST_NAME))


class NodeTest(_Validator):
    # pylint: disable=too-few-public-methods
    '''
    [Base class for node-type validators.  Derived classes *may* be restricted
    to specific RRType's by specifying a TEST_RRTYPE]
    '''
    TEST_TYPE = NODE_TEST

    def run(self, context, suggested_tested, name, node):
        # pylint: disable=unused-argument
        '''
        Runs the node-type validator.  If a TEST_RRTYPE specified, the node
        presented to the validator will be filtered accordingly.

        :param obj context: The testing context.
        :param str suggested_tested: A suggested tested value.
        :param str name: The name being tested.
        :param obj node: The dns.Node corresponding to the name.
        :return: A 2-tuple (tested, result)
        '''
        return ('OOPS!', 'ERROR: run() not overridden for %s' % (self.TEST_NAME))


class RRSetTest(_Validator):
    # pylint: disable=too-few-public-methods
    '''
    [Base class for rrset-type validators.  Derived classes *may* be restricted
    to specific RRType's by specifying a TEST_RRTYPE]
    '''
    TEST_TYPE = RRSET_TEST

    def run(self, context, suggested_tested, name, rdataset):
        # pylint: disable=unused-argument
        '''
        Runs the name-type validator.  If a TEST_RRTYPE is specified, the RRSet
        presented to the validator will be filtered accordingly.

        :param obj context: The testing context.
        :param str suggested_tested: A suggested tested value.
        :param str name: The name being tested.
        :param obj rdataset: The dns.rdataset corresponding to the name.
        :return: A 2-tuple (tested, result)
        '''
        return ('OOPS!', 'ERROR: run() not overridden for %s' % (self.TEST_NAME))


class RecTest(_Validator):
    # pylint: disable=too-few-public-methods
    '''
    [Base class for record-type validators.  Derived classes *may* be restricted
    to specific RRType's by specifying a TEST_RRTYPE]
    '''
    TEST_TYPE = REC_TEST

    def run(self, context, suggested_tested, name, ttl, rdata):
        # pylint: disable=too-many-arguments
        # pylint: disable=unused-argument
        '''
        Runs the record-type validator.  If a TEST_RRTYPE is specified, the
        validator will only see those types of records.

        :param obj context: The testing context.
        :param str suggested_tested: A suggested tested value.
        :param str name: The name of the record being tested.
        :param int ttl: The TTL of the record being tested.
        :param obj rdata: The dns.rdata.Rdata object being tested.
        :return: A 2-tuple (tested, result)
        '''
        return ('OOPS!', 'ERROR: run() not overridden for %s' % (self.TEST_NAME))

# end of file
