import urllib.request
import urllib.error

def run(target_ip: str, config: dict) -> bool:
    port = config.get("services", {}).get("http", {}).get("port", 80)
    url = f"http://{target_ip}:{port}/"
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            response.read(1024) # Read a small chunk
            return True
    except Exception:
        return False
