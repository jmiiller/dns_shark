from src.CommandLineParsing import create_parser  # type: ignore
import sys
import socket
from argparse import ArgumentParser, Namespace
from src.DNSMessageUtilities import DNSMessageUtilities  # type: ignore
from src.DNSMessage import DNSMessage  # type: ignore
from src.ResourceRecord import ResourceRecord  # type: ignore
from io import BytesIO
from typing import List
from random import randint

#Todo
# - break up resolve_domain_name into nice, digestible methods that make the method easier to modify and understand.
# - add docstrings to resolver.py
# - add timeout
# - make into a python package and publish to pip
# - write tests to get complete test coverage

class Resolver:
    """
    Top-level class in charge of resolving domain names.
    """

    def __init__(self, sock, verbose: bool, starting_dns_server: str):
        self.udp_socket = sock
        self.verbose: bool = verbose
        self.starting_dns_server: str = starting_dns_server
        self.counter: int = 30  # Maximum number of requests allowed for name resolution. Used to avoid infinite loops.

    def resolve_domain_name(self,
                            requested_domain_name: str,
                            queried_dns_server_ip: str,
                            requested_type: int):
        if self.counter == 0:
            Resolver.print_zero_counter_error()

        dns_response: DNSMessage = self._request_domain_name(requested_domain_name, queried_dns_server_ip, requested_type)

        if dns_response.rcode != 0:
            Resolver.print_rcode_error_message(dns_response.rcode)

        self._handle_tracing_for_dns_response(dns_response)

        if dns_response.authoritative:
            # If the response is from a DNS server that is authoritative,
            # it will either have a CNAME or A entry for the fqdn.
            answer_resource_records = dns_response.get_answer_records_that_match_domain_name_and_type(requested_domain_name, requested_type)
            cname_resource_records = dns_response.get_answer_records_that_match_domain_name_and_type(requested_domain_name, 5)

            if answer_resource_records:
                return answer_resource_records

            elif cname_resource_records:
                cname_domain_name: str = cname_resource_records[0].rdata
                return self.resolve_domain_name(cname_domain_name, self.starting_dns_server, requested_type)

            else:
                pass
                # print pseudo error
        else:  # not an authoritative response. Therefore, look for a name server to send the next request to.
            name_server_ip: str = dns_response.get_name_server_ip_address()

            if name_server_ip: # Response contains an address for one of the name servers, send packet to that server.
                return self.resolve_domain_name(requested_domain_name, name_server_ip, requested_type)

            else:
                # Name server ip address could not be found. Thus, resolve the name server domain name. When found,
                # use the resolved ip address to continue search for originally desired domain name.
                name_server_records: List[ResourceRecord] = self.resolve_domain_name(dns_response.name_server_records[0].rdata,
                                                                                     self.starting_dns_server, 1)
                name_server_ip = name_server_records[0].rdata
                return self.resolve_domain_name(domain_name, name_server_ip, requested_type)

    def _request_domain_name(self,
                             requested_domain_name: str,
                             queried_dns_server_ip: str,
                             requested_type: int):
        #start_time =
        random_query_id: int = randint(0, 65535)

        domain_name_query: BytesIO = DNSMessageUtilities.create_domain_name_query(requested_domain_name,
                                                                                  random_query_id,
                                                                                  requested_type)
        self.udp_socket.sendto(domain_name_query.getvalue(), (queried_dns_server_ip, 53))

        self.counter = self.counter - 1 # decrement the counter by one, since we have just sent a request

        Resolver._handle_tracing_for_dns_query(domain_name_query, queried_dns_server_ip, self.verbose)

        return self._receive_dns_message(random_query_id)

    def _receive_dns_message(self, expected_query_id: int):
        #handle_timeout_error()
        received_data = self.udp_socket.recv(1024)
        received_dns_message: DNSMessage = DNSMessage(BytesIO(received_data))

        if (received_dns_message.query_id != expected_query_id) or not received_dns_message.is_response:
            self._receive_dns_message(expected_query_id)
        else:
            return received_dns_message

    def _handle_tracing_for_dns_response(self, dns_message: DNSMessage):
        if self.verbose:
            dns_message.print_message()

    @staticmethod
    def _handle_tracing_for_dns_query(domain_name_query: BytesIO, queried_dns_server_ip: str, verbose: bool):
        if verbose:
            print('')
            print('')
            domain_name_query.seek(0)  # need to ensure we are at the start of the writer
                                       # to be able to correctly decode into a DNS Question
            DNSMessage(domain_name_query).print_dns_question(queried_dns_server_ip)

    @staticmethod
    def print_answers(domain_name: str, answer_records: List[ResourceRecord]):
        print('')
        print("Answers:")
        for answer in answer_records:
            answer.print_record_with_supplied_domain_name(domain_name)

    @staticmethod
    def print_zero_counter_error() -> None:
        """
        Prints an error message for when too many queries are sent to resolve a domain name. Exits the program.

        :return: None
        """
        print("")
        print("Too many queries error: there appears to be a loop in resolving this domain name.")
        exit(1)

    @staticmethod
    def print_rcode_error_message(rcode: int) -> None:
        """
        Prints the appropriate error message for the given rcode. Exits if an error occurs.

        The error messages are taken from RFC 1035.

        :param rcode: a given rcode value
        :return: None
        """
        if rcode == 1:
            print("")
            print("Format error: the name server was unable to interpret the query.")
            exit(1)
        elif rcode == 2:
            print("")
            print("Server failure: The name server was unable to process this "
                  "query due to a problem with the name server.")
            exit(1)
        elif rcode == 3:
            print("")
            print("Name Error: the domain name you are attempt to resolve does not exist.")
            exit(1)
        elif rcode == 4:
            print("")
            print("Not Implemented: The name server does not support the requested kind of query.")
            exit(1)
        elif rcode == 5:
            print("")
            print("Refused - The name server refuses to perform the specified operation for policy reasons.")
            exit(1)



if __name__ == '__main__':
    IPV6_TYPE = 28
    IPV4_TYPE = 1

    parser: ArgumentParser = create_parser()
    args: Namespace = parser.parse_args(sys.argv[1:])

    dns_server_ip: str = args.dns_server_ip.pop()
    domain_name: str = args.domain_name.pop()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:

        answers: List[ResourceRecord]

        resolver: Resolver = Resolver(udp_socket, args.verbose, dns_server_ip)
        if args.ipv6:
            answers = resolver.resolve_domain_name(domain_name, dns_server_ip, IPV6_TYPE)
            pass
        else:
            answers = resolver.resolve_domain_name(domain_name, dns_server_ip, IPV4_TYPE)

        Resolver.print_answers(domain_name, answers)


