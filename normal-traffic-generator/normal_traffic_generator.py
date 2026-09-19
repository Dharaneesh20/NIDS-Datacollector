import argparse
import sys
import os
import time
import random
import yaml
import socket
import csv
from datetime import datetime, timezone

CONFIG_FILE = "config.yaml"
LOG_DIR = "logs"
CSV_LOG = os.path.join(LOG_DIR, "normal_traffic_log.csv")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"ERROR: Configuration file {CONFIG_FILE} not found.")
        sys.exit(1)
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)

config = load_config()
LAB_SUBNET = config.get("lab_subnet", "192.168.56.0/24")

def validate_lab_ip(ip: str) -> bool:
    import ipaddress
    try:
        ip_obj = ipaddress.ip_address(ip)
        subnet_obj = ipaddress.ip_network(LAB_SUBNET, strict=False)
        return ip_obj in subnet_obj
    except ValueError:
        return False

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('192.168.56.1', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_next_experiment_id():
    max_id = 0
    if os.path.exists(CSV_LOG):
        with open(CSV_LOG, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                exp_id = row.get("experiment_id", "")
                if exp_id.startswith("NORMAL-"):
                    try:
                        num = int(exp_id[7:])
                        if num > max_id:
                            max_id = num
                    except ValueError:
                        pass
    return f"NORMAL-{max_id + 1:06d}"

def log_activity(timestamp, exp_id, machine, src_ip, dst_ip, activity, dst_port, status):
    os.makedirs(LOG_DIR, exist_ok=True)
    file_exists = os.path.isfile(CSV_LOG)
    with open(CSV_LOG, 'a', newline='') as f:
        fieldnames = ['timestamp', 'experiment_id', 'source_machine', 'source_ip', 'destination_ip', 'activity', 'destination_port', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'timestamp': timestamp,
            'experiment_id': exp_id,
            'source_machine': machine,
            'source_ip': src_ip,
            'destination_ip': dst_ip,
            'activity': activity,
            'destination_port': dst_port,
            'status': status
        })

def main():
    parser = argparse.ArgumentParser(description="NIDS Lab Normal Traffic Generator")
    parser.add_argument("--target", help="Target IP address (defaults to config)")
    parser.add_argument("--machine", required=True, choices=["KALI", "MINT"], help="Machine identifier metadata")
    parser.add_argument("--duration", type=int, required=True, help="Total duration in seconds")
    parser.add_argument("--min-delay", type=float, help="Minimum delay between activities")
    parser.add_argument("--max-delay", type=float, help="Maximum delay between activities")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without executing traffic")
    
    args = parser.parse_args()

    target_ip = args.target if args.target else config.get("default_target", "192.168.56.129")
    
    if not validate_lab_ip(target_ip):
        print(f"ERROR: Target IP {target_ip} is strictly outside the authorized lab subnet {LAB_SUBNET}.")
        sys.exit(1)

    min_d = args.min_delay if args.min_delay else config.get("traffic", {}).get("min_delay", 2.0)
    max_d = args.max_delay if args.max_delay else config.get("traffic", {}).get("max_delay", 10.0)

    src_ip = get_local_ip()
    exp_id = get_next_experiment_id()

    print("=" * 56)
    print("NIDS LAB - NORMAL TRAFFIC GENERATOR")
    print("=" * 56)
    print(f"Experiment ID : {exp_id}")
    print(f"Machine       : {args.machine}")
    print(f"Source IP     : {src_ip}")
    print(f"Target        : {target_ip}")
    print(f"Lab Network   : {LAB_SUBNET}")
    print("\nStatus: RUNNING\n")

    # Load available activities
    activities = ["icmp", "tcp", "udp"]
    services_conf = config.get("services", {})
    if services_conf.get("http", {}).get("enabled"): activities.append("http")
    if services_conf.get("https", {}).get("enabled"): activities.append("https")
    if services_conf.get("ssh", {}).get("enabled"): activities.append("ssh")
    if services_conf.get("ftp", {}).get("enabled"): activities.append("ftp")
    if services_conf.get("telnet", {}).get("enabled"): activities.append("telnet")
    if services_conf.get("dns", {}).get("enabled"): activities.append("dns")

    import modules.icmp as icmp_mod
    import modules.tcp as tcp_mod
    import modules.udp as udp_mod
    import modules.http as http_mod
    import modules.https as https_mod
    import modules.ssh as ssh_mod
    import modules.ftp as ftp_mod
    import modules.telnet as telnet_mod
    import modules.dns as dns_mod

    mod_map = {
        "icmp": (icmp_mod, 0),
        "tcp": (tcp_mod, 80),
        "udp": (udp_mod, 53),
        "http": (http_mod, services_conf.get("http", {}).get("port", 80)),
        "https": (https_mod, services_conf.get("https", {}).get("port", 443)),
        "ssh": (ssh_mod, services_conf.get("ssh", {}).get("port", 22)),
        "ftp": (ftp_mod, services_conf.get("ftp", {}).get("port", 21)),
        "telnet": (telnet_mod, services_conf.get("telnet", {}).get("port", 23)),
        "dns": (dns_mod, services_conf.get("dns", {}).get("port", 53)),
    }

    start_time = time.time()
    end_time = start_time + args.duration

    total = 0
    success = 0
    failed = 0

    try:
        while time.time() < end_time:
            activity = random.choice(activities)
            mod, port = mod_map[activity]
            
            port_str = f":{port}" if port != 0 else ""
            print(f"[NORMAL] {activity.upper()} → {target_ip}{port_str}")
            
            status = "failed"
            ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            
            if args.dry_run:
                status = "dry-run"
                success += 1
            else:
                try:
                    result = mod.run(target_ip, config)
                    if result:
                        status = "success"
                        success += 1
                    else:
                        failed += 1
                except Exception as e:
                    failed += 1
            
            total += 1
            
            if not args.dry_run:
                log_activity(ts, exp_id, args.machine, src_ip, target_ip, activity.upper(), port, status)
            
            remaining = end_time - time.time()
            if remaining <= 0:
                break
                
            delay = random.uniform(min_d, max_d)
            delay = min(delay, remaining)
            print(f"Waiting {delay:.1f} seconds...\n")
            time.sleep(delay)
            
    except KeyboardInterrupt:
        print("\nAborted by user.")
        
    print("=" * 56)
    print("Experiment completed")
    print(f"Duration            : {int(time.time() - start_time)} seconds")
    print(f"Number of activities: {total}")
    print(f"Successful          : {success}")
    print(f"Failed              : {failed}")
    print(f"Log file location   : {os.path.abspath(CSV_LOG)}")

if __name__ == "__main__":
    main()
