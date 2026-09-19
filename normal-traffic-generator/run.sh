#!/bin/bash

echo "========================================================"
echo "      NIDS LAB - NORMAL TRAFFIC GENERATOR MENU"
echo "========================================================"
echo ""

read -p "Enter Target IP [Default: 192.168.56.129]: " TARGET
TARGET=${TARGET:-192.168.56.129}

echo ""
echo "Select Machine Identifier:"
echo "1) KALI"
echo "2) MINT"
read -p "Choose an option (1-2) [Default: 1]: " MACHINE_OPT
MACHINE_OPT=${MACHINE_OPT:-1}

if [ "$MACHINE_OPT" == "1" ]; then
    MACHINE="KALI"
elif [ "$MACHINE_OPT" == "2" ]; then
    MACHINE="MINT"
else
    echo "Invalid selection. Exiting."
    exit 1
fi

echo ""
read -p "Enter Duration in seconds [Default: 60]: " DURATION
DURATION=${DURATION:-60}

echo ""
read -p "Do you want to perform a DRY RUN (no traffic generated)? (y/n) [Default: n]: " DRY_RUN_OPT
DRY_RUN_OPT=${DRY_RUN_OPT:-n}

CMD="python3 normal_traffic_generator.py --target $TARGET --machine $MACHINE --duration $DURATION"

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
