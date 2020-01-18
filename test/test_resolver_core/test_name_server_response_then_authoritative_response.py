from unittest.mock import Mock
import unittest
from dns_shark.resolver_core import ResolverCore
from dns_shark.resource_record import ResourceRecord
from typing import List


class NameServerResponseThenAuthoritativeResponseTest(unittest.TestCase):
    """
    Unit testing for resolver_core.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """

        cls.first_response: bytes = bytes.fromhex('0581800000010000000d000e0377777706676f6f676c6503636f6d0000010001c'
                                                  '017000200010002a300001401610c67746c642d73657276657273036e657400c0'
                                                  '17000200010002a30000040162c02ec017000200010002a30000040163c02ec01'
                                                  '7000200010002a30000040164c02ec017000200010002a30000040165c02ec017'
                                                  '000200010002a30000040166c02ec017000200010002a30000040167c02ec0170'
                                                  '00200010002a30000040168c02ec017000200010002a30000040169c02ec01700'
                                                  '0200010002a3000004016ac02ec017000200010002a3000004016bc02ec017000'
                                                  '200010002a3000004016cc02ec017000200010002a3000004016dc02ec02c0001'
                                                  '00010002a3000004c005061ec04c000100010002a3000004c0210e1ec05c00010'
                                                  '0010002a3000004c01a5c1ec06c000100010002a3000004c01f501ec07c000100'
                                                  '010002a3000004c00c5e1ec08c000100010002a3000004c023331ec09c0001000'
                                                  '10002a3000004c02a5d1ec0ac000100010002a3000004c036701ec0bc00010001'
                                                  '0002a3000004c02bac1ec0cc000100010002a3000004c0304f1ec0dc000100010'
                                                  '002a3000004c034b21ec0ec000100010002a3000004c029a21ec0fc0001000100'
                                                  '02a3000004c037531ec02c001c00010002a300001020010503a83e00000000000'
                                                  '000020030')

        cls.second_response: bytes = bytes.fromhex('64eb800000010000000400080377777706676f6f676c6503636f6d0000010001'
                                                   'c010000200010002a3000006036e7332c010c010000200010002a3000006036e'
                                                   '7331c010c010000200010002a3000006036e7333c010c010000200010002a300'
                                                   '0006036e7334c010c02c001c00010002a3000010200148604802003400000000'
                                                   '0000000ac02c000100010002a3000004d8ef220ac03e001c00010002a3000010'
                                                   '2001486048020032000000000000000ac03e000100010002a3000004d8ef200a'
                                                   'c050001c00010002a30000102001486048020036000000000000000ac0500001'
                                                   '00010002a3000004d8ef240ac062001c00010002a30000102001486048020038'
                                                   '000000000000000ac062000100010002a3000004d8ef260a')


        cls.authoritative_response: bytes = bytes.fromhex('0a7b840000010001000000000377777706676f6f676c6503636f6d000'
                                                          '0010001c00c000100010000012c0004acd90ec4')

        cls.mock_socket: Mock = Mock(**{'recv.side_effect': [cls.first_response,
                                                             cls.second_response,
                                                             cls.authoritative_response]})

        cls.mock_random: Mock = Mock(**{'randint.side_effect': [0x0581, 0x64eb, 0x0a7b]})

    def test_name_server_response_then_authoritative(self):
        """
        Test case for when the first two responses non-authoritative responses and the final one is authoritative and
        contains a matching resource record.

        The first two responses both contain the ip address a name server, so we do
        not need to do a separate lookup for the ip address of the name server.
        """

        resolver: ResolverCore = ResolverCore(self.mock_socket, False, "1.2.3.4", self.mock_random)

        answers: List[ResourceRecord] = resolver.resolve_domain_name("www.google.com", "1.2.3.4", 1)
        expected_answer: List[ResourceRecord] = [ResourceRecord('www.google.com', 1, 1, 300, 4, '172.217.14.196')]

        self.assertEqual(answers, expected_answer)

