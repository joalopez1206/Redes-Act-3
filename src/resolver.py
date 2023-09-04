import socket
import dnslib
from dns_parse_mod import parse_dns_message
from utils import send_dns_request, has_type_a_in_section_ans, SIZE, has_type_ns_in_section_auth

ROOT_SV = ("192.33.4.12", 53)
local_addr = ('localhost', 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local_addr)


def resolver(consulta: bytes, loc_addr=ROOT_SV):
    # Enviamos la query al servidor raiz y esperamos la consulta
    answer: bytes = send_dns_request(loc_addr, consulta)
    # Parseamos la respuesta
    parsed_answer = parse_dns_message(answer)
    print(parsed_answer.header)
    if has_type_a_in_section_ans(parsed_answer):
        return answer
    if has_type_ns_in_section_auth(parsed_answer):
        first_ip: dnslib.dns.RR = parsed_answer.ar[0]
        return resolver(consulta, loc_addr=(first_ip, 53))
    return answer

while True:
    data, a = sock.recvfrom(SIZE)
    reply = resolver(data)
    sock.sendto(reply, a)
