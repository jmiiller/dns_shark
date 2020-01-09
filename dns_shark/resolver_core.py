from dns_shark.dns_message_utilities import DNSMessageUtilities
from dns_shark.dns_message import DNSMessage
from dns_shark.resource_record import ResourceRecord
from io import BytesIO
from typing import List, Optional
from random import randint
from dns_shark.error_messages import ErrorMessages


class ResolverCore:
    """
    Top-level class in charge of resolving domain names.

    Use the resolve_domain_name() method to resolve domain names to the requested resource record type.
    """

    def __init__(self, sock, verbose: bool, starting_dns_server: str):
        self.udp_socket = sock
        self.verbose: bool = verbose
        self.starting_dns_server: str = starting_dns_server
        self.counter: int = 30  # Maximum number of requests allowed for name resolution. Used to avoid infinite loops.


    def resolve_domain_name(self, requested_domain_name: str,
                            next_dns_server_ip: str,
                            requested_type: int) -> List[ResourceRecord]:
        """
        Resolves a requested domain name of the requested type. Begins the name resolution process via sending a dns
        query to the next_dns_server_ip.

        :param requested_domain_name: the domain name we wish to resolve.
        :param next_dns_server_ip: the starting dns server which we use in the name resolution process.
        :param requested_type: the desired resource record type we seek to resolve the domain name to.
        :return: a list of the answer records that match the desired domain name and type, if present.
        """

        self._check_counter()

        dns_response: DNSMessage = self._request_domain_name(requested_domain_name, next_dns_server_ip, requested_type)

        ResolverCore._check_rcode(dns_response.rcode)
        self._handle_tracing_for_dns_response(dns_response)

        if dns_response.authoritative:
            # If the response is from a DNS server that is authoritative,
            # it will either have a CNAME or A entry for the fqdn.
            return self._handle_authoritative_response(dns_response, requested_domain_name, requested_type)

        else:
            # not an authoritative response. Therefore, look for a name server to send the next request to.
            return self._handle_non_authoritative_response(dns_response, requested_domain_name, requested_type)

    def _handle_authoritative_response(self, dns_response: DNSMessage,
                                       requested_domain_name: str,
                                       requested_type: int) -> List[ResourceRecord]:
        """
        If an authoritative response is received from the domain name server, then first look for any matching
        answer records. If there is one or more answer records, return them.

        If there are no such records, then find a cname record and resolve the domain using its cname value.

        :param dns_response: the most recently received dns response in the name resolution process.
        :param requested_domain_name: the domain name we wish to resolve.
        :param requested_type: the type of address we wish to resolve the domain name to.
        :return: a list of the answer records that match the desired domain name and type, if present.
        """

        answer_resource_records = dns_response.get_answer_records_that_match_domain_name_and_type(requested_domain_name, requested_type)
        cname_resource_records = dns_response.get_answer_records_that_match_domain_name_and_type(requested_domain_name, 5)

        if answer_resource_records:
            return answer_resource_records

        elif cname_resource_records:
            cname_domain_name: str = cname_resource_records[0].rdata
            return self.resolve_domain_name(cname_domain_name, self.starting_dns_server, requested_type)

        else:
            ErrorMessages.print_no_matching_ip_address_error()
            return []  # included to make MyPy happy

    def _handle_non_authoritative_response(self, dns_response: DNSMessage,
                                                 requested_domain_name: str,
                                                 requested_type: int) -> List[ResourceRecord]:
        """
        Attempts to find a name server address to send the next name resolution request to.

        If the name server ip is included in the additional resource records, then use it for next dns query.

        If name server ip is not present, first resolve the name server domain name to an ipv4 address and send the
        next dns query there.

        :param dns_response: the most recently received dns response in the name resolution process.
        :param requested_domain_name: the domain name we wish to resolve.
        :param requested_type: the type of address we wish to resolve the domain name to.
        :return: a list of the answer records that match the desired domain name and type, if present.
        """
        name_server_ip: Optional[str] = dns_response.get_name_server_ip_address()

        if name_server_ip:  # Response contains an address for one of the name servers, send packet to that server.
            return self.resolve_domain_name(requested_domain_name, name_server_ip, requested_type)

        else:
            # Name server ip address could not be found. Thus, resolve the name server domain name. When found,
            # use the resolved ip address to continue search for originally desired domain name.
            name_server_records: List[ResourceRecord] = self.resolve_domain_name(dns_response.name_server_records[0].rdata,
                                                                                 self.starting_dns_server, 1)
            name_server_ip = name_server_records[0].rdata
            return self.resolve_domain_name(requested_domain_name, name_server_ip, requested_type)

    def _request_domain_name(self,
                             requested_domain_name: str,
                             next_dns_server_ip: str,
                             requested_type: int) -> DNSMessage:
        """
        Creates a dns query to send to the starting_dns_server resource records pertaining to the requested_domain_name
        of the requested_type.

        Decrements the resolver counter by 1, since we sent a dns query.

        :param requested_domain_name: the domain name we wish to resolve.
        :param next_dns_server_ip: the dns server we wish to send the next dns query to.
        :param requested_type: the type of address we wish to resolve the domain name to.
        :return: the dns response from the next_dns_server_ip.
        """
        random_query_id: int = randint(0, 65535)

        domain_name_query: BytesIO = DNSMessageUtilities.create_domain_name_query(requested_domain_name,
                                                                                  random_query_id,
                                                                                  requested_type)
        self.udp_socket.sendto(domain_name_query.getvalue(), (next_dns_server_ip, 53))

        self.counter = self.counter - 1 # decrement the counter by one, since we have just sent a request
        self._handle_tracing_for_dns_query(domain_name_query, next_dns_server_ip)

        return self._receive_dns_message(random_query_id)

    def _receive_dns_message(self, expected_query_id: int) -> DNSMessage:
        """
        Receives and decodes a dns message from a dns server.

        If the received dns message does not have the expected query_id or is not a response, then simply wait for the
        next message received.

        :param expected_query_id: the query id we expect the incoming dns response to possess.
        :return: the dns response that has been received, successfully decoded, and has the correct query_id and is_
        response value.
        """
        received_data = self.udp_socket.recv(1024)
        received_dns_message: DNSMessage = DNSMessage.decode_dns_message(BytesIO(received_data))

        if (received_dns_message.query_id != expected_query_id) or not received_dns_message.is_response:
            self._receive_dns_message(expected_query_id)

        return received_dns_message

    def _handle_tracing_for_dns_response(self, dns_response: DNSMessage) -> None:
        """
        If the resolver is set to verbose, then print tracing information for the dns response.

        :param dns_response: the dns response we wish to provide tracing information of.
        :return: None.
        """
        if self.verbose:
            dns_response.print_dns_response()

    def _handle_tracing_for_dns_query(self, domain_name_query: BytesIO, next_dns_server_ip: str) -> None:
        """
        If the resolver is set to verbose, then print tracing information for the dns query.

        :param domain_name_query: the domain name query that is sent to the next_dns_server_ip.
        :param next_dns_server_ip: the dns server we send the domain name query to.
        :return: None
        """
        if self.verbose:
            print('')
            print('')
            domain_name_query.seek(0)  # need to ensure we are at the start of the writer
                                       # to be able to correctly decode into a DNS Question
            DNSMessage.decode_dns_message(domain_name_query).print_dns_question(next_dns_server_ip)

    @staticmethod
    def print_answers(requested_domain_name: str, answer_records: List[ResourceRecord]) -> None:
        """
        Prints all answer records that the name resolution of the domain name produced.

        :param requested_domain_name: the domain name we resolved.
        :param answer_records: the answer records received from the name resolution process.
        :return: None
        """
        print('')
        print("Answers:")
        for answer in answer_records:
            answer.print_record_with_supplied_domain_name(requested_domain_name)

    def _check_counter(self) -> None:
        """
        If the resolver's counter is zero, then print the zero counter error and exit.

        :return: None
        """
        if self.counter == 0:
            ErrorMessages.print_zero_counter_error()

    @staticmethod
    def _check_rcode(rcode: int) -> None:
        """
        If rcode is non-zero, then print the appropriate rcode error message and exit.

        :param rcode: the rcode the most recent dns response possessed
        :return: None
        """
        if rcode != 0:
            ErrorMessages.print_rcode_error_message(rcode)


