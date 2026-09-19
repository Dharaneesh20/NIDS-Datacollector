from scapy.all import sniff, wrpcap
import threading
import time
import os
from datetime import datetime
from backend.config import settings
from backend.processing.packet_parser import parse_packet
from backend.database.database import get_db

class PacketCaptureEngine:
    def __init__(self):
        self.is_capturing = False
        self.session_id = None
        self.capture_thread = None
        self.packet_count = 0
        self.byte_count = 0
        self.start_time = None
        self.pcap_file = None
        self.flow_queue = None # Will connect to flow builder
        
    def _get_next_session_id(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT session_id FROM capture_sessions ORDER BY session_id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        
        if row and row['session_id'].startswith('CAP-'):
            try:
                num = int(row['session_id'][4:])
                return f"CAP-{num + 1:06d}"
            except ValueError:
                pass
        return "CAP-000001"

    def start_capture(self, flow_queue):
        if self.is_capturing:
            return False
            
        self.session_id = self._get_next_session_id()
        self.is_capturing = True
        self.packet_count = 0
        self.byte_count = 0
        self.start_time = datetime.utcnow().isoformat() + "Z"
        self.flow_queue = flow_queue
        
        self.pcap_file = os.path.join(settings.pcap_dir, f"{self.session_id}.pcap")
        
        # Start sniffing thread
        self.capture_thread = threading.Thread(target=self._sniff_loop)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        
        # Log to DB
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO capture_sessions (session_id, start_time, interface, host_ip, subnet, pcap_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.session_id, self.start_time, settings.interface, settings._config['network']['host_ip'], settings.subnet, self.pcap_file))
        conn.commit()
        conn.close()
        
        return self.session_id

    def _packet_callback(self, pkt):
        if not self.is_capturing:
            return
            
        self.packet_count += 1
        self.byte_count += len(pkt)
        
        # Parse and send to queue
        parsed = parse_packet(pkt)
        if parsed["source_ip"] and parsed["destination_ip"]:
            self.flow_queue.put(parsed)

    def _sniff_loop(self):
        # We write packets to pcap asynchronously or directly using wrpcap append
        # For performance in a real NIDS, scapy's sniff with prn is slow, but acceptable for lab.
        # We'll sniff in chunks to allow stopping
        while self.is_capturing:
            pkts = sniff(iface=settings.interface, timeout=settings.capture_timeout, prn=self._packet_callback, store=True)
            if len(pkts) > 0 and self.pcap_file:
                wrpcap(self.pcap_file, pkts, append=True)

    def stop_capture(self):
        if not self.is_capturing:
            return False
            
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join(timeout=2.0)
            
        end_time = datetime.utcnow().isoformat() + "Z"
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE capture_sessions 
            SET end_time = ?, packet_count = ?, byte_count = ?
            WHERE session_id = ?
        ''', (end_time, self.packet_count, self.byte_count, self.session_id))
        conn.commit()
        conn.close()
        
        return True

    def get_status(self):
        return {
            "is_capturing": self.is_capturing,
            "session_id": self.session_id,
            "packet_count": self.packet_count,
            "byte_count": self.byte_count,
            "start_time": self.start_time
        }

capture_engine = PacketCaptureEngine()
