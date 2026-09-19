import socket

def run(target_ip: str, config: dict) -> bool:
    port = config.get("services", {}).get("telnet", {}).get("port", 23)
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3.0)
            s.connect((target_ip, port))
            
            # Read whatever banner telnet provides
            s.recv(1024)
            return True
    except Exception:
        return False
