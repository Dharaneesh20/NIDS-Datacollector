import subprocess

def run(target_ip: str, config: dict) -> bool:
    try:
        # Send a single ICMP echo request
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", target_ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False
