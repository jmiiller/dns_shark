import unittest
from io import BytesIO
from src.DNSMessage import DNSMessage
from src.DNSQuestion import DNSQuestion
from src.ResourceRecord import ResourceRecord


class DNSMessageTests(unittest.TestCase):

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
        cls.dns_question_encoded: bytes = b'\x03www\x02cs\x03ubc\x02ca\x00\x00\x01\x00\x01'
        cls.resource_record_encoded: bytes = b'\x02ca\x00\x00\x02\x00\x01\x00\x02MY\x00\x0e\x01x\nca-servers\x00'

    def test_decode_dns_message(self):
        """
        Test case to decode an entire dns message. This dns message contains resource records with pointers.
        """
        dns_message: DNSMessage = DNSMessage(BytesIO(self.dns_message_encoded))

        # Check that flags are correct
        self.assertEqual(dns_message.is_response, True)
        self.assertEqual(dns_message.opcode, 0)
        self.assertEqual(dns_message.authoritative, False)
        self.assertEqual(dns_message.is_truncated, False)
        self.assertEqual(dns_message.recursion_desired, False)
        self.assertEqual(dns_message.recursion_available, True)
        self.assertEqual(dns_message.rcode, 0)
        self.assertEqual(dns_message.question_count, 1)

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

    def test_decode_dns_question(self):
        """
        Test case to decode a dns question
        """
        dns_question: DNSQuestion = DNSQuestion(BytesIO(self.dns_question_encoded), BytesIO(self.dns_question_encoded))

        self.assertEqual(dns_question.name, 'www.cs.ubc.ca')
        self.assertEqual(dns_question.type, 1)
        self.assertEqual(dns_question.response_class, 1)

    def test_decode_resource_record(self):
        """
        Test case to decode a dns question
        """
        resource_record: ResourceRecord = ResourceRecord(BytesIO(self.resource_record_encoded), BytesIO(self.resource_record_encoded))

        self.assertEqual(resource_record.name, 'ca')
        self.assertEqual(resource_record.type, 2)
        self.assertEqual(resource_record.response_class, 1)
        self.assertEqual(resource_record.ttl, 150873)
        self.assertEqual(resource_record.rdlength, 14)
        self.assertEqual(resource_record.rdata, 'x.ca-servers')


