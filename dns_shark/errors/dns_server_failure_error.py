from dns_shark.errors.dns_shark_error import DNSSharkError


class DNSServerFailureError(DNSSharkError):
    """
    An error that indicates an rcode of 2 was returned by a dns message.

    'Server failure - The name server was unable to process this query due to a
     problem with the name server.'

    see https://tools.ietf.org/rfc/rfc1035.txt for more info.
    """