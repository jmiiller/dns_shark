from dns_shark.errors.dns_shark_error import DNSSharkError


class DNSFormatError(DNSSharkError):
    """
    An error that indicates an rcode of 1 was returned by a dns message.

    'Format error - The name server was unable to interpret the query.'

    see https://tools.ietf.org/rfc/rfc1035.txt for more info.
    """
