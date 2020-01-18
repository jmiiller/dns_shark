class DNSSharkError(Exception):
    """
    Top level exception class from which all exceptions thrown by DNS Shark will be derived from.

    Allows for any DNS Shark exception to be caught, as needed.
    """