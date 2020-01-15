from dns_shark.dns_question import DNSQuestion
from io import BytesIO
import unittest
from test.utilities import Utilities


class DNSQuestionTests(unittest.TestCase):
    """
    Unit testing for dns_question
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """
        cls.dns_question_encoded: bytes = Utilities().dns_question_encoded

    def test_decode_dns_question(self):
        """
        Test case to decode a dns question.
        """
        dns_question: DNSQuestion = DNSQuestion.decode_dns_question(BytesIO(self.dns_question_encoded),
                                                                    BytesIO(self.dns_question_encoded))

        self.assertEqual(dns_question.name, 'www.cs.ubc.ca')
        self.assertEqual(dns_question.type, 1)
        self.assertEqual(dns_question.response_class, 1)