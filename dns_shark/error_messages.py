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
