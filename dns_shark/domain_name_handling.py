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
    def decode_domain_name(data: BytesIO, copy_of_message: BytesIO) -> str:
        """
        Decode the domain name that was provided when the object was initially created.

        :param data: the remaining data to be decoded of the dns message, the domain name should be at the start
        :param copy_of_message: a copy of the entire dns message, used for handling pointers in domain names.
        :return: the decoded domain name as a str
        """
        string_builder: StringIO = StringIO()

        DomainNameDecoder._decode_domain_name_helper(data, copy_of_message, string_builder)

        return string_builder.getvalue()[1:]  # we remove the first char, since it is an extra '.'.

    @staticmethod
    def _decode_domain_name_helper(data: BytesIO, copy_of_message: BytesIO, string_builder: StringIO) -> None:
        """
        Helper function to decode domain names. (Used to allow for a mutually recursive solution).

        :param data: the remaining data to be decoded of the dns message, the domain name should be at the start
        :param copy_of_message: a copy of the entire dns message, used for handling pointers in domain names.
        :param string_builder: the currently decoded domain name
        :return: None
        """
        label_length: bytes = data.read(1)

        if label_length != b'\x00':
            if DomainNameDecoder._is_pointer(label_length):
                pointer: int = int.from_bytes(DomainNameDecoder._get_last_six_bits_of_pointer(label_length), 'big')
                pointer = pointer << 8
                pointer = pointer + int.from_bytes(data.read(1), 'big')
                DomainNameDecoder._decode_pointer(pointer, copy_of_message, string_builder)
            else:
                DomainNameDecoder._decode_label(data, copy_of_message, string_builder, int.from_bytes(label_length, 'big'))

    @staticmethod
    def _decode_label(data: BytesIO, copy_of_message: BytesIO, string_builder: StringIO, label_length: int) -> None:
        """
        Decodes a single label of a encoded domain name.

        :param data: the remaining data to be decoded of the dns message, the domain name should be at the start
        :param copy_of_message: a copy of the entire dns message, used for handling pointers in domain names.
        :param string_builder: the currently decoded domain name
        :param label_length: the length of the label to be decoded
        :return: None
        """
        string_builder.write('.')

        for _ in range(label_length):
            char: str = data.read(1).decode('ascii')
            string_builder.write(char)

        DomainNameDecoder._decode_domain_name_helper(data, copy_of_message, string_builder)

    @staticmethod
    def _decode_pointer(pointer: int, copy_of_message: BytesIO, string_builder: StringIO) -> None:
        """
        Decodes a pointer in a domain name.

        :param pointer: the pointer value
        :param copy_of_message: a copy of the entire dns message, used for handling pointers in domain names.
        :param string_builder: the currently decoded domain name string
        :return: None
        """
        new_data = BytesIO(copy_of_message.getvalue())
        new_data.seek(pointer)  # set the new data to point to the pointer specified location
        DomainNameDecoder._decode_domain_name_helper(new_data, copy_of_message, string_builder)

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
        """
        Retrieves the last six bits of the label_length bytes, to be used in decoding the pointer.

        :param label_length: the label_length bytes that contain the pointer.
        :return: the last six bits of the label_length bytes
        """
        bitmask: int = int.from_bytes(b'\x3f', 'big')
        label_length_as_int: int = int.from_bytes(label_length, 'big')
        return (label_length_as_int & bitmask).to_bytes(1, 'big')






