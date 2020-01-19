from dns_shark.domain_name_handling import DomainNameDecoder
from io import BytesIO
from socket import inet_ntop, AF_INET, AF_INET6


class ResourceRecord:
    """
    Handles all logic pertaining to decoding and encoding Resource Records.

    Instance Attributes:

        name: the name field of the resource record
        type: the type field of the resource record
        response_class: the class field of the resource record
        ttl: the ttl field of the resource record
        rdlength: the rdlength field of the resource record
        rdata: the rdata field of the resource record

        see https://tools.ietf.org/rfc/rfc1035.txt for more description on the meaning of these fields
    """

    def __init__(self, name: str, type: int, response_class: int, ttl: int, rdlength: int, rdata: str):
        self.name: str = name
        self.type: int = type
        self.response_class: int = response_class
        self.ttl: int = ttl
        self.rdlength: int = rdlength
        self.rdata: str = rdata

    def __eq__(self, other: object):
        if not isinstance(other, ResourceRecord):
            return False
        else:
            return self.name == other.name and \
                   self.type == other.type and \
                   self.response_class == other.response_class and \
                   self.ttl == other.ttl and \
                   self.rdlength == other.rdlength and \
                   self.rdata == other.rdata

    def __repr__(self):
        return 'ResourceRecord(name: ' + str(self.name) + ', type: ' + str(self.type) + ', class: ' + str(self.response_class) + \
               ', ttl: ' + str(self.ttl) + ', rdlength: ' + str(self.rdlength) + ', rdata: ' + str(self.rdata) + ')'

    @staticmethod
    def decode_resource_record(data: BytesIO, copy_of_message: BytesIO) -> 'ResourceRecord':
        """
        Factory method to decode a resource record from the provided data.

        :param data: the data to be decoded into a resource record.
        :param copy_of_message: a copy of the entire dns message to be decoded. Used for pointer handling.
        :return: a newly built resource record object, with fields decoded from the data.
        """
        name: str = DomainNameDecoder.decode_domain_name(data, copy_of_message)
        type: int = int.from_bytes(data.read(2), 'big')
        response_class: int = int.from_bytes(data.read(2), 'big')
        ttl: int = int.from_bytes(data.read(4), 'big')
        rdlength: int = int.from_bytes(data.read(2), 'big')
        rdata: str = ResourceRecord._decode_rdata(BytesIO(data.read(rdlength)), copy_of_message, type)

        return ResourceRecord(name, type, response_class, ttl, rdlength, rdata)

    @staticmethod
    def _decode_rdata(rdata: BytesIO, copy_of_message: BytesIO, record_type: int) -> str:
        """
        Decode the rdata field to a string.

        :param rdata: the rdata of the resource record
        :param copy_of_message: a copy of the entire data of the dns message, used for handling pointers in domain names.
        :param record_type: the type of the resource record.
        :return: the decoded rdata field as a string
        """
        if record_type == 1:
            return ResourceRecord._decode_ipv4_address(rdata)
        elif record_type == 2:
            return DomainNameDecoder.decode_domain_name(rdata, copy_of_message)
        elif record_type == 5:
            return DomainNameDecoder.decode_domain_name(rdata, copy_of_message)
        elif record_type == 28:
            return ResourceRecord._decode_ipv6_address(rdata)
        else:
            return 'UNSUPPORTED RESOURCE RECORD TYPE'

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
        Decode the rdata field to an ipv6 address.

        :param rdata: the redata of the resource record
        :return: the rdata as an ipv6 address string
        """
        return inet_ntop(AF_INET6, rdata.read(16))

    def print_record_for_trace(self) -> None:
        """
        Print a trace of the resource record.

        Used for printing the trace of a dns name resolution process.

        :return: None
        """
        print("      %-30s %-10d %-4s %s" % (self.name, self.ttl, ResourceRecord.parse_type(self.type), self.rdata))

    def print_record_with_supplied_domain_name(self, domain_name: str) -> None:
        """
        Print a record with the supplied domain name as the first thing printed.

        Used for printing the answers to the resolution.

        :param domain_name: the domain name to be printed
        :return: None
        """
        print("  %s %d   %s %s" % (domain_name, self.ttl, ResourceRecord.parse_type(self.type), self.rdata))

    @staticmethod
    def parse_type(given_type: int) -> str:
        """
        Convert the resource record type to its appropriate string representation.

        :param given_type: the type value
        :return: the type value as a string.
        """
        if given_type == 1:
            return 'A'
        elif given_type == 2:
            return 'NS'
        elif given_type == 5:
            return 'CN'
        elif given_type == 28:
            return 'AAAA'
        else:
            return str(given_type)
