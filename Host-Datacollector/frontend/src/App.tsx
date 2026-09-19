import { useState, useEffect } from 'react';
import { Play, Square, Activity, Database, Shield, AlertTriangle } from 'lucide-react';

export default function App() {
  const [status, setStatus] = useState<any>(null);

  const fetchStatus = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/status');
      const data = await res.json();
      setStatus(data);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleStart = async () => {
    try {
      await fetch('http://127.0.0.1:8000/api/capture/start', { method: 'POST' });
      fetchStatus();
    } catch (e) {
      console.error(e);
    }
  };

  const handleStop = async () => {
    try {
      await fetch('http://127.0.0.1:8000/api/capture/stop', { method: 'POST' });
      fetchStatus();
    } catch (e) {
      console.error(e);
    }
  };

  const isCapturing = status?.capture?.is_capturing;

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-500/20 rounded-xl">
              <Shield className="w-8 h-8 text-blue-400" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight">NIDS Dashboard</h1>
              <p className="text-slate-400 text-sm">Zorin Host Data Collector • 192.168.56.1</p>
            </div>
          </div>
          
          <div className="flex gap-4">
            <button 
              onClick={handleStart}
              disabled={isCapturing}
              className={`flex items-center gap-2 px-6 py-2.5 rounded-lg font-medium transition-all ${
                isCapturing 
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed' 
                  : 'bg-emerald-500 hover:bg-emerald-600 text-white shadow-lg shadow-emerald-500/20'
              }`}
            >
              <Play className="w-4 h-4" /> Start Capture
            </button>
            <button 
              onClick={handleStop}
              disabled={!isCapturing}
              className={`flex items-center gap-2 px-6 py-2.5 rounded-lg font-medium transition-all ${
                !isCapturing 
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed' 
                  : 'bg-rose-500 hover:bg-rose-600 text-white shadow-lg shadow-rose-500/20'
              }`}
            >
              <Square className="w-4 h-4" /> Stop & Compile
            </button>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700/50 flex flex-col gap-2">
            <div className="flex items-center gap-3 text-slate-400 mb-2">
              <Activity className="w-5 h-5" />
              <span className="font-medium">System Status</span>
            </div>
            <div className="flex items-end gap-3">
              <div className={`w-3 h-3 rounded-full animate-pulse ${isCapturing ? 'bg-emerald-400' : 'bg-slate-500'}`} />
              <span className="text-3xl font-semibold tracking-tight text-white">
                {isCapturing ? 'RUNNING' : 'STOPPED'}
              </span>
            </div>
          </div>

          <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700/50 flex flex-col gap-2">
            <div className="flex items-center gap-3 text-slate-400 mb-2">
              <Database className="w-5 h-5" />
              <span className="font-medium">Packets Captured</span>
            </div>
            <span className="text-3xl font-semibold tracking-tight text-white">
              {(status?.capture?.packet_count || 0).toLocaleString()}
            </span>
          </div>

          <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700/50 flex flex-col gap-2">
            <div className="flex items-center gap-3 text-slate-400 mb-2">
              <AlertTriangle className="w-5 h-5" />
              <span className="font-medium">Current Session ID</span>
            </div>
            <span className="text-3xl font-semibold tracking-tight text-white font-mono">
              {status?.capture?.session_id || 'NONE'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
