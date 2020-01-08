from io import BytesIO
from src.DomainNameHandling import DomainNameDecoder  # type: ignore


class DNSQuestion:
    """
    Handles all logic pertaining to decoding and encoding DNS Questions
    """

    def __init__(self, data: BytesIO, copy_of_data: BytesIO):
        self.name: str = DomainNameDecoder.decode_domain_name(data, copy_of_data)
        self.type: int = int.from_bytes(data.read(2), 'big')
        self.response_class: int = int.from_bytes(data.read(2), 'big')