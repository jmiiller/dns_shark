from unittest.mock import Mock
import unittest
from dns_shark.__main__ import main_helper
from contextlib import redirect_stdout
from io import StringIO
from dns_shark.errors.dns_format_error import DNSFormatError
from dns_shark.errors.dns_name_error import DNSNameError
from dns_shark.errors.dns_not_implemented_error import DNSNotImplementedError
from dns_shark.errors.dns_server_failure_error import DNSServerFailureError
from dns_shark.errors.dns_refused_error import DNSRefusedError
from dns_shark.errors.dns_no_matching_resource_record_error import DNSNoMatchingResourceRecordError
from dns_shark.errors.dns_zero_counter_error import DNSZeroCounterError
from dns_shark.resource_record import ResourceRecord


class MainTests(unittest.TestCase):
    """
    Unit testing for __main__.py
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize test values used in the tests.
        """
        cls.format_error_message = "Format error: the name server was unable to interpret the query."

    def setUp(self):
        """
        Initialize test values used in tests.
        """
        self.buffer = StringIO()

    def test_main_helper_format_error(self):
        """
        Test case for when the resolver raises a DNSFormatErrpr
        """
        mock_resolver: Mock = Mock(**{'ask.side_effect': DNSFormatError('Format Error Message')})

        with redirect_stdout(self.buffer):
            main_helper(mock_resolver, "www.cs.ubc.ca", "1.2.3.4", False, False)

        self.assertEqual(self.buffer.getvalue(), "\nFormat Error Message\n")

    def test_main_helper_name_error(self):
        """
        Test case for when the resolver raises a DNSNameError
        """
        mock_resolver: Mock = Mock(**{'ask.side_effect': DNSNameError('Name Error Message')})

        with redirect_stdout(self.buffer):
            main_helper(mock_resolver, "www.cs.ubc.ca", "1.2.3.4", False, False)

        self.assertEqual(self.buffer.getvalue(), "\nName Error Message\n")

    def test_main_helper_not_implemented_error(self):
        """
        Test case for when the resolver raises a DNSNotImplementedError
        """
        mock_resolver: Mock = Mock(**{'ask.side_effect': DNSNotImplementedError('Not Implemented Error Message')})

        with redirect_stdout(self.buffer):
            main_helper(mock_resolver, "www.cs.ubc.ca", "1.2.3.4", False, False)

        self.assertEqual(self.buffer.getvalue(), "\nNot Implemented Error Message\n")

    def test_main_helper_server_failure_error(self):
        """
        Test case for when the resolver raises a DNSServerFailureError
        """
        mock_resolver: Mock = Mock(**{'ask.side_effect': DNSServerFailureError('Server Failure Error Message')})

        with redirect_stdout(self.buffer):
            main_helper(mock_resolver, "www.cs.ubc.ca", "1.2.3.4", False, False)

        self.assertEqual(self.buffer.getvalue(), "\nServer Failure Error Message\n")

    def test_main_helper_refused_error(self):
        """
        Test case for when the resolver raises a DNSRefusedError
        """
        mock_resolver: Mock = Mock(**{'ask.side_effect': DNSRefusedError('Refused Error Message')})

        with redirect_stdout(self.buffer):
            main_helper(mock_resolver, "www.cs.ubc.ca", "1.2.3.4", False, False)

        self.assertEqual(self.buffer.getvalue(), "\nRefused Error Message\n")

    def test_main_helper_no_matching_resource_record_error(self):
        """
        Test case for when the resolver raises a DNSNoMatchingResourceRecordError
        """
        mock_resolver: Mock = Mock(**{'ask.side_effect': DNSNoMatchingResourceRecordError('No Matching Resource Record Error Message')})

        with redirect_stdout(self.buffer):
            main_helper(mock_resolver, "www.cs.ubc.ca", "1.2.3.4", False, False)

        self.assertEqual(self.buffer.getvalue(), "\nNo Matching Resource Record Error Message\n")

    def test_main_helper_zero_counter_error(self):
        """
        Test case for when the resolver raises a DNSZeroCounterError
        """
        mock_resolver: Mock = Mock(**{'ask.side_effect': DNSZeroCounterError('Zero Counter Error Message')})

        with redirect_stdout(self.buffer):
            main_helper(mock_resolver, "www.cs.ubc.ca", "1.2.3.4", False, False)

        self.assertEqual(self.buffer.getvalue(), "\nZero Counter Error Message\n")

    def test_main_helper_one_answer_returned(self):
        """
        Test case for when the resolver returns a single answer
        """
        mock_resolver: Mock = Mock(**{'ask.return_value': [ResourceRecord("www.ubc.cs.ca", 1, 1, 600, 4, "1.2.3.4")]})

        with redirect_stdout(self.buffer):
            main_helper(mock_resolver, "www.cs.ubc.ca", "1.2.3.4", False, False)

        self.assertEqual(self.buffer.getvalue(), "\nAnswers:"
                                                 "\n  www.cs.ubc.ca 600   A 1.2.3.4\n")

    def test_main_helper_two_answers_returned(self):
        """
        Test case for when the resolver returns two answers
        """
        mock_resolver: Mock = Mock(**{'ask.return_value': [ResourceRecord("www.ubc.cs.ca", 1, 1, 600, 4, "1.2.3.4"),
                                                           ResourceRecord("www.ubc.cs.ca", 28, 1, 2000, 4, "5.6.7.8")]})

        with redirect_stdout(self.buffer):
            main_helper(mock_resolver, "www.cs.ubc.ca", "1.2.3.4", False, False)

        self.assertEqual(self.buffer.getvalue(), "\nAnswers:"
                                                 "\n  www.cs.ubc.ca 600   A 1.2.3.4"
                                                 "\n  www.cs.ubc.ca 2000   AAAA 5.6.7.8\n")

