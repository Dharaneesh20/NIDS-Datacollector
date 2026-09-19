import time
import sys
from tqdm import tqdm

def run(target: str, config: dict):
    max_attempts = config.get("limits", {}).get("max_ssh_attempts", 10)
    
    print(f"Running SSH authentication test against {target} (max {max_attempts} attempts)")
    
    try:
        import paramiko
    except ImportError:
        print("ERROR: paramiko is required for SSH testing. Please install it.")
        sys.exit(1)
        
    usernames = ["root", "admin", "user", "test"]
    passwords = ["123456", "password", "admin", "root"]
    
    attempts = 0
    with tqdm(total=max_attempts, desc="SSH Auth Test") as pbar:
        for user in usernames:
            for password in passwords:
                if attempts >= max_attempts:
                    break
                    
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    # Intentionally fail auth
                    client.connect(target, port=22, username=user, password=password, timeout=2)
                except paramiko.AuthenticationException:
                    pass
                except Exception:
                    pass
                finally:
                    client.close()
                
                attempts += 1
                pbar.update(1)
                time.sleep(1) # delay between attempts
