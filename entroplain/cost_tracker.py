"""
Cost tracking and savings calculator.

Estimates cost savings from early exit based on token usage.
"""

import math
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class PricingTier(Enum):
    """Pricing tiers for different models."""
    # OpenAI
    GPT4O = ("gpt-4o", 2.50, 10.00)  # input, output per 1M tokens
    GPT4O_MINI = ("gpt-4o-mini", 0.15, 0.60)
    GPT4_TURBO = ("gpt-4-turbo", 10.00, 30.00)
    
    # Anthropic
    CLAUDE_4_OPUS = ("claude-4-opus", 15.00, 75.00)
    CLAUDE_4_SONNET = ("claude-4-sonnet", 3.00, 15.00)
    
    # NVIDIA
    LLAMA_70B = ("meta/llama-3.1-70b-instruct", 0.70, 0.70)
    LLAMA_405B = ("meta/llama-3.1-405b-instruct", 2.70, 2.70)
    
    # Default (unknown model)
    DEFAULT = ("default", 1.00, 1.00)


@dataclass
class CostEstimate:
    """Estimated cost for a completion."""
    model: str
    input_tokens: int
    output_tokens: int
    output_tokens_full: int  # If no early exit
    cost_actual_usd: float
    cost_full_usd: float
    cost_saved_usd: float
    savings_percent: float


class CostTracker:
    """
    Track token usage and calculate cost savings.
    
    Usage:
        tracker = CostTracker(model="gpt-4o")
        tracker.track_input(100)  # 100 input tokens
        tracker.track_output(50)  # 50 output tokens
        tracker.set_full_estimate(150)  # Would have been 150 output tokens
        
        estimate = tracker.get_estimate()
        print(f"Saved ${estimate.cost_saved_usd:.4f}")
    """
    
    # Model name to pricing tier mapping
    MODEL_ALIASES = {
        # OpenAI
        "gpt-4o": PricingTier.GPT4O,
        "gpt-4o-mini": PricingTier.GPT4O_MINI,
        "gpt-4-turbo": PricingTier.GPT4_TURBO,
        "gpt-4-turbo-preview": PricingTier.GPT4_TURBO,
        
        # Anthropic
        "claude-4-opus": PricingTier.CLAUDE_4_OPUS,
        "claude-opus-4": PricingTier.CLAUDE_4_OPUS,
        "claude-4-sonnet": PricingTier.CLAUDE_4_SONNET,
        "claude-sonnet-4": PricingTier.CLAUDE_4_SONNET,
        
        # NVIDIA / Meta
        "meta/llama-3.1-70b-instruct": PricingTier.LLAMA_70B,
        "llama-3.1-70b": PricingTier.LLAMA_70B,
        "meta/llama-3.1-405b-instruct": PricingTier.LLAMA_405B,
        "llama-3.1-405b": PricingTier.LLAMA_405B,
    }
    
    def __init__(
        self,
        model: str = "default",
        custom_pricing: Optional[tuple] = None
    ):
        """
        Initialize cost tracker.
        
        Args:
            model: Model name (e.g., "gpt-4o", "claude-4-sonnet")
            custom_pricing: Optional (input_price, output_price) per 1M tokens
        """
        self.model = model
        self.input_tokens = 0
        self.output_tokens = 0
        self.estimated_full_output = None
        self._custom_pricing = custom_pricing
        
        # Get pricing for model
        if custom_pricing:
            self._input_price, self._output_price = custom_pricing
        else:
            tier = self.MODEL_ALIASES.get(model.lower(), PricingTier.DEFAULT)
            self._input_price, self._output_price = tier.value[1], tier.value[2]
    
    def track_input(self, tokens: int):
        """Track input tokens."""
        self.input_tokens += tokens
    
    def track_output(self, tokens: int):
        """Track output tokens generated."""
        self.output_tokens += tokens
    
    def set_full_estimate(self, tokens: int):
        """Set estimate of what output would have been without early exit."""
        self.estimated_full_output = tokens
    
    def estimate_full_output(self, multiplier: float = 2.0) -> int:
        """
        Auto-estimate full output if not set.
        
        Uses a simple multiplier based on observed tokens.
        Default assumes early exit saves ~50%.
        """
        if self.estimated_full_output:
            return self.estimated_full_output
        return int(self.output_tokens * multiplier)
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for given token counts."""
        input_cost = (input_tokens / 1_000_000) * self._input_price
        output_cost = (output_tokens / 1_000_000) * self._output_price
        return input_cost + output_cost
    
    def get_estimate(self) -> CostEstimate:
        """Get cost estimate with savings calculation."""
        full_output = self.estimate_full_output()
        
        cost_actual = self.calculate_cost(self.input_tokens, self.output_tokens)
        cost_full = self.calculate_cost(self.input_tokens, full_output)
        cost_saved = cost_full - cost_actual
        
        if cost_full > 0:
            savings_pct = (cost_saved / cost_full) * 100
        else:
            savings_pct = 0.0
        
        return CostEstimate(
            model=self.model,
            input_tokens=self.input_tokens,
            output_tokens=self.output_tokens,
            output_tokens_full=full_output,
            cost_actual_usd=cost_actual,
            cost_full_usd=cost_full,
            cost_saved_usd=cost_saved,
            savings_percent=savings_pct
        )
    
    def reset(self):
        """Reset tracking for new request."""
        self.input_tokens = 0
        self.output_tokens = 0
        self.estimated_full_output = None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current stats as dict."""
        estimate = self.get_estimate()
        return {
            "model": estimate.model,
            "input_tokens": estimate.input_tokens,
            "output_tokens": estimate.output_tokens,
            "output_tokens_full": estimate.output_tokens_full,
            "tokens_saved": estimate.output_tokens_full - estimate.output_tokens,
            "cost_actual_usd": estimate.cost_actual_usd,
            "cost_full_usd": estimate.cost_full_usd,
            "cost_saved_usd": estimate.cost_saved_usd,
            "savings_percent": estimate.savings_percent,
        }


# Convenience function for quick estimates
def estimate_savings(
    model: str,
    tokens_generated: int,
    tokens_if_full: int,
    input_tokens: int = 0
) -> CostEstimate:
    """
    Quick estimate of cost savings.
    
    Args:
        model: Model name
        tokens_generated: Actual tokens generated (with early exit)
        tokens_if_full: Tokens that would have been generated without early exit
        input_tokens: Input prompt tokens
    
    Returns:
        CostEstimate with savings details
    """
    tracker = CostTracker(model)
    tracker.track_input(input_tokens)
    tracker.track_output(tokens_generated)
    tracker.set_full_estimate(tokens_if_full)
    return tracker.get_estimate()


def format_cost_report(estimate: CostEstimate) -> str:
    """Format a human-readable cost report."""
    lines = [
        f"📊 Cost Report for {estimate.model}",
        f"",
        f"  Input tokens:    {estimate.input_tokens:,}",
        f"  Output tokens:   {estimate.output_tokens:,} (actual)",
        f"                   {estimate.output_tokens_full:,} (if no early exit)",
        f"  Tokens saved:    {estimate.output_tokens_full - estimate.output_tokens:,}",
        f"",
        f"  Cost actual:     ${estimate.cost_actual_usd:.6f}",
        f"  Cost if full:    ${estimate.cost_full_usd:.6f}",
        f"  💰 Cost saved:   ${estimate.cost_saved_usd:.6f} ({estimate.savings_percent:.1f}%)",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    # Demo
    estimate = estimate_savings(
        model="gpt-4o",
        tokens_generated=82,
        tokens_if_full=150,
        input_tokens=50
    )
    print(format_cost_report(estimate))
