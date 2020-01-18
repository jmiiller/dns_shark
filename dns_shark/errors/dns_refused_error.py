from dns_shark.errors.dns_shark_error import DNSSharkError


class DNSRefusedError(DNSSharkError):
    """
    An error that indicates an rcode of 5 was returned by a dns message.

    'Refused - The name server refuses to perform the specified operation for policy reasons.  For example, a name
    server may not wish to provide the information to the particular requester, or a name server may not wish to perform
    a particular operation (e.g., zone transfer) for particular data.'

    see https://tools.ietf.org/rfc/rfc1035.txt for more info.
    """
