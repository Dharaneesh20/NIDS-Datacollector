import sqlite3
from backend.config import settings

def get_db():
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Capture Sessions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS capture_sessions (
            session_id TEXT PRIMARY KEY,
            start_time TEXT,
            end_time TEXT,
            interface TEXT,
            host_ip TEXT,
            subnet TEXT,
            packet_count INTEGER DEFAULT 0,
            byte_count INTEGER DEFAULT 0,
            pcap_path TEXT,
            processed_flow_path TEXT
        )
    ''')
    
    # Experiments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS experiments (
            experiment_id TEXT PRIMARY KEY,
            start_time TEXT,
            end_time TEXT,
            source_ip TEXT,
            destination_ip TEXT,
            traffic_type TEXT,
            label TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()
