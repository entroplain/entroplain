"""
Real-time entropy visualization dashboard.

Run with: entroplain-dashboard --port 8050
Then open: http://localhost:8050
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn


@dataclass
class DashboardConfig:
    """Configuration for the dashboard."""
    port: int = 8050
    proxy_port: int = 8765
    update_interval_ms: int = 100


# Fixed-height dashboard HTML
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Entroplain Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body {
            height: 100%;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
        }
        .app {
            height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        h1 {
            font-size: 20px;
            margin-bottom: 15px;
            color: #4ade80;
            flex-shrink: 0;
        }
        .main-grid {
            flex: 1;
            display: grid;
            grid-template-columns: 1fr 280px;
            gap: 15px;
            min-height: 0;
        }
        .chart-container {
            background: #1a1a1a;
            border-radius: 8px;
            padding: 15px;
            display: flex;
            flex-direction: column;
            min-height: 0;
        }
        .chart-wrapper {
            flex: 1;
            position: relative;
            min-height: 0;
        }
        .chart-wrapper canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        .legend {
            display: flex;
            gap: 15px;
            margin-top: 10px;
            font-size: 11px;
            flex-shrink: 0;
        }
        .legend-item { display: flex; align-items: center; gap: 5px; }
        .legend-dot { width: 8px; height: 8px; border-radius: 50%; }
        .dot-entropy { background: #60a5fa; }
        .dot-valley { background: #f59e0b; }
        .dot-threshold { background: #ef4444; }
        
        .stats-panel {
            display: flex;
            flex-direction: column;
            gap: 10px;
            overflow-y: auto;
        }
        .stat-card {
            background: #1a1a1a;
            border-radius: 8px;
            padding: 12px;
            flex-shrink: 0;
        }
        .stat-label {
            font-size: 10px;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .stat-value {
            font-size: 24px;
            font-weight: 600;
            color: #fff;
            margin-top: 4px;
        }
        .stat-value.savings { color: #4ade80; }
        .stat-value.cost { color: #fbbf24; }
        .stat-value.valleys { color: #60a5fa; }
        
        .status-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 500;
        }
        .status-active { background: #22c55e; color: #000; }
        .status-idle { background: #374151; color: #888; }
        .status-exited { background: #f59e0b; color: #000; }
        
        .connection-status {
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 11px;
            margin-bottom: 10px;
        }
        .connected { background: #166534; color: #4ade80; }
        .disconnected { background: #7f1d1d; color: #fca5a5; }
        
        .waiting-message {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: #666;
            text-align: center;
        }
        .waiting-message h2 { font-size: 16px; margin-bottom: 8px; color: #888; }
        .waiting-message p { font-size: 12px; }
    </style>
</head>
<body>
    <div class="app">
        <h1>🎯 Entroplain Dashboard</h1>
        
        <div class="main-grid">
            <div class="chart-container">
                <div id="connectionStatus" class="connection-status disconnected">
                    Connecting...
                </div>
                <div class="chart-wrapper">
                    <canvas id="entropyChart"></canvas>
                    <div id="waitingMessage" class="waiting-message">
                        <h2>Waiting for data...</h2>
                        <p>Make a request through the proxy to see entropy visualization</p>
                    </div>
                </div>
                <div class="legend">
                    <div class="legend-item"><div class="legend-dot dot-entropy"></div><span>Entropy</span></div>
                    <div class="legend-item"><div class="legend-dot dot-valley"></div><span>Valley</span></div>
                    <div class="legend-item"><div class="legend-dot dot-threshold"></div><span>Threshold</span></div>
                </div>
            </div>
            
            <div class="stats-panel">
                <div class="stat-card">
                    <div class="stat-label">Status</div>
                    <div class="stat-value" id="status"><span class="status-badge status-idle">Idle</span></div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-label">Tokens Generated</div>
                    <div class="stat-value" id="tokens">0</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-label">Valleys Detected</div>
                    <div class="stat-value valleys" id="valleys">0</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-label">Current Entropy</div>
                    <div class="stat-value" id="currentEntropy">-</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-label">Mean Entropy</div>
                    <div class="stat-value" id="meanEntropy">-</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-label">Tokens Saved</div>
                    <div class="stat-value savings" id="saved">-</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-label">Cost Saved</div>
                    <div class="stat-value cost" id="costSaved">-</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let chart = null;
        let hasData = false;
        const maxDataPoints = 200;

        function initChart() {
            const ctx = document.getElementById('entropyChart').getContext('2d');
            
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        {
                            label: 'Entropy',
                            data: [],
                            borderColor: '#60a5fa',
                            backgroundColor: 'rgba(96, 165, 250, 0.1)',
                            fill: true,
                            tension: 0.3,
                            pointRadius: 0,
                            pointHoverRadius: 4,
                            borderWidth: 2,
                        },
                        {
                            label: 'Threshold',
                            data: [],
                            borderColor: '#ef4444',
                            borderDash: [5, 5],
                            pointRadius: 0,
                            fill: false,
                            borderWidth: 1,
                        },
                        {
                            label: 'Valleys',
                            data: [],
                            borderColor: '#f59e0b',
                            pointBackgroundColor: '#f59e0b',
                            pointRadius: 5,
                            pointHoverRadius: 7,
                            showLine: false,
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: { duration: 0 },
                    interaction: { intersect: false, mode: 'index' },
                    scales: {
                        x: {
                            title: { display: true, text: 'Tokens', color: '#888', font: { size: 11 } },
                            grid: { color: '#222' },
                            ticks: { color: '#666', maxTicksLimit: 10 }
                        },
                        y: {
                            title: { display: true, text: 'Entropy (bits)', color: '#888', font: { size: 11 } },
                            min: 0,
                            max: 1,
                            grid: { color: '#222' },
                            ticks: { color: '#666' }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: '#1a1a1a',
                            titleColor: '#fff',
                            bodyColor: '#888',
                            borderColor: '#333',
                            borderWidth: 1,
                        }
                    }
                }
            });
        }

        function updateChart(data) {
            if (!chart) return;
            
            if (!hasData && data.trajectory && data.trajectory.length > 0) {
                hasData = true;
                document.getElementById('waitingMessage').style.display = 'none';
                document.getElementById('connectionStatus').className = 'connection-status connected';
                document.getElementById('connectionStatus').textContent = 'Connected - Live';
            }
            
            if (!data.trajectory || data.trajectory.length === 0) return;

            // Limit data points for performance
            let trajectory = data.trajectory;
            if (trajectory.length > maxDataPoints) {
                trajectory = trajectory.slice(-maxDataPoints);
            }

            const labels = trajectory.map((_, i) => i);
            const entropies = trajectory.map(p => p.entropy);
            const threshold = trajectory.map(() => 0.15); // Default threshold
            const valleyPoints = trajectory.map(p => p.is_valley ? p.entropy : null);

            chart.data.labels = labels;
            chart.data.datasets[0].data = entropies;
            chart.data.datasets[1].data = threshold;
            chart.data.datasets[2].data = valleyPoints;
            chart.update('none');
        }

        function updateStats(data) {
            document.getElementById('tokens').textContent = data.token_count || 0;
            document.getElementById('valleys').textContent = data.valley_count || 0;
            
            if (data.current_entropy !== undefined) {
                document.getElementById('currentEntropy').textContent = data.current_entropy.toFixed(3);
            }
            if (data.mean_entropy !== undefined) {
                document.getElementById('meanEntropy').textContent = data.mean_entropy.toFixed(3);
            }
            
            if (data.exited_early) {
                document.getElementById('status').innerHTML = '<span class="status-badge status-exited">Exited Early</span>';
                if (data.tokens_saved && data.tokens_total) {
                    const savedPct = Math.round((data.tokens_saved / data.tokens_total) * 100);
                    document.getElementById('saved').textContent = savedPct + '%';
                }
                if (data.cost_saved) {
                    document.getElementById('costSaved').textContent = '$' + data.cost_saved.toFixed(4);
                }
            } else if (data.active) {
                document.getElementById('status').innerHTML = '<span class="status-badge status-active">Active</span>';
                document.getElementById('saved').textContent = '-';
                document.getElementById('costSaved').textContent = '-';
            } else {
                document.getElementById('status').innerHTML = '<span class="status-badge status-idle">Idle</span>';
            }
        }

        // Initialize on load
        initChart();

        // WebSocket connection
        const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
        const ws = new WebSocket(`${protocol}//${location.host}/ws`);
        
        ws.onopen = () => {
            document.getElementById('connectionStatus').className = 'connection-status connected';
            document.getElementById('connectionStatus').textContent = 'Connected - Waiting for data';
        };
        
        ws.onclose = () => {
            document.getElementById('connectionStatus').className = 'connection-status disconnected';
            document.getElementById('connectionStatus').textContent = 'Disconnected - Reconnecting...';
            setTimeout(() => location.reload(), 3000);
        };
        
        ws.onerror = () => {
            document.getElementById('connectionStatus').className = 'connection-status disconnected';
            document.getElementById('connectionStatus').textContent = 'Connection error';
        };
        
        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                updateChart(data);
                updateStats(data);
            } catch (e) {
                console.error('Parse error:', e);
            }
        };
    </script>
</body>
</html>
"""


class Dashboard:
    """Real-time dashboard server."""
    
    def __init__(self, config: DashboardConfig):
        self.config = config
        self.app = FastAPI(title="Entroplain Dashboard")
        self._websocket_clients: List[WebSocket] = []
        self._current_data: Dict[str, Any] = {
            "trajectory": [],
            "token_count": 0,
            "valley_count": 0,
            "current_entropy": 0,
            "mean_entropy": 0,
            "active": False,
            "exited_early": False,
        }
        self._setup_routes()
    
    def _setup_routes(self):
        @self.app.get("/")
        async def root():
            return HTMLResponse(content=DASHBOARD_HTML)
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            self._websocket_clients.append(websocket)
            try:
                # Send initial state
                await websocket.send_json(self._current_data)
                # Keep connection alive
                while True:
                    data = await websocket.receive_text()
                    # Echo back current state on any message
                    await websocket.send_json(self._current_data)
            except WebSocketDisconnect:
                if websocket in self._websocket_clients:
                    self._websocket_clients.remove(websocket)
            except Exception:
                if websocket in self._websocket_clients:
                    self._websocket_clients.remove(websocket)
    
    async def broadcast_update(self, data: Dict[str, Any]):
        """Broadcast entropy data to all connected clients."""
        self._current_data = data
        dead_clients = []
        for client in self._websocket_clients:
            try:
                await client.send_json(data)
            except Exception:
                dead_clients.append(client)
        for client in dead_clients:
            if client in self._websocket_clients:
                self._websocket_clients.remove(client)
    
    def run(self):
        """Start the dashboard server."""
        uvicorn.run(self.app, host="0.0.0.0", port=self.config.port)


def main():
    """CLI entry point for the dashboard."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Entroplain Dashboard")
    parser.add_argument("--port", type=int, default=8050, help="Dashboard port")
    parser.add_argument("--proxy-port", type=int, default=8765, help="Proxy port to monitor")
    args = parser.parse_args()
    
    config = DashboardConfig(port=args.port, proxy_port=args.proxy_port)
    dashboard = Dashboard(config)
    
    print(f"""
==============================================================
  ENTROPPLAIN DASHBOARD
==============================================================
  Dashboard: http://localhost:{args.port}
  Monitoring proxy on port {args.proxy_port}
==============================================================
  Open the dashboard to see real-time entropy visualization
==============================================================
""")
    
    dashboard.run()


if __name__ == "__main__":
    main()
