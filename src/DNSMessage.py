from src.DNSQuestion import DNSQuestion
from src.ResourceRecord import ResourceRecord
from typing import List
from io import BytesIO


class DNSMessage():
    """
    Handles all logic pertaining to decoding and encoding DNS Messages.
    """

    def __init__(self, data: BytesIO):
        self.query_id: int = int.from_bytes(data.read(2), 'big')

        # retrieve flag values from data
        flags: int = int.from_bytes(data.read(2), 'big')
        self.is_response: bool = DNSMessage.get_response_value_from_flags(flags)
        self.opcode: int = DNSMessage.get_opcode_value_from_flags(flags)
        self.authoritative: bool = DNSMessage.get_authoritative_value_from_flags(flags)
        self.is_truncated: bool = DNSMessage.get_is_truncated_from_flags(flags)
        self.recursion_desired: bool = DNSMessage.get_recursion_desired_from_flags(flags)
        self.recursion_available: bool = DNSMessage.get_recursion_available_from_flags(flags)
        self.rcode: int = DNSMessage.get_rcode_from_flags(flags)

        # retrieve counts from data
        self.question_count: int = int.from_bytes(data.read(2), 'big')
        self.answer_count: int = int.from_bytes(data.read(2), 'big')
        self.nameserver_count: int = int.from_bytes(data.read(2), 'big')
        self.additional_count: int = int.from_bytes(data.read(2), 'big')

        self.dns_questions: List[DNSQuestion] = DNSMessage.read_dns_questions(data, data, self.question_count)
        self.answer_records: List[ResourceRecord] = DNSMessage.read_resource_records(data, data, self.answer_count)
        self.name_server_records: List[ResourceRecord] = DNSMessage.read_resource_records(data, data, self.nameserver_count)
        self.additional_records: List[ResourceRecord] = DNSMessage.read_resource_records(data, data, self.additional_count)

    @staticmethod
    def get_response_value_from_flags(flags: int) -> bool:
        return (flags >> 15) == 1

    @staticmethod
    def get_opcode_value_from_flags(flags: int) -> int:
        return (flags & int.from_bytes(b'\x00\x00\x78\x00', 'big')) >> 11

    @staticmethod
    def get_authoritative_value_from_flags(flags: int) -> bool:
        return ((flags & int.from_bytes(b'\x00\x00\x04\x00', 'big')) >> 10) == 1

    @staticmethod
    def get_is_truncated_from_flags(flags: int) -> bool:
        return ((flags & int.from_bytes(b'\x00\x00\x02\x00', 'big')) >> 9) == 1

    @staticmethod
    def get_recursion_desired_from_flags(flags: int) -> bool:
        return ((flags & int.from_bytes(b'\x00\x00\x01\x00', 'big')) >> 8) == 1

    @staticmethod
    def get_recursion_available_from_flags(flags: int) -> bool:
        return ((flags & int.from_bytes(b'\x00\x00\x00\x80', 'big')) >> 7) == 1

    @staticmethod
    def get_rcode_from_flags(flags: int) -> int:
        return flags & int.from_bytes(b'\x00\x00\x00\x0f', 'big')

    @staticmethod
    def read_dns_questions(data: BytesIO, copy_of_data: BytesIO, num_of_questions: int) -> List[DNSQuestion]:
        list_of_questions = []
        for _ in range(num_of_questions):
            list_of_questions.append(DNSQuestion(data, copy_of_data))

        return list_of_questions

    @staticmethod
    def read_resource_records(data: BytesIO, copy_of_data: BytesIO, num_of_records: int) -> List[ResourceRecord]:
        list_of_records = []
        for _ in range(num_of_records):
            list_of_records.append(ResourceRecord(data, copy_of_data))

        return list_of_records

    def get_is_response(self):
        return self.is_response

    def get_authoritative(self):
        return self.authoritative
