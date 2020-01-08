class ErrorMessages:
    """
    Contains all logic pertaining to error messages and logging.
    """

    @staticmethod
    def print_zero_counter_error() -> None:
        """
        Prints an error message for when too many queries are sent to resolve a domain name. Exits the program.

        :return: None
        """
        print("")
        print("Too many queries error: there appears to be a loop in resolving this domain name.")
        exit(1)

    @staticmethod
    def print_rcode_error_message(rcode: int) -> None:
        """
        Prints the appropriate error message for the given rcode. Exits if an error occurs.

        The error messages are taken from RFC 1035.

        :param rcode: a given rcode value
        :return: None
        """
        if rcode == 1:
            print("")
            print("Format error: the name server was unable to interpret the query.")
            exit(1)
        elif rcode == 2:
            print("")
            print("Server failure: The name server was unable to process this "
                  "query due to a problem with the name server.")
            exit(1)
        elif rcode == 3:
            print("")
            print("Name Error: the domain name you are attempt to resolve does not exist.")
            exit(1)
        elif rcode == 4:
            print("")
            print("Not Implemented: The name server does not support the requested kind of query.")
            exit(1)
        elif rcode == 5:
            print("")
            print("Refused - The name server refuses to perform the specified operation for policy reasons.")
            exit(1)

    @staticmethod
    def print_no_matching_ip_address_error() -> None:
        """
        Prints an error message for when a domain name is resolved, but there is no corresponding ip address.

        This type of error occurs when an authoritative response is given for the domain name and the rcode is 0
        (i.e. it successfully found the domain name), but there is no corresponding answer resource record with
        an ip for the domain name.

        An example of this error is when attempting to look up the ipv6 address of a domain name that only has an
        ipv4 address.

        :return: None
        """
        print("")
        print("Missing IP address error: the domain name exists, but does not have the specified "
              "type of IP address associated with it.")
        exit(1)
