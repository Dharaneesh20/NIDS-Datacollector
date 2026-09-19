import time
import sys
from tqdm import tqdm

def run(target: str, config: dict):
    try:
        import requests
    except ImportError:
        print("ERROR: requests library is required for web testing. Please install it.")
        sys.exit(1)
        
    # Benign but anomalous HTTP requests for web security testing
    payloads = [
        "/",
        "/admin",
        "/login.php",
        "/?id=1' OR '1'='1",
        "/../../../../etc/passwd",
        "/.git/config"
    ]
    
    print(f"Running Web security test against {target} ({len(payloads)} requests)")
    
    for path in tqdm(payloads, desc="Web Test"):
        url = f"http://{target}{path}"
        try:
            requests.get(url, timeout=2, headers={"User-Agent": "Lab-Web-Tester/1.0"})
        except requests.RequestException:
            pass
        time.sleep(1)
