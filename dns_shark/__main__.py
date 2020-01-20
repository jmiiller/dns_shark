from dns_shark.command_line_parsing import create_parser
import sys
from argparse import ArgumentParser, Namespace
from dns_shark.resource_record import ResourceRecord
from typing import List
from dns_shark.resolver_core import ResolverCore
from dns_shark.dns_resolver import Resolver
from dns_shark.errors.dns_format_error import DNSFormatError
from dns_shark.errors.dns_name_error import DNSNameError
from dns_shark.errors.dns_not_implemented_error import DNSNotImplementedError
from dns_shark.errors.dns_server_failure_error import DNSServerFailureError
from dns_shark.errors.dns_refused_error import DNSRefusedError
from dns_shark.errors.dns_no_matching_resource_record_error import DNSNoMatchingResourceRecordError
from dns_shark.errors.dns_zero_counter_error import DNSZeroCounterError


def main():
    parser: ArgumentParser = create_parser()
    args: Namespace = parser.parse_args(sys.argv[1:])

    dns_server_ip: str = args.dns_server_ip.pop()
    domain_name: str = args.domain_name.pop()

    main_helper(Resolver(), domain_name, dns_server_ip, args.ipv6 is not None, args.verbose is not None)

    exit(0)


def main_helper(resolver: Resolver, domain_name: str, dns_server_ip: str, ipv6: bool, verbose: bool):

    try:
        answers: List[ResourceRecord] = resolver.ask(domain_name, dns_server_ip, ipv6, verbose)
    except DNSFormatError as e:
        print("")
        print(e)
    except DNSNameError as e:
        print("")
        print(e)
    except DNSNotImplementedError as e:
        print("")
        print(e)
    except DNSServerFailureError as e:
        print("")
        print(e)
    except DNSRefusedError as e:
        print("")
        print(e)
    except DNSNoMatchingResourceRecordError as e:
        print("")
        print(e)
    except DNSZeroCounterError as e:
        print("")
        print(e)
    else:
        ResolverCore.print_answers(domain_name, answers)


if __name__ == '__main__':
    main()
