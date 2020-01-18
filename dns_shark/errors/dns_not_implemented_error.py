from dns_shark.errors.dns_shark_error import DNSSharkError


class DNSNotImplementedError(DNSSharkError):
    """
    An error that indicates an rcode of 4 was returned by a dns message.

    'Not Implemented - The name server does not support the requested kind of query.'

    see https://tools.ietf.org/rfc/rfc1035.txt for more info.
    """