'''
ValidatorTestHarness - Test harness for validators.
---------------------------------------------------

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns_sprockets_lib.utils as utils
import dns_sprockets_lib.loaders as loaders
import dns_sprockets_lib.validators as validators
from dns_sprockets_lib.dns_sprockets_impl import DNSSprocketsImpl


def test_validator(test_name, zone_name, file_name,
                   extra_defines=None, dnssec_type='detect'):
    '''
    Tests a validator using SprocketImpl instance.

    :param str test_name: The name of the test to run.
    :param str zone_name: The name of the zone to load.
    :param str file_name: The name of the file to load (w.r.t. dns_sprockets_lib/tests/data)
    :param list extra_defines: List of extra defines, in command-line format.
    :param str dnssec_type: Set to force dnssec_type.
    :return: A 2-tuple (test_cnt, error_cnt).
    '''

    class TestArgs(object):
        # pylint: disable=too-few-public-methods
        '''
        Simulated command-line arguments.
        '''
        zone = zone_name
        loader = 'file'
        source = 'dns_sprockets_lib/tests/data/%s' % (file_name)
        include_tests = [test_name]
        exclude_tests = []
        force_dnssec_type = dnssec_type
        errors_only = False
        defines = extra_defines
        verbose = False

    avail_loaders = utils.public_modules_in_package(loaders, ['tests'])
    avail_tests = utils.public_modules_in_package(validators, ['tests'])

    test_args_inst = TestArgs()
    if test_args_inst.defines is None:
        test_args_inst.defines = []
    for sec_param in test_args_inst.defines:
        (p_name, p_val) = sec_param.split('=')[:2]
        setattr(test_args_inst, p_name, p_val)

    sprocket = DNSSprocketsImpl(avail_loaders, avail_tests, test_args_inst)
    (_, test_cnt, err_cnt) = sprocket.run()
    return (test_cnt, err_cnt)

# end of file
