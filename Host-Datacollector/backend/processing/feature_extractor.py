import time
import numpy as np

class FlowFeatures:
    def __init__(self, pkt_data):
        self.flow_id = None # Set by builder
        self.start_time = pkt_data['timestamp']
        self.end_time = pkt_data['timestamp']
        self.src_ip = pkt_data['source_ip']
        self.dst_ip = pkt_data['destination_ip']
        self.src_mac = pkt_data['source_mac']
        self.dst_mac = pkt_data['destination_mac']
        self.src_port = pkt_data['source_port']
        self.dst_port = pkt_data['destination_port']
        self.protocol = pkt_data['protocol']
        
        self.packet_count = 0
        self.forward_packet_count = 0
        self.backward_packet_count = 0
        
        self.total_bytes = 0
        self.forward_bytes = 0
        self.backward_bytes = 0
        
        self.tcp_syn_count = 0
        self.tcp_ack_count = 0
        self.tcp_fin_count = 0
        self.tcp_rst_count = 0
        self.tcp_psh_count = 0
        self.tcp_urg_count = 0
        
        self.packet_sizes = []
        self.inter_arrival_times = []
        self.last_timestamp = pkt_data['timestamp']
        
        self.add_packet(pkt_data)

    def add_packet(self, pkt_data):
        is_forward = (pkt_data['source_ip'] == self.src_ip)
        
        self.packet_count += 1
        self.total_bytes += pkt_data['packet_length']
        self.packet_sizes.append(pkt_data['packet_length'])
        
        if is_forward:
            self.forward_packet_count += 1
            self.forward_bytes += pkt_data['packet_length']
        else:
            self.backward_packet_count += 1
            self.backward_bytes += pkt_data['packet_length']
            
        if self.packet_count > 1:
            iat = pkt_data['timestamp'] - self.last_timestamp
            if iat >= 0:
                self.inter_arrival_times.append(iat)
                
        self.last_timestamp = pkt_data['timestamp']
        self.end_time = pkt_data['timestamp']
        
        if self.protocol == 'TCP' and pkt_data['tcp_flags']:
            flags = pkt_data['tcp_flags']
            if 'S' in flags: self.tcp_syn_count += 1
            if 'A' in flags: self.tcp_ack_count += 1
            if 'F' in flags: self.tcp_fin_count += 1
            if 'R' in flags: self.tcp_rst_count += 1
            if 'P' in flags: self.tcp_psh_count += 1
            if 'U' in flags: self.tcp_urg_count += 1

    def to_dict(self):
        duration = max(self.end_time - self.start_time, 0.000001)
        
        return {
            "flow_id": self.flow_id,
            "timestamp": self.start_time,
            "duration": duration,
            "src_ip": self.src_ip,
            "dst_ip": self.dst_ip,
            "src_mac": self.src_mac,
            "dst_mac": self.dst_mac,
            "src_port": self.src_port,
            "dst_port": self.dst_port,
            "protocol": self.protocol,
            
            "packet_count": self.packet_count,
            "forward_packet_count": self.forward_packet_count,
            "backward_packet_count": self.backward_packet_count,
            
            "total_bytes": self.total_bytes,
            "forward_bytes": self.forward_bytes,
            "backward_bytes": self.backward_bytes,
            
            "packets_per_second": self.packet_count / duration,
            "bytes_per_second": self.total_bytes / duration,
            
            "average_packet_size": float(np.mean(self.packet_sizes)) if self.packet_sizes else 0,
            "minimum_packet_size": min(self.packet_sizes) if self.packet_sizes else 0,
            "maximum_packet_size": max(self.packet_sizes) if self.packet_sizes else 0,
            "packet_size_std": float(np.std(self.packet_sizes)) if len(self.packet_sizes) > 1 else 0.0,
            
            "inter_arrival_time_mean": float(np.mean(self.inter_arrival_times)) if self.inter_arrival_times else 0.0,
            "inter_arrival_time_std": float(np.std(self.inter_arrival_times)) if len(self.inter_arrival_times) > 1 else 0.0,
            
            "tcp_syn_count": self.tcp_syn_count,
            "tcp_ack_count": self.tcp_ack_count,
            "tcp_fin_count": self.tcp_fin_count,
            "tcp_rst_count": self.tcp_rst_count,
            "tcp_psh_count": self.tcp_psh_count,
            "tcp_urg_count": self.tcp_urg_count
        }
