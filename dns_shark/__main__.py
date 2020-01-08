# TODO:
# Add test coverage for ResourceRecord.py
# Add test coverage for Resolver.py
# Add to PyPi
# Add exception handling. (Maybe convert error messages into exceptions.)





from dns_shark.command_line_parsing import create_parser  # type: ignore
import sys
import socket
from argparse import ArgumentParser, Namespace
from dns_shark.ResourceRecord import ResourceRecord  # type: ignore
from typing import List
from dns_shark.Resolver import Resolver  # type: ignore


def main():
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
        else:
            answers = resolver.resolve_domain_name(domain_name, dns_server_ip, IPV4_TYPE)

        Resolver.print_answers(domain_name, answers)

        exit(0)


if __name__ == '__main__':
    main()