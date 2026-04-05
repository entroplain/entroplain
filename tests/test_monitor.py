"""Tests for Entroplain entropy monitor."""

import pytest
from entroplain import EntropyMonitor, calculate_entropy


class TestEntropyCalculation:
    """Tests for entropy calculation."""
    
    def test_calculate_entropy_uniform(self):
        """Uniform distribution should have maximum entropy."""
        # log(0.5) ≈ -0.693
        entropy = calculate_entropy([-0.693, -0.693], from_probs=False)
        assert 0.99 < entropy < 1.01  # Should be ~1.0 for 50/50
    
    def test_calculate_entropy_deterministic(self):
        """Deterministic distribution should have zero entropy."""
        entropy = calculate_entropy([0.0, -100], from_probs=False)
        assert entropy < 0.01  # Should be ~0
    
    def test_calculate_entropy_from_probs(self):
        """Should work with probabilities directly."""
        entropy = calculate_entropy([0.5, 0.5], from_probs=True)
        assert 0.99 < entropy < 1.01
    
    def test_calculate_entropy_empty(self):
        """Empty input should return zero."""
        entropy = calculate_entropy([])
        assert entropy == 0.0


class TestEntropyMonitor:
    """Tests for the EntropyMonitor class."""
    
    def test_track_token(self):
        """Should track tokens and return entropy points."""
        monitor = EntropyMonitor()
        
        point = monitor.track("Hello", 0.5)
        
        assert point.token == "Hello"
        assert point.entropy == 0.5
        assert point.index == 0
        assert point.is_valley == False  # First token can't be valley
    
    def test_valley_detection(self):
        """Should detect local minima (valleys)."""
        monitor = EntropyMonitor()
        
        # Create trajectory: high -> low -> high (valley in middle)
        monitor.track("A", 0.8)
        monitor.track("B", 0.3)  # Valley
        monitor.track("C", 0.7)
        
        valleys = monitor.get_valleys()
        assert len(valleys) == 1
        assert valleys[0][0] == 1  # Index of "B"
        assert valleys[0][1] == 0.3
    
    def test_velocity_calculation(self):
        """Should calculate entropy velocity (rate of change)."""
        monitor = EntropyMonitor()
        
        monitor.track("A", 0.5)
        monitor.track("B", 0.7)
        
        velocity = monitor.get_velocity()
        assert abs(velocity - 0.2) < 0.01
    
    def test_should_exit_respects_min_tokens(self):
        """Should not exit before min_tokens."""
        monitor = EntropyMonitor(min_tokens=10)
        
        for i in range(5):
            monitor.track(f"token_{i}", 0.1)  # Low entropy
        
        assert not monitor.should_exit()  # Too few tokens
    
    def test_should_exit_respects_min_valleys(self):
        """Should not exit before min_valleys."""
        monitor = EntropyMonitor(min_valleys=3, min_tokens=0)
        
        # Create trajectory with only 2 valleys
        for entropy in [0.8, 0.3, 0.8, 0.4, 0.8]:
            monitor.track("t", entropy)
        
        assert len(monitor.get_valleys()) == 2
        assert not monitor.should_exit()  # Not enough valleys
    
    def test_get_stats(self):
        """Should return correct statistics."""
        monitor = EntropyMonitor()
        
        for entropy in [0.5, 0.3, 0.7, 0.2, 0.6]:
            monitor.track("t", entropy)
        
        stats = monitor.get_stats()
        
        assert stats["token_count"] == 5
        assert stats["min_entropy"] == 0.2
        assert stats["max_entropy"] == 0.7
        assert abs(stats["mean_entropy"] - 0.46) < 0.01
    
    def test_reset(self):
        """Should clear all tracked data."""
        monitor = EntropyMonitor()
        
        for i in range(10):
            monitor.track("t", 0.5)
        
        monitor.reset()
        
        assert len(monitor.get_trajectory()) == 0
        assert len(monitor.get_valleys()) == 0


class TestExitConditions:
    """Tests for different exit conditions."""
    
    def test_entropy_drop_exit(self):
        """Should exit when entropy drops below threshold."""
        monitor = EntropyMonitor(
            entropy_threshold=0.15,
            min_valleys=0,
            min_tokens=5,
            exit_condition="entropy_drop"
        )
        
        for i in range(5):
            monitor.track("t", 0.1)  # Below threshold
        
        assert monitor.should_exit()
    
    def test_velocity_zero_exit(self):
        """Should exit when velocity stabilizes."""
        monitor = EntropyMonitor(
            velocity_threshold=0.01,
            min_tokens=5,
            exit_condition="velocity_zero"
        )
        
        # Start varying, then stabilize
        for entropy in [0.5, 0.3, 0.4, 0.39, 0.395, 0.392]:
            monitor.track("t", entropy)
        
        # Should exit because velocity is low
        assert monitor.should_exit()
    
    def test_combined_exit(self):
        """Combined condition should work."""
        monitor = EntropyMonitor(
            entropy_threshold=0.2,
            velocity_threshold=0.05,
            min_tokens=10,
            min_valleys=2,
            exit_condition="combined"
        )
        
        # Create trajectory with valleys and low entropy
        trajectory = [0.8, 0.3, 0.8, 0.3, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15]
        for e in trajectory:
            monitor.track("t", e)
        
        # Should exit: entropy is low and velocity is low
        assert monitor.should_exit()
