from dnslib import DNSRecord
import dnslib
import socket

SIZE = 4096

def has_type_a_in_section_ans(parsed_answer: DNSRecord):
    if parsed_answer.header.a > 1:
        return parsed_answer.header.a > 0 and any(map(lambda x: x.rtype == dnslib.QTYPE.A, parsed_answer.a))
    elif parsed_answer.header.a == 1:
        return parsed_answer.a.rtype == dnslib.QTYPE.A
    else:
        return False

def has_type_ns_in_section_auth(parsed_answer: DNSRecord):
    return parsed_answer.header.auth > 0 and any(map(lambda x: x.rtype == dnslib.QTYPE.NS, parsed_answer.auth))


def has_type_a_in_section_add(parsed_answer: DNSRecord):
    return parsed_answer.header.ar > 0 and any(map(lambda x: x.rtype == dnslib.QTYPE.A, parsed_answer.ar))


def send_dns_request(addr: tuple[str, int], msg: bytes):
    sock_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock_s.sendto(msg, addr)
        data, _ = sock_s.recvfrom(4096)
    finally:
        sock_s.close()
    return data
