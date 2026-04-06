"""
Entroplain — Entropy-based early exit for efficient agent reasoning.
"""

__version__ = "0.2.1"
__author__ = "Entroplain Contributors"

from .monitor import EntropyMonitor, calculate_entropy_from_logprobs
from .providers import (
    OpenAIProvider,
    AnthropicProvider,
    GeminiProvider,
    NVIDIAProvider,
    OllamaProvider,
    LlamaCppProvider,
)
from .hooks import track_entropy, early_exit
from .cost_tracker import CostTracker

__all__ = [
    "EntropyMonitor",
    "calculate_entropy_from_logprobs",
    "OpenAIProvider",
    "AnthropicProvider",
    "GeminiProvider",
    "NVIDIAProvider",
    "OllamaProvider",
    "LlamaCppProvider",
    "track_entropy",
    "early_exit",
    "CostTracker",
]
