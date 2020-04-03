'''
loader_classes - Functions for dealing with zone loaders
--------------------------------------------------------

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import importlib

import dns_sprockets_lib.utils as utils
import dns_sprockets_lib.loaders as loaders


# Dictionary of loader_name -> loader_class:
ALL_CLASSES = {}


def load_all():
    '''
    Scans the sprocket_support.loaders package for "public" modules and loads
    their classes into the ALL_CLASSES dictionary.
    '''
    if not ALL_CLASSES:
        avail_loaders = utils.public_modules_in_package(loaders, ['tests'])
        for loader_name in avail_loaders:
            loader_module_name = 'dns_sprockets_lib.loaders.%s' % (loader_name)
            loader_module = importlib.import_module(loader_module_name)
            ALL_CLASSES[loader_name] = getattr(
                loader_module, utils.underscores_to_camelcase(loader_name))


def _get_descriptions():
    '''
    Get a list of descriptions of all loaders in the ALL_CLASSES dictionary.
    Each description is a tuple: (loader_name, doc_string, loader_optargs).
    The returned list is ordered by loader_name.
    '''
    load_all()
    return sorted(
        [(key, val.__doc__.strip(), val.LOADER_OPTARGS)
         for (key, val) in ALL_CLASSES.items()])


def get_formatted_descriptions():
    '''
    Gets a formatted string containing descriptions of all loaders in the
    ALL_CLASSES dictionary.
    '''
    descs = _get_descriptions()
    return '\n'.join(
        ['LOADER: %s - %s%s' % (
            ld[0],
            ld[1],
            ''.join(sorted(
                ['\n    DEFINE: (%s_)%s - %s (default=%s)' % (
                    ld[0], opt_name, opt_val[1], opt_val[0])
                 for (opt_name, opt_val) in ld[2].items()])))
         for ld in descs])

# end of file
