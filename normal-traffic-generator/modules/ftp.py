import socket

def run(target_ip: str, config: dict) -> bool:
    port = config.get("services", {}).get("ftp", {}).get("port", 21)
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3.0)
            s.connect((target_ip, port))
            # Read the FTP greeting banner
            banner = s.recv(1024)
            
            # Optionally send a benign QUIT command
            s.sendall(b"QUIT\r\n")
            
            return len(banner) > 0
    except Exception:
        return False
