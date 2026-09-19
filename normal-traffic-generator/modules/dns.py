import socket
import struct

def run(target_ip: str, config: dict) -> bool:
    port = config.get("services", {}).get("dns", {}).get("port", 53)
    
    # Simple DNS query packet for 'example.com' (A record)
    # Transaction ID: 0x1234
    # Flags: 0x0100 (Standard query)
    # Questions: 1
    # Answer RRs: 0, Authority RRs: 0, Additional RRs: 0
    # Query: \x07example\x03com\x00, Type A (0x0001), Class IN (0x0001)
    dns_query = b'\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01'
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(2.0)
            s.sendto(dns_query, (target_ip, port))
            # Just verify we can send, receiving a response is not strictly required if target doesn't run a DNS server
            try:
                s.recvfrom(1024)
            except Exception:
                pass
            return True
    except Exception:
        return False
