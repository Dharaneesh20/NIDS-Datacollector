import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

class Config:
    def __init__(self):
        with open(CONFIG_PATH, "r") as f:
            self._config = yaml.safe_load(f)

    @property
    def interface(self):
        return self._config.get("network", {}).get("interface", "vmnet1")
    
    @property
    def subnet(self):
        return self._config.get("network", {}).get("subnet", "192.168.56.0/24")

    @property
    def capture_timeout(self):
        return self._config.get("capture", {}).get("packet_timeout", 1)
        
    @property
    def flow_timeout(self):
        return self._config.get("capture", {}).get("flow_timeout", 15)

    @property
    def pcap_dir(self):
        path = os.path.join(os.path.dirname(__file__), "..", self._config.get("storage", {}).get("raw_pcap_directory", "data/raw/pcap"))
        os.makedirs(path, exist_ok=True)
        return path

    @property
    def db_path(self):
        path = os.path.join(os.path.dirname(__file__), "..", self._config.get("storage", {}).get("database_path", "data/nids.db"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

settings = Config()
