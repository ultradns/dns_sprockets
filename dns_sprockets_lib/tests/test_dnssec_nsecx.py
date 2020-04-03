'''
test_dnssec_nsecx - Tests NSECx support routines.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns.rdatatype

import dns_sprockets_lib.dnssec_nsecx as nsecx


def test_encode_salt():

    tests = [
        (None, None),
        (1, None),
        (b'', ''),
        (b'1', '31'),
        (b'a', '61'),
        (b'Testing', '54657374696e67')]

    for test in tests:
        print(test)
        assert nsecx.encode_salt(test[0]) == test[1]


def test_decode_salt():

    tests = [
        (None, None),
        (1, None),
        ('', b''),
        ('1', None),
        ('31', b'1'),
        ('54657374696e67', b'Testing'),
        ('54657374696E67', b'Testing')]

    for test in tests:
        print(test)
        assert nsecx.decode_salt(test[0]) == test[1]


def test_hash_nsec3_name():

    tests = [
        (None, '7f1962f2', 1, 15, None),
        (1, '7f1962f2', 1, 15, None),
        ('', '7f1962f2', 1, 15, 'lsa969sfkmlb6c92ea510pohd54douqu'),
        ('.', '7f1962f2', 1, 15, 'lsa969sfkmlb6c92ea510pohd54douqu'),
        ('001.cst.net.', '7f1962f2', 1, 15, 'uqml1am96tftfmlkagtbs82isr050sh0'),
        ('001.cst.net.', '7F1962F2', 1, 15, 'uqml1am96tftfmlkagtbs82isr050sh0'),
        ('001.001.cst.net.', '7F1962F2', 1, 15, '06es9cggdrorfdd4ns9ahocaikldrrp8'),
        ('test.001.cst.net.', '7F1962F2', 1, 15, 'kqgpu8i0ai43nem212bd0079j5si5r3k'),
        ('test2.001.cst.net.', '7F1962F2', 1, 15, 'al016abkh6lvdig6503fs92kdmotqh4v'),
        ('example', 'aabbccdd', 1, 12, '0p9mhaveqvm6t7vbl5lop2u3t2rp3tom'),
        ('a.example', 'aabbccdd', 1, 12, '35mthgpgcu1qg68fab165klnsnk3dpvl'),
        ('ai.example', 'aabbccdd', 1, 12, 'gjeqe526plbf1g8mklp59enfd789njgi'),
        ('ns1.example', 'aabbccdd', 1, 12, '2t7b4g4vsa5smi47k61mv5bv1a22bojr'),
        ('ns2.example', 'aabbccdd', 1, 12, 'q04jkcevqvmu85r014c7dkba38o0ji5r'),
        ('w.example', 'aabbccdd', 1, 12, 'k8udemvp1j2f7eg6jebps17vp3n8i58h'),
        ('*.w.example', 'aabbccdd', 1, 12, 'r53bq7cc2uvmubfu5ocmm6pers9tk9en'),
        ('x.w.example', 'aabbccdd', 1, 12, 'b4um86eghhds6nea196smvmlo4ors995'),
        ('y.w.example', 'aabbccdd', 1, 12, 'ji6neoaepv8b5o6k4ev33abha8ht9fgc'),
        ('x.y.w.example', 'aabbccdd', 1, 12, '2vptu5timamqttgl4luu9kg21e0aor3s'),
        ('xx.example', 'aabbccdd', 1, 12, 't644ebqk9bibcna874givr6joj62mlhv'),
        ('2t7b4g4vsa5smi47k61mv5bv1a22bojr.example', 'aabbccdd', 1, 12,
            'kohar7mbb8dc2ce8a9qvl8hon4k53uhi')]

    for test in tests:
        print(test)
        assert nsecx.hash_nsec3_name(test[0], test[1], test[2], test[3], False) == test[4]


def test__windows_covers():

    tests = [
        ([(0, None)], dns.rdatatype.A, False),
        ([(0, bytearray(b'\x00'))], dns.rdatatype.A, False),
        ([(0, bytearray(b'\x40'))], dns.rdatatype.A, True),
        ([(0, bytearray(b'\x40'))], dns.rdatatype.NS, False),
        ([(1, bytearray(b'\x40'))], dns.rdatatype.A, False),
        ([(1, bytearray(b'\x40'))], dns.rdatatype.CAA, True),
        ([(0, bytearray(b'\x00\x08'))], dns.rdatatype.PTR, True),
        ([(0, bytearray(
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08'))],
            dns.rdatatype.AXFR, True)]

    for test in tests:
        print(test)
        assert nsecx._windows_covers(test[0], test[1]) == test[2]


def test__windows_get_covered_types():

    tests = [
        ([(0, None)], []),
        ([(0, bytearray(b'\x00'))], []),
        ([(0, bytearray(b'\x40'))], [dns.rdatatype.A]),
        ([(0, bytearray(b'\x60'))], [dns.rdatatype.A, dns.rdatatype.NS]),
        ([(0, bytearray(b'\x64'))], [
            dns.rdatatype.A, dns.rdatatype.NS, dns.rdatatype.CNAME]),
        ([(1, bytearray(b'\x40'))], [dns.rdatatype.CAA]),
        ([(0, bytearray(b'\x40')),
          (1, bytearray(b'\x40'))], [dns.rdatatype.A, dns.rdatatype.CAA]),
        ([(0, bytearray(b'\x40\x08')),
          (1, bytearray(b'\x40'))], [
            dns.rdatatype.A, dns.rdatatype.CAA, dns.rdatatype.PTR])]

    for test in tests:
        print(test)
        assert sorted(nsecx._windows_get_covered_types(test[0])) == sorted(test[1])

# end of file
