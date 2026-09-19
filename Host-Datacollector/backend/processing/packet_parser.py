from scapy.all import Packet, IP, TCP, UDP, ICMP, Ether
import time
from typing import Dict, Any

def parse_packet(pkt: Packet) -> Dict[str, Any]:
    """Extracts required fields from a Scapy packet, returning None where inapplicable."""
    data = {
        "timestamp": float(pkt.time),
        "source_mac": None,
        "destination_mac": None,
        "source_ip": None,
        "destination_ip": None,
        "protocol": None,
        "source_port": None,
        "destination_port": None,
        "packet_length": len(pkt),
        "ip_ttl": None,
        "ip_header_length": None,
        "tcp_header_length": None,
        "tcp_flags": None,
        "udp_length": None,
        "icmp_type": None,
        "icmp_code": None
    }
    
    if Ether in pkt:
        data["source_mac"] = pkt[Ether].src
        data["destination_mac"] = pkt[Ether].dst
        
    if IP in pkt:
        data["source_ip"] = pkt[IP].src
        data["destination_ip"] = pkt[IP].dst
        data["ip_ttl"] = pkt[IP].ttl
        data["ip_header_length"] = pkt[IP].ihl * 4
        
        # Protocol logic
        if TCP in pkt:
            data["protocol"] = "TCP"
            data["source_port"] = pkt[TCP].sport
            data["destination_port"] = pkt[TCP].dport
            data["tcp_header_length"] = pkt[TCP].dataofs * 4
            data["tcp_flags"] = str(pkt[TCP].flags)
        elif UDP in pkt:
            data["protocol"] = "UDP"
            data["source_port"] = pkt[UDP].sport
            data["destination_port"] = pkt[UDP].dport
            data["udp_length"] = pkt[UDP].len
        elif ICMP in pkt:
            data["protocol"] = "ICMP"
            data["icmp_type"] = pkt[ICMP].type
            data["icmp_code"] = pkt[ICMP].code
        else:
            data["protocol"] = "OTHER"
            
    return data
