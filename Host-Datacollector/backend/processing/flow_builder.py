import threading
import time
import queue
from backend.processing.feature_extractor import FlowFeatures
from backend.config import settings

class FlowBuilder:
    def __init__(self, event_callback=None):
        self.active_flows = {}
        self.completed_flows = []
        self.flow_counter = 0
        self.event_callback = event_callback
        self.running = False
        self.processor_thread = None
        self.packet_queue = queue.Queue()
        
    def start(self):
        self.running = True
        self.processor_thread = threading.Thread(target=self._process_queue)
        self.processor_thread.daemon = True
        self.processor_thread.start()
        
    def stop(self):
        self.running = False
        if self.processor_thread:
            self.processor_thread.join(timeout=2.0)
        self._flush_all_flows()
            
    def _get_flow_key(self, pkt):
        # Bidirectional hash key
        ips = sorted([str(pkt['source_ip']), str(pkt['destination_ip'])])
        ports = sorted([str(pkt['source_port']), str(pkt['destination_port'])])
        return f"{ips[0]}:{ports[0]}-{ips[1]}:{ports[1]}-{pkt['protocol']}"

    def _process_queue(self):
        last_cleanup = time.time()
        while self.running:
            try:
                pkt = self.packet_queue.get(timeout=1.0)
                self._add_packet(pkt)
            except queue.Empty:
                pass
                
            if time.time() - last_cleanup > 5:
                self._cleanup_stale_flows()
                last_cleanup = time.time()

    def _add_packet(self, pkt):
        key = self._get_flow_key(pkt)
        
        if key not in self.active_flows:
            self.flow_counter += 1
            flow = FlowFeatures(pkt)
            flow.flow_id = f"FLOW-{self.flow_counter:08d}"
            self.active_flows[key] = flow
            if self.event_callback:
                self.event_callback("flow_created", flow.to_dict())
        else:
            self.active_flows[key].add_packet(pkt)
            
        # If TCP FIN or RST is seen, we might want to close the flow soon, but timeout handles it safely.

    def _cleanup_stale_flows(self):
        current_time = time.time()
        to_remove = []
        timeout = settings.flow_timeout
        
        for key, flow in self.active_flows.items():
            # If last packet was seen more than timeout seconds ago
            if current_time - flow.last_timestamp > timeout:
                to_remove.append(key)
                
        for key in to_remove:
            flow = self.active_flows.pop(key)
            self.completed_flows.append(flow.to_dict())
            if self.event_callback:
                self.event_callback("flow_completed", flow.to_dict())

    def _flush_all_flows(self):
        for key, flow in list(self.active_flows.items()):
            self.completed_flows.append(flow.to_dict())
            if self.event_callback:
                self.event_callback("flow_completed", flow.to_dict())
        self.active_flows.clear()

    def get_completed_flows(self):
        flows = self.completed_flows[:]
        self.completed_flows.clear()
        return flows
