import urllib.request
import urllib.error
import ssl

def run(target_ip: str, config: dict) -> bool:
    port = config.get("services", {}).get("https", {}).get("port", 443)
    url = f"https://{target_ip}:{port}/"
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    # Ignore self-signed certs in lab
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, timeout=3, context=ctx) as response:
            response.read(1024)
            return True
    except Exception:
        return False
