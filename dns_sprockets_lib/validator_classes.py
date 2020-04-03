'''
validator_classes - Functions for dealing with validators.
----------------------------------------------------------

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import importlib

import dns_sprockets_lib.utils as utils
import dns_sprockets_lib.validators as validators


# Dictionary of validator_name -> validator_class:
ALL_CLASSES = {}


def load_all():
    '''
    Scans the sprocket_support.validators package for "public" modules and loads
    their classes into the ALL_CLASSES dictionary.
    '''
    if not ALL_CLASSES:
        avail_tests = utils.public_modules_in_package(validators, ['tests'])
        for test_name in avail_tests:
            test_module_name = 'dns_sprockets_lib.validators.%s' % (test_name)
            test_module = importlib.import_module(test_module_name)
            ALL_CLASSES[test_name] = getattr(
                test_module, utils.underscores_to_camelcase(test_name))


def _get_descriptions():
    '''
    Get a list of descriptions of all validators in the ALL_CLASSES dictionary.
    Each description is a tuple: (validator_name, doc_string, test_type,
    test_rrtype, validator_optargs).  The returned list is ordered by
    validator_name.
    '''
    load_all()
    return sorted(
        [(key, val.__doc__.strip(), val.TEST_TYPE, val.TEST_RRTYPE, val.TEST_OPTARGS)
         for (key, val) in ALL_CLASSES.items()])


def get_formatted_descriptions():
    '''
    Gets a formatted string containing descriptions of all validators in the
    ALL_CLASSES dictionary.
    '''
    descs = _get_descriptions()
    return '\n'.join(
        ['TEST: %s (%s) - %s%s' % (
            td[0],
            validators.test_type_to_str(td[2], td[3]),
            td[1],
            ''.join(sorted(
                ['\n    DEFINE: (%s_)%s - %s (default=%s)' % (
                    td[0], opt_name, opt_val[1], opt_val[0])
                 for (opt_name, opt_val) in td[4].items()])))
         for td in descs])

# end of file
