'''
test_dns_utils- Tests misc. DNS support routines.

.. Copyright (c) 2015 Neustar, Inc. All rights reserved.
.. See COPYRIGHT.txt for full notice.  See LICENSE.txt for terms and conditions.
'''
# pylint: skip-file


import dns.name

import dns_sprockets_lib.dns_utils as dns_utils


def test_is_delegated():

    tests = [
        ([], '', False),
        ([], 'test', False),
        (['test'], '', False),
        (['test'], 'test', True),
        (['test'], 'a.test', True),
        (['test'], 'b.a.test', True),
        (['test1', 'test2'], 'test', False),
        (['test1', 'test2'], 'test1.test2', True),
        (['test1', 'test2'], 'test2.test1', True)]

    for test in tests:
        names = [dns.name.from_text(s) for s in test[0]]
        name = dns.name.from_text(test[1])
        assert dns_utils.is_delegated(names, name) is test[2]


def test_dnssec_name_cmp_to_key():

    key_class = dns_utils.dns_name_cmp_to_key()
    a = key_class(dns.name.from_text('a.b.c'))
    b = key_class(dns.name.from_text('b.c'))
    assert (a < b) is False
    assert (a > b) is True
    assert (a == b) is False
    assert (a <= b) is False
    assert (a >= b) is True
    assert (a != b) is True


def test_dnssec_sort_names():

    tests = [
        ([], []),
        ([''], ['']),
        (['a'], ['a']),
        (['a', ''], ['', 'a']),
        (['a', 'b'], ['a', 'b']),
        (['b', 'a'], ['a', 'b']),
        (['a.b', 'b'], ['b', 'a.b']),
        (['a.b', 'c.a.b', 'b'], ['b', 'a.b', 'c.a.b']),
        (['aa.b', 'a.b', 'caa.b'], ['a.b', 'aa.b', 'caa.b'])]

    for test in tests:
        ins = [dns.name.from_text(s) for s in test[0]]
        outs = [dns.name.from_text(s) for s in test[1]]
        assert dns_utils.dnssec_sort_names(ins) == outs


def test_calc_node_names():

    tests = [
        ('', False, [], []),
        ('', False, [''], ['']),
        ('', False, ['a'], ['a']),
        ('', False, ['d.c.b.a'], ['d.c.b.a']),
        ('', False, ['*.a'], ['*.a']),
        ('', False, ['a', '*.a'], ['a', '*.a']),
        ('', False, ['b.a', '*.a'], ['*.a', 'b.a']),
        ('', False, ['c.b.a', '*.a'], ['*.a', 'c.b.a']),
        ('', False, ['d.c.b.a', '*.a'], ['*.a', 'd.c.b.a']),
        ('', False, ['d.c.b.a', '*.*.a'], ['*.*.a', 'd.c.b.a']),
        ('', False, ['d.c.b.a', '*.a', '*.*.a'], ['*.a', '*.*.a', 'd.c.b.a']),
        ('a', True, [], []),
        ('a', True, [''], ['']),
        ('a', True, ['a'], ['a']),
        ('a', True, ['d.c.b.a'], ['a', 'b.a', 'c.b.a', 'd.c.b.a']),
        ('a', True, ['*.a'], ['a', '*.a']),
        ('a', True, ['a', '*.a'], ['a', '*.a']),
        ('a', True, ['b.a', '*.a'], ['a', '*.a', 'b.a']),
        ('a', True, ['c.b.a', '*.a'], ['a', '*.a', 'b.a', 'c.b.a']),
        ('a', True, ['d.c.b.a', '*.a'],
                    ['a', '*.a', 'b.a', 'c.b.a', 'd.c.b.a']),
        ('a', True, ['d.c.b.a', '*.*.a'],
                    ['a', '*.a', '*.*.a', 'b.a', 'c.b.a', 'd.c.b.a']),
        ('a', True, ['d.c.b.a', '*.a', '*.*.a'],
                    ['a', '*.a', '*.*.a', 'b.a', 'c.b.a', 'd.c.b.a']),
        ('example', True,
            ['example', 'a.example', 'ns1.a.example', 'ns2.a.example',
             'ai.example', 'c.example', 'ns1.c.example', 'ns2.c.example',
             'ns1.example', 'ns2.example', '*.w.example', 'x.w.example',
             'x.y.w.example', 'xx.example'],
            ['example', 'a.example', 'ns1.a.example', 'ns2.a.example',
             'ai.example', 'c.example', 'ns1.c.example', 'ns2.c.example',
             'ns1.example', 'ns2.example', 'w.example', '*.w.example',
             'x.w.example', 'y.w.example', 'x.y.w.example', 'xx.example'])]

    for test in tests:
        ents_too = test[1]
        zname = ents_too and dns.name.from_text(test[0]) or None
        ins = [dns.name.from_text(s) for s in test[2]]
        outs = [dns.name.from_text(s) for s in test[3]]
        actual = dns_utils.calc_node_names(ins, ents_too, zname)
        #print zname, ents_too, ins, outs, actual
        assert actual == outs

# end of file
