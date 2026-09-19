# NIDS Data Collector

This is the central Data Collection and Dataset Generation application for the Zorin Host NIDS project.

## Architecture
- **Packet Capture**: `scapy` on `vmnet1`
- **Flow Generation**: Bidirectional 5-tuple hash flow building
- **Feature Extraction**: Inter-arrival times, packet sizes, TCP flags, byte/packet rates.
- **Experiment Matching**: Loads `experiments.csv` and assigns `NORMAL` or `ATTACK` labels based on time intervals.

## Usage
1. Setup Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```
2. Run the application (requires sudo for scapy sniffing):
   ```bash
   sudo .venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```
3. Use the API endpoints:
   - `POST http://127.0.0.1:8000/api/capture/start` (Starts sniffing and flow building)
   - `POST http://127.0.0.1:8000/api/capture/stop` (Stops sniffing, matches experiments, and generates `network_dataset.csv`)
