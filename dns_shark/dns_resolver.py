import socket
from dns_shark.resolver_core import ResolverCore
from typing import List
from dns_shark.resource_record import ResourceRecord
from random import Random


class Resolver:
    """
    This class contains the API for dns shark.

    These are the methods that should be used by any other developer seeking to leverage dns shark in their application.
    """

    @staticmethod
    def ask(domain_name: str, dns_server: str, ipv6: bool = False, verbose: bool = False) -> List[ResourceRecord]:
        """
        Resolves a domain name by starting the name resolution at the specified dns server ip.

        Can optionally specify whether an ipv6 address or verbose output is desired.

        :param domain_name: the domain name that will be resolved
        :param dns_server: the dns server ipv4 address that the name resolution process will begin with
        :param ipv6: a boolean flag indicating whether you want to find an ipv6 address for the domain name
        :param verbose: a boolean flag indicating whether you want verbose output for the name resolution process
        :raises: DNSFormatError, DNSServerFailureError, DNSNameError, DNSNotImplementedError, DNSRefusedError,
                 DNSZeroCounterError, DNSNoMatchingResourceRecordError
        :return: a list of the resource records the domain name resolved to
        """

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:

            resolver: ResolverCore = ResolverCore(udp_socket, verbose, dns_server, Random())
            type = 28 if ipv6 else 1

            answers: List[ResourceRecord] = resolver.resolve_domain_name(domain_name, dns_server, type)
            return answers

