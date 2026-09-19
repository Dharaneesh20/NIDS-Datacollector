import time
import sys

def run(target: str, duration: int, config: dict):
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
    
    print(f"Running Web security test against {target} for {duration} seconds...")
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        for path in payloads:
            if time.time() - start_time >= duration:
                break
            url = f"http://{target}{path}"
            try:
                requests.get(url, timeout=2, headers={"User-Agent": "Lab-Web-Tester/1.0"})
            except requests.RequestException:
                pass
            time.sleep(1)
