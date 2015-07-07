**dns_sprockets**
=================

Overview
--------

dns_sprockets is a command-line framework for loading and validating DNS zones.
It is written in Python and uses the excellent dns_python library for much of
its functionality.

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

