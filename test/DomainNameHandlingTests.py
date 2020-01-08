import unittest
from dns_shark.DomainNameHandling import DomainNameEncoder, DomainNameDecoder  
from io import BytesIO


class DomainNameHandlingTests(unittest.TestCase):
    """
    Unit testing for DomainNameHandling.py (i.e. domain name encoding/decoding logic)
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """
        cls.simple_domain_name: str = "www.cs.ubc.ca"
        cls.simple_domain_name_encoded: bytes = b'\x03\x77\x77\x77\x02\x63\x73\x03\x75\x62\x63\x02\x63\x61\x00'

        cls.simple_label: str = "ubc"
        cls.simple_label_encoded: bytes = b'\x03\x75\x62\x63'

        cls.domain_name_with_pointers: str = "www.cbu.cs.ubc.ca"
        # This encoding has two domain names in it. At the start is www.cs.ubc.ca. After is www.cbu.cs.ubc.ca,
        # which contains a pointer to the first one.
        cls.domain_name_with_pointers_encoded = b'\x03www\x02cs\x03ubc\x02ca\x00\x03\x77\x77\x77\x03\x63\x62\x75\xc0\x04'

    def test_encode_simple_domain_name(self):
        """
        Test case for encoding the simple domain name.
        """
        encoded_domain: bytes = DomainNameEncoder.encode_domain_name(self.simple_domain_name)

        self.assertEqual(encoded_domain, self.simple_domain_name_encoded)

    def test_encode_simple_label(self):
        """
        Test case for encoding a simple label in a domain name.
        """
        writer: BytesIO = BytesIO()

        DomainNameEncoder._encode_label(self.simple_label, writer)

        self.assertEqual(writer.getvalue(), self.simple_label_encoded)

    def test_decode_simple_domain_name(self):
        """
        Test case for decoding a simple domain name.
        """

        result: str = DomainNameDecoder.decode_domain_name(BytesIO(self.simple_domain_name_encoded), BytesIO(self.simple_domain_name_encoded))

        self.assertEqual(result, self.simple_domain_name)

    def test_simple_domain_name_round_trip(self):
        """
        Test case for performing a round trip decoding/encoding.
        """

        # Encode then decode
        encoding = DomainNameEncoder.encode_domain_name(self.simple_domain_name)
        decode_after_encoding= DomainNameDecoder.decode_domain_name(BytesIO(encoding), BytesIO(encoding))

        self.assertEqual(decode_after_encoding, self.simple_domain_name)

        # Decode then encode
        decoding = DomainNameDecoder.decode_domain_name(BytesIO(self.simple_domain_name_encoded), BytesIO(self.simple_domain_name_encoded))
        encode_after_decoding = DomainNameEncoder.encode_domain_name(decoding)

        self.assertEqual(encode_after_decoding, self.simple_domain_name_encoded)

    def test_decode_domain_name_with_pointer(self):
        """
        Test case for decoding a simple domain name.
        """
        reader: BytesIO = BytesIO(self.domain_name_with_pointers_encoded)
        reader.seek(15)  # navigate to the start of the second domain name, which is the one we want to decode
        copy_of_data: BytesIO = BytesIO(self.domain_name_with_pointers_encoded)

        result: str = DomainNameDecoder.decode_domain_name(reader, copy_of_data)

        self.assertEqual(result, self.domain_name_with_pointers)
