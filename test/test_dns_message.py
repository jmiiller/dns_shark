import unittest
from io import BytesIO
from dns_shark.dns_message import DNSMessage


class DNSMessageTests(unittest.TestCase):
    """
    Unit testing for dns_message.py
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """
        cls.dns_message_encoded: bytes = b'\x00\x01\x80\x80\x00\x01\x00\x00\x00\x04\x00\x08\x03www\x02cs\x03ubc' \
                                         b'\x02ca\x00\x00\x01\x00\x01\x02ca\x00\x00\x02\x00\x01\x00\x02MY\x00\x0f' \
                                         b'\x01x\nca-servers\xc0\x1f\xc0\x1f\x00\x02\x00\x01\x00\x02MY\x00\x04' \
                                         b'\x01c\xc0/\xc0\x1f\x00\x02\x00\x01\x00\x02MY\x00\x04\x01j\xc0/\xc0\x1f' \
                                         b'\x00\x02\x00\x01\x00\x02MY\x00\x06\x03any\xc0/\xc0-\x00\x01\x00\x01\x00' \
                                         b'\x02MY\x00\x04\xc7\xfd\xfaD\xc0-\x00\x1c\x00\x01\x00\x02MY\x00\x10& \x01' \
                                         b'\n\x80\xba\x00\x00\x00\x00\x00\x00\x00\x00\x00h\xc0H\x00\x01\x00\x01\x00' \
                                         b'\x02MY\x00\x04\xb9\x9f\xc4\x02\xc0H\x00\x1c\x00\x01\x00\x02MY\x00\x10& \x01' \
                                         b'\n\x80S\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xc0X\x00\x01\x00\x01\x00\x02MY' \
                                         b'\x00\x04\xc6\xb6\xa7\x01\xc0X\x00\x1c\x00\x01\x00\x02MY\x00\x10 \x01' \
                                         b'\x05\x00\x00\x83\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc0h\x00\x01\x00' \
                                         b'\x01\x00\x02MY\x00\x04\xc7\x04\x90\x02\xc0h\x00\x1c\x00\x01\x00\x02MY\x00' \
                                         b'\x10 \x01\x05\x00\x00\xa7\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'

    def test_decode_dns_message(self):
        """
        Test case to decode an entire dns message. This dns message contains resource records with pointers.
        """
        dns_message: DNSMessage = DNSMessage.decode_dns_message(BytesIO(self.dns_message_encoded))

        # Check that the query id is correct
        self.assertEqual(dns_message.query_id, 1)

        # Check that flags are correct
        self.assertEqual(dns_message.is_response, True)
        self.assertEqual(dns_message.opcode, 0)
        self.assertEqual(dns_message.authoritative, False)
        self.assertEqual(dns_message.is_truncated, False)
        self.assertEqual(dns_message.recursion_desired, False)
        self.assertEqual(dns_message.recursion_available, True)
        self.assertEqual(dns_message.rcode, 0)

        # Check that record/question counts are correct
        self.assertEqual(dns_message.question_count, 1)
        self.assertEqual(dns_message.answer_count, 0)
        self.assertEqual(dns_message.nameserver_count, 4)
        self.assertEqual(dns_message.additional_count, 8)

        # Check that the question was properly decoded
        self.assertEqual(dns_message.dns_questions[0].name, 'www.cs.ubc.ca')
        self.assertEqual(dns_message.dns_questions[0].type, 1)
        self.assertEqual(dns_message.dns_questions[0].response_class, 1)

        # Check that the first name server record was correctly decoded
        self.assertEqual(dns_message.name_server_records[0].name, 'ca')
        self.assertEqual(dns_message.name_server_records[0].type, 2)
        self.assertEqual(dns_message.name_server_records[0].response_class, 1)
        self.assertEqual(dns_message.name_server_records[0].ttl, 150873)
        self.assertEqual(dns_message.name_server_records[0].rdlength, 15)
        self.assertEqual(dns_message.name_server_records[0].rdata, 'x.ca-servers.ca')

        # Check that the first additional record was correctly decoded
        self.assertEqual(dns_message.additional_records[0].name, 'x.ca-servers.ca')
        self.assertEqual(dns_message.additional_records[0].type, 1)
        self.assertEqual(dns_message.additional_records[0].response_class, 1)
        self.assertEqual(dns_message.additional_records[0].ttl, 150873)
        self.assertEqual(dns_message.additional_records[0].rdlength, 4)
        self.assertEqual(dns_message.additional_records[0].rdata, '199.253.250.68')

    def test_get_response_value_from_flags_true(self):
        """
        Test case to retrieve the get_response field when set to True in the flags.
        """
        # flags = 32768 has get_response flag set
        get_response_value_true: bool = DNSMessage._get_response_value_from_flags(32768)

        self.assertEqual(get_response_value_true, True)

    def test_get_response_value_from_flags_false(self):
        """
        Test case to retrieve the get_response field when set to False in the flags.
        """

        # flags = 0 has get_response not set
        get_response_value_false: bool = DNSMessage._get_response_value_from_flags(0)

        self.assertEqual(get_response_value_false, False)

    def test_get_opcode_value_from_flags_large(self):
        """
        Test case to retrieve the opcode field when set to a large value in the flags.
        """
        # flags = 30720 has opcode = 15
        get_opcode_value_large: int = DNSMessage._get_opcode_value_from_flags(30720)

        self.assertEqual(get_opcode_value_large, 15)

    def test_get_opcode_value_from_flags_zero(self):
        """
        Test case to retrieve the opcode field when set to zero in the flags.
        """
        # flags = 0 has opcode = 0
        get_opcode_value_small: int = DNSMessage._get_opcode_value_from_flags(0)

        self.assertEqual(get_opcode_value_small, 0)

    def test_get_authoritative_value_from_flags_true(self):
        """
        Test case to retrieve the authoritative field when set to True in the flags.
        """
        # flags = 1024 has authoritative = True
        get_authoritative_value_true: bool = DNSMessage._get_authoritative_value_from_flags(1024)

        self.assertEqual(get_authoritative_value_true, True)

    def test_get_authoritative_value_from_flags_false(self):
        """
        Test case to retrieve the authoritative field when set to False in the flags.
        """
        # flags = 0 has authoritative = False
        get_authoritative_value_false: bool = DNSMessage._get_authoritative_value_from_flags(0)

        self.assertEqual(get_authoritative_value_false, False)

    def test_get_is_truncated_value_from_flags_true(self):
        """
        Test case to retrieve the is_truncated field when set to True in the flags.
        """
        # flags = 512 has is_truncated = True
        get_is_truncated_value_true: bool = DNSMessage._get_is_truncated_value_from_flags(512)

        self.assertEqual(get_is_truncated_value_true, True)

    def test_get_is_truncated_value_from_flags_false(self):
        """
        Test case to retrieve the is_truncated field when set to False in the flags.
        """
        # flags = 0 has is_truncated = False
        get_is_truncated_value_false: bool = DNSMessage._get_is_truncated_value_from_flags(0)

        self.assertEqual(get_is_truncated_value_false, False)

    def test_get_recursion_desired_value_from_flags_true(self):
        """
        Test case to retrieve the recursion_desired field when set to True in the flags.
        """
        # flags = 256 has recursion_desired = True
        get_recursion_desired_value_true: bool = DNSMessage._get_recursion_desired_value_from_flags(256)

        self.assertEqual(get_recursion_desired_value_true, True)

    def test_get_recursion_desired_value_from_flags_false(self):
        """
        Test case to retrieve the recursion_desired field when set to False in the flags.
        """
        # flags = 0 has recursion_desired = False
        get_recursion_desired_value_false: bool = DNSMessage._get_recursion_desired_value_from_flags(0)

        self.assertEqual(get_recursion_desired_value_false, False)

    def test_get_recursion_available_value_from_flags_true(self):
        """
        Test case to retrieve the recursion_available field when set to True in the flags.
        """
        # flags = 128 has recursion_available = True
        get_recursion_available_value_true: bool = DNSMessage._get_recursion_available_value_from_flags(128)

        self.assertEqual(get_recursion_available_value_true, True)

    def test_get_recursion_available_value_from_flags_false(self):
        """
        Test case to retrieve the recursion_available field when set to false in the flags.
        """
        # flags = 0 has recursion_available = False
        get_recursion_available_value_false: bool = DNSMessage._get_recursion_available_value_from_flags(0)

        self.assertEqual(get_recursion_available_value_false, False)

    def test_get_rcode_value_from_flags_large(self):
        """
        Test case to retrieve the rcode field when set to fifteen in the flags.
        """
        # flags = 15 has rcode = 15
        get_rcode_value_large: int = DNSMessage._get_rcode_value_from_flags(15)

        self.assertEqual(get_rcode_value_large, 15)

    def test_get_rcode_value_from_flags_zero(self):
        """
        Test case to retrieve the rcode field when set to zero in the flags.
        """
        # flags = 0 has rcode = 0
        get_rcode_value_small: int = DNSMessage._get_rcode_value_from_flags(0)

        self.assertEqual(get_rcode_value_small, 0)

    def test_attempt_to_retrieve_all_flags(self):
        """
        Test case to retrieve all the flag values from a hypothetical flags value for a dns message.
        """

        get_response_value: bool = DNSMessage._get_response_value_from_flags(46218)
        get_opcode_value: int = DNSMessage._get_opcode_value_from_flags(46218)
        get_authoritative_value: bool = DNSMessage._get_authoritative_value_from_flags(46218)
        get_is_truncated_value: bool = DNSMessage._get_is_truncated_value_from_flags(46218)
        get_recursion_desired_value: bool = DNSMessage._get_recursion_desired_value_from_flags(46218)
        get_recursion_available_value: bool = DNSMessage._get_recursion_available_value_from_flags(46218)
        get_rcode_value: int = DNSMessage._get_rcode_value_from_flags(46218)

        self.assertEqual(get_response_value, True)
        self.assertEqual(get_opcode_value, 6)
        self.assertEqual(get_authoritative_value, True)
        self.assertEqual(get_is_truncated_value, False)
        self.assertEqual(get_recursion_desired_value, False)
        self.assertEqual(get_recursion_available_value, True)
        self.assertEqual(get_rcode_value, 10)
