import unittest
from dns_shark.domain_name_handling import DomainNameEncoder, DomainNameDecoder
from io import BytesIO
from test.utilities import Utilities


class DomainNameHandlingTests(unittest.TestCase):
    """
    Unit testing for domain_name_handling.py (i.e. domain name encoding/decoding logic)
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """
        cls.simple_domain_name: str = Utilities().simple_domain_name
        cls.simple_domain_name_encoded: bytes = Utilities().simple_domain_name_encoded

        cls.simple_label: str = Utilities().simple_label
        cls.simple_label_encoded: bytes = Utilities().simple_label_encoded

        cls.domain_name_with_pointers: str = Utilities().domain_name_with_pointers
        # This encoding has two domain names in it. At the start is www.cs.ubc.ca. After is www.cbu.cs.ubc.ca,
        # which contains a pointer to the first one.
        cls.domain_name_with_pointers_encoded: bytes = Utilities().domain_name_with_pointers_encoded

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
        copy_of_message: BytesIO = BytesIO(self.domain_name_with_pointers_encoded)

        result: str = DomainNameDecoder.decode_domain_name(reader, copy_of_message)

        self.assertEqual(result, self.domain_name_with_pointers)
