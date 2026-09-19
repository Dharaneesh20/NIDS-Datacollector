import socket
import time

def run(target: str, duration: int, config: dict):
    ports = [21, 22, 23, 25, 53, 80, 111, 139, 443, 445, 3306, 8080]
    
    print(f"Scanning target {target} on {len(ports)} common ports for {duration} seconds...")
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        for port in ports:
            if time.time() - start_time >= duration:
                break
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                s.connect_ex((target, port))
        time.sleep(0.5)
