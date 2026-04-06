"""
Real-time entropy visualization dashboard.

Run with: entroplain-dashboard --port 8765
Then open: http://localhost:8050
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn


@dataclass
class DashboardConfig:
    """Configuration for the dashboard."""
    port: int = 8050
    proxy_port: int = 8765
    update_interval_ms: int = 100


# HTML template for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Entroplain Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
            color: #4ade80;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 20px;
        }
        .chart-container {
            background: #1a1a1a;
            border-radius: 8px;
            padding: 20px;
        }
        .stats-panel {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .stat-card {
            background: #1a1a1a;
            border-radius: 8px;
            padding: 15px;
        }
        .stat-label {
            font-size: 12px;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .stat-value {
            font-size: 32px;
            font-weight: 600;
            color: #fff;
            margin-top: 5px;
        }
        .stat-value.savings { color: #4ade80; }
        .stat-value.cost { color: #fbbf24; }
        .valleys { color: #60a5fa; }
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }
        .status-active { background: #22c55e; color: #000; }
        .status-idle { background: #374151; color: #888; }
        .status-exited { background: #f59e0b; color: #000; }
        #status { margin-top: 10px; }
        .legend {
            display: flex;
            gap: 20px;
            margin-top: 15px;
            font-size: 12px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .legend-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }
        .dot-entropy { background: #60a5fa; }
        .dot-valley { background: #f59e0b; }
        .dot-threshold { background: #ef4444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Entroplain Dashboard</h1>
        
        <div class="grid">
            <div class="chart-container">
                <canvas id="entropyChart" height="300"></canvas>
                <div class="legend">
                    <div class="legend-item">
                        <div class="legend-dot dot-entropy"></div>
                        <span>Entropy</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-dot dot-valley"></div>
                        <span>Valley Detected</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-dot dot-threshold"></div>
                        <span>Threshold (0.15)</span>
                    </div>
                </div>
            </div>
            
            <div class="stats-panel">
                <div class="stat-card">
                    <div class="stat-label">Status</div>
                    <div id="status">
                        <span class="status-badge status-idle">Idle</span>
                    </div>
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
                    <div class="stat-value savings" id="saved">0%</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-label">Cost Saved</div>
                    <div class="stat-value cost" id="costSaved">$0.00</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('entropyChart').getContext('2d');
        
        const chart = new Chart(ctx, {
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
                    },
                    {
                        label: 'Threshold',
                        data: [],
                        borderColor: '#ef4444',
                        borderDash: [5, 5],
                        pointRadius: 0,
                        fill: false,
                    },
                    {
                        label: 'Valleys',
                        data: [],
                        borderColor: '#f59e0b',
                        pointBackgroundColor: '#f59e0b',
                        pointRadius: 6,
                        showLine: false,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: { duration: 0 },
                scales: {
                    x: {
                        title: { display: true, text: 'Tokens', color: '#888' },
                        grid: { color: '#333' },
                        ticks: { color: '#888' }
                    },
                    y: {
                        title: { display: true, text: 'Entropy (bits)', color: '#888' },
                        min: 0,
                        max: 1,
                        grid: { color: '#333' },
                        ticks: { color: '#888' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });

        const ws = new WebSocket(`ws://${location.host}/ws`);
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            updateChart(data);
            updateStats(data);
        };

        function updateChart(data) {
            const labels = data.trajectory.map((_, i) => i);
            const entropies = data.trajectory.map(p => p.entropy);
            const threshold = data.trajectory.map(() => data.threshold || 0.15);
            
            // Mark valleys
            const valleyPoints = data.trajectory.map(p => 
                p.is_valley ? p.entropy : null
            );

            chart.data.labels = labels;
            chart.data.datasets[0].data = entropies;
            chart.data.datasets[1].data = threshold;
            chart.data.datasets[2].data = valleyPoints;
            chart.update();
        }

        function updateStats(data) {
            document.getElementById('tokens').textContent = data.token_count;
            document.getElementById('valleys').textContent = data.valley_count;
            document.getElementById('currentEntropy').textContent = 
                data.current_entropy ? data.current_entropy.toFixed(3) : '-';
            document.getElementById('meanEntropy').textContent = 
                data.mean_entropy ? data.mean_entropy.toFixed(3) : '-';
            
            // Calculate savings
            if (data.exited_early) {
                const savedPct = Math.round((data.tokens_saved / data.tokens_total) * 100);
                document.getElementById('saved').textContent = savedPct + '%';
                document.getElementById('costSaved').textContent = '$' + data.cost_saved.toFixed(4);
            }
            
            // Update status
            const statusEl = document.getElementById('status');
            if (data.exited_early) {
                statusEl.innerHTML = '<span class="status-badge status-exited">Exited Early</span>';
            } else if (data.active) {
                statusEl.innerHTML = '<span class="status-badge status-active">Active</span>';
            } else {
                statusEl.innerHTML = '<span class="status-badge status-idle">Idle</span>';
            }
        }
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
                while True:
                    # Keep connection alive
                    data = await websocket.receive_text()
            except Exception:
                self._websocket_clients.remove(websocket)
    
    async def broadcast_update(self, data: Dict[str, Any]):
        """Broadcast entropy data to all connected clients."""
        self._current_data = data
        for client in self._websocket_clients:
            try:
                await client.send_json(data)
            except Exception:
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
