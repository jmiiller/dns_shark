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
        self.is_response: bool = DNSMessage._get_response_value_from_flags(flags)
        self.opcode: int = DNSMessage._get_opcode_value_from_flags(flags)
        self.authoritative: bool = DNSMessage._get_authoritative_value_from_flags(flags)
        self.is_truncated: bool = DNSMessage._get_is_truncated_from_flags(flags)
        self.recursion_desired: bool = DNSMessage._get_recursion_desired_from_flags(flags)
        self.recursion_available: bool = DNSMessage._get_recursion_available_from_flags(flags)
        self.rcode: int = DNSMessage._get_rcode_from_flags(flags)

        # retrieve counts from data
        self.question_count: int = int.from_bytes(data.read(2), 'big')
        self.answer_count: int = int.from_bytes(data.read(2), 'big')
        self.nameserver_count: int = int.from_bytes(data.read(2), 'big')
        self.additional_count: int = int.from_bytes(data.read(2), 'big')

        self.dns_questions: List[DNSQuestion] = DNSMessage._read_dns_questions(data, data, self.question_count)
        self.answer_records: List[ResourceRecord] = DNSMessage._read_resource_records(data, data, self.answer_count)
        self.name_server_records: List[ResourceRecord] = DNSMessage._read_resource_records(data, data, self.nameserver_count)
        self.additional_records: List[ResourceRecord] = DNSMessage._read_resource_records(data, data, self.additional_count)

    @staticmethod
    def _get_response_value_from_flags(flags: int) -> bool:
        """
        Retrieve the get_response value from flags.
        :param flags: an integer representing the flags of a dns message
        :return: value of the get_response field as bool
        """
        return (flags >> 15) == 1

    @staticmethod
    def _get_opcode_value_from_flags(flags: int) -> int:
        """
        Retrieve the opcode value from flags.
        :param flags: an integer representing the flags of a dns message
        :return: value of the opcode field as int
        """
        return (flags & int.from_bytes(b'\x00\x00\x78\x00', 'big')) >> 11

    @staticmethod
    def _get_authoritative_value_from_flags(flags: int) -> bool:
        """
        Retrieve the authoritative value from flags.
        :param flags: an integer representing the flags of a dns message
        :return: value of the authoritative field as bool
        """
        return ((flags & int.from_bytes(b'\x00\x00\x04\x00', 'big')) >> 10) == 1

    @staticmethod
    def _get_is_truncated_from_flags(flags: int) -> bool:
        """
        Retrieve the is_truncated value from flags.
        :param flags: an integer representing the flags of a dns message
        :return: value of the is_truncated field as bool
        """
        return ((flags & int.from_bytes(b'\x00\x00\x02\x00', 'big')) >> 9) == 1

    @staticmethod
    def _get_recursion_desired_from_flags(flags: int) -> bool:
        """
        Retrieve the recursion_desired value from flags.
        :param flags: an integer representing the flags of a dns message
        :return: value of the recursion_desired field as bool
        """
        return ((flags & int.from_bytes(b'\x00\x00\x01\x00', 'big')) >> 8) == 1

    @staticmethod
    def _get_recursion_available_from_flags(flags: int) -> bool:
        """
        Retrieve the recursion_available value from flags.
        :param flags: an integer representing the flags of a dns message
        :return: value of the recursion_available field as bool
        """
        return ((flags & int.from_bytes(b'\x00\x00\x00\x80', 'big')) >> 7) == 1

    @staticmethod
    def _get_rcode_from_flags(flags: int) -> int:
        """
        Retrieve the rcode value from flags.
        :param flags: an integer representing the flags of a dns message
        :return: value of the rcode field as int
        """
        return flags & int.from_bytes(b'\x00\x00\x00\x0f', 'big')

    @staticmethod
    def _read_dns_questions(data: BytesIO, copy_of_data: BytesIO, num_of_questions: int) -> List[DNSQuestion]:
        """
        Read the dns questions from the remaining dns message data.
        :param data: the remaining data of the dns message to be processed
        :param copy_of_data: a copy of the entire dns message, used for handling pointers in domain names
        :param num_of_questions: number of questions to decode
        :return: list of the dns questions decoded
        """
        list_of_questions = []
        for _ in range(num_of_questions):
            list_of_questions.append(DNSQuestion(data, copy_of_data))

        return list_of_questions

    @staticmethod
    def _read_resource_records(data: BytesIO, copy_of_data: BytesIO, num_of_records: int) -> List[ResourceRecord]:
        """
        Read the resource records from the remaining dns message data.
        :param data: the remaining data of the dns message to be processed
        :param copy_of_data: a copy of the entire dns message, used for handling pointers in domain names
        :param num_of_records: number of records to decode
        :return: list of the resource records decoded
        """
        list_of_records = []
        for _ in range(num_of_records):
            list_of_records.append(ResourceRecord(data, copy_of_data))

        return list_of_records

    def get_is_response(self) -> bool:
        return self.is_response

    def get_authoritative(self) -> bool:
        return self.authoritative

    def print_dns_question(self, dns_server_ip: str) -> None
        """
        Print a dns question/query to stdout.
        :param dns_server_ip: ip address of the dns server the domain name resolution request was sent to.
        :return: None
        """
        print('Query ID     ' + str(self.query_id) + ' ' + self.dns_questions[0].name + '  ' +
              ResourceRecord.parse_type(self.dns_questions[0].type) + ' --> ' + dns_server_ip)

    def print_message(self) -> None:
        """
        Print a dns message received from a dns server.
        :return: None
        """
        print('Response ID: ' + str(self.query_id) + ' Authoritative = ' + str(self.authoritative))

        print('  Answers (' + str(self.answer_count) + ')')
        DNSMessage.print_resource_records_trace(self.answer_records)

        print('  Name Servers (' + str(self.nameserver_count) + ')')
        DNSMessage.print_resource_records_trace(self.name_server_records)

        print('  Additional Information (' + str(self.additional_count) + ')')
        DNSMessage.print_resource_records_trace(self.additional_records)

    @staticmethod
    def print_resource_records_trace(records: List[ResourceRecord]) -> None:
        """
        Print a list of resource records.
        :param records: a list of resource records
        :return: None
        """
        for record in records:
            record.print_record_for_trace()