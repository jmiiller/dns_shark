"""
Contains functionality that allows domain names to be encoded and decoded according to the
DNS data compression algorithm.
"""

from typing import List
from io import StringIO, BytesIO


class DomainNameEncoder:
    """
    Provides the ability to encode a domain name string to the appropriate dns compression/encoding format.
    """

    @staticmethod
    def encode_domain_name(domain_name: str) -> bytes:
        """
        Encode a domain name according to the DNS message compression and encoding scheme.

        :param domain_name: the domain name that needs to be compressed and encoded
        :return: return the bytes that the writer contains after encoding the domain name
        """
        writer: BytesIO = BytesIO()  # ensure we start with a clean writer

        split_domain_name: List[str] = domain_name.split('.')
        for item in split_domain_name:
            DomainNameEncoder._encode_label(item, writer)

        writer.write(b'\x00')  # Must add a 0x00 to the end to terminate the compressed domain name.

        return writer.getvalue()

    @staticmethod
    def _encode_label(label: str, writer: BytesIO) -> None:
        """
        Encode a single label in a DNS domain name.

        :param label: the domain name label that needs to be compressed and encoded
        :return: None
        """

        writer.write(len(label).to_bytes(1, 'big'))
        for char in label:
            writer.write(char.encode('ascii'))


class DomainNameDecoder:
    """
    Provides the ability to decode a domain name string to the appropriate dns compression/encoding format.
    """

    @staticmethod
    def decode_domain_name(data: BytesIO) -> str:
        """
        Decode the domain name that was provided when the object was initially created.

        :return: the decoded domain name as a str
        """
        reader: BytesIO = data
        copy_of_data: BytesIO = data
        string_builder: StringIO = StringIO()

        DomainNameDecoder._decode_domain_name_helper(reader, copy_of_data, string_builder)

        return string_builder.getvalue()[1:]  # we remove the first char, since it is an extra '.'.

    @staticmethod
    def _decode_domain_name_helper(reader: BytesIO, copy_of_data: BytesIO, string_builder: StringIO) -> None:
        """
        Helper function to decode domain names. (Used to allow for a mutually recursive solution).

        :return: None
        """
        label_length: int = int.from_bytes(reader.read(1), 'big')

        if label_length != 0:
            DomainNameDecoder._decode_label(reader, copy_of_data, string_builder, label_length)

    @staticmethod
    def _decode_label(reader: BytesIO, copy_of_data: BytesIO, string_builder: StringIO, label_length: int) -> None:
        """
        Decodes a single label of a encoded domain name.

        :param label_length: the length of the label to be decoded
        :return: None
        """

        string_builder.write('.')

        for _ in range(label_length):
            char: str = reader.read(1).decode('ascii')
            string_builder.write(char)

        DomainNameDecoder._decode_domain_name_helper(reader, copy_of_data, string_builder)
