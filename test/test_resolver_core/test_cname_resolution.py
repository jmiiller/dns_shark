from unittest.mock import Mock
import unittest
from dns_shark.resolver_core import ResolverCore
from dns_shark.resource_record import ResourceRecord
from typing import List


class CNameResolutionTest(unittest.TestCase):
    """
    Unit testing for resolver_core.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """

        cls.first_response: bytes = bytes.fromhex('dc00800000010000000600070470726570026169036d6974036564750000010001c018000200010002a300001301610b6564752d73657276657273036e657400c018000200010002a30000040163c02fc018000200010002a30000040164c02fc018000200010002a30000040166c02fc018000200010002a30000040167c02fc018000200010002a3000004016cc02fc02d000100010002a3000004c005061ec04c000100010002a3000004c01a5c1ec05c000100010002a3000004c01f501ec06c000100010002a3000004c023331ec07c000100010002a3000004c02a5d1ec08c000100010002a3000004c029a21ec07c001c00010002a300001020010503cc2c00000000000000020036')

        cls.second_response: bytes = bytes.fromhex('990a8000000100000008000b0470726570026169036d6974036564750000010001c014000200010002a300000f047573773204616b616d036e657400c014000200010002a3000008056173696131c032c014000200010002a3000008056173696132c032c014000200010002a30000070475736532c032c014000200010002a3000009066e73312d3337c032c014000200010002a300000a076e73312d313733c032c014000200010002a30000070465757235c032c014000200010002a30000070475736535c032c02d000100010002a3000004b81aa140c048000100010002a30000045f64af40c05c000100010002a30000045f652440c070000100010002a300000460073140c083000100010002a3000004c16c5b25c083001c00010002a300001026001401000200000000000000000025c098000100010002a3000004c16c5badc098001c00010002a3000010260014010002000000000000000000adc0ae000100010002a3000004174a1940c0c1000100010002a300000402102840c0c1001c00010002a300001026001401000100000000000000000040')

        cls.third_response: bytes = bytes.fromhex('b96a800000010000000400040470726570026169036d6974036564750000010001c0110002000100000708001108617574682d6e733005637361696cc014c0110002000100000708000b08617574682d6e7333c036c0110002000100000708000b08617574682d6e7332c036c0110002000100000708000b08617574682d6e7331c036c02d00010001000007080004801e027bc0780001000100000708000412180078c0610001000100000708000480342050c04a0001000100000708000480342050')

        cls.fourth_response: bytes = bytes.fromhex('1b4a840000010001000000000470726570026169036d6974036564750000010001c00c0005000100000708000d0366747003676e75036f726700')

        cls.fifth_response: bytes = bytes.fromhex('75738000000100000006000c0366747003676e75036f72670000010001c014000200010002a3000019026130036f72670b6166696c6961732d6e737404696e666f00c014000200010002a3000005026132c02cc014000200010002a3000015026230036f72670b6166696c6961732d6e7374c014c014000200010002a3000005026232c062c014000200010002a3000005026330c02cc014000200010002a3000005026430c062c029000100010002a3000004c7133801c04e000100010002a3000004c7f97001c05f000100010002a3000004c7133601c080000100010002a3000004c7f97801c091000100010002a3000004c7133501c0a2000100010002a3000004c7133901c029001c00010002a300001020010500000e00000000000000000001c04e001c00010002a300001020010500004000000000000000000001c05f001c00010002a300001020010500000c00000000000000000001c080001c00010002a300001020010500004800000000000000000001c091001c00010002a300001020010500000b00000000000000000001c0a2001c00010002a300001020010500000f00000000000000000001')

        cls.sixth_response: bytes = bytes.fromhex('3a73800000010000000300050366747003676e75036f72670000010001c01000020001000151800006036e7331c010c01000020001000151800006036e7332c010c01000020001000151800006036e7333c010c02900010001000151800004d076eba4c029001c00010001518000102001483001340003000000000000000fc03b000100010001518000045762fd66c04d000100010001518000042e2b2546c04d001c0001000151800010200141c8002002d3000000000000000a')

        cls.authoritative_response: bytes = bytes.fromhex('a21c840000010001000400060366747003676e75036f72670000010001c00c000100010000012c0004d076eb14c010000200010000012c0006036e7331c010c010000200010000012c0006036e7332c010c010000200010000012c0006036e7333c010c010000200010000012c0006036e7334c010c039000100010000012c0004d076eba4c039001c00010000012c00102001483001340003000000000000000fc04b000100010000012c00045762fd66c05d000100010000012c00042e2b2546c05d001c00010000012c0010200141c8002002d3000000000000000ac06f000100010000012c0004d0461f7d')

        cls.mock_socket: Mock = Mock(**{'recv.side_effect': [cls.first_response,
                                                             cls.second_response,
                                                             cls.third_response,
                                                             cls.fourth_response,
                                                             cls.fifth_response,
                                                             cls.sixth_response,
                                                             cls.authoritative_response]})

        cls.mock_random: Mock = Mock(**{'randint.side_effect': [0xdc00, 0x990a, 0xb96a, 0x1b4a, 0x7573, 0x3a73, 0xa21c]})

    def test_cname_resolution(self):
        """
        Test case for when name resolution requires performing a cname resolution.
        """

        resolver: ResolverCore = ResolverCore(self.mock_socket, False, "1.2.3.4", self.mock_random)

        answers: List[ResourceRecord] = resolver.resolve_domain_name("prep.ai.mit.edu", "1.2.3.4", 1)
        expected_answer: List[ResourceRecord] = [ResourceRecord('ftp.gnu.org', 1, 1, 300, 4, '208.118.235.20')]

        self.assertEqual(answers, expected_answer)
