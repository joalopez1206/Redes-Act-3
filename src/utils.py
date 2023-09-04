from dnslib import DNSRecord
import socket

SIZE = 4096


def has_type_a_in_section_ans(parsed_answer: DNSRecord):
    print(f"parsed rr answers: {parsed_answer.rr}")
    print(f"parsed rr authority: {parsed_answer.auth}")
    print(f"parsed rr header: {parsed_answer.header}")
    # print(f"parsed rr a : {parsed_answer.a}")
    # Todo: find a lambda that says if there is atleast one
    # any(map(lambda x: x.,parsed_answer.a))
    return parsed_answer.header.a > 0


def has_type_ns_in_section_auth(parsed_answer: DNSRecord):
    print(f"parsed ar {parsed_answer.ar}")
    return parsed_answer.header.ar > 0


def send_dns_request(addr: tuple[str, int], msg: bytes):
    sock_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock_s.sendto(msg, addr)
        data, _ = sock_s.recvfrom(4096)
    finally:
        sock_s.close()
    return data
