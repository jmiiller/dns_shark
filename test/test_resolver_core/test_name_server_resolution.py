from unittest.mock import Mock
import unittest
from dns_shark.resolver_core import ResolverCore
from dns_shark.resource_record import ResourceRecord
from typing import List


class NameServerResolutionTest(unittest.TestCase):
    """
    Unit testing for resolver_core.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """

        cls.first_response: bytes = bytes.fromhex('b21e8000000100000006000703777777087374616e666f7264036564750000010001c019000200010002a300001301610b6564752d73657276657273036e657400c019000200010002a30000040163c030c019000200010002a30000040164c030c019000200010002a30000040166c030c019000200010002a30000040167c030c019000200010002a3000004016cc030c02e000100010002a3000004c005061ec04d000100010002a3000004c01a5c1ec05d000100010002a3000004c01f501ec06d000100010002a3000004c023331ec07d000100010002a3000004c02a5d1ec08d000100010002a3000004c029a21ec07d001c00010002a300001020010503cc2c00000000000000020036')

        cls.second_response: bytes = bytes.fromhex('094b8000000100000003000603777777087374616e666f7264036564750000010001c010000200010002a300000b086176616c6c6f6e65c010c010000200010002a300000b086174616c616e7465c010c010000200010002a3000008056172677573c010c02e000100010002a3000004ab400758c02e001c00010002a30000102607f6d00000911600000000ab400758c045000100010002a3000004ab40073dc045001c00010002a30000102607f6d000000d3200000000ab40073dc05c000100010002a3000004ab400773c05c001c00010002a30000102607f6d00000911300000000ab400773')

        cls.third_response: bytes = bytes.fromhex('56058000000100000004000003777777087374616e666f7264036564750000010001c00c000200010002a3000017076e732d3132333409617773646e732d3236036f726700c00c000200010002a3000016066e732d33303909617773646e732d333803636f6d00c00c000200010002a3000019076e732d3230323709617773646e732d363102636f02756b00c00c000200010002a3000016066e732d35313409617773646e732d3030036e657400')

        cls.fourth_response: bytes = bytes.fromhex('a40a8000000100000006000c076e732d3132333409617773646e732d3236036f72670000010001c01e000200010002a3000019026130036f72670b6166696c6961732d6e737404696e666f00c01e000200010002a3000005026132c036c01e000200010002a3000015026230036f72670b6166696c6961732d6e7374c01ec01e000200010002a3000005026232c06cc01e000200010002a3000005026330c036c01e000200010002a3000005026430c06cc033000100010002a3000004c7133801c058000100010002a3000004c7f97001c069000100010002a3000004c7133601c08a000100010002a3000004c7f97801c09b000100010002a3000004c7133501c0ac000100010002a3000004c7133901c033001c00010002a300001020010500000e00000000000000000001c058001c00010002a300001020010500004000000000000000000001c069001c00010002a300001020010500000c00000000000000000001c08a001c00010002a300001020010500004800000000000000000001c09b001c00010002a300001020010500000b00000000000000000001c0ac001c00010002a300001020010500000f00000000000000000001')

        cls.fifth_response: bytes = bytes.fromhex('c7e280000001000000040004076e732d3132333409617773646e732d3236036f72670000010001c0140002000100015180000b08672d6e732d313534c014c0140002000100015180000b08672d6e732d373332c014c0140002000100015180000c09672d6e732d31303533c014c0140002000100015180000c09672d6e732d31363236c014c03300010001000151800004cdfbc09ac04a00010001000151800004cdfbc2dcc06100010001000151800004cdfbc41dc07900010001000151800004cdfbc65a')

        cls.sixth_response: bytes = bytes.fromhex('f68384000001000100040004076e732d3132333409617773646e732d3236036f72670000010001c00c000100010002a3000004cdfbc4d2c014000200010002a300000c09672d6e732d31303533c014c014000200010002a300000b08672d6e732d313534c014c014000200010002a300000c09672d6e732d31363236c014c014000200010002a300000b08672d6e732d373332c014c043000100010002a3000004cdfbc41dc05b000100010002a3000004cdfbc09ac072000100010002a3000004cdfbc65ac08a000100010002a3000004cdfbc2dc')

        cls.authoritative_response: bytes = bytes.fromhex('54848400000100030004000003777777087374616e666f7264036564750000010001c00c000100010000003c000436da5be4c00c000100010000003c0004341baf8bc00c000100010000003c0004340af7d9c00c000200010002a3000017076e732d3132333409617773646e732d3236036f726700c00c000200010002a3000019076e732d3230323709617773646e732d363102636f02756b00c00c000200010002a3000016066e732d33303909617773646e732d333803636f6d00c00c000200010002a3000016066e732d35313409617773646e732d3030036e657400')

        cls.mock_socket: Mock = Mock(**{'recv.side_effect': [cls.first_response,
                                                             cls.second_response,
                                                             cls.third_response,
                                                             cls.fourth_response,
                                                             cls.fifth_response,
                                                             cls.sixth_response,
                                                             cls.authoritative_response]})

        cls.mock_random: Mock = Mock(**{'randint.side_effect': [0xb21e, 0x094b, 0x5605, 0xa40a, 0xc7e2, 0xf683, 0x5484]})

    def test_name_resolution(self):
        """
        Test case for when name resolution requires performing a name resolution.

        This is also a case where the name resolution returns multiple answers.
        """

        resolver: ResolverCore = ResolverCore(self.mock_socket, False, "1.2.3.4", self.mock_random)

        answers: List[ResourceRecord] = resolver.resolve_domain_name("www.stanford.edu", "1.2.3.4", 1)
        expected_answer: List[ResourceRecord] = [ResourceRecord('www.stanford.edu', 1, 1, 60, 4, '54.218.91.228'),
                                                 ResourceRecord('www.stanford.edu', 1, 1, 60, 4, '52.27.175.139'),
                                                 ResourceRecord('www.stanford.edu', 1, 1, 60, 4, '52.10.247.217')]

        self.assertEqual(answers, expected_answer)
