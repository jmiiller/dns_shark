import unittest
from dns_shark.CommandLineParsing import create_parser  # type: ignore


class CommandLineParsingTests(unittest.TestCase):
    """
    Unit testing for CommandLineParsing.py (i.e. command line parsing logic)
    """

    def setUp(self):
        self.parser = create_parser()

    def test_no_args_provided(self):
        """
        Test case for when no arguments are supplied.
        """
        self.assertRaises(SystemExit, self.parser.parse_args, [])

    def test_one_arg_provided(self):
        """
        Test case for when only one argument is supplied.
        """
        self.assertRaises(SystemExit, self.parser.parse_args, ["127.0.0.1"])

    def test_only_required_args_given(self):
        """
        Test case for when only the two required arguments are supplied.
        """
        parsed_args = self.parser.parse_args(['127.0.0.1', 'www.jeffreymiiller.com'])

        self.assertEqual(parsed_args.dns_server_ip, ['127.0.0.1'])
        self.assertEqual(parsed_args.domain_name, ['www.jeffreymiiller.com'])
        self.assertEqual(parsed_args.verbose, None)
        self.assertEqual(parsed_args.ipv6, None)

    def test_verbose_true(self):
        """
        Test case for when the verbose argument is supplied.
        """
        parsed_args = self.parser.parse_args(['127.0.0.1', 'www.jeffreymiiller.com', '--verbose', '1'])

        self.assertEqual(parsed_args.dns_server_ip, ['127.0.0.1'])
        self.assertEqual(parsed_args.domain_name, ['www.jeffreymiiller.com'])
        self.assertEqual(parsed_args.verbose, [True])
        self.assertEqual(parsed_args.ipv6, None)

    def test_ipv6_true(self):
        """
        Test case for when the ipv6 argument is supplied.
        """
        parsed_args = self.parser.parse_args(['127.0.0.1', 'www.jeffreymiiller.com', '--ipv6', '1'])

        self.assertEqual(parsed_args.dns_server_ip, ['127.0.0.1'])
        self.assertEqual(parsed_args.domain_name, ['www.jeffreymiiller.com'])
        self.assertEqual(parsed_args.verbose, None)
        self.assertEqual(parsed_args.ipv6, [True])

    def test_ipv6_and_verbose_true(self):
        """
        Test case for when both the ipv6 and verbose arguments are supplied.
        """
        parsed_args = self.parser.parse_args(['127.0.0.1', 'www.jeffreymiiller.com', '--verbose', '1', '--ipv6', '1'])

        self.assertEqual(parsed_args.dns_server_ip, ['127.0.0.1'])
        self.assertEqual(parsed_args.domain_name, ['www.jeffreymiiller.com'])
        self.assertEqual(parsed_args.verbose, [True])
        self.assertEqual(parsed_args.ipv6, [True])

    def test_ipv6_and_verbose_reverse_order(self):
        """
        Test case that reverses the order the ipv6 and verbose arguments.
        """
        parsed_args = self.parser.parse_args(['127.0.0.1', 'www.jeffreymiiller.com', '--ipv6', '1', '--verbose', '1'])

        self.assertEqual(parsed_args.dns_server_ip, ['127.0.0.1'])
        self.assertEqual(parsed_args.domain_name, ['www.jeffreymiiller.com'])
        self.assertEqual(parsed_args.verbose, [True])
        self.assertEqual(parsed_args.ipv6, [True])