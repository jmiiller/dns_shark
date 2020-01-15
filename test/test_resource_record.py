import unittest
from dns_shark.resource_record import ResourceRecord
from io import BytesIO
from test.utilities import Utilities


class DNSMessageTests(unittest.TestCase):
    """
    Unit testing for resource_record.py
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

        cls.ipv4_address_data: bytes = Utilities().ipv4_address_data
        cls.ipv6_address_data: bytes = Utilities().ipv6_address_data

        cls.resource_record_encoded: bytes = Utilities().resource_record_encoded

        cls.simple_domain_name: bytes = Utilities().simple_domain_name
        cls.simple_domain_name_encoded: bytes = Utilities().simple_domain_name_encoded

    def test_decode_resource_record(self):
        """
        Test case to decode a resource record.
        """
        resource_record: ResourceRecord = ResourceRecord.decode_resource_record(BytesIO(self.resource_record_encoded),
                                                                                BytesIO(self.resource_record_encoded))

        self.assertEqual(resource_record.name, 'ca')
        self.assertEqual(resource_record.type, self.ns_type)
        self.assertEqual(resource_record.response_class, 1)
        self.assertEqual(resource_record.ttl, 150873)
        self.assertEqual(resource_record.rdlength, 14)
        self.assertEqual(resource_record.rdata, 'x.ca-servers')

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

    def test_decode_rdata_a_type(self):
        """
        Test case to decode rdata of type a (ipv4).
        """
        rdata: BytesIO = BytesIO(self.ipv4_address_data)
        copy: BytesIO = BytesIO(self.ipv4_address_data)
        ipv4_address: str = ResourceRecord._decode_rdata(rdata, copy, self.a_type)
        self.assertEqual(ipv4_address, '16.8.32.2')

    def test_decode_rdata_ns_type(self):
        """
        Test case to decode rdata of type ns (name server).
        """
        rdata: BytesIO = BytesIO(self.simple_domain_name_encoded)
        copy: BytesIO = BytesIO(self.simple_domain_name_encoded)
        decoded_domain_name: str = ResourceRecord._decode_rdata(rdata, copy, self.ns_type)
        self.assertEqual(decoded_domain_name, self.simple_domain_name)

    def test_decode_rdata_cn_type(self):
        """
        Test case to decode rdata of type cn (name server).
        """
        rdata: BytesIO = BytesIO(self.simple_domain_name_encoded)
        copy: BytesIO = BytesIO(self.simple_domain_name_encoded)
        decoded_domain_name: str = ResourceRecord._decode_rdata(rdata, copy, self.cn_type)
        self.assertEqual(decoded_domain_name, self.simple_domain_name)

    def test_decode_rdata_aaaa_type(self):
        """
        Test case to decode rdata of type aaaa (ipv6).
        """
        rdata: BytesIO = BytesIO(self.ipv6_address_data)
        copy: BytesIO = BytesIO(self.ipv6_address_data)
        ipv6_address: str = ResourceRecord._decode_rdata(rdata, copy, self.aaaa_type)
        self.assertEqual(ipv6_address, '1008:2002:1008:2002:1008:2002:1008:2002')

    def test_decode_rdata_unsupported_type(self):
        """
        Test case to decode rdata of an unsupported type.
        """
        rdata: BytesIO = BytesIO(self.ipv6_address_data)
        copy: BytesIO = BytesIO(self.ipv6_address_data)
        ipv6_address: str = ResourceRecord._decode_rdata(rdata, copy, self.unsupported_type)
        self.assertEqual(ipv6_address, 'UNSUPPORTED RESOURCE RECORD TYPE')

