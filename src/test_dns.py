import socket
from dnslib import DNSRecord


def send_dns_msg(addrs, port):
    qname = "example.com"
    q = DNSRecord.question(qname)
    sv_addr = (addrs, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(bytes(q.pack()), sv_addr)
        data, _ = sock.recvfrom(4096)
        d = DNSRecord.parse(data)
    finally:
        sock.close()
    return d


if __name__ == "__main__":
    print(send_dns_msg("8.8.8.8", 53))
