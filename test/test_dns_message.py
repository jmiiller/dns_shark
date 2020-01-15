import unittest
from io import BytesIO
from dns_shark.dns_message import DNSMessage
from test.utilities import Utilities
from dns_shark.dns_question import DNSQuestion
from typing import List
from dns_shark.resource_record import ResourceRecord


class DNSMessageTests(unittest.TestCase):
    """
    Unit testing for dns_message.py
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """
        cls.dns_message_encoded: bytes = Utilities().dns_message_encoded

        cls.three_consecutive_dns_questions_encoded: bytes = Utilities().three_consecutive_dns_questions_encoded

        cls.three_consecutive_resource_records_encoded: bytes = Utilities().three_consecutive_resource_records_encoded

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

    def test_read_dns_questions_no_questions(self):
        """
        Test case to attempt to decode 0 questions. In other words, decode nothing and return an empty list.
        """
        dns_questions: List[DNSQuestion] = DNSMessage._read_dns_questions(BytesIO(self.three_consecutive_dns_questions_encoded),
                                                                          BytesIO(self.three_consecutive_dns_questions_encoded),
                                                                          0)

        self.assertEqual(len(dns_questions), 0)

    def test_read_dns_questions(self):
        """
        Test case to decode three consecutive dns questions.
        """
        dns_questions: List[DNSQuestion] = DNSMessage._read_dns_questions(BytesIO(self.three_consecutive_dns_questions_encoded),
                                                                          BytesIO(self.three_consecutive_dns_questions_encoded),
                                                                          3)

        # Check that the first question was properly decoded
        self.assertEqual(dns_questions[0].name, 'www.cs.ubc.ca')
        self.assertEqual(dns_questions[0].type, 1)
        self.assertEqual(dns_questions[0].response_class, 1)

        # Check that the second question was properly decoded
        self.assertEqual(dns_questions[1].name, 'hello.world.its.me')
        self.assertEqual(dns_questions[1].type, 2)
        self.assertEqual(dns_questions[1].response_class, 2)

        # Check that the third question was properly decoded
        self.assertEqual(dns_questions[2].name, 'oh.hi.there.stranger')
        self.assertEqual(dns_questions[2].type, 3)
        self.assertEqual(dns_questions[2].response_class, 3)

    def test_read_resource_questions_no_records(self):
        """
        Test case to attempt to decode 0 resource records. In other words, don't decode anything and return an empty list.
        """
        records: List[ResourceRecord] = DNSMessage._read_resource_records(BytesIO(self.three_consecutive_resource_records_encoded),
                                                                          BytesIO(self.three_consecutive_resource_records_encoded),
                                                                          0)

        self.assertEqual(len(records), 0)

    def test_read_resource_records(self):
        """
        Test case to decode three consecutive resource records
        """
        records: List[ResourceRecord] = DNSMessage._read_resource_records(BytesIO(self.three_consecutive_resource_records_encoded),
                                                                          BytesIO(self.three_consecutive_resource_records_encoded),
                                                                          3)

        # Check that the first name server record was correctly decoded
        self.assertEqual(records[0].name, 'ca')
        self.assertEqual(records[0].type, 2)
        self.assertEqual(records[0].response_class, 1)
        self.assertEqual(records[0].ttl, 150873)
        self.assertEqual(records[0].rdlength, 14)
        self.assertEqual(records[0].rdata, 'x.ca-servers')

        # Check that the first name server record was correctly decoded
        self.assertEqual(records[1].name, 'ubc')
        self.assertEqual(records[1].type, 1)
        self.assertEqual(records[1].response_class, 2)
        self.assertEqual(records[1].ttl, 150873)
        self.assertEqual(records[1].rdlength, 4)
        self.assertEqual(records[1].rdata, '1.2.3.4')

        # Check that the first name server record was correctly decoded
        self.assertEqual(records[2].name, 'tsn')
        self.assertEqual(records[2].type, 5)
        self.assertEqual(records[2].response_class, 3)
        self.assertEqual(records[2].ttl, 150873)
        self.assertEqual(records[2].rdlength, 13)
        self.assertEqual(records[2].rdata, 'x.z-servers')

