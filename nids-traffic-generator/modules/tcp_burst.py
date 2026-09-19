import socket
import time
from tqdm import tqdm

def run(target: str, duration: int, rate: int, config: dict):
    max_conn = config.get("limits", {}).get("max_tcp_connections", 100)
    
    # Calculate connections based on duration and rate
    total_connections = min(duration * rate, max_conn)
    interval = 1.0 / rate if rate > 0 else 1.0
    
    target_port = 80 # default to HTTP port for burst
    
    print(f"Generating TCP connection burst to {target}:{target_port} (total: {total_connections})")
    
    for _ in tqdm(range(total_connections), desc="TCP Burst"):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                s.connect_ex((target, target_port))
        except Exception:
            pass
        time.sleep(interval)
