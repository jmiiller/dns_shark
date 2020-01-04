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
    def decode_domain_name(reader: BytesIO, copy_of_data: BytesIO) -> str:
        """
        Decode the domain name that was provided when the object was initially created.

        :return: the decoded domain name as a str
        """
        string_builder: StringIO = StringIO()

        DomainNameDecoder._decode_domain_name_helper(reader, copy_of_data, string_builder)

        return string_builder.getvalue()[1:]  # we remove the first char, since it is an extra '.'.

    @staticmethod
    def _decode_domain_name_helper(reader: BytesIO, copy_of_data: BytesIO, string_builder: StringIO) -> None:
        """
        Helper function to decode domain names. (Used to allow for a mutually recursive solution).

        :return: None
        """
        label_length: bytes = reader.read(1)

        if label_length != b'\x00':
            if DomainNameDecoder._is_pointer(label_length):
                pointer: int = int.from_bytes(DomainNameDecoder._get_last_six_bits_of_pointer(label_length), 'big')
                pointer = pointer << 8
                pointer = pointer + int.from_bytes(reader.read(1), 'big')
                DomainNameDecoder._decode_pointer(pointer, copy_of_data, string_builder)
            else:
                DomainNameDecoder._decode_label(reader, copy_of_data, string_builder, int.from_bytes(label_length, 'big'))

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

    @staticmethod
    def _decode_pointer(pointer: int, copy_of_data: BytesIO, string_builder: StringIO):
        new_reader = BytesIO(copy_of_data.getvalue())
        new_reader.seek(pointer)  # set the new reader to point to the pointer specified location
        DomainNameDecoder._decode_domain_name_helper(new_reader, copy_of_data, string_builder)

    @staticmethod
    def _is_pointer(label_length: bytes) -> bool:
        """
        Returns true if the label_length byte is a pointer.
        :param label_length: The label_length byte from a dns encoded domain name
        :return: true if pointer, false otherwise
        """
        bitmask: int = int.from_bytes(b'\xc0', 'big')
        label_length_as_int: int = int.from_bytes(label_length, 'big')
        return (label_length_as_int & bitmask) == bitmask

    @staticmethod
    def _get_last_six_bits_of_pointer(label_length: bytes) -> bytes:
        bitmask: int = int.from_bytes(b'\x3f', 'big')
        label_length_as_int: int = int.from_bytes(label_length, 'big')
        return (label_length_as_int & bitmask).to_bytes(1, 'big')






