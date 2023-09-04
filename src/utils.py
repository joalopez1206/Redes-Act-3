from dnslib import DNSRecord
import socket

SIZE = 4096


def has_type_a_in_section_ans(parsed_answer: DNSRecord):
    print(f"parsed rr answers: {parsed_answer.rr}")
    return True


def send_dns_msg(sock_s: socket.socket, addr: tuple[str, int], msg: bytes):
    try:
        sock_s.sendto(msg, addr)
        data, _ = sock_s.recvfrom(4096)
    finally:
        sock_s.close()
    return data
