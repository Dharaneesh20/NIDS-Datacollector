import socket
from tqdm import tqdm

def run(target: str, config: dict):
    # Use python socket to perform a basic connect scan on limited lab-only port range
    ports = [21, 22, 23, 25, 53, 80, 111, 139, 443, 445, 3306, 8080]
    
    print(f"Scanning target {target} on {len(ports)} common ports...")
    
    for port in tqdm(ports, desc="Port Scanning"):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect_ex((target, port))
