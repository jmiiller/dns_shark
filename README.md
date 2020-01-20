# DNS Shark
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.com/jmiiller/dns_shark.svg?branch=master)](https://travis-ci.com/jmiiller/dns_shark)
[![codecov](https://codecov.io/gh/jmiiller/dns_shark/branch/master/graph/badge.svg)](https://codecov.io/gh/jmiiller/dns_shark)




DNS Shark is a simple domain name resolver.

At the moment, DNS Shark is capable of resolving domain names to either an IPv4 or IPv6 address. In addition, DNS Shark can provide verbose tracing output, if desired.

DNS Shark is currently only able to handle A, AAAA, NS, and CNAME resource record types. Thus, any name resolution process that involves other resource record types is currently unsupported, although I wish to add complete handling of all resource record types in the future.

DNS Shark has been developed with MyPy and, thus, it strives to provide complete static type annotation for all the code.

Continuous Integration with Travis CI. Code coverage tracking with Codecov.

## Installation

You can install DNS Shark from [PyPI](https://pypi.org/project/realpython-reader/):

```
pip install dns_shark
```

DNS Shark is supported on Python 3.6 and above.

## How to use

DNS Shark is a command line application, named `dns_shark`. 

To resolve a domain name, call the program with two required arguments:
1. The IP address of a DNS server. (The domain name resolution process will begin with this specified DNS server.)
2. The domain name you wish to resolve.

A simple domain name resolution for www.google.com.
```
$ dns_shark 199.7.83.42 www.google.com

Answers:
  www.google.com 300   A 172.217.3.196
```

If you want to resolve the domain name to IPv6 addresses, instead of IPv4 addresses, then specify the `--ipv6 1` option.

```
$ dns_shark 199.7.83.42 www.google.com --ipv6 1

Answers:
  www.google.com 300   AAAA 2607:f8b0:400a:809::2004
```

If you want verbose tracing information of the name resolution process, specify the  `--verbose 1` option.

```
$ dns_shark 199.7.83.42 www.google.com --verbose 1


Query ID:    25408 www.google.com  A --> 199.7.83.42
Response ID: 25408 Authoritative = False
  Answers (0)
  Name Servers (13)
      com                            172800     NS   a.gtld-servers.net
      com                            172800     NS   b.gtld-servers.net
      com                            172800     NS   c.gtld-servers.net
      com                            172800     NS   d.gtld-servers.net
      com                            172800     NS   e.gtld-servers.net
      com                            172800     NS   f.gtld-servers.net
      com                            172800     NS   g.gtld-servers.net
      com                            172800     NS   h.gtld-servers.net
      com                            172800     NS   i.gtld-servers.net
      com                            172800     NS   j.gtld-servers.net
      com                            172800     NS   k.gtld-servers.net
      com                            172800     NS   l.gtld-servers.net
      com                            172800     NS   m.gtld-servers.net
  Additional Information (14)
      a.gtld-servers.net             172800     A    192.5.6.30
      b.gtld-servers.net             172800     A    192.33.14.30
      c.gtld-servers.net             172800     A    192.26.92.30
      d.gtld-servers.net             172800     A    192.31.80.30
      e.gtld-servers.net             172800     A    192.12.94.30
      f.gtld-servers.net             172800     A    192.35.51.30
      g.gtld-servers.net             172800     A    192.42.93.30
      h.gtld-servers.net             172800     A    192.54.112.30
      i.gtld-servers.net             172800     A    192.43.172.30
      j.gtld-servers.net             172800     A    192.48.79.30
      k.gtld-servers.net             172800     A    192.52.178.30
      l.gtld-servers.net             172800     A    192.41.162.30
      m.gtld-servers.net             172800     A    192.55.83.30
      a.gtld-servers.net             172800     AAAA 2001:503:a83e::2:30


Query ID:    50458 www.google.com  A --> 192.5.6.30
Response ID: 50458 Authoritative = False
  Answers (0)
  Name Servers (4)
      google.com                     172800     NS   ns2.google.com
      google.com                     172800     NS   ns1.google.com
      google.com                     172800     NS   ns3.google.com
      google.com                     172800     NS   ns4.google.com
  Additional Information (8)
      ns2.google.com                 172800     AAAA 2001:4860:4802:34::a
      ns2.google.com                 172800     A    216.239.34.10
      ns1.google.com                 172800     AAAA 2001:4860:4802:32::a
      ns1.google.com                 172800     A    216.239.32.10
      ns3.google.com                 172800     AAAA 2001:4860:4802:36::a
      ns3.google.com                 172800     A    216.239.36.10
      ns4.google.com                 172800     AAAA 2001:4860:4802:38::a
      ns4.google.com                 172800     A    216.239.38.10


Query ID:    46368 www.google.com  A --> 216.239.34.10
Response ID: 46368 Authoritative = True
  Answers (1)
      www.google.com                 300        A    172.217.3.196
  Name Servers (0)
  Additional Information (0)

Answers:
  www.google.com 300   A 172.217.3.196
```

These options can also be specified together.

```
$ dns_shark 199.7.83.42 www.google.com --verbose 1 --ipv6 1


Query ID:    18404 www.google.com  AAAA --> 199.7.83.42
Response ID: 18404 Authoritative = False
  Answers (0)
  Name Servers (13)
      com                            172800     NS   a.gtld-servers.net
      com                            172800     NS   b.gtld-servers.net
      com                            172800     NS   c.gtld-servers.net
      com                            172800     NS   d.gtld-servers.net
      com                            172800     NS   e.gtld-servers.net
      com                            172800     NS   f.gtld-servers.net
      com                            172800     NS   g.gtld-servers.net
      com                            172800     NS   h.gtld-servers.net
      com                            172800     NS   i.gtld-servers.net
      com                            172800     NS   j.gtld-servers.net
      com                            172800     NS   k.gtld-servers.net
      com                            172800     NS   l.gtld-servers.net
      com                            172800     NS   m.gtld-servers.net
  Additional Information (14)
      a.gtld-servers.net             172800     A    192.5.6.30
      b.gtld-servers.net             172800     A    192.33.14.30
      c.gtld-servers.net             172800     A    192.26.92.30
      d.gtld-servers.net             172800     A    192.31.80.30
      e.gtld-servers.net             172800     A    192.12.94.30
      f.gtld-servers.net             172800     A    192.35.51.30
      g.gtld-servers.net             172800     A    192.42.93.30
      h.gtld-servers.net             172800     A    192.54.112.30
      i.gtld-servers.net             172800     A    192.43.172.30
      j.gtld-servers.net             172800     A    192.48.79.30
      k.gtld-servers.net             172800     A    192.52.178.30
      l.gtld-servers.net             172800     A    192.41.162.30
      m.gtld-servers.net             172800     A    192.55.83.30
      a.gtld-servers.net             172800     AAAA 2001:503:a83e::2:30


Query ID:    36919 www.google.com  AAAA --> 192.5.6.30
Response ID: 36919 Authoritative = False
  Answers (0)
  Name Servers (4)
      google.com                     172800     NS   ns2.google.com
      google.com                     172800     NS   ns1.google.com
      google.com                     172800     NS   ns3.google.com
      google.com                     172800     NS   ns4.google.com
  Additional Information (8)
      ns2.google.com                 172800     AAAA 2001:4860:4802:34::a
      ns2.google.com                 172800     A    216.239.34.10
      ns1.google.com                 172800     AAAA 2001:4860:4802:32::a
      ns1.google.com                 172800     A    216.239.32.10
      ns3.google.com                 172800     AAAA 2001:4860:4802:36::a
      ns3.google.com                 172800     A    216.239.36.10
      ns4.google.com                 172800     AAAA 2001:4860:4802:38::a
      ns4.google.com                 172800     A    216.239.38.10


Query ID:    35735 www.google.com  AAAA --> 216.239.34.10
Response ID: 35735 Authoritative = True
  Answers (1)
      www.google.com                 300        AAAA 2607:f8b0:400a:809::2004
  Name Servers (0)
  Additional Information (0)

Answers:
  www.google.com 300   AAAA 2607:f8b0:400a:809::2004
```

You can also call DNS Shark in your own Python code, by importing from the dns_resolver package:

```
>>> from dns_shark.dns_resolver import Resolver
>>> records = Resolver.ask('www.google.com', '199.7.83.42')
>>> print(records)
[ResourceRecord(name: www.google.com, type: 1, class: 1, ttl: 300, rdlength: 4, rdata: 172.217.3.196)]
```
