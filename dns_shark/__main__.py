from dns_shark.command_line_parsing import create_parser
import sys
from argparse import ArgumentParser, Namespace
from dns_shark.resource_record import ResourceRecord
from typing import List
from dns_shark.resolver_core import ResolverCore
from dns_shark.dns_resolver import Resolver

IPV6_TYPE = 28
IPV4_TYPE = 1


def main():

    parser: ArgumentParser = create_parser()
    args: Namespace = parser.parse_args(sys.argv[1:])

    dns_server_ip: str = args.dns_server_ip.pop()
    domain_name: str = args.domain_name.pop()

    if args.ipv6 is None:
        ipv6: bool = False
    else:
        ipv6: bool = True

    if args.verbose is None:
        verbose: bool = False
    else:
        verbose: bool = True

    answers: List[ResourceRecord] = Resolver.ask(domain_name, dns_server_ip, ipv6, verbose)

    ResolverCore.print_answers(domain_name, answers)

    exit(0)


if __name__ == '__main__':
    main()
