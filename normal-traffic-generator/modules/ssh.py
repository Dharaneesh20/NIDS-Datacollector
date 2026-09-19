import socket

def run(target_ip: str, config: dict) -> bool:
    port = config.get("services", {}).get("ssh", {}).get("port", 22)
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3.0)
            s.connect((target_ip, port))
            # Wait for and read the SSH banner
            banner = s.recv(1024)
            return len(banner) > 0
    except Exception:
        return False
