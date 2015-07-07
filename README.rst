**dns_sprockets**
=================

Overview
--------

dns_sprockets is a command-line framework for loading and validating DNS zones.
It is written in Python and uses the excellent `dnspython <http://www.dnspython.org>`_
library for much of its functionality.

Audience
''''''''

Possible users include DNS code developers and quality assurance, internet 
customer service, system administrators, and end-users who are interested to 
know if their DNS zones are valid.

Features
''''''''

The command-line tool returns useful return codes, supporting automated build
systems.  It is built around the concept of plug-ins for implementing both the
zone loading and zone validating functions, and easily allows end-users the
ability to define new loaders and validators.

* Zones may be loaded using various means.  The framework supports "loader" 
  plug-ins that pull DNS zone data from any source.  Initially provided are
  'File' and 'Xfr' plugins to pull zone data from host files and XFR servers,
  respectively.

* Validations are modular pieces of code that may be selectively enabled.  The
  framework supports "validator" plug-ins that operate in one of four views:
  
  - Zone: Some aspect of the entire zone is validated.
  - Node: Every node (i.e. list of RRSets with the same owner name) can be validated.
  - RRSet: Every RRSet can be validated.
  - Record: Every DNS record can be validated.
  
  Initially provided in this package are some basic zone validators, and a
  fairly complete set of DNSSEC-type zone validators.

The Node, RRSet, and Record views may be optionally filtered by one or more 
resource record types, to simplify and focus the validation code.  Additionally,
each validator can be marked to run for non-DNSSEC zones, NSEC1-style DNSSEC
zones, or NSEC3-style DNSSEC zones. 

Installation
------------

Easy!  Use pip (preferably in a virtual python environment)::

    $ pip install dns_sprockets

Usage
-----

Once installed, simply issue the dns_sprockets command.  For example to get a
usage message::

    $ dns_sprockets --help

    # dns_sprockets (1.0.0) - A DNS zone validation tool
    usage: dns_sprockets [-h] [-z s] [-l s] [-s s] [-i s] [-x s] [-d s] [-f s]
                         [-e] [-v]
    
    optional arguments:
      -h, --help            show this help message and exit
      -z s, --zone s        Name of zone to validate [www.ultradns.com]
      -l s, --loader s      Zone loader method to use (one of: file, xfr) [xfr]
      -s s, --source s      Loader source to use [127.0.0.1#53]
      -i s, --include s     Only include this test (can use multiple times)
      -x s, --exclude s     Exclude this test (can use multiple times)
      -d s, --define s      Define other params (can use multiple times)
      -f s, --force-dnssec-type s
                            Use DNSSEC type (one of: detect, unsigned, NSEC,
                            NSEC3) [detect]
      -e, --errors-only     Show validation errors only [False]
      -v, --verbose         Show detailed processing info [False]
    
    Use @filename to read some/all arguments from a file.
    
    Use -d's to define optional, module-specific parameters if desired (e.g. to tell
    'xfr' loader to use a specific source address, use "-d xfr_source=1.2.3.4").
    The optional parameters are listed under each loader and test description in
    DEFINE lines, if available.
    
    By default, all tests are run.  Use -i's to explicitly specify desired tests,
    or -x's to eliminate undesired tests.
    
    The list of available loaders is:
    ---------------------------------------------------------------------------
    LOADER: file - Loads a zone from a file in AXFR-type or Bind host-type format.
        DEFINE: file_allow_include - Allow file to include other files (default=1)
        DEFINE: file_rdclass - Class of records to pull (default=IN)
    LOADER: xfr - Loads a zone by XFR from a name server.
        DEFINE: xfr_af - The address family to use, AF_INET or AF_INET6 (default=None)
        DEFINE: xfr_keyalgorithm - The TSIG algorithm to use, one of: HMAC-MD5.SIG-ALG.REG.INT. hmac-sha1. hmac-sha224. hmac-sha256. hmac-sha384. hmac-sha512. (default=HMAC-MD5.SIG-ALG.REG.INT.)
        DEFINE: xfr_keyname - The name of the TSIG to use (default=None)
        DEFINE: xfr_keyring - The TSIG keyring to use, a text dict of name->base64_secret e.g. "{'n1':'H477A900','n2':'K845CL21'}" (default=None)
        DEFINE: xfr_lifetime - Total seconds to wait for complete transfer (default=None)
        DEFINE: xfr_rdclass - Class of records to pull (default=IN)
        DEFINE: xfr_rdtype - Type of XFR to perform, AXFR or IXFR (default=AXFR)
        DEFINE: xfr_serial - SOA serial number to use as base for IXFR diff (default=0)
        DEFINE: xfr_source - Source address for the transfer (default=None)
        DEFINE: xfr_source_port - Source port for the transfer (default=0)
        DEFINE: xfr_timeout - Seconds to wait for each response message (default=5.0)
        DEFINE: xfr_use_udp - Use UDP for IXFRing (default=0)
    
    The list of available tests is:
    ---------------------------------------------------------------------------
    TEST: dnskey_bits (REC_TEST[DNSKEY]) - Checks DNSKEY flags and protocol.
    TEST: dnskey_origin (ZONE_TEST) - Checks for a ZSK at zone origin.
    TEST: dnssectype_ambiguous (ZONE_TEST) - Checks for existence of both NSEC and NSEC3 in the zone.
    TEST: ns_origin (ZONE_TEST) - Checks for at least one NS at zone origin.
    TEST: nsec3_chain (ZONE_TEST) - Checks for valid NSEC3 chain.
    TEST: nsec3_missing (RRSET_TEST) - Checks that all (non-NSEC3/RRSIG, non-delegated) RRSets are covered with an NSEC3.
    TEST: nsec3_orphan (REC_TEST[NSEC3]) - Checks for orphan or invalid-covers NSEC3s.
    TEST: nsec3param_origin (ZONE_TEST) - Checks for an NSEC3PARAM at zone origin for nsec3-type zones.
    TEST: nsec_chain (ZONE_TEST) - Checks for valid NSEC chain.
    TEST: nsec_missing (RRSET_TEST) - Checks that all (non-NSEC/RRSIG, non-delegated) RRSets are covered with an NSEC.
    TEST: nsec_orphan (REC_TEST[NSEC]) - Checks for orphan or invalid-covers NSECs.
    TEST: nsecx_ttls_match (REC_TEST[NSEC,NSEC3]) - Checks that NSECx TTL's match SOA's minimum.
    TEST: rrsig_covers (REC_TEST[RRSIG]) - Checks RRSIG's don't cover RRSIG's.
    TEST: rrsig_missing (RRSET_TEST) - Checks that all (non-RRSIG, non-delegated) RRSets are covered with an RRSIG.
        DEFINE: rrsig_missing_now - Time to use for validating RRSIG time windows, e.g. 20150101123000 (default=None)
    TEST: rrsig_orphan (REC_TEST[RRSIG]) - Checks for orphan RRSIGs.
        DEFINE: rrsig_orphan_now - Time to use for validating RRSIG time windows, e.g. 20150101123000 (default=None)
    TEST: rrsig_signer_match (REC_TEST[RRSIG]) - Checks RRSIG signers match the zone.
    TEST: rrsig_time (REC_TEST[RRSIG]) - Checks RRSIG's inception <= expiration.
    TEST: rrsig_ttls_match (REC_TEST[RRSIG]) - Checks RRSIG TTL's match original and covered TTL's.
    TEST: soa_origin (ZONE_TEST) - Checks for an SOA at zone origin.
    TEST: soa_unique (ZONE_TEST) - Checks for a single SOA in the zone.

Sample Usage
''''''''''''

Let's say you want to validate and only see errors an NSEC3-style DNSSEC zone
called "example", from a file, and wish to run all available/applicable validations.
Since this will check RRSIG signatures, you'll need to add a few defines to properly
state the "now" time to use for two of the validators::

    $ ZONE_FILE=$(VIRTUAL_ENV)/lib/python2.7/site-packages/dns_sprockets_lib/tests/data/rfc5155_example.
    
    $ TIME_NOW=20100101000000
    
    $ dns_sprocket -z example -l file -s $(ZONE_FILE) -e \
        -d rrsig_missing_now=$(TIME_NOW) -d rrsig_orphan_now=$(TIME_NOW)
    
    # dns_sprockets (1.0.0) - A DNS Zone validation tool
    # Checking zone: example.
    # Loader: file from: rfc5155_example. elapsed=0.018354 secs
    # Zone appears to be DNSSEC type: NSEC3
    # Extra defines: ['rrsig_missing_now=20100101000000', 'rrsig_orphan_now=20100101000000']
    # Skipping test: nsec_chain  (DNSSEC type for zone: NSEC3, for test: NSEC)
    # Skipping test: nsec_missing  (DNSSEC type for zone: NSEC3, for test: NSEC)
    # Skipping test: nsec_orphan  (DNSSEC type for zone: NSEC3, for test: NSEC)
    # Running tests: ['dnskey_origin', 'dnssectype_ambiguous', 'ns_origin', 'nsec3_chain', 'nsec3param_origin', 'soa_origin', 'soa_unique', 'nsec3_missing', 'rrsig_missing', 'dnskey_bits', 'nsec3_orphan', 'nsecx_ttls_match', 'rrsig_covers', 'rrsig_orphan', 'rrsig_signer_match', 'rrsig_time', 'rrsig_ttls_match']
    # END RESULT: 0 ERRORS in 229 tests
    # TOTAL ELAPSED TIME: 0.063526 SECS  LOAD TIME: 0.018354 SECS  TEST TIME: 0.045172 SECS
    
    $ echo $?
    0

