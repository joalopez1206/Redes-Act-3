import socket
from dnslib import DNSRecord
import dnslib
from dns_parse_mod import parse_dns_message
from utils import (send_dns_request, has_type_a_in_section_ans, SIZE,
                   has_type_ns_in_section_auth,
                   has_type_a_in_section_add)

import logging

logging.basicConfig(format="%(levelname)s-%(message)s", level=logging.DEBUG)
ROOT_SV = ("192.33.4.12", 53)
local_addr = ('localhost', 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local_addr)


def resolver(consulta: bytes, loc_addr=ROOT_SV):
    # Enviamos la query al servidor raiz y esperamos la consulta
    logging.debug(f"Preguntando por la consulta: {consulta}")
    answer: bytes = send_dns_request(loc_addr, consulta)

    # Parseamos la respuesta
    parsed_answer = parse_dns_message(answer)
    logging.debug(f"Respuesta en formato de dig\n {parsed_answer}")

    if has_type_a_in_section_ans(parsed_answer):
        return answer
    logging.debug("la respuesta no tiene tipo A en seccion answers")

    if has_type_ns_in_section_auth(parsed_answer):

        if has_type_a_in_section_add(parsed_answer):

            #gets the ip for the rquest
            addr = (str(parsed_answer.ar[0].rdata), 53)
            logging.debug(f"la direccion es: {addr}")
            return resolver(consulta, loc_addr=addr)

        # else:
        #     query_name = get_name_ns(parsed_answer)
        #     consulta_ns = DNSRecord.question(query_name)
        #     answer_ns = resolver(consulta_ns) #<<- habemus ip
        #     parse_dns_message(answer_ns)
        #     addrs = get_addrs_from_answer(parsed_answer_ns)
        #     return resolver(consulta, loc_addr=addrs)
    return answer

while True:
    data, a = sock.recvfrom(SIZE)
    reply = resolver(data)
    sock.sendto(reply, a)
