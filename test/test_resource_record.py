import unittest
from dns_shark.resource_record import ResourceRecord
from io import BytesIO


class DNSMessageTests(unittest.TestCase):
    """
    Unit testing for ResourceRecord.py
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """
        cls.a_type: int = 1
        cls.ns_type: int = 2
        cls.cn_type: int = 5
        cls.aaaa_type: int = 28
        cls.unsupported_type: int = 3

        cls.ipv4_address_data: bytes = b'\x10\x08\x20\x02'
        cls.ipv6_address_data: bytes = b'\x10\x08\x20\x02\x10\x08\x20\x02\x10\x08\x20\x02\x10\x08\x20\x02'

        cls.type_a_resource_record: ResourceRecord = ResourceRecord()

    def test_parse_type_a_type(self):
        """
        Test case to parse a type of value 1 (A type).
        """

        a_type: str = ResourceRecord.parse_type(self.a_type)
        self.assertEqual(a_type, 'A')

    def test_parse_type_ns_type(self):
        """
        Test case to parse a type of value 2 (NS type).
        """

        a_type: str = ResourceRecord.parse_type(self.ns_type)
        self.assertEqual(a_type, 'NS')

    def test_parse_type_cn_type(self):
        """
        Test case to parse a type of value 5 (CN type).
        """

        a_type: str = ResourceRecord.parse_type(self.cn_type)
        self.assertEqual(a_type, 'CN')

    def test_parse_type_aaaa_type(self):
        """
        Test case to parse a type of value 28 (AAAA type).
        """

        a_type: str = ResourceRecord.parse_type(self.aaaa_type)
        self.assertEqual(a_type, 'AAAA')

    def test_parse_type_unsupported_type(self):
        """
        Test case to parse a type of value 3, which is unsupported by dns_shark.
        """

        a_type: str = ResourceRecord.parse_type(self.unsupported_type)
        self.assertEqual(a_type, '3')

    def test_decode_ipv4_address(self):
        """
        Test case to decode an ipv4 address to its string representation.
        """
        ipv4_address: str = ResourceRecord._decode_ipv4_address(BytesIO(self.ipv4_address_data))
        self.assertEqual(ipv4_address, '16.8.32.2')

    def test_decode_ipv6_address(self):
        """
        Test case to decode an ipv6 address to its string representation
        """
        ipv6_address: str = ResourceRecord._decode_ipv6_address(BytesIO(self.ipv6_address_data))
        self.assertEqual(ipv6_address, '1008:2002:1008:2002:1008:2002:1008:2002')

