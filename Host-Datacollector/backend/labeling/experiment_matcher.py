import pandas as pd
from datetime import datetime
import os
from backend.config import settings

class ExperimentMatcher:
    def __init__(self):
        self.experiments = []
        self._load_experiments()

    def _load_experiments(self):
        exp_dir = os.path.join(os.path.dirname(__file__), "..", "..", settings._config['storage']['experiment_directory'])
        os.makedirs(exp_dir, exist_ok=True)
        # We might load from DB or CSV here
        from backend.database.database import get_db
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM experiments")
        rows = cursor.fetchall()
        
        for row in rows:
            self.experiments.append({
                'experiment_id': row['experiment_id'],
                'start_time': datetime.fromisoformat(row['start_time'].replace("Z", "+00:00")).timestamp(),
                'end_time': datetime.fromisoformat(row['end_time'].replace("Z", "+00:00")).timestamp(),
                'source_ip': row['source_ip'],
                'destination_ip': row['destination_ip'],
                'label': row['label']
            })
        conn.close()

    def reload(self):
        self.experiments = []
        self._load_experiments()

    def match_flow(self, flow):
        flow_time = flow['timestamp']
        src = flow['src_ip']
        dst = flow['dst_ip']
        
        for exp in self.experiments:
            if exp['start_time'] <= flow_time <= exp['end_time']:
                if exp['source_ip'] == src and exp['destination_ip'] == dst:
                    return exp['label'], exp['experiment_id']
                    
        return "UNLABELED", None

    def build_dataset(self, flows, session_id):
        # Convert list of dicts to dataframe
        if not flows:
            return None
            
        df = pd.DataFrame(flows)
        
        # Apply matching
        labels = []
        exp_ids = []
        label_sources = []
        
        for _, row in df.iterrows():
            label, exp_id = self.match_flow(row.to_dict())
            labels.append(label)
            exp_ids.append(exp_id)
            label_sources.append("EXPERIMENT_LOG" if exp_id else "UNLABELED")
            
        df['label'] = labels
        df['experiment_id'] = exp_ids
        df['label_source'] = label_sources
        df['session_id'] = session_id
        
        dataset_dir = os.path.join(os.path.dirname(__file__), "..", "..", settings._config['storage']['dataset_directory'])
        os.makedirs(dataset_dir, exist_ok=True)
        
        csv_path = os.path.join(dataset_dir, "network_dataset.csv")
        
        # Append or write new
        if os.path.exists(csv_path):
            df.to_csv(csv_path, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_path, index=False)
            
        return len(df)
