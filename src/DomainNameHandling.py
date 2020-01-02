"""
Contains functionality that allows domain names to be encoded and decoded according to the
DNS data compression algorithm.
"""

from typing import List


def encode_domain_name(query: bytearray, domain_name: str) -> None:
    """
    Encode a domain name according to the DNS message compression and encoding scheme.

    :param query: a byte array that contains the dns message as it is being built
    :param domain_name: the domain name that needs to be compressed and encoded
    :return: None
    """

    split_domain_name: List[str] = domain_name.split('.')

    for item in split_domain_name:
        encode_label(query, item)

    query.append(0x00)  # Must add a x00 to the end to terminate the compressed domain name.


def encode_label(query: bytearray, label: str) -> None:
    """
    Encode a single label in a DNS domain name.

    :param query: a byte array that contains the dns message as it is being built
    :param label: the domain name that needs to be compressed and encoded
    :return: None
    """
    array = bytearray(label, "ascii")

    query.append(len(label))
    for item in array:
        query.append(item)
