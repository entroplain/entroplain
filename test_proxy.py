"""Test the proxy with a real API call."""

import requests
import json

# Test health endpoint
try:
    response = requests.get("http://localhost:8765/health")
    print(f"Health check: {response.status_code}")
    print(response.json())
except Exception as e:
    print(f"Proxy not running: {e}")
    print("\nTo test the proxy, run:")
    print("  entroplain-proxy --port 8765")
    print("\nThen in another terminal:")
    print("  python test_proxy.py")
