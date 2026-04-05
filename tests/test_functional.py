#!/usr/bin/env python3
"""
Functional test for Entroplain - verify core functionality works.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entroplain import EntropyMonitor, calculate_entropy


def test_entropy_calculation():
    """Test Shannon entropy calculation."""
    print("=" * 60)
    print("TEST: Entropy Calculation")
    print("=" * 60)
    
    # Test 1: Uniform distribution (should be ~1.0 for 2 choices)
    entropy = calculate_entropy([-0.693, -0.693])  # log(0.5) ≈ -0.693
    print(f"Uniform distribution entropy: {entropy:.4f}")
    assert 0.99 < entropy < 1.01, f"Expected ~1.0, got {entropy}"
    print("✓ Uniform distribution test passed")
    
    # Test 2: Deterministic (should be ~0)
    entropy = calculate_entropy([0.0, -100])  # One certain, one impossible
    print(f"Deterministic entropy: {entropy:.4f}")
    assert entropy < 0.01, f"Expected ~0, got {entropy}"
    print("✓ Deterministic test passed")
    
    # Test 3: Empty input
    entropy = calculate_entropy([])
    print(f"Empty input entropy: {entropy}")
    assert entropy == 0.0, f"Expected 0.0, got {entropy}"
    print("✓ Empty input test passed")
    
    print()
    return True


def test_valley_detection():
    """Test valley (local minimum) detection."""
    print("=" * 60)
    print("TEST: Valley Detection")
    print("=" * 60)
    
    monitor = EntropyMonitor()
    
    # Create trajectory: high -> low -> high (valley at index 1)
    trajectory = [0.8, 0.3, 0.7]
    for i, entropy in enumerate(trajectory):
        point = monitor.track(f"token_{i}", entropy)
        print(f"  Token {i}: entropy={entropy}, is_valley={point.is_valley}")
    
    valleys = monitor.get_valleys()
    print(f"Valleys detected: {valleys}")
    assert len(valleys) == 1, f"Expected 1 valley, got {len(valleys)}"
    assert valleys[0] == (1, 0.3), f"Expected (1, 0.3), got {valleys[0]}"
    print("✓ Valley detection test passed")
    
    print()
    return True


def test_velocity_calculation():
    """Test entropy velocity (rate of change)."""
    print("=" * 60)
    print("TEST: Velocity Calculation")
    print("=" * 60)
    
    monitor = EntropyMonitor()
    
    monitor.track("A", 0.5)
    velocity_initial = monitor.get_velocity()
    print(f"Initial velocity: {velocity_initial}")
    assert velocity_initial == 0.0, "Initial velocity should be 0"
    
    monitor.track("B", 0.7)
    velocity = monitor.get_velocity()
    print(f"Velocity after second token: {velocity:.4f}")
    assert abs(velocity - 0.2) < 0.01, f"Expected ~0.2, got {velocity}"
    
    print("✓ Velocity calculation test passed")
    
    print()
    return True


def test_exit_conditions():
    """Test various exit conditions."""
    print("=" * 60)
    print("TEST: Exit Conditions")
    print("=" * 60)
    
    # Test min_tokens requirement
    monitor = EntropyMonitor(min_tokens=10, min_valleys=0)
    for i in range(5):
        monitor.track(f"t_{i}", 0.1)  # Low entropy
    should_exit = monitor.should_exit()
    print(f"min_tokens=10, 5 tokens: should_exit={should_exit}")
    assert not should_exit, "Should not exit before min_tokens"
    print("✓ min_tokens requirement works")
    
    # Test min_valleys requirement
    monitor = EntropyMonitor(min_tokens=0, min_valleys=3)
    for entropy in [0.8, 0.3, 0.8, 0.4, 0.8]:  # Only 2 valleys
        monitor.track("t", entropy)
    should_exit = monitor.should_exit()
    print(f"min_valleys=3, 2 valleys: should_exit={should_exit}")
    assert not should_exit, "Should not exit before min_valleys"
    print("✓ min_valleys requirement works")
    
    # Test entropy_drop condition
    monitor = EntropyMonitor(
        entropy_threshold=0.15,
        min_valleys=0,
        min_tokens=5,
        exit_condition="entropy_drop"
    )
    for i in range(10):
        monitor.track(f"t_{i}", 0.1)  # Below threshold
    should_exit = monitor.should_exit()
    print(f"entropy_drop, entropy=0.1, threshold=0.15: should_exit={should_exit}")
    assert should_exit, "Should exit when entropy below threshold"
    print("✓ entropy_drop condition works")
    
    print()
    return True


def test_stats():
    """Test statistics output."""
    print("=" * 60)
    print("TEST: Statistics")
    print("=" * 60)
    
    monitor = EntropyMonitor()
    
    trajectory = [0.5, 0.3, 0.7, 0.2, 0.6]
    for i, entropy in enumerate(trajectory):
        monitor.track(f"t_{i}", entropy)
    
    stats = monitor.get_stats()
    print(f"Statistics: {stats}")
    
    assert stats["token_count"] == 5
    assert stats["min_entropy"] == 0.2
    assert stats["max_entropy"] == 0.7
    assert abs(stats["mean_entropy"] - 0.46) < 0.01
    
    print("✓ Statistics test passed")
    
    print()
    return True


def test_reset():
    """Test monitor reset."""
    print("=" * 60)
    print("TEST: Reset")
    print("=" * 60)
    
    monitor = EntropyMonitor()
    
    for i in range(10):
        monitor.track(f"t_{i}", 0.5)
    
    assert len(monitor.get_trajectory()) == 10
    print(f"Before reset: {len(monitor.get_trajectory())} tokens")
    
    monitor.reset()
    
    assert len(monitor.get_trajectory()) == 0
    assert len(monitor.get_valleys()) == 0
    print(f"After reset: {len(monitor.get_trajectory())} tokens")
    print("✓ Reset test passed")
    
    print()
    return True


def run_security_audit():
    """Security audit for the codebase."""
    print("=" * 60)
    print("SECURITY AUDIT")
    print("=" * 60)
    
    issues = []
    warnings = []
    
    # Check 1: No hardcoded secrets
    print("\n[CHECK] Hardcoded secrets...")
    import entroplain.monitor as monitor_module
    import entroplain.providers as providers_module
    
    monitor_code = open(monitor_module.__file__).read()
    providers_code = open(providers_module.__file__).read()
    combined = monitor_code + providers_code
    
    # Look for potential secrets
    import re
    api_key_patterns = [
        r'sk-[a-zA-Z0-9]{20,}',
        r'sk-ant-[a-zA-Z0-9]{20,}',
        r'nvapi-[a-zA-Z0-9]{20,}',
        r'AIza[a-zA-Z0-9_-]{35}',
    ]
    
    for pattern in api_key_patterns:
        matches = re.findall(pattern, combined)
        if matches:
            issues.append(f"Potential API key found: {matches[0][:10]}...")
    
    if not issues:
        print("✓ No hardcoded secrets found")
    
    # Check 2: Environment variables for auth
    print("\n[CHECK] Authentication handling...")
    if 'os.environ.get' in providers_code:
        print("✓ Uses environment variables for API keys")
    else:
        warnings.append("Consider using environment variables for API keys")
    
    # Check 3: Input validation
    print("\n[CHECK] Input validation...")
    if 'if not logprobs' in monitor_code:
        print("✓ Empty input validation present")
    
    # Check 4: No eval/exec
    print("\n[CHECK] Dangerous functions...")
    dangerous = ['eval(', 'exec(', 'compile(', '__import__']
    for d in dangerous:
        if d in combined:
            issues.append(f"Dangerous function found: {d}")
    
    if not any(d in combined for d in dangerous):
        print("✓ No dangerous eval/exec found")
    
    # Check 5: No shell injection vectors
    print("\n[CHECK] Shell injection vectors...")
    if 'subprocess' in combined or 'os.system' in combined:
        issues.append("Potential shell injection vector")
    else:
        print("✓ No shell injection vectors found")
    
    # Check 6: Data sanitization
    print("\n[CHECK] Data sanitization...")
    if '1e-10' in monitor_code:  # Prevents log(0)
        print("✓ Math sanitization present (prevents log(0))")
    
    print("\n" + "=" * 60)
    print("SECURITY SUMMARY")
    print("=" * 60)
    
    if issues:
        print(f"\n❌ ISSUES ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ No security issues found")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")
    
    return len(issues) == 0


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("ENTROPPLAIN FUNCTIONAL TESTS")
    print("=" * 60 + "\n")
    
    all_passed = True
    
    try:
        all_passed &= test_entropy_calculation()
        all_passed &= test_valley_detection()
        all_passed &= test_velocity_calculation()
        all_passed &= test_exit_conditions()
        all_passed &= test_stats()
        all_passed &= test_reset()
        all_passed &= run_security_audit()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
