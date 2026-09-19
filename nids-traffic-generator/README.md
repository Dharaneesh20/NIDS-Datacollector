# NIDS Lab Traffic Generator

This project is a Python 3 CLI application designed to safely generate controlled network traffic in an isolated VMware Host-Only laboratory network. It is intended for use in a college Data Science + Cybersecurity project for generating a Network Intrusion Detection System (NIDS) dataset.

## Safety and Scope

> [!CAUTION]
> **AUTHORIZED ISOLATED LAB ONLY**
> This script is strictly limited to operating against targets within the `192.168.56.0/24` subnet. It will outright refuse to generate traffic to the Internet, your local LAN, or any arbitrary public IPs.

## Architecture

```
    Kali traffic generator (192.168.56.128)
            ↓ (Generates Traffic)
       VMware VMnet1 (Host-Only Network)
            ↓
       Zorin collector (192.168.56.1)
            ↓ (Captures PCAP)
       flow extraction & feature engineering
            ↓
       experiment-log matching
            ↓
       final labeled CSV for Machine Learning
```

**Important**: This script does not capture packets or create the final ML dataset. It only generates traffic and logs the *intent* (experiment metadata) into JSONL/CSV logs. The Zorin NIDS host uses these logs to label the network flows based on time windows.

## Requirements

- Python 3.6+
- Installed packages listed in `requirements.txt`
- `nmap` system package (for service enumeration)

## Installation

```bash
cd nids-traffic-generator
pip install -r requirements.txt
```

## Configuration

Edit `config.yaml` to specify the lab setup and limits:
- `lab_subnet`: The allowed subnet (must be `192.168.56.0/24`).
- `limits`: Hard maximums for duration, packet rates, and connections.

## Usage

### Example Commands

**1. Normal Background Traffic**
```bash
python3 lab_traffic_generator.py --target 192.168.56.129 --mode normal --duration 60
```

**2. Attack: Port Scan**
```bash
python3 lab_traffic_generator.py --target 192.168.56.129 --mode attack --type port_scan
```

**3. Attack: ICMP Burst**
```bash
python3 lab_traffic_generator.py --target 192.168.56.129 --mode attack --type icmp_burst --rate 10 --duration 5
```

**4. Dry Run (No traffic generated)**
```bash
python3 lab_traffic_generator.py --target 192.168.56.129 --mode attack --type tcp_connection_burst --dry-run
```

## Logs and Labels

Logs are generated in the `logs/` directory:
- `experiments.jsonl`: One JSON object per run.
- `experiments.csv`: A tabular version.

The labels used by this script are:
`NORMAL`, `PORT_SCAN`, `SERVICE_ENUMERATION`, `ICMP_BURST`, `TCP_CONNECTION_BURST`, `SSH_AUTH_TEST`, `WEB_TEST`.

## Troubleshooting

- **Target Validation Error**: Ensure your target IP is strictly within `192.168.56.0/24`.
- **Missing nmap**: Ensure `nmap` is installed via `sudo apt install nmap` for service enumeration.
- **Missing requests/paramiko**: Ensure you run `pip install -r requirements.txt`.
