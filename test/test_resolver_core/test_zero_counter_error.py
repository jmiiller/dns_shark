from unittest.mock import Mock
import unittest
from dns_shark.resolver_core import ResolverCore
from dns_shark.errors.dns_zero_counter_error import DNSZeroCounterError


class DNSZeroCounterErrorTest(unittest.TestCase):
    """
    Unit testing for resolver_core.
    """

    @classmethod
    def setUp(cls):
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

        cls.third_response: bytes = bytes.fromhex('c98f840000010001000000000377777706676f6f676c6503636f6d00'
                                                          '001c0001c00c001c00010000012c00102607f8b0400a080300000000'
                                                          '00002004')

        cls.mock_socket: Mock = Mock(**{'recv.side_effect': [cls.first_response,
                                                             cls.second_response,
                                                             cls.third_response]})

        cls.mock_random: Mock = Mock(**{'randint.side_effect': [0x150e, 0xe13b, 0xc98f]})

    def test_zero_counter_error_counter_zero(self):
        """
        Test case for when the counter is set to zero and then fully exhausted
        """

        resolver: ResolverCore = ResolverCore(self.mock_socket, False, "1.2.3.4", self.mock_random, 0)

        self.assertRaises(DNSZeroCounterError, resolver.resolve_domain_name, "www.google.ca", "1.2.3.4", 1)

    def test_zero_counter_error_counter_one(self):
        """
        Test case for when the counter is
        """

        resolver: ResolverCore = ResolverCore(self.mock_socket, False, "1.2.3.4", self.mock_random, 1)

        self.assertRaises(DNSZeroCounterError, resolver.resolve_domain_name, "www.google.ca", "1.2.3.4", 1)

    def test_zero_counter_error_counter_two(self):
        """
        Test case for when the counter is set to two and exhausted.
        """

        resolver: ResolverCore = ResolverCore(self.mock_socket, False, "1.2.3.4", self.mock_random, 2)

        self.assertRaises(DNSZeroCounterError, resolver.resolve_domain_name, "www.google.ca", "1.2.3.4", 1)

