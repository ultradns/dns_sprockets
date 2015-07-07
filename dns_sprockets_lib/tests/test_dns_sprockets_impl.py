'''
test_dns_sprockets_impl - Tests DNSSprocketsImpl implementation class.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns_sprockets_lib.utils as utils
import dns_sprockets_lib.loaders as loaders
import dns_sprockets_lib.validators as validators
from dns_sprockets_lib.dns_sprockets_impl import DNSSprocketsImpl


def test_SprocketImpl():

    class TestArgs(object):
        zone = '001.cst.net'
        loader = 'file'
        source = 'dns_sprockets_lib/tests/data/001.cst.net.'
        include_tests = ['soa_origin', 'soa_unique']
        exclude_tests = ['soa_unique']
        force_dnssec_type = 'detect'
        errors_only = False
        defines = ['file_allow_include=0']
        file_allow_include = '0'

    avail_loaders = utils.public_modules_in_package(loaders, ['tests'])
    avail_tests = utils.public_modules_in_package(validators, ['tests'])

    test_args_inst = TestArgs()
    sprocket = DNSSprocketsImpl(avail_loaders, avail_tests, test_args_inst)
    (_, test_cnt, err_cnt) = sprocket.run()
    assert test_cnt == 1
    assert err_cnt == 0


# end of file
