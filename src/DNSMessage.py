from src.DNSQuestion import DNSQuestion  # type: ignore
from src.ResourceRecord import ResourceRecord  # type: ignore
from typing import List, Optional
from io import BytesIO


class DNSMessage:
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
        self.is_truncated: bool = DNSMessage._get_is_truncated_value_from_flags(flags)
        self.recursion_desired: bool = DNSMessage._get_recursion_desired_value_from_flags(flags)
        self.recursion_available: bool = DNSMessage._get_recursion_available_value_from_flags(flags)
        self.rcode: int = DNSMessage._get_rcode_value_from_flags(flags)

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
    def _get_is_truncated_value_from_flags(flags: int) -> bool:
        """
        Retrieve the is_truncated value from flags.

        :param flags: an integer representing the flags of a dns message
        :return: value of the is_truncated field as bool
        """
        return ((flags & int.from_bytes(b'\x00\x00\x02\x00', 'big')) >> 9) == 1

    @staticmethod
    def _get_recursion_desired_value_from_flags(flags: int) -> bool:
        """
        Retrieve the recursion_desired value from flags.

        :param flags: an integer representing the flags of a dns message
        :return: value of the recursion_desired field as bool
        """
        return ((flags & int.from_bytes(b'\x00\x00\x01\x00', 'big')) >> 8) == 1

    @staticmethod
    def _get_recursion_available_value_from_flags(flags: int) -> bool:
        """
        Retrieve the recursion_available value from flags.

        :param flags: an integer representing the flags of a dns message
        :return: value of the recursion_available field as bool
        """
        return ((flags & int.from_bytes(b'\x00\x00\x00\x80', 'big')) >> 7) == 1

    @staticmethod
    def _get_rcode_value_from_flags(flags: int) -> int:
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

    def print_dns_question(self, dns_server_ip: str) -> None:
        """
        Print a dns query message.

        This includes printing the query id, domain name being asked for by the dns query,
        the type of record being asked for, and the dns server that is being queried.

        :param dns_server_ip: ip address of the dns server the domain name resolution request was sent to.
        :return: None
        """
        print('Query ID:    ' + str(self.query_id) + ' ' + self.dns_questions[0].name + '  ' +
              ResourceRecord.parse_type(self.dns_questions[0].type) + ' --> ' + dns_server_ip)

    def print_dns_response(self) -> None:
        """
        Print a dns response message.

        This includes printing the response id, answer records, name server records, additional records,
        and authoritative value of a dns message.

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

    def get_answer_records_that_match_domain_name_and_type(self, domain_name: str, type: int) -> List[ResourceRecord]:
        """
        Retrieves the answer resource records that contain the supplied domain name and record type.

        :param domain_name: the domain name used to select from the answer resource records
        :param type: the record type used to select from the answer resource records
        :return:
        """
        results = []

        for record in self.answer_records:
            if record.name.lower() == domain_name.lower() and record.type == type:
                results.append(record)

        return results

    def get_name_server_ip_address(self) -> Optional[str]:
        """
        Retrieves the first available name server ip address.

        :return: the name server ip address as a string, if present. Otherwise, return None.
        """
        for name_server_record in self.name_server_records:
            name_server_ip: Optional[str] = self.get_name_server_ip_address_from_matching_additional_record(name_server_record)

            if name_server_ip:
                return name_server_ip

        return None

    def get_name_server_ip_address_from_matching_additional_record(self, name_server_record: ResourceRecord) -> Optional[str]:
        """
        Given a name server resource record, search the additional records for a corresponding ip address.

        :param name_server_record: the name server record whose ip address is being searched for
        :return: the name server ip address, if present. Otherwise, return None.
        """
        for additional_record in self.additional_records:
            if additional_record.name.lower() == name_server_record.rdata.lower() and additional_record.type == 1:
                return additional_record.rdata

        return None
