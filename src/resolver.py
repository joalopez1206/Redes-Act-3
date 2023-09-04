import socket
from dns_parse_mod import parse_dns_message
from utils import send_dns_msg, has_type_a_in_section_ans, SIZE

ROOT_SV = ("192.33.4.12", 53)
local_addr = ('localhost', 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local_addr)


def resolver(consulta: bytes, loc_addr=ROOT_SV):
    # Enviamos la query al servidor raiz y esperamos la consulta
    answer: bytes = send_dns_msg(sock, loc_addr, consulta)
    # Parseamos la respuesta
    parsed_answer = parse_dns_message(answer)
    if has_type_a_in_section_ans(parsed_answer):
        return answer


while True:
    data, a = sock.recvfrom(SIZE)
    reply = resolver(data)
    sock.sendto(reply, a)
