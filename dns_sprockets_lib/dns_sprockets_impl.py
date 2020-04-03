'''
dns_sprockets_impl - DNS Zone validation tool implementation class.
-------------------------------------------------------------------

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import time

import dns_sprockets_lib.loader_classes as loader_classes
import dns_sprockets_lib.validators as validators
import dns_sprockets_lib.validator_classes as validator_classes


class DNSSprocketsImpl(object):
    # pylint: disable=too-few-public-methods
    '''
    Performs zone validation.
    '''

    def __init__(self, avail_loaders, avail_tests, args):
        '''
        Constructor.

        :param list avail_loaders: List of loader module names.
        :param list avail_tests: List of validator module names.
        :param obj args: The application's command-line args.
        '''
        self.avail_loaders = avail_loaders
        self.avail_tests = avail_tests
        self.args = args

    def run(self):
        '''
        Runs the instance, which loads a zone with the specified loader, and
        loads and runs the specified tests.

        :return: A 3-tuple (loader_elapsed_time, test_count, error_count)
        '''

        # Create the zone loader instance:
        loader_classes.load_all()
        loader_class = loader_classes.ALL_CLASSES[self.args.loader]
        loader = loader_class(self.args)

        # Create the test instances:
        validator_classes.load_all()
        tests_pool = self.args.include_tests or self.avail_tests
        test_names = [t for t in tests_pool if t not in self.args.exclude_tests]
        tests = {
            validators.ZONE_TEST: [],
            validators.NODE_TEST: [],
            validators.RRSET_TEST: [],
            validators.REC_TEST: []}
        for test_name in test_names:
            test_class = validator_classes.ALL_CLASSES[test_name]
            test = test_class(self.args)
            tests[test.TEST_TYPE].append(test)

        # Load the zone:
        load_start_time = time.time()
        zone_obj = loader.run()
        load_time = time.time() - load_start_time
        if not zone_obj:
            raise RuntimeError('No zone to validate!')
        context = validators.Context(self.args, zone_obj)

        # Print some stats:
        print('# Checking zone:', context.zone_name)
        print('# Loader: %s from: %s elapsed=%f secs' % (
            self.args.loader, self.args.source, load_time))
        if self.args.force_dnssec_type == 'detect':
            print('# Zone appears to be DNSSEC type:', context.dnssec_type)
        else:
            print('# Forcing DNSSEC type for zone to:', context.dnssec_type)
        print('# Extra defines:', self.args.defines)

        # Filter tests based on zone's DNSSEC type:
        running_test_names = []
        for tests_type in list(tests):
            validators.dnssec_filter_tests_by_context(tests[tests_type], context)
            running_test_names += [test.TEST_NAME for test in tests[tests_type]]
        print('# Running tests:', running_test_names)

        counts = {'tests': 0, 'errors': 0}

        # Run the zone tests:
        for test in tests[validators.ZONE_TEST]:
            DNSSprocketsImpl._run_test(self.args, test, context, counts)

        # Run the node, rrset, and rec tests:
        for name in context.node_names:
            node = context.zone_obj.get_node(name)
            if node:  # Not present for Empty Non-Terminals

                # Node tests:
                for test in tests[validators.NODE_TEST]:
                    test_node = validators.filter_node(node, test.TEST_RRTYPE)
                    DNSSprocketsImpl._run_test(
                        self.args, test, context, counts,
                        name=name, node=test_node)

                # RRSet tests:
                for rdataset in node.rdatasets:
                    for test in tests[validators.RRSET_TEST]:
                        if validators.test_covers_type(test, rdataset.rdtype):
                            DNSSprocketsImpl._run_test(
                                self.args, test, context, counts,
                                name=name, rdataset=rdataset)

                    # Rec tests:
                    for rdata in rdataset:
                        for test in tests[validators.REC_TEST]:
                            if validators.test_covers_type(test, rdata.rdtype):
                                DNSSprocketsImpl._run_test(
                                    self.args, test, context, counts,
                                    name=name, ttl=rdataset.ttl, rdata=rdata)

        print('# END RESULT: %d ERRORS in %d tests' % (counts['errors'], counts['tests']))
        if hasattr(self.args, 'verbose') and self.args.verbose:
            print('#  TEST TIMES:')
            for key in list(tests):
                for test in tests[key]:
                    print('#  %f secs for %s (%d runs for %f secs each)' % (
                        test.total_time, 
                        test.TEST_NAME, 
                        test.total_runs,
                        test.total_time / test.total_runs))
        return (load_time, counts['tests'], counts['errors'])

    @staticmethod
    def _run_test(args, test, context, counts, **kwargs):
        '''
        Runs an individual test.

        :param obj args: The application's command-line args.
        :param obj test: The validator instance to use.
        :param obj context: The testing context.
        :param dict counts: Dictionary of test and error counts.
        :param dict kwargs: Other parameters specific to the TEST_TYPE being run.
        '''
        suggested_tested = validators.make_suggested_tested(test, context, **kwargs)
        test.start_timer()
        (tested, result) = test.run(context, suggested_tested, **kwargs)
        test.stop_timer()
        if tested is not None:
            test.total_runs += 1
            counts['tests'] += 1
            good = not result
            if not good:
                counts['errors'] += 1
            if not good or not args.errors_only:
                print('TEST %s(%s) => %s' % (
                    test.TEST_NAME,
                    tested,
                    good and 'OK' or 'FAIL: %s' % (result)))

# end of file
