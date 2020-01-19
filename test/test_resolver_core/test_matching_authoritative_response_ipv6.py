from unittest.mock import Mock
import unittest
from dns_shark.resolver_core import ResolverCore
from dns_shark.resource_record import ResourceRecord
from typing import List


class MatchingAuthoritativeResponseTest(unittest.TestCase):
    """
    Unit testing for resolver_core.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """

        cls.authoritative_response: bytes = bytes.fromhex('5c00840000010001000000000377777706676f6f676c6503636f6d000'
                                                          '01c0001c00c001c00010000012c00102607f8b0400a08000000000000'
                                                          '002004')

        cls.mock_socket: Mock = Mock(**{'recv.return_value': cls.authoritative_response})

        cls.mock_random: Mock = Mock(**{'randint.return_value': 0x5c00})

    def test_matching_authoritative_response_ipv6(self):
        """
        Test case for when the first response given by the queried dns name server is an authoritative response with
        an ipv6 resource record type, which is what was asked for.
        """

        resolver: ResolverCore = ResolverCore(self.mock_socket, False, "1.2.3.4", self.mock_random)

        answers: List[ResourceRecord] = resolver.resolve_domain_name("www.google.com", "1.2.3.4", 28)
        expected_answer: List[ResourceRecord] = [ResourceRecord('www.google.com', 28, 1, 300, 16, '2607:f8b0:400a:800::2004')]

        self.assertEqual(answers, expected_answer)

