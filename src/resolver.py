import socket
from dnslib import DNSRecord, QTYPE, A
from dnslib import RR
from dns_parse_mod import parse_dns_message
from utils import (send_dns_request, has_type_a_in_section_ans, SIZE,
                   has_type_ns_in_section_auth,
                   has_type_a_in_section_add)

import logging

logging.basicConfig(format="(debug) :: %(message)s", level=logging.DEBUG)
ROOT_SV = ("192.33.4.12", 53)
local_addr = ('localhost', 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local_addr)
cache = {}


def resolver(consulta: bytes, loc_addr=ROOT_SV, loc_qname='.'):
    # Vemos el cache!
    query_name = parse_dns_message(consulta).q.qname
    if query_name in cache:
        logging.debug("Se uso el cache!")
        dns_query = parse_dns_message(consulta)
        ip_answer = cache[query_name]
        dns_query.add_answer(*RR.fromZone("{} A {}".format(query_name, ip_answer)))
        return dns_query.pack()
    # Si no
    # Enviamos la query al servidor raiz y esperamos la consulta
    answer: bytes = send_dns_request(loc_addr, consulta)

    # Parseamos la respuesta
    parsed_answer = parse_dns_message(answer)
    logging.debug(f"Consultando '{parsed_answer.q.qname}' a '{loc_qname}' con direccion IP {loc_addr[0]} ")

    if has_type_a_in_section_ans(parsed_answer):
        cache[query_name] = parsed_answer.get_a().rdata
        return answer

    if has_type_ns_in_section_auth(parsed_answer):

        if has_type_a_in_section_add(parsed_answer):

            # gets the ip for the rquest
            addr = (str(parsed_answer.ar[0].rdata), 53)
            return resolver(consulta, loc_addr=addr, loc_qname=parsed_answer.ar[0].rname)

        else:
            if type(parsed_answer.auth) == list:
                query_name = str(parsed_answer.auth[0].rdata)
            else:
                query_name = str(parsed_answer.auth.rdata)

            consulta_ns = DNSRecord.question(query_name)

            answer_ns = resolver(consulta_ns.pack())  # <<- habemus ip

            parsed_answer_ns = parse_dns_message(answer_ns)
            if type(parsed_answer_ns.a) == list:
                addrs = (str(parsed_answer_ns.a[0].rdata), 53)
            else:
                addrs = (str(parsed_answer_ns.a.rdata), 53)

            return resolver(consulta, loc_addr=addrs, loc_qname=query_name)

    return answer


while True:
    data, a = sock.recvfrom(SIZE)
    reply = resolver(data)
    sock.sendto(reply, a)
