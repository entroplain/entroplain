"""
Provider integrations for entropy extraction.
"""

import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncIterator, Iterator
from dataclasses import dataclass


@dataclass
class TokenWithEntropy:
    """A token with its entropy value."""
    token: str
    entropy: float
    logprob: float
    top_logprobs: List[Dict[str, float]]


class BaseProvider(ABC):
    """Base class for LLM providers."""
    
    @abstractmethod
    def calculate_entropy(self, response: Any) -> float:
        """Calculate entropy from provider response."""
        pass
    
    @abstractmethod
    def stream_with_entropy(self, *args, **kwargs) -> Iterator[TokenWithEntropy]:
        """Stream tokens with entropy values."""
        pass
    
    @abstractmethod
    async def astream_with_entropy(self, *args, **kwargs) -> AsyncIterator[TokenWithEntropy]:
        """Async stream tokens with entropy values."""
        pass


class OpenAIProvider(BaseProvider):
    """
    Provider for OpenAI GPT models.
    
    Usage:
        provider = OpenAIProvider(api_key="sk-...")
        
        for token in provider.stream_with_entropy(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello"}]
        ):
            print(f"{token.token} (entropy: {token.entropy:.3f})")
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.api_key)
        return self._client
    
    def calculate_entropy(self, logprobs_data: Dict) -> float:
        """Calculate entropy from OpenAI logprobs format."""
        if not logprobs_data or "top_logprobs" not in logprobs_data:
            return 0.0
        
        import math
        entropy = 0.0
        for lp in logprobs_data["top_logprobs"]:
            prob = math.exp(lp["logprob"])
            if prob > 0:
                entropy -= prob * math.log2(prob + 1e-10)
        return entropy
    
    def stream_with_entropy(
        self,
        model: str = "gpt-4o",
        messages: List[Dict] = None,
        **kwargs
    ) -> Iterator[TokenWithEntropy]:
        """Stream tokens with entropy."""
        # Ensure logprobs are enabled
        kwargs["logprobs"] = True
        kwargs["top_logprobs"] = kwargs.get("top_logprobs", 5)
        
        response = self.client.chat.completions.create(
            model=model,
            messages=messages or [],
            stream=True,
            **kwargs
        )
        
        for chunk in response:
            if not chunk.choices:
                continue
            
            choice = chunk.choices[0]
            
            if choice.delta and choice.delta.content:
                logprobs_data = getattr(choice, "logprobs", None)
                if logprobs_data and logprobs_data.content:
                    for content in logprobs_data.content:
                        entropy = self.calculate_entropy(content)
                        yield TokenWithEntropy(
                            token=content.get("token", ""),
                            entropy=entropy,
                            logprob=content.get("logprob", 0),
                            top_logprobs=content.get("top_logprobs", [])
                        )
    
    async def astream_with_entropy(self, *args, **kwargs) -> AsyncIterator[TokenWithEntropy]:
        """Async version of stream_with_entropy."""
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(api_key=self.api_key)
        kwargs["logprobs"] = True
        kwargs["top_logprobs"] = kwargs.get("top_logprobs", 5)
        
        response = await client.chat.completions.create(
            stream=True,
            *args,
            **kwargs
        )
        
        async for chunk in response:
            if not chunk.choices:
                continue
            
            choice = chunk.choices[0]
            
            if choice.delta and choice.delta.content:
                logprobs_data = getattr(choice, "logprobs", None)
                if logprobs_data and logprobs_data.content:
                    for content in logprobs_data.content:
                        entropy = self.calculate_entropy(content)
                        yield TokenWithEntropy(
                            token=content.get("token", ""),
                            entropy=entropy,
                            logprob=content.get("logprob", 0),
                            top_logprobs=content.get("top_logprobs", [])
                        )


class AnthropicProvider(BaseProvider):
    """
    Provider for Anthropic Claude models.
    
    Usage:
        provider = AnthropicProvider(api_key="sk-ant-...")
        
        for token in provider.stream_with_entropy(
            model="claude-sonnet-4-20250514",
            messages=[{"role": "user", "content": "Hello"}]
        ):
            print(f"{token.token} (entropy: {token.entropy:.3f})")
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client
    
    def calculate_entropy(self, logprobs_data: Dict) -> float:
        """Calculate entropy from Anthropic logprobs format."""
        if not logprobs_data or "top_logprobs" not in logprobs_data:
            return 0.0
        
        import math
        entropy = 0.0
        for lp in logprobs_data["top_logprobs"]:
            prob = math.exp(lp["logprob"])
            if prob > 0:
                entropy -= prob * math.log2(prob + 1e-10)
        return entropy
    
    def stream_with_entropy(
        self,
        model: str = "claude-sonnet-4-20250514",
        messages: List[Dict] = None,
        **kwargs
    ) -> Iterator[TokenWithEntropy]:
        """Stream tokens with entropy."""
        kwargs["logprobs"] = True
        kwargs["top_logprobs"] = kwargs.get("top_logprobs", 5)
        
        with self.client.messages.stream(
            model=model,
            messages=messages or [],
            **kwargs
        ) as stream:
            for event in stream:
                if event.type == "content_block_delta":
                    # Claude doesn't expose per-token logprobs in streaming
                    # We approximate from the delta
                    delta = event.delta
                    if hasattr(delta, "text"):
                        yield TokenWithEntropy(
                            token=delta.text,
                            entropy=0.0,  # Not available in streaming
                            logprob=0.0,
                            top_logprobs=[]
                        )
    
    async def astream_with_entropy(self, *args, **kwargs) -> AsyncIterator[TokenWithEntropy]:
        """Async version (not implemented for Anthropic)."""
        raise NotImplementedError("Use sync streaming for Anthropic")


class GeminiProvider(BaseProvider):
    """
    Provider for Google Gemini models.
    
    Usage:
        provider = GeminiProvider(api_key="...")
        
        for token in provider.stream_with_entropy(
            model="gemini-2.0-flash",
            prompt="Hello"
        ):
            print(f"{token.token} (entropy: {token.entropy:.3f})")
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._client = genai
        return self._client
    
    def calculate_entropy(self, logprobs_data: Dict) -> float:
        """Calculate entropy from Gemini logprobs format."""
        if not logprobs_data:
            return 0.0
        
        import math
        entropy = 0.0
        
        candidates = logprobs_data.get("candidates", [])
        if candidates:
            logprobs = candidates[0].get("logprobs", {})
            for lp in logprobs.get("top_logprobs", []):
                prob = math.exp(lp.get("logprob", 0))
                if prob > 0:
                    entropy -= prob * math.log2(prob + 1e-10)
        
        return entropy
    
    def stream_with_entropy(
        self,
        model: str = "gemini-2.0-flash",
        prompt: str = "",
        **kwargs
    ) -> Iterator[TokenWithEntropy]:
        """Stream tokens with entropy."""
        model_instance = self.client.GenerativeModel(model)
        
        # Enable logprobs in generation config
        generation_config = {
            "response_logprobs": True,
            "logprobs": kwargs.get("top_logprobs", 5)
        }
        
        response = model_instance.generate_content(
            prompt,
            generation_config=generation_config,
            stream=True
        )
        
        for chunk in response:
            if chunk.text:
                # Extract logprobs if available
                logprobs = getattr(chunk, "logprobs", None)
                entropy = self.calculate_entropy({"candidates": [{"logprobs": logprobs}]}) if logprobs else 0.0
                
                yield TokenWithEntropy(
                    token=chunk.text,
                    entropy=entropy,
                    logprob=0.0,
                    top_logprobs=[]
                )
    
    async def astream_with_entropy(self, *args, **kwargs) -> AsyncIterator[TokenWithEntropy]:
        """Async version of stream_with_entropy."""
        # Use the async version of the Gemini SDK
        raise NotImplementedError("Async streaming not yet implemented")


class NVIDIAProvider(BaseProvider):
    """
    Provider for NVIDIA NIM API.
    
    Usage:
        provider = NVIDIAProvider(api_key="nvapi-...")
        
        for token in provider.stream_with_entropy(
            model="meta/llama-3.1-70b-instruct",
            messages=[{"role": "user", "content": "Hello"}]
        ):
            print(f"{token.token} (entropy: {token.entropy:.3f})")
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("NVIDIA_API_KEY")
        self.base_url = "https://integrate.api.nvidia.com/v1"
    
    def calculate_entropy(self, logprobs_data: Dict) -> float:
        """Calculate entropy from NVIDIA logprobs format (OpenAI-compatible)."""
        if not logprobs_data or "top_logprobs" not in logprobs_data:
            return 0.0
        
        import math
        entropy = 0.0
        for lp in logprobs_data["top_logprobs"]:
            prob = math.exp(lp["logprob"])
            if prob > 0:
                entropy -= prob * math.log2(prob + 1e-10)
        return entropy
    
    def stream_with_entropy(
        self,
        model: str = "meta/llama-3.1-70b-instruct",
        messages: List[Dict] = None,
        **kwargs
    ) -> Iterator[TokenWithEntropy]:
        """Stream tokens with entropy via HTTP."""
        import requests
        import json
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages or [],
            "logprobs": True,
            "top_logprobs": kwargs.get("top_logprobs", 5),
            "stream": True,
            **kwargs
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            stream=True
        )
        
        for line in response.iter_lines():
            if not line:
                continue
            
            line = line.decode("utf-8")
            if line.startswith("data: "):
                data = line[6:]
                if data == "[DONE]":
                    break
                
                try:
                    chunk = json.loads(data)
                    if "choices" in chunk:
                        for choice in chunk["choices"]:
                            if "delta" in choice and "content" in choice["delta"]:
                                logprobs_data = choice.get("logprobs"); logprobs = logprobs_data.get("content", []) if logprobs_data else []
                                for lp_data in logprobs:
                                    entropy = self.calculate_entropy(lp_data)
                                    yield TokenWithEntropy(
                                        token=lp_data.get("token", ""),
                                        entropy=entropy,
                                        logprob=lp_data.get("logprob", 0),
                                        top_logprobs=lp_data.get("top_logprobs", [])
                                    )
                except json.JSONDecodeError:
                    continue
    
    async def astream_with_entropy(self, *args, **kwargs) -> AsyncIterator[TokenWithEntropy]:
        """Async version of stream_with_entropy."""
        import aiohttp
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": kwargs.get("model", "meta/llama-3.1-70b-instruct"),
            "messages": kwargs.get("messages", []),
            "logprobs": True,
            "top_logprobs": kwargs.get("top_logprobs", 5),
            "stream": True
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                async for line in response.content:
                    line = line.decode("utf-8").strip()
                    if not line or not line.startswith("data: "):
                        continue
                    
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    
                    import json
                    try:
                        chunk = json.loads(data)
                        if "choices" in chunk:
                            for choice in chunk["choices"]:
                                if "delta" in choice and "content" in choice["delta"]:
                                    logprobs_data = choice.get("logprobs"); logprobs = logprobs_data.get("content", []) if logprobs_data else []
                                    for lp_data in logprobs:
                                        entropy = self.calculate_entropy(lp_data)
                                        yield TokenWithEntropy(
                                            token=lp_data.get("token", ""),
                                            entropy=entropy,
                                            logprob=lp_data.get("logprob", 0),
                                            top_logprobs=lp_data.get("top_logprobs", [])
                                        )
                    except json.JSONDecodeError:
                        continue


class OllamaProvider(BaseProvider):
    """
    Provider for Ollama (local models).
    
    Usage:
        provider = OllamaProvider()
        
        for token in provider.stream_with_entropy(
            model="llama3.1",
            prompt="Hello"
        ):
            print(f"{token.token} (entropy: {token.entropy:.3f})")
    """
    
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host
    
    def calculate_entropy(self, logits: List[float]) -> float:
        """Calculate entropy from logits (requires softmax first)."""
        import math
        
        # Softmax
        max_logit = max(logits)
        exp_logits = [math.exp(l - max_logit) for l in logits]
        sum_exp = sum(exp_logits)
        probs = [e / sum_exp for e in exp_logits]
        
        # Shannon entropy
        entropy = 0.0
        for p in probs:
            if p > 0:
                entropy -= p * math.log2(p)
        
        return entropy
    
    def stream_with_entropy(
        self,
        model: str = "llama3.1",
        prompt: str = "",
        **kwargs
    ) -> Iterator[TokenWithEntropy]:
        """Stream tokens with entropy from Ollama."""
        import requests
        import json
        
        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": True,
                "options": kwargs.get("options", {})
            },
            stream=True
        )
        
        for line in response.iter_lines():
            if not line:
                continue
            
            data = json.loads(line)
            token = data.get("response", "")
            
            if token:
                # Note: Ollama doesn't expose logits by default
                # For entropy, you'd need to modify Ollama or use llama.cpp directly
                yield TokenWithEntropy(
                    token=token,
                    entropy=0.0,  # Would need logits
                    logprob=0.0,
                    top_logprobs=[]
                )
    
    async def astream_with_entropy(self, *args, **kwargs) -> AsyncIterator[TokenWithEntropy]:
        """Async version of stream_with_entropy."""
        import aiohttp
        import json
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.host}/api/generate",
                json={
                    "model": kwargs.get("model", "llama3.1"),
                    "prompt": kwargs.get("prompt", ""),
                    "stream": True
                }
            ) as response:
                async for line in response.content:
                    line = line.decode("utf-8").strip()
                    if not line:
                        continue
                    
                    data = json.loads(line)
                    token = data.get("response", "")
                    
                    if token:
                        yield TokenWithEntropy(
                            token=token,
                            entropy=0.0,
                            logprob=0.0,
                            top_logprobs=[]
                        )


class LlamaCppProvider(BaseProvider):
    """
    Provider for llama.cpp (direct Python bindings).
    
    This provides full access to logits for accurate entropy calculation.
    
    Usage:
        provider = LlamaCppProvider(model_path="./llama-3.1.gguf")
        
        for token in provider.stream_with_entropy(prompt="Hello"):
            print(f"{token.token} (entropy: {token.entropy:.3f})")
    """
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self._model = None
    
    @property
    def model(self):
        if self._model is None:
            from llama_cpp import Llama
            self._model = Llama(
                model_path=self.model_path,
                logits_all=True,  # Required for entropy tracking
                verbose=False
            )
        return self._model
    
    def calculate_entropy(self, logits: List[float]) -> float:
        """Calculate entropy from raw logits."""
        import math
        import numpy as np
        
        # Softmax
        logits = np.array(logits)
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / exp_logits.sum()
        
        # Shannon entropy
        entropy = -np.sum(probs[probs > 0] * np.log2(probs[probs > 0]))
        
        return float(entropy)
    
    def stream_with_entropy(
        self,
        prompt: str = "",
        max_tokens: int = 512,
        **kwargs
    ) -> Iterator[TokenWithEntropy]:
        """Stream tokens with entropy from llama.cpp."""
        generator = self.model.create_completion(
            prompt=prompt,
            max_tokens=max_tokens,
            stream=True,
            **kwargs
        )
        
        for chunk in generator:
            if "choices" in chunk:
                for choice in chunk["choices"]:
                    token = choice.get("text", "")
                    if token:
                        # Get logits from the last token
                        # Note: This requires logits_all=True
                        logits = self.model._ctx.get_logits()
                        entropy = self.calculate_entropy(logits)
                        
                        yield TokenWithEntropy(
                            token=token,
                            entropy=entropy,
                            logprob=0.0,
                            top_logprobs=[]
                        )
    
    async def astream_with_entropy(self, *args, **kwargs) -> AsyncIterator[TokenWithEntropy]:
        """Async version (run in thread pool)."""
        import asyncio
        
        loop = asyncio.get_event_loop()
        for token in self.stream_with_entropy(*args, **kwargs):
            yield token
            await asyncio.sleep(0)  # Yield control
