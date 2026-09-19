import time
import sys

def run(target: str, duration: int, config: dict):
    print(f"Running SSH authentication test against {target} for {duration} seconds...")
    
    try:
        import paramiko
    except ImportError:
        print("ERROR: paramiko is required for SSH testing. Please install it.")
        sys.exit(1)
        
    usernames = ["root", "admin", "user", "test"]
    passwords = ["123456", "password", "admin", "root"]
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        for user in usernames:
            for password in passwords:
                if time.time() - start_time >= duration:
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
                
                time.sleep(1) # delay between attempts
