"""
Unit testing for DomainNameHandling.py (i.e. domain name encoding/decoding logic)
"""


import unittest
from src.DomainNameHandling import encode_domain_name, encode_label


class DomainNameHandlingTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """
        cls.simple_domain_name: str = "www.cs.ubc.ca"
        cls.simple_domain_name_encoded: bytearray = b'\x03\x77\x77\x77\x02\x63\x73\x03\x75\x62\x63\x02\x63\x61\x00'

        cls.simple_label: str = "ubc"
        cls.simple_label_encoded: bytearray = b'\x03\x75\x62\x63'

    def setUp(self):
        """
        Initialize an empty bytearray accumulator to be modified in each test case.
        """
        self.acc: bytearray = bytearray()

    def test_encode_simple_domain_name(self):
        """
        Test case for encoding the simple domain name.
        """
        encode_domain_name(self.acc, self.simple_domain_name)

        self.assertEqual(self.acc, self.simple_domain_name_encoded)

    def test_encode_simple_label(self):
        """
        Test case for encoding a simple label in a domain name.
        """
        encode_label(self.acc, self.simple_label)

        self.assertEqual(self.acc, self.simple_label_encoded)