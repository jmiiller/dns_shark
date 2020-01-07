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


class Resolver:
    """
    Top level class for the DNS Resolver.

    Handles command line argument parsing, setting
    """

    @staticmethod
    def resolve_domain_name(sending_socket,
                            requested_domain_name: str,
                            queried_dns_server_ip: str,
                            requested_type: int,
                            verbose: bool,
                            starting_dns_server_ip: str):
        #if counter = 0:
        #   too many queries error printing

        dns_response = Resolver._request_domain_name(sending_socket, requested_domain_name, queried_dns_server_ip, requested_type, verbose)
        #counter =- 1

        Resolver._handle_tracing_for_dns_response(dns_response, verbose)

        #if dns_response.rcode = 3:
        #   print error message

        #if dns_response.rcode != 0:
        # print other errors

        if dns_response.authoritative:  # If the response is from a DNS server that is authoritative, it will either have a CNAME or A entry for the fqdn.
            answer_resource_records = dns_response.get_resource_records_that_match_domain_name_and_type(requested_domain_name, requested_type)
            cname_resource_records = dns_response.get_resource_records_that_match_domain_name_and_type(requested_domain_name, 5)

            if answer_resource_records:
                return answer_resource_records

            elif cname_resource_records:
                cname_domain_name: str = cname_resource_records[0].rdata
                return Resolver.resolve_domain_name(sending_socket, cname_domain_name, starting_dns_server_ip, requested_type, verbose, starting_dns_server_ip)

            else:
                pass
                # print pseudo error
        else:  # not an authoritative response. Therefore, look for a name server to send the next request to.
            name_server_ip = dns_response.get_name_server_ip_address()

            if name_server_ip: # Response contains an address for one of the name servers, send packet to that server.
                return Resolver.resolve_domain_name(sending_socket, requested_domain_name, name_server_ip, requested_type, verbose, starting_dns_server_ip)

            else: # Response does not contain an address for any of the name servers in its nameserver section. Search for the ip of the first name server now. When found, use that to continue searching for fqdn.
                name_server_records: List[ResourceRecord] = Resolver.resolve_domain_name(sending_socket, dns_response.name_server_records[0].rdata, starting_dns_server_ip, 1, verbose, starting_dns_server_ip)
                name_server_ip: str = name_server_records[0].rdata
                return Resolver.resolve_domain_name(sending_socket, domain_name, name_server_ip, requested_type, verbose, starting_dns_server_ip)


    @staticmethod
    def _request_domain_name(sending_socket,
                             requested_domain_name: str,
                             queried_dns_server_ip: str,
                             requested_type: int,
                             verbose: bool):
        #start_time =
        random_query_id: int = randint(0, 65535)

        domain_name_query: BytesIO = create_domain_name_query(requested_domain_name, random_query_id, requested_type)
        sending_socket.sendto(domain_name_query.getvalue(), (queried_dns_server_ip, 53))

        Resolver._handle_tracing_for_dns_query(domain_name_query, queried_dns_server_ip, verbose)

        return Resolver._receive_dns_message(sending_socket, random_query_id)

    @staticmethod
    def _receive_dns_message(receiving_socket, expected_query_id: int):
        #handle_timeout_error()
        received_data = receiving_socket.recv(1024)
        received_dns_message: DNSMessage = DNSMessage(BytesIO(received_data))

        if (received_dns_message.query_id != expected_query_id) or not received_dns_message.is_response:
            Resolver.receive_dns_message(socket, expected_query_id)
        else:
            return received_dns_message

    @staticmethod
    def _handle_tracing_for_dns_response(dns_message: DNSMessage, verbose: bool):
        if verbose:
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


if __name__ == '__main__':
    IPV6_TYPE = 28
    IPV4_TYPE = 1

    parser: ArgumentParser = create_parser()
    args: Namespace = parser.parse_args(sys.argv[1:])

    dns_server_ip: str = args.dns_server_ip.pop()
    domain_name: str = args.domain_name.pop()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket:

        answers: List[ResourceRecord]

        # counter = 30
        if args.ipv6:
            answers: List[ResourceRecord] = Resolver.resolve_domain_name(socket,
                                                                         domain_name,
                                                                         dns_server_ip,
                                                                         IPV6_TYPE,
                                                                         args.verbose,
                                                                         dns_server_ip)
            pass
        else:
            answers: List[ResourceRecord] = Resolver.resolve_domain_name(socket,
                                                                         domain_name,
                                                                         dns_server_ip,
                                                                         IPV4_TYPE,
                                                                         args.verbose,
                                                                         dns_server_ip)

        Resolver.print_answers(domain_name, answers)


