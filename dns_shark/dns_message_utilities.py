from dns_shark.domain_name_handling import DomainNameEncoder
from io import BytesIO


class DNSMessageUtilities:
    """
    Contains utility functions pertaining to DNS Queries.

    In particular, contains functionality to generate dns queries to request the resolution of
    a specified domain name.
    """

    @staticmethod
    def create_domain_name_query(domain_name: str, query_id: int, type_requested: int) -> BytesIO:
        """

        :param domain_name: the domain name to be looked up
        :param query_id: the unique id of this dns query
        :param type_requested: the type of resource requested (ipv4 or ipv6)
        :return: a bytearray that contains a dns query that will request a particular domain name
        """
        query = BytesIO()
        DNSMessageUtilities.encode_header(query, query_id)
        query.write(DomainNameEncoder.encode_domain_name(domain_name))
        DNSMessageUtilities.encode_query_type(query, type_requested)
        DNSMessageUtilities.encode_query_class(query, 1)
        return query

    @staticmethod
    def encode_header(query: BytesIO, query_id: int) -> None:
        """
        Encodes the header of the dns query.

        :param query: the byte array that is accumulating the dns query
        :param query_id: the unique id of the dns query
        :return: the query with an updated header
        """

        query.write(query_id.to_bytes(2, 'big'))  # add query id
        query.write(b'\x00\x00')                  # add flags
        query.write(b'\x00\x01')                  # add dns question count
        query.write(b'\x00\x00')                  # add answer record count
        query.write(b'\x00\x00')                  # add name server count
        query.write(b'\x00\x00')                  # add additional record count

    @staticmethod
    def encode_query_type(query: BytesIO, type: int) -> None:
        """
        Encodes the query type of a dns query.

        :param query: the byte array that is accumulating the dns query
        :param type: the type of the query
        :return: None
        """
        query.write(type.to_bytes(2, 'big'))

    @staticmethod
    def encode_query_class(query: BytesIO, query_class: int) -> None:
        """
        Encode the query class of a dns query.

        :param query: the byte array that is accumulating the dns query
        :param query_class: the class of the dns message (1 for Internet)
        :return: None
        """
        query.write(query_class.to_bytes(2, 'big'))
