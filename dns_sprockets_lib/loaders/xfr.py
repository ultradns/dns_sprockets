'''
xfr - Zone loader: Xfr
----------------------

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import dns.rdatatype
import dns.inet
import dns.tsig
import dns.tsigkeyring
import dns.query
import dns.zone

import dns_sprockets_lib.loaders as loaders


_KEYALGORITHMS = {
    str(dns.tsig.HMAC_MD5): dns.tsig.HMAC_MD5,
    str(dns.tsig.HMAC_SHA1): dns.tsig.HMAC_SHA1,
    str(dns.tsig.HMAC_SHA224): dns.tsig.HMAC_SHA224,
    str(dns.tsig.HMAC_SHA256): dns.tsig.HMAC_SHA256,
    str(dns.tsig.HMAC_SHA384): dns.tsig.HMAC_SHA384,
    str(dns.tsig.HMAC_SHA512): dns.tsig.HMAC_SHA512}


class Xfr(loaders.ZoneLoader):
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    '''
    Loads a zone by XFR from a name server.
    '''
    LOADER_OPTARGS = {
        'rdtype': ('AXFR', 'Type of XFR to perform, AXFR or IXFR'),
        'rdclass': ('IN', 'Class of records to pull'),
        'timeout': ('5.0', 'Seconds to wait for each response message'),
        'keyring': (None,
            "The TSIG keyring to use, a text dict of name->base64_secret"
            " e.g. \"{'n1':'H477A900','n2':'K845CL21'}\""),
        'keyname': (None, 'The name of the TSIG to use'),
        'af': (None, 'The address family to use, AF_INET or AF_INET6'),
        'lifetime': (None, 'Total seconds to wait for complete transfer'),
        'source': (None, 'Source address for the transfer'),
        'source_port': ('0', 'Source port for the transfer'),
        'serial': ('0', 'SOA serial number to use as base for IXFR diff'),
        'use_udp': ('0', 'Use UDP for IXFRing'),
        'keyalgorithm': (str(dns.tsig.default_algorithm),
            'The TSIG algorithm to use, one of: %s' % (
                ' '.join(sorted(_KEYALGORITHMS.keys()))))}

    DEFAULT_PORT = 53

    def __init__(self, args):
        '''
        Ctor.

        :param obj args: The application's command-line arguments object.
        '''
        self.rdtype = None
        self.rdclass = None
        self.timeout = None
        self.keyring = None
        self.keyname = None
        # pylint: disable=invalid-name
        self.af = None
        self.lifetime = None
        self.source = None
        self.source_port = None
        self.serial = None
        self.use_udp = None
        self.keyalgorithm = None
        super(Xfr, self).__init__(args)

    def run(self):
        '''
        :return: A dns.zone.Zone instance.
        '''
        afs = {'AF_INET': dns.inet.AF_INET, 'AF_INET6': dns.inet.AF_INET6}
        (where, port) = ('#' in self.args.source
            and self.args.source.split('#')[:2]
            or (self.args.source, self.DEFAULT_PORT))

        other_args = {
            'port': int(port),
            'relativize': False,
            'rdtype': self.rdtype,
            'rdclass': self.rdclass,
            'timeout': self.timeout and float(self.timeout) or None,
            # pylint: disable=eval-used
            'keyring': self.keyring and dns.tsigkeyring.from_text(eval(self.keyring)) or None,
            'keyname': self.keyname,
            'af': self.af and afs[self.af] or None,
            'lifetime': self.lifetime and float(self.lifetime) or None,
            'source': self.source,
            'source_port': int(self.source_port),
            'serial': int(self.serial),
            'use_udp': bool(int(self.use_udp)),
            'keyalgorithm': _KEYALGORITHMS[self.keyalgorithm]}

        msg_gen = dns.query.xfr(where, self.args.zone, **other_args)
        try:
            return dns.zone.from_xfr(msg_gen, relativize=False, check_origin=False)
        except dns.rdatatype.UnknownRdatatype:
            print('ERROR: Unable to XFR from %s - Permission to XFR from here?' % (
                self.args.source))
            return None

# end of file
