"""
Hooks for agent framework integration.
"""

from typing import Dict, Any, Optional
from .monitor import EntropyMonitor


# Global monitor instance for hooks
_monitor: Optional[EntropyMonitor] = None
_config: Dict[str, Any] = {}


def init_hooks(config: Dict[str, Any] = None):
    """
    Initialize entropy hooks for agent frameworks.
    
    Args:
        config: Configuration for the entropy monitor
    """
    global _monitor, _config
    
    _config = config or {}
    _monitor = EntropyMonitor(
        entropy_threshold=_config.get("entropy_threshold", 0.15),
        min_valleys=_config.get("min_valleys", 2),
        velocity_threshold=_config.get("velocity_threshold", 0.05),
        min_tokens=_config.get("min_tokens", 50)
    )


def track_entropy(token: str, entropy: float) -> Dict[str, Any]:
    """
    Hook to track entropy for each token.
    
    Use in agent frameworks as an on_token callback.
    
    Args:
        token: The generated token
        entropy: The entropy value for this token
    
    Returns:
        Dict with tracking info and convergence status
    """
    global _monitor
    
    if _monitor is None:
        init_hooks()
    
    point = _monitor.track(token, entropy)
    
    return {
        "token": token,
        "entropy": entropy,
        "index": point.index,
        "is_valley": point.is_valley,
        "velocity": point.velocity,
        "should_exit": _monitor.should_exit(),
        "stats": _monitor.get_stats()
    }


def early_exit() -> bool:
    """
    Hook to check if reasoning has converged.
    
    Use in agent frameworks as an exit condition.
    
    Returns:
        True if reasoning has converged, False otherwise
    """
    global _monitor
    
    if _monitor is None:
        return False
    
    return _monitor.should_exit()


def reset_hooks():
    """Reset the global monitor state."""
    global _monitor
    
    if _monitor:
        _monitor.reset()


def get_monitor() -> Optional[EntropyMonitor]:
    """Get the current monitor instance."""
    return _monitor


# OpenClaw integration
def openclaw_config() -> Dict[str, Any]:
    """
    Generate OpenClaw configuration for entropy monitoring.
    
    Returns:
        Dict with OpenClaw config structure
    """
    return {
        "entropy_monitor": {
            "enabled": True,
            "exit_threshold": _config.get("entropy_threshold", 0.15),
            "min_valleys": _config.get("min_valleys", 2),
            "velocity_threshold": _config.get("velocity_threshold", 0.05),
            "hooks": {
                "on_token": "entroplain.hooks.track_entropy",
                "on_exit_check": "entroplain.hooks.early_exit"
            }
        }
    }


# Claude Code integration
def claude_code_hooks() -> Dict[str, str]:
    """
    Generate Claude Code hook configuration.
    
    Returns:
        Dict with hook function paths
    """
    return {
        "hooks": {
            "on_token": "entroplain.hooks.track_entropy",
            "on_converge": "entroplain.hooks.early_exit"
        },
        "config": {
            "entropy_threshold": _config.get("entropy_threshold", 0.15),
            "min_valleys": _config.get("min_valleys", 2)
        }
    }


# Generic agent framework integration
class EntropyHook:
    """
    Class-based hook for frameworks that prefer class instances.
    
    Usage:
        hook = EntropyHook(config={"entropy_threshold": 0.15})
        
        # In your agent loop
        for token in agent.generate():
            result = hook.on_token(token, entropy)
            if result["should_exit"]:
                break
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.monitor = EntropyMonitor(
            entropy_threshold=self.config.get("entropy_threshold", 0.15),
            min_valleys=self.config.get("min_valleys", 2),
            velocity_threshold=self.config.get("velocity_threshold", 0.05),
            min_tokens=self.config.get("min_tokens", 50)
        )
    
    def on_token(self, token: str, entropy: float) -> Dict[str, Any]:
        """Process a token and return tracking info."""
        point = self.monitor.track(token, entropy)
        
        return {
            "token": token,
            "entropy": entropy,
            "index": point.index,
            "is_valley": point.is_valley,
            "velocity": point.velocity,
            "should_exit": self.monitor.should_exit(),
            "stats": self.monitor.get_stats()
        }
    
    def should_exit(self) -> bool:
        """Check if reasoning has converged."""
        return self.monitor.should_exit()
    
    def reset(self):
        """Reset the monitor state."""
        self.monitor.reset()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return self.monitor.get_stats()
