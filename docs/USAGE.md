# Entroplain Documentation

## Installation

### pip (Python)

```bash
# Core package
pip install entroplain

# With provider support
pip install "entroplain[openai]"
pip install "entroplain[anthropic]"
pip install "entroplain[all]"
```

### npm (Node.js)

```bash
npm install entroplain
```

### From Source

```bash
git clone https://github.com/entroplain/entroplain.git
cd entroplain
pip install -e .
```

---

## Quick Start

```python
from entroplain import EntropyMonitor

monitor = EntropyMonitor()

# Track tokens with entropy
monitor.track("The", 0.8)
monitor.track("answer", 0.5)
monitor.track("is", 0.2)

# Check convergence
if monitor.should_exit():
    print("Reasoning complete!")
```

---

## How It Works

### 1. Entropy Calculation

For each token, we calculate **Shannon entropy** from the model's output distribution:

```
H = -Σ p(x) * log₂(p(x))
```

Where `p(x)` is the probability of token x.

### 2. Valley Detection

A **valley** is a local minimum in the entropy trajectory:

```
Token:    A    B    C    D    E
Entropy: 0.8  0.3* 0.7  0.4* 0.9
               ↑         ↑
            Valley 1  Valley 2
```

Valleys indicate moments when the model was confident about the next token — reasoning milestones.

### 3. Exit Conditions

| Condition | When to Exit |
|-----------|--------------|
| `entropy_drop` | Entropy < threshold |
| `valleys_plateau` | Valley count stabilizes |
| `velocity_zero` | Entropy change < threshold |
| `combined` | (entropy_low OR valleys_plateau) AND velocity_stable |

---

## Configuration

```python
monitor = EntropyMonitor(
    # Exit when entropy drops below this
    entropy_threshold=0.15,
    
    # Require at least N valleys
    min_valleys=2,
    
    # Exit when velocity < this
    velocity_threshold=0.05,
    
    # Don't exit before N tokens
    min_tokens=50,
    
    # Exit condition strategy
    exit_condition="combined"  # or "entropy_drop", "valleys_plateau", "velocity_zero"
)
```

### Environment Variables

```bash
# Provider API keys
ENTROPPLAIN_OPENAI_API_KEY=sk-...
ENTROPPLAIN_ANTHROPIC_API_KEY=sk-ant-...
ENTROPPLAIN_NVIDIA_API_KEY=nvapi-...
ENTROPPLAIN_GOOGLE_API_KEY=...

# Local models
ENTROPPLAIN_LOCAL_PROVIDER=ollama
ENTROPPLAIN_LOCAL_MODEL=llama3.1
```

---

## Provider Examples

### OpenAI

```python
from openai import OpenAI
from entroplain import EntropyMonitor

client = OpenAI()
monitor = EntropyMonitor()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    logprobs=True,
    top_logprobs=5,
    stream=True
)

for chunk in response:
    if chunk.choices[0].logprobs:
        for content in chunk.choices[0].logprobs.content:
            entropy = monitor.calculate_entropy(
                [lp["logprob"] for lp in content["top_logprobs"]]
            )
            monitor.track(content["token"], entropy)
            
            if monitor.should_exit():
                break
```

### NVIDIA NIM

```python
from entroplain import NVIDIAProvider, EntropyMonitor

provider = NVIDIAProvider()
monitor = EntropyMonitor()

for token in provider.stream_with_entropy(
    model="meta/llama-3.1-70b-instruct",
    messages=[{"role": "user", "content": "Hello"}]
):
    monitor.track(token.token, token.entropy)
    
    if monitor.should_exit():
        print("Early exit!")
        break
```

### Ollama (Local)

```python
from entroplain import OllamaProvider, EntropyMonitor

provider = OllamaProvider()
monitor = EntropyMonitor()

for token in provider.stream_with_entropy(
    model="llama3.1",
    prompt="Think step by step..."
):
    print(token.token, end="")
    monitor.track(token.token, token.entropy)
```

---

## Agent Framework Integration

### OpenClaw

```yaml
# In your agent config
entropy_monitor:
  enabled: true
  entropy_threshold: 0.15
  min_valleys: 2
  
  hooks:
    on_token: entroplain.hooks.track_entropy
    on_exit_check: entroplain.hooks.early_exit
```

### Claude Code

```json
{
  "hooks": {
    "on_token": "entroplain.hooks.track_entropy",
    "on_converge": "entroplain.hooks.early_exit"
  }
}
```

### Custom Agent

```python
from entroplain.hooks import EntropyHook

hook = EntropyHook(config={"entropy_threshold": 0.15})

# In your agent loop
for token, entropy in your_agent.generate():
    result = hook.on_token(token, entropy)
    
    if result["should_exit"]:
        print(f"Exiting early at token {result['index']}")
        break
```

---

## CLI Reference

```bash
# Analyze entropy trajectory
entroplain analyze "What is 2+2?" --model gpt-4o --output results.json

# Stream with early exit
entroplain stream "Solve: x^2=16" --exit-on-converge --threshold 0.15

# Run benchmarks
entroplain benchmark --problems gsm8k --output benchmark.json

# Visualize trajectory
entroplain visualize results.json --output entropy_plot.png
```

---

## Research

### Key Findings

| Metric | Easy | Medium | Hard |
|--------|------|--------|------|
| Avg Valleys | 61.3 | 53.0 | 70.2 |
| Avg Entropy | 0.376 | 0.327 | 0.295 |
| Avg Velocity | 0.485 | 0.439 | 0.410 |

**H1 Supported:** Harder problems have more entropy valleys (correlates with reasoning complexity)

**H2 Supported:** Entropy velocity differs by difficulty (useful for crystallization detection)

### Paper

See [`paper.md`](../paper.md) for the full research proposal.

---

## Troubleshooting

### "No logprobs returned"

Ensure your API request includes:
- OpenAI/NVIDIA: `logprobs=True, top_logprobs=5`
- Anthropic: `logprobs=True`
- Gemini: `response_logprobs=True`

### "Entropy is always 0"

Some providers don't expose logprobs in streaming mode. Try non-streaming or check provider docs.

### "Should_exit always returns False"

Check your thresholds:
- `entropy_threshold` too low?
- `min_valleys` too high?
- `min_tokens` not reached?

---

## Support

- **Issues:** https://github.com/entroplain/entroplain/issues
- **Discord:** https://discord.gg/entroplain
- **Docs:** https://entroplain.ai/docs
