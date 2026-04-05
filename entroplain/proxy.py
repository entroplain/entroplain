"""
Entropy Monitoring Proxy for OpenClaw/Claude Code.

This proxy intercepts LLM API calls and adds entropy monitoring,
enabling early exit without modifying the agent framework itself.

Usage:
    # Set as your API endpoint
    export OPENAI_BASE_URL=http://localhost:8765
    
    # Run the proxy
    python -m entroplain.proxy --port 8765 --provider openai
"""

import json
import asyncio
import logging
from typing import Optional, Dict, Any, AsyncIterator
from dataclasses import dataclass
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
import uvicorn

from .monitor import EntropyMonitor

logger = logging.getLogger(__name__)


@dataclass
class ProxyConfig:
    """Configuration for the entropy proxy."""
    port: int = 8765
    provider: str = "openai"  # openai, anthropic, nvidia
    api_base: str = "https://api.openai.com/v1"
    entropy_threshold: float = 0.15
    min_valleys: int = 2
    min_tokens: int = 50
    velocity_threshold: float = 0.05
    enable_early_exit: bool = True
    log_entropy: bool = True


class EntropyProxy:
    """
    Proxy that adds entropy monitoring to LLM API calls.
    
    Intercepts streaming responses, calculates entropy, and can
    terminate early when reasoning has converged.
    """
    
    def __init__(self, config: ProxyConfig):
        self.config = config
        self.monitor = EntropyMonitor(
            entropy_threshold=config.entropy_threshold,
            min_valleys=config.min_valleys,
            min_tokens=config.min_tokens,
            velocity_threshold=config.velocity_threshold
        )
        self.app = FastAPI(title="Entroplain Proxy")
        self._setup_routes()
    
    def _setup_routes(self):
        @self.app.post("/v1/chat/completions")
        async def chat_completions(request: Request):
            return await self._handle_chat(request)
        
        @self.app.get("/health")
        async def health():
            return {"status": "ok", "monitor": self.monitor.get_stats()}
        
        @self.app.post("/reset")
        async def reset():
            self.monitor.reset()
            return {"status": "reset"}
    
    async def _handle_chat(self, request: Request):
        """Handle chat completion requests with entropy monitoring."""
        body = await request.json()
        
        # Ensure logprobs are enabled for entropy calculation
        if "logprobs" not in body:
            body["logprobs"] = True
        if "top_logprobs" not in body:
            body["top_logprobs"] = 5
        
        # Reset monitor for new request
        self.monitor.reset()
        
        # Forward request to actual API
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
            # Non-streaming: just return response
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        
        # Streaming: monitor entropy and potentially exit early
        return StreamingResponse(
            self._stream_with_entropy(response),
            media_type="text/event-stream"
        )
    
    async def _stream_with_entropy(
        self, response: httpx.Response
    ) -> AsyncIterator[str]:
        """Stream response with entropy monitoring."""
        exited_early = False
        full_content = ""
        
        async for line in response.aiter_lines():
            if not line.startswith("data: "):
                yield line + "\n"
                continue
            
            data = line[6:]  # Remove "data: " prefix
            if data == "[DONE]":
                yield line + "\n"
                break
            
            try:
                chunk = json.loads(data)
            except json.JSONDecodeError:
                yield line + "\n"
                continue
            
            # Extract token and logprobs
            if chunk.get("choices"):
                choice = chunk["choices"][0]
                
                # Get token content
                if choice.get("delta", {}).get("content"):
                    token = choice["delta"]["content"]
                    full_content += token
                
                # Calculate entropy from logprobs (handle null)
                logprobs = choice.get("logprobs")
                if logprobs and logprobs.get("content"):
                    logprobs_data = logprobs["content"]
                    if logprobs_data:
                        entropy = self._calculate_entropy(logprobs_data[0])
                        self.monitor.track(token, entropy)
                        
                        if self.config.log_entropy:
                            logger.info(
                                f"Token: {repr(token)}, Entropy: {entropy:.4f}, "
                                f"Valleys: {len(self.monitor.get_valleys())}"
                            )
                        
                        # Check for early exit
                        if (
                            self.config.enable_early_exit 
                            and self.monitor.should_exit()
                        ):
                            logger.info(
                                f"Early exit triggered! "
                                f"Tokens: {len(full_content)}, "
                                f"Valleys: {len(self.monitor.get_valleys())}"
                            )
                            exited_early = True
                            yield "data: [DONE]\n\n"
                            break
            
            yield line + "\n"
        
        if not exited_early:
            logger.info(
                f"Stream completed. "
                f"Tokens: {self.monitor.get_stats()['token_count']}, "
                f"Valleys: {len(self.monitor.get_valleys())}"
            )
    
    def _calculate_entropy(self, logprobs_data: Dict) -> float:
        """Calculate Shannon entropy from logprobs."""
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
        """Start the proxy server."""
        uvicorn.run(self.app, host="0.0.0.0", port=self.config.port)


def main():
    """CLI entry point for running the proxy."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Entropy Monitoring Proxy")
    parser.add_argument("--port", type=int, default=8765, help="Proxy port")
    parser.add_argument(
        "--provider", 
        default="openai", 
        choices=["openai", "anthropic", "nvidia"],
        help="LLM provider"
    )
    parser.add_argument(
        "--api-base",
        default="https://api.openai.com/v1",
        help="API base URL"
    )
    parser.add_argument(
        "--entropy-threshold",
        type=float,
        default=0.15,
        help="Entropy threshold for early exit"
    )
    parser.add_argument(
        "--min-valleys",
        type=int,
        default=2,
        help="Minimum valleys before early exit"
    )
    parser.add_argument(
        "--no-early-exit",
        action="store_true",
        help="Disable early exit (monitor only)"
    )
    parser.add_argument(
        "--log-entropy",
        action="store_true",
        help="Log entropy values to console"
    )
    
    args = parser.parse_args()
    
    config = ProxyConfig(
        port=args.port,
        provider=args.provider,
        api_base=args.api_base,
        entropy_threshold=args.entropy_threshold,
        min_valleys=args.min_valleys,
        enable_early_exit=not args.no_early_exit,
        log_entropy=args.log_entropy
    )
    
    proxy = EntropyProxy(config)
    
    # Clean banner with fixed formatting
    print("\n" + "="*62)
    print("  ENTROPPLAIN ENTROPY MONITORING PROXY")
    print("="*62)
    print(f"  Proxy:      http://localhost:{args.port}")
    print(f"  Provider:   {args.provider}")
    print(f"  API Base:   {args.api_base}")
    print(f"  Early Exit: {'ENABLED' if not args.no_early_exit else 'DISABLED'}")
    print("="*62)
    print("  Usage:")
    print(f"    export OPENAI_BASE_URL=http://localhost:{args.port}")
    print("    # or for NVIDIA:")
    print(f"    export NVIDIA_BASE_URL=http://localhost:{args.port}")
    print("="*62 + "\n")
    
    proxy.run()


if __name__ == "__main__":
    main()
