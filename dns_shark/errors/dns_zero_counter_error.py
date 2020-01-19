from dns_shark.errors.dns_shark_error import DNSSharkError


class DNSZeroCounterError(DNSSharkError):
    """
    An error that occurs when the resolver counter is set to 0. Indicates that either an abnormally long resolution
    occurred or the resolver is in an infinite loop.
    """
