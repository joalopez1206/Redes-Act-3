from dnslib import DNSRecord


def parse_dns_message(encoded_msg: bytes) -> DNSRecord:
    return DNSRecord.parse(encoded_msg)

