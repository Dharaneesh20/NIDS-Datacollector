import ipaddress
import yaml
import sys
import argparse
import os
import csv
import json
import time
from datetime import datetime
from tqdm import tqdm

CONFIG_FILE = "config.yaml"
LOG_DIR = "logs"
CSV_LOG = os.path.join(LOG_DIR, "experiments.csv")
JSONL_LOG = os.path.join(LOG_DIR, "experiments.jsonl")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"ERROR: Configuration file {CONFIG_FILE} not found.")
        sys.exit(1)
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)

config = load_config()
LAB_SUBNET = config.get("lab_subnet", "192.168.56.0/24")

def validate_lab_ip(ip: str) -> bool:
    try:
        ip_obj = ipaddress.ip_address(ip)
        subnet_obj = ipaddress.ip_network(LAB_SUBNET, strict=False)
        return ip_obj in subnet_obj
    except ValueError:
        return False

def validate_target(ip: str):
    if not validate_lab_ip(ip):
        print("ERROR: Target is outside the authorized isolated lab network.")
        sys.exit(1)

def get_next_experiment_id():
    max_id = 0
    if os.path.exists(CSV_LOG):
        with open(CSV_LOG, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                exp_id = row.get("experiment_id", "")
                if exp_id.startswith("EXP-"):
                    try:
                        num = int(exp_id[4:])
                        if num > max_id:
                            max_id = num
                    except ValueError:
                        pass
    return f"EXP-{max_id + 1:06d}"

def log_experiment(exp_data):
    # Ensure log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Write JSONL
    with open(JSONL_LOG, 'a') as f:
        f.write(json.dumps(exp_data) + '\n')
    
    # Write CSV
    file_exists = os.path.isfile(CSV_LOG)
    with open(CSV_LOG, 'a', newline='') as f:
        fieldnames = ['experiment_id', 'start_time', 'end_time', 'source_ip', 'destination_ip', 'mode', 'traffic_type', 'description', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        
        csv_data = {
            'experiment_id': exp_data['experiment_id'],
            'start_time': exp_data['timestamp_start'],
            'end_time': exp_data['timestamp_end'],
            'source_ip': exp_data['source_ip'],
            'destination_ip': exp_data['destination_ip'],
            'mode': exp_data['mode'],
            'traffic_type': exp_data.get('attack_type', 'NORMAL'),
            'description': exp_data.get('description', ''),
            'status': exp_data['status']
        }
        writer.writerow(csv_data)

def display_start(exp_id, mode, type_label, source, target):
    print("=" * 50)
    print("NIDS LAB TRAFFIC GENERATOR")
    print("=" * 50)
    print(f"Experiment ID : {exp_id}")
    print(f"Mode          : {mode.upper()}")
    print(f"Type          : {type_label}")
    print(f"Source        : {source}")
    print(f"Target        : {target}")
    print("")
    print(f"Network       : {LAB_SUBNET}")
    print(f"Status        : AUTHORIZED LAB TARGET")
    if mode == "attack":
        print("\n*** AUTHORIZED ISOLATED LAB ONLY ***")
    print("\nStarting experiment...\n")

def display_end(exp_id, start_time, end_time, label):
    print("\nExperiment completed.\n")
    print(f"Start       : {start_time}")
    print(f"End         : {end_time}")
    print(f"Experiment  : {exp_id}")
    print(f"Label       : {label}")
    print("=" * 50)

def main():
    parser = argparse.ArgumentParser(description="NIDS Lab Traffic Generator")
    parser.add_argument("--target", required=True, help="Target IP address in the lab network")
    parser.add_argument("--mode", required=True, choices=["normal", "attack"], help="Traffic mode")
    parser.add_argument("--type", help="Attack type (required for attack mode)")
    parser.add_argument("--duration", type=int, default=10, help="Duration in seconds")
    parser.add_argument("--rate", type=int, default=5, help="Rate parameter for specific attacks")
    parser.add_argument("--experiment-id", help="Override experiment ID")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without generating traffic")
    parser.add_argument("--list", action="store_true", help="List available attack types")
    
    args = parser.parse_args()

    if args.list:
        print("Available attack types:")
        print("  port_scan, service_enumeration, icmp_burst, tcp_connection_burst, ssh_auth_test, web_test")
        sys.exit(0)

    validate_target(args.target)

    if args.mode == "attack" and not args.type:
        print("ERROR: --type is required when --mode is attack.")
        sys.exit(1)

    exp_id = args.experiment_id if args.experiment_id else get_next_experiment_id()
    source_ip = config.get("attacker_ip", "192.168.56.128") if args.mode == "attack" else config.get("normal_client_ip", "192.168.56.130")
    
    type_label = "NORMAL"
    if args.mode == "attack":
        type_label = args.type.upper()

    display_start(exp_id, args.mode, type_label, source_ip, args.target)

    start_time = datetime.now(datetime.UTC).isoformat() + "Z"

    if args.dry_run:
        print(f"[DRY-RUN] Would execute {args.mode} mode with type {type_label} against {args.target} for {args.duration}s.")
        for _ in tqdm(range(100), desc="Dry-Run Progress"):
            time.sleep(0.01)
    else:
        # We will dispatch to modules here. For now just sleep to simulate.
        if args.mode == "normal":
            import modules.normal as normal_mod
            normal_mod.run(args.target, args.duration, config)
        elif args.mode == "attack":
            if args.type == "port_scan":
                import modules.port_scan as port_scan_mod
                port_scan_mod.run(args.target, config)
            elif args.type == "service_enumeration":
                import modules.service_enum as service_enum_mod
                service_enum_mod.run(args.target, config)
            elif args.type == "icmp_burst":
                import modules.icmp_burst as icmp_burst_mod
                icmp_burst_mod.run(args.target, args.duration, args.rate, config)
            elif args.type == "tcp_connection_burst":
                import modules.tcp_burst as tcp_burst_mod
                tcp_burst_mod.run(args.target, args.duration, args.rate, config)
            elif args.type == "ssh_auth_test":
                import modules.ssh_test as ssh_test_mod
                ssh_test_mod.run(args.target, config)
            elif args.type == "web_test":
                import modules.web_test as web_test_mod
                web_test_mod.run(args.target, config)
            else:
                print(f"ERROR: Unknown attack type '{args.type}'")
                sys.exit(1)

    end_time = datetime.now(datetime.UTC).isoformat() + "Z"
    
    exp_data = {
        "experiment_id": exp_id,
        "timestamp_start": start_time,
        "timestamp_end": end_time,
        "source_ip": source_ip,
        "destination_ip": args.target,
        "mode": args.mode,
        "attack_type": type_label,
        "status": "completed"
    }

    if not args.dry_run:
        log_experiment(exp_data)

    display_end(exp_id, start_time, end_time, type_label)

if __name__ == "__main__":
    main()
