'''
utils - "dns_sprockets" zone validation tool utility functions

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import os
import re
import pkgutil


_CC_TO_UND_REGEX = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')


def public_modules_in_package(pkg, excludes=None):
    '''
    Scans a loaded package for "public" (i.e. no leading underscore) module names.
    @param pkg The package to scan (e.g. sprocket_support.tests).
    @param excludes List of names to exclude.
    @return List of module names in the package.
    '''
    if excludes is None:
        excludes = []
    pkg_path = os.path.dirname(pkg.__file__)
    return [name for (_, name, _) in pkgutil.iter_modules([pkg_path])
            if not name.startswith('_') and name not in excludes]


def camelcase_to_underscores(name):
    '''
    @param name Name to convert from camelcase to underscore style.
    @return Underscores-style string from camelcase-style.
    '''
    return _CC_TO_UND_REGEX.sub(r'_\1', name).lower()


def underscores_to_camelcase(name):
    '''
    @param name Name to convert from underscore to camelcase style.
    @return Camelcase-style string from underscores-style.
    '''
    # pylint: disable=bad-builtin
    return ''.join(map(''.__class__.capitalize, name.split('_')))


# end of file
