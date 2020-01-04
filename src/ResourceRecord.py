from src.DomainNameHandling import DomainNameDecoder
from io import BytesIO
from socket import inet_ntop, AF_INET, AF_INET6

class ResourceRecord():
    """
    Handles all logic pertaining to decoding and encoding Resource Records
    """

    def __init__(self, data: BytesIO, copy_of_data: BytesIO):
        self.name: str = DomainNameDecoder.decode_domain_name(data, copy_of_data)
        self.type: int = int.from_bytes(data.read(2), 'big')
        self.response_class: int = int.from_bytes(data.read(2), 'big')
        self.ttl: int = int.from_bytes(data.read(4), 'big')
        self.rdlength: int = int.from_bytes(data.read(2), 'big')
        self.rdata: str = self._decode_rdata(BytesIO(data.read(self.rdlength)), copy_of_data)

    def _decode_rdata(self, data: BytesIO, copy_of_data: BytesIO):
        if self.type == 1:
            return ResourceRecord._decode_ipv4_address(data)
        elif self.type == 2:
            return DomainNameDecoder.decode_domain_name(data, copy_of_data)
        elif self.type == 5:
            return DomainNameDecoder.decode_domain_name(data, copy_of_data)
        elif self.type == 28:
            return ResourceRecord._decode_ipv6_address(data)
        else:
            return ''

    @staticmethod
    def _decode_ipv4_address(data: BytesIO) -> str:
        return inet_ntop(AF_INET, data.read(4))

    @staticmethod
    def _decode_ipv6_address(data: BytesIO) -> str:
        return inet_ntop(AF_INET6, data.read(16))
