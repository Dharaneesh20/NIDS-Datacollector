import socket
import time

def run(target: str, duration: int, rate: int, config: dict):
    interval = 1.0 / rate if rate > 0 else 1.0
    target_port = 80 # default to HTTP port for burst
    
    print(f"Generating TCP connection burst to {target}:{target_port} for {duration} seconds (rate: {rate}/s)")
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                s.connect_ex((target, target_port))
        except Exception:
            pass
        time.sleep(interval)
