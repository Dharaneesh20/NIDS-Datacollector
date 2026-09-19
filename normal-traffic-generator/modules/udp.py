import socket

def run(target_ip: str, config: dict) -> bool:
    port = 53 # DNS port typically accepts UDP, or use an echo port
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(2.0)
            # Send a benign tiny UDP payload
            s.sendto(b"HELLO", (target_ip, port))
            return True
    except Exception:
        return False
