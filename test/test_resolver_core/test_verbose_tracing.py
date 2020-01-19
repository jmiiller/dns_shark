from unittest.mock import Mock
import unittest
from dns_shark.resolver_core import ResolverCore
from dns_shark.resource_record import ResourceRecord
from typing import List
from contextlib import redirect_stdout
from io import StringIO


class NameServerResponseThenAuthoritativeResponseIpv6Test(unittest.TestCase):
    """
    Unit testing for resolver_core.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """

        cls.first_response: bytes = bytes.fromhex('150e800000010000000d000c0377777706676f6f676c6503636f6d00001c0001'
                                                  'c017000200010002a300001401650c67746c642d73657276657273036e657400'
                                                  'c017000200010002a30000040162c02ec017000200010002a3000004016ac02e'
                                                  'c017000200010002a3000004016dc02ec017000200010002a30000040169c02e'
                                                  'c017000200010002a30000040166c02ec017000200010002a30000040161c02e'
                                                  'c017000200010002a30000040167c02ec017000200010002a30000040168c02e'
                                                  'c017000200010002a3000004016cc02ec017000200010002a3000004016bc02e'
                                                  'c017000200010002a30000040163c02ec017000200010002a30000040164c02e'
                                                  'c02c000100010002a3000004c00c5e1ec02c001c00010002a300001020010502'
                                                  '1ca100000000000000000030c04c000100010002a3000004c0210e1ec04c001c'
                                                  '00010002a300001020010503231d00000000000000020030c05c000100010002'
                                                  'a3000004c0304f1ec05c001c00010002a3000010200105027094000000000000'
                                                  '00000030c06c000100010002a3000004c037531ec06c001c00010002a3000010'
                                                  '20010501b1f900000000000000000030c07c000100010002a3000004c02bac1e'
                                                  'c07c001c00010002a30000102001050339c100000000000000000030c08c0001'
                                                  '00010002a3000004c023331ec09c000100010002a3000004c005061e')

        cls.second_response: bytes = bytes.fromhex('e13b800000010000000400080377777706676f6f676c6503636f6d00001c000'
                                                   '1c010000200010002a3000006036e7332c010c010000200010002a300000603'
                                                   '6e7331c010c010000200010002a3000006036e7333c010c010000200010002a'
                                                   '3000006036e7334c010c02c001c00010002a300001020014860480200340000'
                                                   '00000000000ac02c000100010002a3000004d8ef220ac03e001c00010002a30'
                                                   '000102001486048020032000000000000000ac03e000100010002a3000004d8'
                                                   'ef200ac050001c00010002a30000102001486048020036000000000000000ac'
                                                   '050000100010002a3000004d8ef240ac062001c00010002a300001020014860'
                                                   '48020038000000000000000ac062000100010002a3000004d8ef260a')

        cls.authoritative_response: bytes = bytes.fromhex('c98f840000010001000000000377777706676f6f676c6503636f6d00'
                                                          '001c0001c00c001c00010000012c00102607f8b0400a080300000000'
                                                          '00002004')

        cls.mock_socket: Mock = Mock(**{'recv.side_effect': [cls.first_response,
                                                             cls.second_response,
                                                             cls.authoritative_response]})

        cls.mock_random: Mock = Mock(**{'randint.side_effect': [0x150e, 0xe13b, 0xc98f]})

        cls.buffer = StringIO()

    def test_verbose_tracing(self):
        """
        Test case to confirm the verbose tracing output is correct.
        """

        resolver: ResolverCore = ResolverCore(self.mock_socket, True, "1.2.3.4", self.mock_random)

        with redirect_stdout(self.buffer):
            resolver.resolve_domain_name("www.google.com", "1.2.3.4", 28)

        self.assertEqual(self.buffer.getvalue(),
                         "\n\nQuery ID:    5390 www.google.com  AAAA --> 1.2.3.4\n"
                         "Response ID: 5390 Authoritative = False\n"
                         "  Answers (0)\n"
                         "  Name Servers (13)\n"
                         "      com                            172800     NS   e.gtld-servers.net\n"
                         "      com                            172800     NS   b.gtld-servers.net\n"
                         "      com                            172800     NS   j.gtld-servers.net\n"
                         "      com                            172800     NS   m.gtld-servers.net\n"
                         "      com                            172800     NS   i.gtld-servers.net\n"
                         "      com                            172800     NS   f.gtld-servers.net\n"
                         "      com                            172800     NS   a.gtld-servers.net\n"
                         "      com                            172800     NS   g.gtld-servers.net\n"
                         "      com                            172800     NS   h.gtld-servers.net\n"
                         "      com                            172800     NS   l.gtld-servers.net\n"
                         "      com                            172800     NS   k.gtld-servers.net\n"
                         "      com                            172800     NS   c.gtld-servers.net\n"
                         "      com                            172800     NS   d.gtld-servers.net\n"
                         "  Additional Information (12)\n"
                         "      e.gtld-servers.net             172800     A    192.12.94.30\n"
                         "      e.gtld-servers.net             172800     AAAA 2001:502:1ca1::30\n"
                         "      b.gtld-servers.net             172800     A    192.33.14.30\n"
                         "      b.gtld-servers.net             172800     AAAA 2001:503:231d::2:30\n"
                         "      j.gtld-servers.net             172800     A    192.48.79.30\n"
                         "      j.gtld-servers.net             172800     AAAA 2001:502:7094::30\n"
                         "      m.gtld-servers.net             172800     A    192.55.83.30\n"
                         "      m.gtld-servers.net             172800     AAAA 2001:501:b1f9::30\n"
                         "      i.gtld-servers.net             172800     A    192.43.172.30\n"
                         "      i.gtld-servers.net             172800     AAAA 2001:503:39c1::30\n"
                         "      f.gtld-servers.net             172800     A    192.35.51.30\n"
                         "      a.gtld-servers.net             172800     A    192.5.6.30\n"
                         "\n"
                         "\nQuery ID:    57659 www.google.com  AAAA --> 192.12.94.30\n"
                         "Response ID: 57659 Authoritative = False\n"
                         "  Answers (0)\n"
                         "  Name Servers (4)\n"
                         "      google.com                     172800     NS   ns2.google.com\n"
                         "      google.com                     172800     NS   ns1.google.com\n"
                         "      google.com                     172800     NS   ns3.google.com\n"
                         "      google.com                     172800     NS   ns4.google.com\n"
                         "  Additional Information (8)\n"
                         "      ns2.google.com                 172800     AAAA 2001:4860:4802:34::a\n"
                         "      ns2.google.com                 172800     A    216.239.34.10\n"
                         "      ns1.google.com                 172800     AAAA 2001:4860:4802:32::a\n"
                         "      ns1.google.com                 172800     A    216.239.32.10\n"
                         "      ns3.google.com                 172800     AAAA 2001:4860:4802:36::a\n"
                         "      ns3.google.com                 172800     A    216.239.36.10\n"
                         "      ns4.google.com                 172800     AAAA 2001:4860:4802:38::a\n"
                         "      ns4.google.com                 172800     A    216.239.38.10\n"
                         "\n"
                         "\nQuery ID:    51599 www.google.com  AAAA --> 216.239.34.10\n"
                         "Response ID: 51599 Authoritative = True\n"
                         "  Answers (1)\n"
                         "      www.google.com                 300        AAAA 2607:f8b0:400a:803::2004\n"
                         "  Name Servers (0)\n"
                         "  Additional Information (0)\n")
