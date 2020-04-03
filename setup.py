#!/usr/bin/env python2.7
'''
setup.py - Setup script for the "dns_sprockets" zone validator.
---------------------------------------------------------------

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import os.path
from codecs import open
from setuptools import setup
from setuptools import find_packages

from dns_sprockets_version import VERSION


# Get the long description from the relevant file:
THIS_DIR = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(THIS_DIR, 'README.rst'), encoding='utf-8') as the_file:
    long_description = the_file.read()


setup(
    name='dns_sprockets',
    version=VERSION,
    license='Apache License, Version 2.0',
    author='Ashley Roeckelein',
    author_email='ashley.roeckelein@neustar.biz',
    maintainer='Ashley Roeckelein',
    maintainer_email='ashley.roeckelein@neustar.biz',
    url='https://github.com/ultradns/dns_sprockets',
    description='Command-line DNS Zone validation tool',
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Customer Service',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'],
    keywords='DNS zone validation',
    install_requires=[
        'dnspython>=1.16.0',
        'pycryptodome>=3.9.7'],
    packages=find_packages(),
    py_modules=[
        'dns_sprockets_version',
        'dns_sprockets'],
    entry_points={'console_scripts': ['dns_sprockets = dns_sprockets:run']},
    include_package_data=True,
    package_data={
        'dns_sprockets_lib/tests/data': ['dns_sprockets_lib/tests/data/*']})

# end of file
