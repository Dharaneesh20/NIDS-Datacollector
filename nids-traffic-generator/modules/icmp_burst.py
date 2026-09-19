import subprocess
import sys
import time

def run(target: str, duration: int, rate: int, config: dict):
    max_duration = config.get("limits", {}).get("max_duration", 60)
    max_rate = config.get("limits", {}).get("max_rate", 20)
    
    duration = min(duration, max_duration)
    rate = min(rate, max_rate)
    
    count = duration * rate
    interval = 1.0 / rate if rate > 0 else 1.0

    print(f"Generating ICMP burst to {target} (rate: {rate}/s, duration: {duration}s, total: {count})")
    
    # We can use ping with interval or subprocess in a loop
    # For better control and visibility with tqdm, we do it in a loop
    from tqdm import tqdm
    for _ in tqdm(range(count), desc="ICMP Burst"):
        subprocess.run(["ping", "-c", "1", "-W", "1", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(interval)
