"""
Entropy Monitor — Core entropy tracking and early exit logic.

Supports multiple exit strategies:
- Valleys plateau: Exit when reasoning milestones stabilize
- Entropy drop: Exit when model confidence is high
- Velocity zero: Exit when entropy stops changing
- Combined: Multiple conditions with AND/OR logic
- Repetition: Exit when model starts repeating
- Confidence: Exit when top token probability > threshold for N tokens
"""

import math
from typing import List, Tuple, Optional, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter


class ExitCondition(Enum):
    VALLEYS_PLATEAU = "valleys_plateau"
    ENTROPY_DROP = "entropy_drop"
    VELOCITY_ZERO = "velocity_zero"
    COMBINED = "combined"
    # New strategies
    REPETITION = "repetition"
    CONFIDENCE = "confidence"
    SEMANTIC = "semantic"


@dataclass
class EntropyPoint:
    """A single point in the entropy trajectory."""
    index: int
    token: str
    entropy: float
    is_valley: bool = False
    velocity: float = 0.0
    confidence: float = 0.0  # Top token probability


@dataclass
class MonitorConfig:
    """Configuration for the entropy monitor."""
    entropy_threshold: float = 0.15
    min_valleys: int = 2
    velocity_threshold: float = 0.05
    min_tokens: int = 50
    valley_window: int = 5
    plateau_threshold: int = 3
    exit_condition: ExitCondition = ExitCondition.COMBINED
    # New config options
    repetition_window: int = 20  # Window to check for repetition
    repetition_threshold: float = 0.3  # 30% repetition = exit
    confidence_threshold: float = 0.95  # 95% confidence = exit
    confidence_min_tokens: int = 5  # Min tokens at high confidence


class EntropyMonitor:
    """
    Monitor entropy trajectory and detect reasoning convergence.

    Usage:
        monitor = EntropyMonitor()
        for token, entropy in stream:
            monitor.track(token, entropy)
            if monitor.should_exit():
                break
    """

    def __init__(
        self,
        entropy_threshold: float = 0.15,
        min_valleys: int = 2,
        velocity_threshold: float = 0.05,
        min_tokens: int = 50,
        valley_window: int = 5,
        plateau_threshold: int = 3,
        exit_condition: str = "combined",
        # New parameters
        repetition_window: int = 20,
        repetition_threshold: float = 0.3,
        confidence_threshold: float = 0.95,
        confidence_min_tokens: int = 5,
    ):
        self.config = MonitorConfig(
            entropy_threshold=entropy_threshold,
            min_valleys=min_valleys,
            velocity_threshold=velocity_threshold,
            min_tokens=min_tokens,
            valley_window=valley_window,
            plateau_threshold=plateau_threshold,
            exit_condition=ExitCondition(exit_condition),
            repetition_window=repetition_window,
            repetition_threshold=repetition_threshold,
            confidence_threshold=confidence_threshold,
            confidence_min_tokens=confidence_min_tokens,
        )
        self._trajectory: List[EntropyPoint] = []
        self._valleys: List[EntropyPoint] = []
        self._index = 0
        self._high_confidence_count = 0  # Track consecutive high confidence

    def calculate_entropy(self, logprobs: List[float], from_probs: bool = False) -> float:
        """
        Calculate Shannon entropy from log probabilities or probabilities.

        Args:
            logprobs: List of log probabilities (natural log) or probabilities
            from_probs: If True, treat input as probabilities (will convert)

        Returns:
            Shannon entropy in bits
        """
        if not logprobs:
            return 0.0

        entropy = 0.0
        for lp in logprobs:
            if from_probs:
                prob = lp
            else:
                prob = math.exp(lp)
            if prob > 0:
                entropy -= prob * math.log2(prob + 1e-10)

        return entropy

    def track(self, token: str, entropy: float, confidence: float = 0.0) -> EntropyPoint:
        """
        Track a token and its entropy value.

        Args:
            token: The generated token
            entropy: Calculated entropy for this token
            confidence: Top token probability (optional, for confidence strategy)

        Returns:
            EntropyPoint with valley detection
        """
        point = EntropyPoint(
            index=self._index,
            token=token,
            entropy=entropy,
            confidence=confidence
        )

        # Calculate velocity
        if len(self._trajectory) > 0:
            prev = self._trajectory[-1]
            point.velocity = abs(entropy - prev.entropy)

        # Detect valley (local minimum)
        if len(self._trajectory) >= 2:
            prev2 = self._trajectory[-2]
            prev1 = self._trajectory[-1]
            if prev1.entropy < prev2.entropy and prev1.entropy < entropy:
                prev1.is_valley = True
                self._valleys.append(prev1)

        self._trajectory.append(point)
        self._index += 1

        # Track high confidence
        if confidence >= self.config.confidence_threshold:
            self._high_confidence_count += 1
        else:
            self._high_confidence_count = 0

        return point

    def get_valleys(self) -> List[Tuple[int, float]]:
        """Get all entropy valleys (local minima) as (index, entropy) tuples."""
        return [(v.index, v.entropy) for v in self._valleys]

    def get_velocity(self) -> float:
        """Get current entropy velocity (rate of change)."""
        if len(self._trajectory) < 2:
            return 0.0
        return self._trajectory[-1].velocity

    def get_mean_entropy(self) -> float:
        """Get mean entropy over the trajectory."""
        if not self._trajectory:
            return 0.0
        return sum(p.entropy for p in self._trajectory) / len(self._trajectory)

    def get_valley_count(self) -> int:
        """Get the number of detected valleys."""
        return len(self._valleys)

    def is_valleys_plateau(self) -> bool:
        """Check if valley count has plateaued."""
        if len(self._valleys) < self.config.min_valleys:
            return False

        # Check if last N valleys have similar spacing
        recent = self._valleys[-self.config.plateau_threshold:]
        if len(recent) < self.config.plateau_threshold:
            return False

        # Calculate spacing between recent valleys
        spacings = [
            recent[i + 1].index - recent[i].index
            for i in range(len(recent) - 1)
        ]
        if not spacings:
            return False

        mean_spacing = sum(spacings) / len(spacings)
        variance = sum((s - mean_spacing) ** 2 for s in spacings) / len(spacings)

        # Low variance in spacing = plateau
        return variance < 10  # Threshold tuned empirically

    def is_entropy_low(self) -> bool:
        """Check if current entropy is below threshold."""
        if not self._trajectory:
            return False
        return self._trajectory[-1].entropy < self.config.entropy_threshold

    def is_velocity_stable(self) -> bool:
        """Check if velocity is below threshold."""
        return self.get_velocity() < self.config.velocity_threshold

    def is_repeating(self) -> bool:
        """
        Check if the model is repeating itself.

        Returns True if the repetition ratio in the recent window
        exceeds the threshold.
        """
        if len(self._trajectory) < self.config.repetition_window:
            return False

        # Get recent tokens
        recent_tokens = [
            p.token for p in self._trajectory[-self.config.repetition_window :]
        ]

        # Count unique vs total
        counter = Counter(recent_tokens)
        unique_count = len(counter)
        total_count = len(recent_tokens)

        # Calculate repetition ratio
        repetition_ratio = 1.0 - (unique_count / total_count)

        return repetition_ratio >= self.config.repetition_threshold

    def is_confident(self) -> bool:
        """
        Check if model has been highly confident for consecutive tokens.

        Returns True if the last N tokens had confidence >= threshold.
        """
        return self._high_confidence_count >= self.config.confidence_min_tokens

    def should_exit(self) -> bool:
        """
        Determine if reasoning has converged and we should exit.

        Uses the configured exit condition:
        - valleys_plateau: Exit when valley count plateaus
        - entropy_drop: Exit when entropy drops below threshold
        - velocity_zero: Exit when velocity stabilizes
        - combined: Use all conditions with AND logic
        - repetition: Exit when model starts repeating
        - confidence: Exit when confidence is high for N tokens
        """
        # Always require minimum tokens
        if len(self._trajectory) < self.config.min_tokens:
            return False

        # Always require minimum valleys (for most strategies)
        condition = self.config.exit_condition

        if condition == ExitCondition.REPETITION:
            # Repetition doesn't require valleys
            return self.is_repeating()

        if condition == ExitCondition.CONFIDENCE:
            # Confidence doesn't require valleys
            return self.is_confident()

        # For other strategies, require minimum valleys
        if len(self._valleys) < self.config.min_valleys:
            return False

        if condition == ExitCondition.VALLEYS_PLATEAU:
            return self.is_valleys_plateau()

        if condition == ExitCondition.ENTROPY_DROP:
            return self.is_entropy_low()

        if condition == ExitCondition.VELOCITY_ZERO:
            return self.is_velocity_stable()

        if condition == ExitCondition.COMBINED:
            # Combined: require entropy low OR valleys plateau, AND velocity stable
            return (self.is_entropy_low() or self.is_valleys_plateau()) and self.is_velocity_stable()

        if condition == ExitCondition.SEMANTIC:
            # Placeholder for future semantic convergence detection
            # Would use embeddings to detect when output stabilizes semantically
            return False

        return False

    def is_converged(self) -> bool:
        """Alias for should_exit()."""
        return self.should_exit()

    def get_trajectory(self) -> List[float]:
        """Get full entropy trajectory as list of floats."""
        return [p.entropy for p in self._trajectory]

    def get_tokens(self) -> List[str]:
        """Get all tracked tokens."""
        return [p.token for p in self._trajectory]

    def get_stats(self) -> Dict[str, Any]:
        """Get summary statistics."""
        if not self._trajectory:
            return {}

        entropies = [p.entropy for p in self._trajectory]
        return {
            "token_count": len(self._trajectory),
            "valley_count": len(self._valleys),
            "mean_entropy": sum(entropies) / len(entropies),
            "min_entropy": min(entropies),
            "max_entropy": max(entropies),
            "current_entropy": entropies[-1],
            "current_velocity": self.get_velocity(),
            "is_converged": self.should_exit(),
            "exit_reason": self._get_exit_reason(),
        }

    def _get_exit_reason(self) -> Optional[str]:
        """Get the reason for early exit (if triggered)."""
        if not self.should_exit():
            return None

        condition = self.config.exit_condition

        if condition == ExitCondition.REPETITION:
            return "repetition_detected"
        if condition == ExitCondition.CONFIDENCE:
            return "high_confidence"
        if condition == ExitCondition.ENTROPY_DROP:
            return "entropy_below_threshold"
        if condition == ExitCondition.VELOCITY_ZERO:
            return "velocity_stable"
        if condition == ExitCondition.VALLEYS_PLATEAU:
            return "valleys_plateau"
        if condition == ExitCondition.COMBINED:
            if self.is_entropy_low() and self.is_velocity_stable():
                return "entropy_low_velocity_stable"
            if self.is_valleys_plateau() and self.is_velocity_stable():
                return "valleys_plateau_velocity_stable"
            return "combined"

        return "unknown"

    def reset(self) -> None:
        """Clear all tracked data."""
        self._trajectory.clear()
        self._valleys.clear()
        self._index = 0
        self._high_confidence_count = 0


# Convenience function for one-shot entropy calculation
def calculate_entropy_from_logprobs(logprobs: List[float]) -> float:
    """
    Calculate Shannon entropy from log probabilities.

    Args:
        logprobs: List of log probabilities (natural log)

    Returns:
        Shannon entropy in bits
    """
    entropy = 0.0
    for lp in logprobs:
        prob = math.exp(lp)
        if prob > 0:
            entropy -= prob * math.log2(prob + 1e-10)
    return entropy
