from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.capture.packet_capture import capture_engine
from backend.processing.flow_builder import FlowBuilder
from backend.labeling.experiment_matcher import ExperimentMatcher
import asyncio

app = FastAPI(title="NIDS Data Collector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
flow_builder = None
matcher = ExperimentMatcher()

def event_callback(event_type, data):
    # This will be hooked up to websockets later
    pass

@app.on_event("startup")
async def startup_event():
    global flow_builder
    flow_builder = FlowBuilder(event_callback=event_callback)
    
@app.get("/api/status")
async def get_status():
    return {
        "status": "RUNNING",
        "capture": capture_engine.get_status()
    }

@app.post("/api/capture/start")
async def start_capture():
    if capture_engine.is_capturing:
        return {"error": "Capture already running"}
        
    flow_builder.start()
    session_id = capture_engine.start_capture(flow_builder.packet_queue)
    return {"message": "Capture started", "session_id": session_id}

@app.post("/api/capture/stop")
async def stop_capture():
    if not capture_engine.is_capturing:
        return {"error": "Capture not running"}
        
    session_id = capture_engine.session_id
    capture_engine.stop_capture()
    flow_builder.stop()
    
    # Process the final flows
    flows = flow_builder.get_completed_flows()
    matcher.reload()
    num_written = matcher.build_dataset(flows, session_id)
    
    return {
        "message": "Capture stopped and dataset generated", 
        "flows_processed": num_written,
        "session_id": session_id
    }
