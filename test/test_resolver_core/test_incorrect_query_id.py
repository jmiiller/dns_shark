from unittest.mock import Mock
import unittest
from dns_shark.resolver_core import ResolverCore
from dns_shark.resource_record import ResourceRecord
from typing import List


class IncorrectQueryIdTest(unittest.TestCase):
    """
    Unit testing for resolver_core.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """

        cls.incorrect_response: bytes = bytes.fromhex('e13b800000010000000400080377777706676f6f676c6503636f6d00001c000'
                                                   '1c010000200010002a3000006036e7332c010c010000200010002a300000603'
                                                   '6e7331c010c010000200010002a3000006036e7333c010c010000200010002a'
                                                   '3000006036e7334c010c02c001c00010002a300001020014860480200340000'
                                                   '00000000000ac02c000100010002a3000004d8ef220ac03e001c00010002a30'
                                                   '000102001486048020032000000000000000ac03e000100010002a3000004d8'
                                                   'ef200ac050001c00010002a30000102001486048020036000000000000000ac'
                                                   '050000100010002a3000004d8ef240ac062001c00010002a300001020014860'
                                                   '48020038000000000000000ac062000100010002a3000004d8ef260a')

        cls.authoritative_response: bytes = bytes.fromhex('19b6840000010001000300030377777702637303756263026361000001'
                                                          '0001c00c0001000100000e1000048e670605c0100002000100000e1000'
                                                          '06036e7331c010c0100002000100000e10000a0774656d70313230c010'
                                                          'c0100002000100000e1000150366733105756772616402637303756263'
                                                          '02636100c0630001000100000e100004c6a22301c03b0001000100000e'
                                                          '1000048e670606c04d0001000100000e10000489523d78')

        cls.mock_socket: Mock = Mock(**{'recv.side_effect': [cls.incorrect_response, cls.authoritative_response]})

        cls.mock_random: Mock = Mock(**{'randint.side_effect': [0x19b6]})

    def test_incorrect_query_id(self):
        """
        Test case for when a response is received that does not match the query id of the previously sent message. Thus,
        the resolver discards the packet and waits for another packet with the correct query id.
        """

        resolver: ResolverCore = ResolverCore(self.mock_socket, False, "1.2.3.4", self.mock_random)

        answers: List[ResourceRecord] = resolver.resolve_domain_name("www.cs.ubc.ca", "1.2.3.4", 1)
        expected_answer: List[ResourceRecord] = [ResourceRecord('www.cs.ubc.ca', 1, 1, 3600, 4, '142.103.6.5')]

        self.assertEqual(answers, expected_answer)

