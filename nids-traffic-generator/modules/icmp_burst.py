import subprocess
import time

def run(target: str, duration: int, rate: int, config: dict):
    interval = 1.0 / rate if rate > 0 else 1.0
    print(f"Generating ICMP burst to {target} for {duration} seconds (rate: {rate}/s)")
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        subprocess.run(["ping", "-c", "1", "-W", "1", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(interval)
