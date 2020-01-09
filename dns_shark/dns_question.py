from io import BytesIO
from dns_shark.domain_name_handling import DomainNameDecoder


class DNSQuestion:
    """
    Handles all logic pertaining to decoding and encoding DNS Questions
    """

    def __init__(self, name: str, type: int, response_class: int):
        self.name: str = name
        self.type: int = type
        self.response_class: int = response_class

    @staticmethod
    def decode_dns_question(data: BytesIO, copy_of_message: BytesIO) -> 'DNSQuestion':
        name: str = DomainNameDecoder.decode_domain_name(data, copy_of_message)
        type: int = int.from_bytes(data.read(2), 'big')
        response_class: int = int.from_bytes(data.read(2), 'big')

        return DNSQuestion(name, type, response_class)