import time
import random
import socket
import urllib.request
import urllib.error
import subprocess
from tqdm import tqdm

def run(target: str, duration: int, config: dict):
    max_duration = config.get("limits", {}).get("max_duration", 60)
    duration = min(duration, max_duration)
    
    activities = ['dns', 'http', 'icmp', 'tcp', 'ssh']
    
    end_time = time.time() + duration
    
    with tqdm(total=duration, desc="Normal Traffic") as pbar:
        while time.time() < end_time:
            activity = random.choice(activities)
            
            try:
                if activity == 'dns':
                    # simulate dns to a known nameserver, or just simple socket gethostbyaddr if it was a real name
                    pass
                elif activity == 'http':
                    try:
                        urllib.request.urlopen(f"http://{target}/", timeout=1)
                    except Exception:
                        pass
                elif activity == 'icmp':
                    subprocess.run(["ping", "-c", "1", "-W", "1", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                elif activity == 'tcp':
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1)
                        s.connect_ex((target, 80))
                elif activity == 'ssh':
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1)
                        s.connect_ex((target, 22))
            except Exception:
                pass
            
            sleep_time = random.uniform(0.1, 1.0)
            time.sleep(sleep_time)
            
            remaining = int(end_time - time.time())
            pbar.update(duration - remaining - pbar.n)
            if pbar.n >= duration:
                break
