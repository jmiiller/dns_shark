from unittest.mock import Mock
import unittest
from dns_shark.resolver_core import ResolverCore
from dns_shark.errors.dns_not_implemented_error import DNSNotImplementedError


class DNSNotImplementedErrorTest(unittest.TestCase):
    """
    Unit testing for resolver_core.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """
        cls.response_with_not_implemented_error: bytes = bytes.fromhex('19b6840400010001000300030377777702637303756263026361000001'
                                                          '0001c00c0001000100000e1000048e670605c0100002000100000e1000'
                                                          '06036e7331c010c0100002000100000e10000a0774656d70313230c010'
                                                          'c0100002000100000e1000150366733105756772616402637303756263'
                                                          '02636100c0630001000100000e100004c6a22301c03b0001000100000e'
                                                          '1000048e670606c04d0001000100000e10000489523d78')

        cls.mock_socket: Mock = Mock(**{'recv.return_value': cls.response_with_not_implemented_error})

        cls.mock_random: Mock = Mock(**{'randint.return_value': 6582})

    def test_not_implemented_error(self):
        """
        Test case for when the first response given by the queried dns name server gives a not implemented error.
        """

        resolver: ResolverCore = ResolverCore(self.mock_socket, False, "1.2.3.4", self.mock_random)

        self.assertRaises(DNSNotImplementedError, resolver.resolve_domain_name, "www.cs.ubc.ca", "1.2.3.4", 1)

