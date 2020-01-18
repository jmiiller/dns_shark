from dns_shark.errors.dns_shark_error import DNSSharkError


class DNSNoMatchingResourceRecordError(DNSSharkError):
    """
    This type of error occurs when an authoritative response is given for the domain name and the rcode is 0
    (i.e. it successfully found the domain name), but there is no corresponding answer resource record with
    the desired type for the domain name.

    An example of this error is when attempting to look up the ipv6 address of a domain name that only has an
    ipv4 address.
    """