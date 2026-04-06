"""
Entropy Monitoring Proxy with built-in Dashboard.

This proxy intercepts LLM API calls and adds entropy monitoring,
enabling early exit without modifying the agent framework itself.

Usage:
    # Set as your API endpoint
    export OPENAI_BASE_URL=http://localhost:8765
    
    # Run the proxy (includes dashboard at /dashboard)
    python -m entroplain.proxy --port 8765 --provider openai
"""

import json
import asyncio
import logging
from typing import Optional, Dict, Any, AsyncIterator, List
from dataclasses import dataclass
import httpx
from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse, HTMLResponse
import uvicorn

from .monitor import EntropyMonitor
from .cost_tracker import CostTracker, format_cost_report

logger = logging.getLogger(__name__)


# Dashboard HTML - embedded in proxy
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
            min-height: 200px;
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
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 11px;
            margin-bottom: 10px;
        }
        .connected { background: #166534; color: #4ade80; }
        .disconnected { background: #7f1d1d; color: #fca5a5; }
        
        .waiting-message {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: #666;
        }
        .waiting-message h2 { font-size: 14px; margin-bottom: 5px; }
        .waiting-message p { font-size: 11px; }
    </style>
</head>
<body>
    <div class="app">
        <h1>🎯 Entroplain Dashboard</h1>
        
        <div class="main-grid">
            <div class="chart-container">
                <div id="connectionStatus" class="connection-status disconnected">Connecting...</div>
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
                    <div class="stat-label">Tokens</div>
                    <div class="stat-value" id="tokens">0</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Valleys</div>
                    <div class="stat-value valleys" id="valleys">0</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Entropy</div>
                    <div class="stat-value" id="currentEntropy">-</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Mean</div>
                    <div class="stat-value" id="meanEntropy">-</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Saved</div>
                    <div class="stat-value savings" id="saved">-</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let chart = null;
        let hasData = false;
        const maxPoints = 200;

        function initChart() {
            const ctx = document.getElementById('entropyChart').getContext('2d');
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        { label: 'Entropy', data: [], borderColor: '#60a5fa', backgroundColor: 'rgba(96, 165, 250, 0.1)', fill: true, tension: 0.3, pointRadius: 0, borderWidth: 2 },
                        { label: 'Threshold', data: [], borderColor: '#ef4444', borderDash: [5, 5], pointRadius: 0, fill: false, borderWidth: 1 },
                        { label: 'Valleys', data: [], borderColor: '#f59e0b', pointBackgroundColor: '#f59e0b', pointRadius: 5, showLine: false }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: { duration: 0 },
                    scales: {
                        x: { title: { display: true, text: 'Tokens', color: '#888' }, grid: { color: '#222' }, ticks: { color: '#666', maxTicksLimit: 10 } },
                        y: { title: { display: true, text: 'Entropy', color: '#888' }, min: 0, max: 1, grid: { color: '#222' }, ticks: { color: '#666' } }
                    },
                    plugins: { legend: { display: false } }
                }
            });
        }

        function updateChart(data) {
            if (!chart || !data.trajectory || data.trajectory.length === 0) return;
            
            if (!hasData) {
                hasData = true;
                document.getElementById('waitingMessage').style.display = 'none';
                document.getElementById('connectionStatus').className = 'connection-status connected';
                document.getElementById('connectionStatus').textContent = 'Live';
            }
            
            let traj = data.trajectory.slice(-maxPoints);
            chart.data.labels = traj.map((_, i) => i);
            chart.data.datasets[0].data = traj.map(p => p.entropy);
            chart.data.datasets[1].data = traj.map(() => 0.15);
            chart.data.datasets[2].data = traj.map(p => p.is_valley ? p.entropy : null);
            chart.update('none');
        }

        function updateStats(data) {
            document.getElementById('tokens').textContent = data.token_count || 0;
            document.getElementById('valleys').textContent = data.valley_count || 0;
            if (data.current_entropy !== undefined) document.getElementById('currentEntropy').textContent = data.current_entropy.toFixed(3);
            if (data.mean_entropy !== undefined) document.getElementById('meanEntropy').textContent = data.mean_entropy.toFixed(3);
            
            if (data.exited_early) {
                document.getElementById('status').innerHTML = '<span class="status-badge status-exited">Exited</span>';
                if (data.cost_saved) document.getElementById('saved').textContent = '$' + data.cost_saved.toFixed(4);
            } else if (data.active) {
                document.getElementById('status').innerHTML = '<span class="status-badge status-active">Active</span>';
                document.getElementById('saved').textContent = '-';
            } else {
                document.getElementById('status').innerHTML = '<span class="status-badge status-idle">Idle</span>';
            }
        }

        initChart();

        const ws = new WebSocket((location.protocol === 'https:' ? 'wss:' : 'ws:') + '//' + location.host + '/ws');
        ws.onopen = () => { document.getElementById('connectionStatus').className = 'connection-status connected'; document.getElementById('connectionStatus').textContent = 'Connected'; };
        ws.onclose = () => { document.getElementById('connectionStatus').className = 'connection-status disconnected'; document.getElementById('connectionStatus').textContent = 'Disconnected'; };
        ws.onmessage = (e) => { try { const d = JSON.parse(e.data); updateChart(d); updateStats(d); } catch(err) {} };
    </script>
</body>
</html>
"""


@dataclass
class ProxyConfig:
    """Configuration for the entropy proxy."""
    port: int = 8765
    provider: str = "openai"
    api_base: str = "https://api.openai.com/v1"
    model: str = "default"
    entropy_threshold: float = 0.15
    min_valleys: int = 2
    min_tokens: int = 50
    velocity_threshold: float = 0.05
    enable_early_exit: bool = True
    log_entropy: bool = True
    track_cost: bool = True


class EntropyProxy:
    """Proxy that adds entropy monitoring to LLM API calls."""
    
    def __init__(self, config: ProxyConfig):
        self.config = config
        self.monitor = EntropyMonitor(
            entropy_threshold=config.entropy_threshold,
            min_valleys=config.min_valleys,
            min_tokens=config.min_tokens,
            velocity_threshold=config.velocity_threshold
        )
        self.cost_tracker = CostTracker(model=config.model) if config.track_cost else None
        self.app = FastAPI(title="Entroplain Proxy")
        self._ws_clients: List[WebSocket] = []
        self._current_data: Dict[str, Any] = {"trajectory": [], "token_count": 0, "valley_count": 0, "active": False}
        self._setup_routes()
    
    def _setup_routes(self):
        @self.app.get("/")
        async def root():
            return {"service": "Entroplain Proxy", "dashboard": "/dashboard", "health": "/health"}
        
        @self.app.get("/dashboard")
        async def dashboard():
            return HTMLResponse(content=DASHBOARD_HTML)
        
        @self.app.websocket("/ws")
        async def ws_endpoint(websocket: WebSocket):
            await websocket.accept()
            self._ws_clients.append(websocket)
            try:
                await websocket.send_json(self._current_data)
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                if websocket in self._ws_clients:
                    self._ws_clients.remove(websocket)
        
        @self.app.post("/v1/chat/completions")
        async def chat_completions(request: Request):
            return await self._handle_chat(request)
        
        @self.app.get("/health")
        async def health():
            stats = self.monitor.get_stats()
            if self.cost_tracker and self.cost_tracker.output_tokens > 0:
                stats["cost"] = self.cost_tracker.get_stats()
            return {"status": "ok", "monitor": stats}
        
        @self.app.post("/reset")
        async def reset():
            self.monitor.reset()
            if self.cost_tracker:
                self.cost_tracker.reset()
            return {"status": "reset"}
    
    async def _broadcast(self, data: Dict[str, Any]):
        """Broadcast data to all WebSocket clients."""
        self._current_data = data
        for ws in self._ws_clients[:]:
            try:
                await ws.send_json(data)
            except Exception:
                self._ws_clients.remove(ws)
    
    async def _handle_chat(self, request: Request):
        """Handle chat completion requests with entropy monitoring."""
        body = await request.json()
        
        model = body.get("model", "default")
        if self.cost_tracker:
            self.cost_tracker = CostTracker(model=model)
        
        input_tokens = self._estimate_tokens(body.get("messages", []))
        if self.cost_tracker:
            self.cost_tracker.track_input(input_tokens)
        
        if "logprobs" not in body:
            body["logprobs"] = True
        if "top_logprobs" not in body:
            body["top_logprobs"] = 5
        
        self.monitor.reset()
        
        # Broadcast active state
        await self._broadcast({"active": True, "trajectory": [], "token_count": 0, "valley_count": 0})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.config.api_base}/chat/completions",
                json=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": request.headers.get("Authorization", "")
                },
                timeout=120.0
            )
        
        if not body.get("stream", False):
            return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
        
        return StreamingResponse(self._stream_with_entropy(response), media_type="text/event-stream")
    
    def _estimate_tokens(self, messages: list) -> int:
        total = 0
        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, str):
                total += len(content) // 4
            elif isinstance(content, list):
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        total += len(part.get("text", "")) // 4
        return max(total, 10)
    
    async def _stream_with_entropy(self, response: httpx.Response) -> AsyncIterator[str]:
        import math
        exited_early = False
        full_content = ""
        
        async for line in response.aiter_lines():
            if not line.startswith("data: "):
                yield line + "\n"
                continue
            
            data = line[6:]
            if data == "[DONE]":
                yield line + "\n"
                break
            
            try:
                chunk = json.loads(data)
            except json.JSONDecodeError:
                yield line + "\n"
                continue
            
            if chunk.get("choices"):
                choice = chunk["choices"][0]
                
                if choice.get("delta", {}).get("content"):
                    token = choice["delta"]["content"]
                    full_content += token
                    if self.cost_tracker:
                        self.cost_tracker.track_output(1)
                
                logprobs = choice.get("logprobs")
                if logprobs and logprobs.get("content"):
                    logprobs_data = logprobs["content"]
                    if logprobs_data:
                        entropy = self._calculate_entropy(logprobs_data[0])
                        confidence = 0.0
                        if logprobs_data[0].get("top_logprobs"):
                            confidence = math.exp(logprobs_data[0]["top_logprobs"][0]["logprob"])
                        
                        self.monitor.track(token, entropy, confidence)
                        
                        if self.config.log_entropy:
                            logger.info(f"Token: {repr(token)}, Entropy: {entropy:.4f}, Valleys: {len(self.monitor.get_valleys())}")
                        
                        # Broadcast update to dashboard
                        stats = self.monitor.get_stats()
                        await self._broadcast({
                            "active": True,
                            "trajectory": [{"entropy": p.entropy, "is_valley": p.is_valley} for p in self.monitor._trajectory],
                            "token_count": stats["token_count"],
                            "valley_count": stats["valley_count"],
                            "current_entropy": stats["current_entropy"],
                            "mean_entropy": stats["mean_entropy"],
                            "exited_early": False
                        })
                        
                        if self.config.enable_early_exit and self.monitor.should_exit():
                            logger.info(f"Early exit! Tokens: {len(full_content)}, Valleys: {len(self.monitor.get_valleys())}")
                            if self.cost_tracker:
                                estimated_full = len(full_content) * 2.5
                                self.cost_tracker.set_full_estimate(int(estimated_full))
                                estimate = self.cost_tracker.get_estimate()
                                logger.info(f"Cost savings: ${estimate.cost_saved_usd:.4f}")
                                await self._broadcast({
                                    "active": False,
                                    "trajectory": [{"entropy": p.entropy, "is_valley": p.is_valley} for p in self.monitor._trajectory],
                                    "token_count": stats["token_count"],
                                    "valley_count": stats["valley_count"],
                                    "current_entropy": stats["current_entropy"],
                                    "mean_entropy": stats["mean_entropy"],
                                    "exited_early": True,
                                    "cost_saved": estimate.cost_saved_usd
                                })
                            exited_early = True
                            yield "data: [DONE]\n\n"
                            break
            
            yield line + "\n"
        
        if not exited_early:
            stats = self.monitor.get_stats()
            await self._broadcast({
                "active": False,
                "trajectory": [{"entropy": p.entropy, "is_valley": p.is_valley} for p in self.monitor._trajectory],
                "token_count": stats["token_count"],
                "valley_count": stats["valley_count"],
                "current_entropy": stats["current_entropy"],
                "mean_entropy": stats["mean_entropy"],
                "exited_early": False
            })
    
    def _calculate_entropy(self, logprobs_data: Dict) -> float:
        import math
        if not logprobs_data or "top_logprobs" not in logprobs_data:
            return 0.0
        entropy = 0.0
        for lp in logprobs_data["top_logprobs"]:
            prob = math.exp(lp["logprob"])
            if prob > 0:
                entropy -= prob * math.log2(prob + 1e-10)
        return entropy
    
    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=self.config.port)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Entropy Monitoring Proxy")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--provider", default="openai", choices=["openai", "anthropic", "nvidia"])
    parser.add_argument("--api-base", default="https://api.openai.com/v1")
    parser.add_argument("--model", default="default")
    parser.add_argument("--entropy-threshold", type=float, default=0.15)
    parser.add_argument("--min-valleys", type=int, default=2)
    parser.add_argument("--no-early-exit", action="store_true")
    parser.add_argument("--log-entropy", action="store_true")
    parser.add_argument("--no-cost-tracking", action="store_true")
    args = parser.parse_args()
    
    config = ProxyConfig(
        port=args.port,
        provider=args.provider,
        api_base=args.api_base,
        model=args.model,
        entropy_threshold=args.entropy_threshold,
        min_valleys=args.min_valleys,
        enable_early_exit=not args.no_early_exit,
        log_entropy=args.log_entropy,
        track_cost=not args.no_cost_tracking
    )
    
    proxy = EntropyProxy(config)
    
    print(f"\n{'='*62}\n  ENTROPPLAIN PROXY WITH DASHBOARD\n{'='*62}")
    print(f"  Proxy:      http://localhost:{args.port}")
    print(f"  Dashboard:  http://localhost:{args.port}/dashboard")
    print(f"  API Base:   {args.api_base}")
    print(f"{'='*62}\n")
    
    proxy.run()


if __name__ == "__main__":
    main()
