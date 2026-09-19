import socket

def run(target_ip: str, config: dict) -> bool:
    # We will pick a common port to test a basic TCP handshake and teardown
    port = 80
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3.0)
            s.connect((target_ip, port))
            return True
    except Exception:
        return False
