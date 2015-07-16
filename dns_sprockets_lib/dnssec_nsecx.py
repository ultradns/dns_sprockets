'''
dnssec_nsec3 - Stuff for dealing with NSEC3-type zones.
-------------------------------------------------------
(maybe contribute somehow to dnspython?)

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import base64

import Crypto.Hash.SHA
import dns.name
import dns.rdtypes.ANY.NSEC3


def encode_salt(bin_salt):
    '''
    Encodes binary NSEC3-type "salt" values to hexadecimal representation.

    :param str bin_salt: The binary salt to encode.
    :return: Lowercase hexadecimal string representating the salt (or None for failure).
    '''
    try:
        return bin_salt.encode('hex-codec')
    except StandardError:
        return None


def decode_salt(hex_salt):
    '''
    Decodes hexedecimal representation of NSEC3-type "salt" values to binary.

    :param str hex_salt: The hex-encoded salt to decode.
    :return: Binary value string of the salt value (or None for failure).
    '''
    try:
        return hex_salt.decode('hex-codec')
    except StandardError:
        return None


def hash_nsec3_name(name, salt, algo, addl_iters, salt_is_binary=True):
    '''
    Hashes a domain name using indicated hashing algorithm / iterations.

    :param str name: The domain name to hash.
    :param str salt: The salt to use (or empty string).
    :param int algo: The hashing algorithm to use.
    :param int addl_iters: The additional iterations to be applied.
    :param bool salt_is_binary: Set True if the salt is binary; False if hex-encoded.
    :return: The (lowercase) base32hex-encoded string result (or None for failure).
    '''

    # Check name:
    if isinstance(name, dns.name.Name):
        name = str(name)
    elif not isinstance(name, (str, unicode)):
        return None

    # We only know how to do SHA-1:
    if algo != dns.rdtypes.ANY.NSEC3.SHA1:
        return None

    # Decode salt if necessary:
    if not salt_is_binary:
        salt = decode_salt(salt)

    # Convert name to lowercase and wire format:
    bin_hash = dns.name.from_text(name.lower()).to_wire()

    # Iterate hashing according to RFC5155 section 5:
    for _ in xrange(1 + int(addl_iters)):
        bin_hash = Crypto.Hash.SHA.new(bin_hash + salt).digest()

    # Convert result to lowercase base32hex:
    return base64.b32encode(bin_hash).translate(
        dns.rdtypes.ANY.NSEC3.b32_normal_to_hex).lower()


def _windows_covers(windows, rrtype):
    '''
    Check to see if an NSECx windows list covers a type.

    :param list windows: An NSEC or NSEC3 windows list.
    :param int rrtype: The dns.rdatatype to test.
    :return: True if the windows covers the type; False if not.
    '''
    window = rrtype // 256
    for win in windows:
        if win[0] == window:
            bitmap = win[1]
            offset = rrtype % 256
            byte = offset // 8
            if bitmap and len(bitmap) >= byte + 1:
                bit = offset % 8
                return bool(ord(bitmap[byte]) & (0x80 >> bit))

    return False


def covers(nsecx_rdata, rrtype):
    '''
    Check to see if an NSECx covers a type.

    :param obj nsec_rdata: An NSEC or NSEC3 instance.
    :param int rrtype: The dns.rdatatype to test.
    :return: True if the NSECx covers the type; False if not.
    '''
    return _windows_covers(nsecx_rdata.windows, rrtype)


def _windows_get_covered_types(windows):
    '''
    Gets list of types covered by an NSECx windows list.

    :param list windows: An NSEC or NSEC3 windows list.
    :return: List of dns.rdatatype's that the NSECx covers.
    '''
    types = []
    for win in windows:
        window = win[0]
        bitmap = win[1]
        if bitmap:
            for byte in range(len(bitmap)):
                bits = ord(bitmap[byte])
                if bits:
                    for bit in range(8):
                        if bits & (0x80 >> bit):
                            types.append(window * 256 + byte * 8 + bit)
    return types


def get_covered_types(nsecx_rdata):
    '''
    Gets list of types covered by an NSECx.

    :param obj nsecx_rdata: The NSEC or NSEC3 instance.
    :return: List of dns.rdatatype's that the NSECx covers.
    '''
    return _windows_get_covered_types(nsecx_rdata.windows)

# end of file
