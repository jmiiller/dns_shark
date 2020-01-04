from src.DomainNameHandling import DomainNameDecoder
from io import BytesIO
from socket import inet_ntop, AF_INET, AF_INET6


class ResourceRecord():
    """
    Handles all logic pertaining to decoding and encoding Resource Records.
    """

    def __init__(self, data: BytesIO, copy_of_data: BytesIO):
        self.name: str = DomainNameDecoder.decode_domain_name(data, copy_of_data)
        self.type: int = int.from_bytes(data.read(2), 'big')
        self.response_class: int = int.from_bytes(data.read(2), 'big')
        self.ttl: int = int.from_bytes(data.read(4), 'big')
        self.rdlength: int = int.from_bytes(data.read(2), 'big')
        self.rdata: str = self._decode_rdata(BytesIO(data.read(self.rdlength)), copy_of_data)

    def _decode_rdata(self, rdata: BytesIO, copy_of_data: BytesIO) -> str:
        """
        Decode the rdata field to a string.

        :param rdata: the rdata of the resource record
        :param copy_of_data: a copy of the entire data of the dns message, used for handling pointers in domain names.
        :return: the decoded rdata field as a string
        """
        if self.type == 1:
            return ResourceRecord._decode_ipv4_address(rdata)
        elif self.type == 2:
            return DomainNameDecoder.decode_domain_name(rdata, copy_of_data)
        elif self.type == 5:
            return DomainNameDecoder.decode_domain_name(rdata, copy_of_data)
        elif self.type == 28:
            return ResourceRecord._decode_ipv6_address(rdata)
        else:
            return ''

    @staticmethod
    def _decode_ipv4_address(rdata: BytesIO) -> str:
        """
        Decode the rdata field to an ipv4 address.

        :param rdata: the rdata of the resource record
        :return: the rdata as an ipv4 address string
        """
        return inet_ntop(AF_INET, rdata.read(4))

    @staticmethod
    def _decode_ipv6_address(rdata: BytesIO) -> str:
        """
        Decode the rdata field to an ipv5 address.

        :param rdata: the redata of the resource record
        :return: the rdata as an ipv6 address string
        """
        return inet_ntop(AF_INET6, rdata.read(16))

    def print_record_for_trace(self):
        """
        Print a trace of the resource record.
        """
        print("      %-30s %-10d %-4s %s" % (self.name, self.ttl, ResourceRecord.parse_type(self.type), self.rdata))

    @staticmethod
    def parse_type(type: int) -> str:
        """
        Convert the resource record type to its appropriate string representation.
        :param type: the type value
        :return: the type value as a string.
        """
        if type == 1:
            return 'A'
        elif type == 2:
            return 'NS'
        elif type == 5:
            return 'CN'
        elif type == 28:
            return 'AAAA'
        else:
            return str(type)
