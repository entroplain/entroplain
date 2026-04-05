"""Test the proxy with NVIDIA API."""

import requests
import json
import os

# Get API key from environment
api_key = os.environ.get("NVIDIA_API_KEY", "")

if not api_key:
    print("ERROR: NVIDIA_API_KEY not set")
    exit(1)

# Make request through proxy
response = requests.post(
    "http://localhost:8766/v1/chat/completions",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    },
    json={
        "model": "meta/llama-3.1-70b-instruct",
        "messages": [{"role": "user", "content": "What is 2+2? Just answer the number."}],
        "max_tokens": 50,
        "temperature": 0.1,
        "stream": True
    },
    stream=True
)

print(f"Status: {response.status_code}")
print("Streaming response:")
print("-" * 40)

for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith("data: "):
            data = line[6:]
            if data == "[DONE]":
                print("\n[DONE]")
                break
            try:
                chunk = json.loads(data)
                if chunk.get("choices"):
                    delta = chunk["choices"][0].get("delta", {})
                    if delta.get("content"):
                        print(delta["content"], end="", flush=True)
            except json.JSONDecodeError:
                pass

print("\n" + "-" * 40)

# Check proxy health
health = requests.get("http://localhost:8766/health")
print(f"\nProxy stats: {health.json()}")
