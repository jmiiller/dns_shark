"""
Contains utility functions pertaining to DNS Queries.

In particular, contains functionality to generate dns queries to request the resolution of
a specified domain name.
"""

from src.DomainNameHandling import DomainNameEncoder
from struct import pack
from io import BytesIO


def create_domain_name_query(domain_name: str, query_id: int, type_requested: int) -> BytesIO:
    """

    :param domain_name: the domain name to be looked up
    :param query_id: the unique id of this dns query
    :param type_requested: the type of resource requested (ipv4 or ipv6)
    :return: a bytearray that contains a dns query that will request a particular domain name
    """
    query = BytesIO()
    encode_header(query, query_id)
    query.write(DomainNameEncoder.encode_domain_name(domain_name))
    encode_query_type(query, type_requested)
    encode_query_class(query, 1)
    return query


def encode_header(query: BytesIO, query_id: int) -> None:
    """
    Encodes the header of the dns query.

    :param query: the byte array that is accumulating the dns query
    :param query_id: the unique id of the dns query
    :return: the query with an updated header
    """

    # fields being packed: query_id, flags, query count, answer record count, name server count, additional record count
    header: str = pack('>HHHHHH', query_id, 0x0000, 0x0001, 0x0000, 0x0000, 0x0000)

    query.write(header)


def encode_query_type(query: bytearray, type: int) -> None:
    """
    Encodes the query type of a dns query.

    :param query: the byte array that is accumulating the dns query
    :param type: the type of the query
    :return: None
    """
    query.write(type.to_bytes(2, 'big'))


def encode_query_class(query: bytearray, query_class: int) -> None:
    """

    :param query: the byte array that is accumulating the dns query
    :param query_class: the class of the dns message (1 for Internet)
    :return: None
    """
    query.write(query_class.to_bytes(2, 'big'))
