# NIDS Normal Traffic Generator

This project is a Python 3 CLI application designed to safely generate **benign/legitimate** network traffic in an isolated VMware Host-Only laboratory network. It is intended for use in a college Data Science + Cybersecurity project for generating the "NORMAL" class label of a Network Intrusion Detection System (NIDS) dataset.

## Purpose

The script simulates realistic but lightweight background activity by randomly executing standard network tasks (ICMP, HTTP, SSH, FTP, etc.) with configurable random delays. 

**Important:** This script is a TRAFFIC GENERATOR only. It does not capture network packets or build the final Machine Learning dataset. It merely generates the activity and records an experiment log. The actual packet capture and flow extraction must be performed separately on the Zorin host (e.g., using Zeek or Scapy).

## VMware Network Setup

- **Subnet:** `192.168.56.0/24` (Host-Only Network)
- **Zorin host (NIDS Collector):** `192.168.56.1`
- **Kali Linux (Attacker/Client):** `192.168.56.128`
- **Metasploitable (Server):** `192.168.56.129`
- **Linux Mint (Client):** `192.168.56.130`

## Installation

This script relies mostly on the Python standard library, but uses `requests` and `pyyaml`.

```bash
cd normal-traffic-generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Edit `config.yaml` to specify the lab setup and active services:
- `lab_subnet`: The allowed subnet (must be `192.168.56.0/24`).
- `services`: Enable or disable specific traffic types (HTTP, SSH, FTP, etc.) and configure their ports.
- `traffic`: Set the minimum and maximum random delay between actions.

## Usage

You can run this on either your Kali Linux or Linux Mint VM. Use the `--machine` argument to label the source appropriately.

### 1. Running on Kali Linux
```bash
python3 normal_traffic_generator.py \
    --target 192.168.56.129 \
    --machine KALI \
    --duration 1800 \
    --min-delay 2 \
    --max-delay 10
```

### 2. Running on Linux Mint
```bash
python3 normal_traffic_generator.py \
    --target 192.168.56.129 \
    --machine MINT \
    --duration 1800 \
    --min-delay 5 \
    --max-delay 15
```

### 3. Dry Run (Safety Test)
```bash
python3 normal_traffic_generator.py --target 192.168.56.129 --machine MINT --duration 60 --dry-run
```

## Log Format

Logs are stored as a CSV file in `logs/normal_traffic_log.csv`. This log tracks *intent*. When generating your final ML dataset, your Zorin host should match its captured network flows against these timestamps to apply the `NORMAL` label accurately.

## Safety Restrictions

> [!CAUTION]
> This script implements strict IP validation. It will only communicate with addresses within `192.168.56.0/24`. It will explicitly refuse to target arbitrary Internet addresses, public DNS, or your home LAN. 

## Troubleshooting

- **Invalid Target Error:** Ensure the `--target` is strictly within `192.168.56.0/24`.
- **Activity Failed:** If you see `[NORMAL] FTP → 192.168.56.129:21` failing, ensure the Metasploitable VM is running and its FTP service is online.
