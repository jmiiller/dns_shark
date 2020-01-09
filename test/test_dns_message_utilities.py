import unittest
from dns_shark.dns_message_utilities import DNSMessageUtilities
from dns_shark.dns_message import DNSMessage
from io import BytesIO


class DNSMessageUtilitiesTests(unittest.TestCase):
    """
    Unit testing for dns_message_utilities.py
    """

    def test_create_domain_name_query(self):
        """
        Test case to create a DNS query to ask for a particular domain name from a dns server.
        """
        encoded_dns_message: BytesIO = DNSMessageUtilities.create_domain_name_query('www.cs.ubc.ca', 12345, 15)

        encoded_dns_message.seek(0)  # need to start reading the dns message from the start of the BytesIO object
        dns_message = DNSMessage.decode_dns_message(encoded_dns_message)

        # Check that the query id is correct
        self.assertEqual(dns_message.query_id, 12345)

        # Check that flags are correct
        self.assertEqual(dns_message.is_response, False)
        self.assertEqual(dns_message.opcode, 0)
        self.assertEqual(dns_message.authoritative, False)
        self.assertEqual(dns_message.is_truncated, False)
        self.assertEqual(dns_message.recursion_desired, False)
        self.assertEqual(dns_message.recursion_available, False)
        self.assertEqual(dns_message.rcode, 0)

        # Check that record/question counts are correct
        self.assertEqual(dns_message.question_count, 1)
        self.assertEqual(dns_message.answer_count, 0)
        self.assertEqual(dns_message.nameserver_count, 0)
        self.assertEqual(dns_message.additional_count, 0)

        # Check that the question was properly decoded
        self.assertEqual(dns_message.dns_questions[0].name, 'www.cs.ubc.ca')
        self.assertEqual(dns_message.dns_questions[0].type, 15)
        self.assertEqual(dns_message.dns_questions[0].response_class, 1)



