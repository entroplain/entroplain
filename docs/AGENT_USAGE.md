# Entroplain Usage Guide for Agents

## Quick Setup

### For OpenClaw/Claude Code (Proxy Method)

Run the entropy proxy and point your agent to it:

```bash
# Start the proxy (monitors entropy, enables early exit)
python -m entroplain.proxy --port 8765 --log-entropy

# Set environment to use proxy
export OPENAI_BASE_URL=http://localhost:8765/v1
# or for NVIDIA:
export NVIDIA_BASE_URL=http://localhost:8765/v1
```

Now OpenClaw/Claude Code will automatically have entropy monitoring!

### How the Proxy Works

```
Agent -> Proxy (localhost:8765) -> Real API
           |
           v
      Entropy Monitor
           |
           v
      Early Exit Check
```

The proxy:
1. Intercepts all chat completion requests
2. Enables logprobs automatically
3. Calculates entropy for each token
4. Terminates stream when reasoning converges
5. Passes everything through unchanged to the agent

---

## Direct Usage (Python)

```python
from entroplain import EntropyMonitor, NVIDIAProvider

monitor = EntropyMonitor()
provider = NVIDIAProvider()

for token in provider.stream_with_entropy(
    model="meta/llama-3.1-70b-instruct",
    messages=[{"role": "user", "content": "Solve: x^2 = 16"}]
):
    monitor.track(token.token, token.entropy)
    print(token.token, end="")
    
    if monitor.should_exit():
        print("\n[Early exit - reasoning converged]")
        break

print(f"\nStats: {monitor.get_stats()}")
```

---

## Supported Providers

| Provider | Works? | How |
|----------|--------|-----|
| OpenAI | YES | `logprobs: true` |
| NVIDIA NIM | YES | OpenAI-compatible |
| Anthropic Claude 4 | YES | `logprobs: True` |
| Google Gemini | YES | `response_logprobs=True` |
| Ollama (local) | YES | Built-in logit access |
| llama.cpp | YES | Built-in logit access |

---

## Configuration

### Exit Conditions

```python
monitor = EntropyMonitor(
    entropy_threshold=0.15,  # Exit when entropy drops below this
    min_valleys=2,           # Require N reasoning milestones
    min_tokens=50,           # Don't exit before this many tokens
    velocity_threshold=0.05, # Exit when change rate stabilizes
    exit_condition="combined"  # or: "valleys_plateau", "entropy_drop", "velocity_zero"
)
```

### Environment Variables

```bash
# API keys (used by providers)
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export NVIDIA_API_KEY=nvapi-...
export GOOGLE_API_KEY=...

# For proxy
export ENTROPPLAIN_PORT=8765
export ENTROPPLAIN_LOG_ENTROPY=true
```

---

## CLI

```bash
# Analyze a prompt
entroplain analyze "What is 2+2?" --model gpt-4o

# Stream with early exit
entroplain stream "Explain quantum computing" --exit-on-converge

# Run proxy
entroplain proxy --port 8765 --log-entropy
```

---

## Agent Integration Examples

### OpenClaw with Proxy

```yaml
# In config.yaml
llm:
  provider: openai-compatible
  base_url: http://localhost:8765/v1  # Point to proxy
  primary_model: meta/llama-3.1-70b-instruct
```

### Claude Code with Proxy

Set environment before running:
```bash
export ANTHROPIC_BASE_URL=http://localhost:8765/v1
claude
```

### Custom Agent

```python
from entroplain.hooks import EntropyHook

hook = EntropyHook(config={"entropy_threshold": 0.15})

for token in your_agent.generate_stream():
    result = hook.on_token(token.text, token.entropy)
    
    if result["should_exit"]:
        print(f"Early exit at token {result['index']}")
        break
```

---

## Troubleshooting

### "No logprobs returned"
Some models don't support logprobs. Try a different model or check provider docs.

### "Entropy is always 0"
Make sure `logprobs: true` and `top_logprobs: 5` are set in your API request.

### "Proxy won't start"
Install dependencies: `pip install entroplain[all] fastapi uvicorn httpx`

---

## Learn More

- GitHub: https://github.com/entroplain/entroplain
- PyPI: https://pypi.org/project/entroplain/
- npm: https://www.npmjs.com/package/entroplain
