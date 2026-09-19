import subprocess
import sys
import time

def run(target: str, duration: int, config: dict):
    print(f"Running limited service enumeration (nmap -sV) against {target} for {duration} seconds...")
    start_time = time.time()
    
    while time.time() - start_time < duration:
        try:
            subprocess.run(
                ["nmap", "-sV", "-T4", "-F", target],
                check=True
            )
        except FileNotFoundError:
            print("ERROR: nmap is not installed. Service enumeration requires nmap.")
            sys.exit(1)
        except subprocess.CalledProcessError:
            print("ERROR: nmap execution failed.")
        time.sleep(2)
