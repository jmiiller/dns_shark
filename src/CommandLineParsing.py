"""
Contains functions that handles command line parsing logic.
"""

import argparse


def create_parser():
    """
    Creates a command line parser.

    There are four arguments allowed for this parser:

    (1) the dns server ip (required)
    (2) the domain name to be resolved (resolved)
    (3) a verbose option, to print tracing information (optional)
    (4) an ipv6 option, to return the ipv6 address for a domain name (optional)

    :return: the command line argument parser
    """
    parser = argparse.ArgumentParser(description='Simple DNS Resolver.')

    parser.add_argument("dns_server_ip", type=str, nargs=1,
                        help='Consumes the IP address (IPv4 only) of a DNS Server.')
    parser.add_argument("domain_name", type=str, nargs=1,
                        help='Consumes any valid, registered domain name.')
    parser.add_argument("--verbose", type=bool, nargs=1,
                        help='If enabled, prints a trace of the resolution. (Input any value to set to true.')
    parser.add_argument("--ipv6", type=bool, nargs=1,
                        help='If enabled, retrieves the IPv6 of the domain name. (Input any value to set to true).')

    return parser