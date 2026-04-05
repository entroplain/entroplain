"""
Entroplain — Entropy-based early exit for efficient agent reasoning.
"""

__version__ = "0.1.2"
__author__ = "Entroplain Contributors"

from .monitor import EntropyMonitor, calculate_entropy
from .providers import (
    OpenAIProvider,
    AnthropicProvider,
    GeminiProvider,
    NVIDIAProvider,
    OllamaProvider,
    LlamaCppProvider,
)
from .hooks import track_entropy, early_exit

__all__ = [
    "EntropyMonitor",
    "calculate_entropy",
    "OpenAIProvider",
    "AnthropicProvider",
    "GeminiProvider",
    "NVIDIAProvider",
    "OllamaProvider",
    "LlamaCppProvider",
    "track_entropy",
    "early_exit",
]
