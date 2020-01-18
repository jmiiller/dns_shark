from dns_shark.errors.dns_shark_error import DNSSharkError


class DNSNameError(DNSSharkError):
    """
    An error that indicates an rcode of 3 was returned by a dns message.

    'Name Error - Meaningful only for responses from an authoritative name server, this code signifies that the
     domain name referenced in the query does not exist.'

    see https://tools.ietf.org/rfc/rfc1035.txt for more info.
    """