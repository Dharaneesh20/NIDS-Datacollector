import subprocess
import sys

def run(target: str, config: dict):
    print(f"Running limited service enumeration (nmap -sV) against {target}...")
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
