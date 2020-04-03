'''
dnssec_nsec3 - Stuff for dealing with NSEC3-type zones.
-------------------------------------------------------
(maybe contribute somehow to dnspython?)

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''


import base64
import codecs

import Crypto.Hash.SHA
import dns.name
import dns.rdtypes.ANY.NSEC3


def encode_salt(b_bin_salt):
    '''
    Encodes binary NSEC3-type "salt" values to hexadecimal representation.

    :param bytes b_bin_salt: The binary salt to encode.
    :return: Lowercase hexadecimal bytes string representating the salt (or None for failure).
    '''
    try:
        b_hex_salt = codecs.encode(b_bin_salt, 'hex-codec')
        return codecs.decode(b_hex_salt, 'latin-1')
    except Exception:
        return None


def decode_salt(hex_salt):
    '''
    Decodes hexedecimal representation of NSEC3-type "salt" values to binary.

    :param str hex_salt: The hex-encoded salt to decode.
    :return: Binary value bytes of the salt value (or None for failure).
    '''
    try:
        b_hex_salt = codecs.encode(hex_salt, 'latin-1')
        return codecs.decode(b_hex_salt, 'hex-codec')
    except Exception:
        return None


def hash_nsec3_name(name, salt, algo, addl_iters, salt_is_binary=True):
    '''
    Hashes a domain name using indicated hashing algorithm / iterations.

    :param (str or dns.name.Name) name: The domain name to hash.
    :param (str or bytes) salt: The encoded salt to use (or empty string).
    :param int algo: The hashing algorithm to use.
    :param int addl_iters: The additional iterations to be applied.
    :param bool salt_is_binary: Set True if the salt is binary; False if hex string.
    :return: The (lowercase) base32hex-encoded string result (or None for failure).
    '''

    # Check name:
    if isinstance(name, dns.name.Name):
        name = name.to_text()
    elif not isinstance(name, str):
        return None

    # We only know how to do SHA-1:
    if algo != dns.rdtypes.ANY.NSEC3.SHA1:
        return None

    # Decode salt if necessary:
    if salt_is_binary:
        if isinstance(salt, str):
            b_salt = codecs.encode(salt, 'latin-1')
        elif isinstance(salt, bytes):
            b_salt = salt
        else:
            return None
    else:
        if not isinstance(salt, str):
            return None
        b_salt = decode_salt(salt)

    # Convert name to lowercase and wire format:
    b_bin_hash = dns.name.from_text(name.lower()).to_wire()

    # Iterate hashing according to RFC5155 section 5:
    for _ in range(1 + int(addl_iters)):
        b_bin_hash = Crypto.Hash.SHA.new(b_bin_hash + b_salt).digest()

    # Convert result to lowercase base32hex:
    b_hash = base64.b32encode(b_bin_hash).translate(
        dns.rdtypes.ANY.NSEC3.b32_normal_to_hex).lower()
    return codecs.decode(b_hash, 'latin-1')


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
                return bool(bitmap[byte] & (0x80 >> bit))

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
                bits = bitmap[byte]
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
