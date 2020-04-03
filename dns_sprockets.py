#!/usr/bin/env python2.7
'''
dns_sprockets - A command-line tool to validate DNS zones.
----------------------------------------------------------

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import os
import sys
import time

from dns_sprockets_version import VERSION
import dns_sprockets_lib.utils as utils
import dns_sprockets_lib.loaders as loaders
import dns_sprockets_lib.loader_classes as loader_classes
import dns_sprockets_lib.validators as validators
import dns_sprockets_lib.validator_classes as validator_classes
from dns_sprockets_lib.dns_sprockets_impl import DNSSprocketsImpl


_PRODUCT = 'dns_sprockets'
_BANNER = '%s (%s) - A DNS Zone validation tool' % (_PRODUCT, VERSION)
_DEFAULT_ZONE = 'www.ultradns.com'
_DEFAULT_LOADER = 'xfr'
_DEFAULT_SOURCE = '127.0.0.1#53'
_FATAL_RETCODE = 255


def _run_main(avail_loaders, avail_tests, args):
    '''
    Constructs and runs a DNSSprocketsImpl instance.
    '''
    start_time = time.time()

    # Construct and run a DNSSprocketsImpl instance:
    try:
        (load_time, _, ret_code) = DNSSprocketsImpl(avail_loaders, avail_tests, args).run()
        total_time = time.time() - start_time
        print('# TOTAL ELAPSED TIME: %f SECS  LOAD TIME: %f SECS  TEST TIME: %f SECS' % (
            total_time, load_time, total_time - load_time))
        sys.stdout.flush()
        os._exit(ret_code >= _FATAL_RETCODE and _FATAL_RETCODE - 1 or ret_code)

    except Exception as err:
        print('FATAL: {%s} %s' % (err.__class__.__name__, err))
        if args.verbose:
            raise
        sys.stdout.flush()
        os._exit(_FATAL_RETCODE)


def run():
    '''
    Run the sprocket command-line application.
    '''
    # Print startup banner:
    print('#', _BANNER)

    # Determine available loaders and tests:
    avail_loaders = utils.public_modules_in_package(loaders, ['tests'])
    avail_tests = utils.public_modules_in_package(validators, ['tests'])

    # Parse command-line:
    import argparse
    parser = argparse.ArgumentParser(
        epilog='''
Use @filename to read some/all arguments from a file.\n\n
Use -d's to define optional, module-specific parameters if desired (e.g. to tell
'xfr' loader to use a specific source address, use "-d xfr_source=1.2.3.4").
The optional parameters are listed under each loader and validator description
in DEFINE lines, if available.  The "short form" of parameter names (i.e. 
without the module name prefix) may be used instead, if multiple modules define
the same "short form" name (e.g. -d now=20160328120000 can be used, and will set
both 'rrsig_missing' and 'rrsig_orphan' validators' rrsig_missing_now and 
rrsig_orphan_now values, respectively).\n\n
By default, all tests are run.  Use -i\'s to explicitly specify desired tests,
or -x\'s to eliminate undesired tests.\n\n
The list of available loaders is:
---------------------------------------------------------------------------\n%s\n\n
The list of available validators is:
---------------------------------------------------------------------------\n%s
            ''' % (loader_classes.get_formatted_descriptions(),
                   validator_classes.get_formatted_descriptions()),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars='@')
    parser.add_argument('-z', '--zone', dest='zone',
        default=_DEFAULT_ZONE, metavar='s',
        help='Name of zone to validate [%(default)s]')
    parser.add_argument('-l', '--loader', dest='loader',
        default=_DEFAULT_LOADER, metavar='s', choices=avail_loaders,
        help='Zone loader method to use (one of: %(choices)s) [%(default)s]')
    parser.add_argument('-s', '--source', dest='source',
        default=_DEFAULT_SOURCE, metavar='s',
        help='Loader source to use [%(default)s]')
    parser.add_argument('-i', '--include', dest='include_tests',
        action='append', metavar='s', choices=avail_tests,
        help='Only include this validator (can use multiple times)')
    parser.add_argument('-x', '--exclude', dest='exclude_tests',
        action='append', metavar='s', choices=avail_tests,
        help='Exclude this validator (can use multiple times)')
    parser.add_argument('-d', '--define', dest='defines',
        action='append', metavar='s',
        help='Define other params (can use multiple times)')
    parser.add_argument('-f', '--force-dnssec-type', dest='force_dnssec_type',
        default='detect', metavar='s',
        choices=['detect', 'unsigned', 'NSEC', 'NSEC3'],
        help='Use DNSSEC type (one of: %(choices)s) [%(default)s]')
    parser.add_argument('-e', '--errors-only', dest='errors_only',
        default=False, action='store_true',
        help='Show validation errors only [%(default)s]')
    parser.add_argument('-v', '--verbose', dest='verbose',
        default=False, action='store_true',
        help='Show detailed processing info [%(default)s]')
    args = parser.parse_args()

    # Fix-up args:
    if args.include_tests is None:
        args.include_tests = []
    if args.exclude_tests is None:
        args.exclude_tests = []
    if args.defines is None:
        args.defines = []
    for sec_param in args.defines:
        (p_name, p_val) = sec_param.split('=')[:2]
        setattr(args, p_name, p_val)

    # Run the app:
    _run_main(avail_loaders, avail_tests, args)


if __name__ == '__main__':
    run()

# end of file
