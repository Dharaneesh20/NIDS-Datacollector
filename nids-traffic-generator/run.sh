#!/bin/bash

echo "========================================================"
echo "      NIDS LAB - ATTACK TRAFFIC GENERATOR MENU"
echo "========================================================"
echo ""

read -p "Enter Target IP [Default: 192.168.56.129]: " TARGET
TARGET=${TARGET:-192.168.56.129}

echo ""
echo "Select Attack Type:"
echo "1) port_scan"
echo "2) service_enumeration"
echo "3) icmp_burst"
echo "4) tcp_connection_burst"
echo "5) ssh_auth_test"
echo "6) web_test"
echo "7) Random Attack"
read -p "Choose an option (1-7): " ATTACK_OPT

ATTACKS=("port_scan" "service_enumeration" "icmp_burst" "tcp_connection_burst" "ssh_auth_test" "web_test")

if [ "$ATTACK_OPT" == "7" ]; then
    # Pick a random attack
    RANDOM_INDEX=$((RANDOM % 6))
    ATTACK_TYPE=${ATTACKS[$RANDOM_INDEX]}
    echo "Randomly selected: $ATTACK_TYPE"
else
    # Adjust index for bash array (0-indexed)
    INDEX=$((ATTACK_OPT - 1))
    ATTACK_TYPE=${ATTACKS[$INDEX]}
    
    if [ -z "$ATTACK_TYPE" ]; then
        echo "Invalid selection. Exiting."
        exit 1
    fi
fi

echo ""
read -p "Do you want to perform a DRY RUN (no traffic generated)? (y/n) [Default: n]: " DRY_RUN_OPT
DRY_RUN_OPT=${DRY_RUN_OPT:-n}

CMD="python3 lab_traffic_generator.py --target $TARGET --mode attack --type $ATTACK_TYPE"

if [[ "$DRY_RUN_OPT" =~ ^[Yy]$ ]]; then
    CMD="$CMD --dry-run"
fi

echo ""
echo "========================================================"
echo "Executing: $CMD"
echo "========================================================"
echo ""

$CMD

echo ""
echo "Execution finished."
