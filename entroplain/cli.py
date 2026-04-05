"""
CLI interface for Entroplain.
"""

import argparse
import json
import sys
from typing import Optional


def analyze_command(args):
    """Analyze a prompt's entropy trajectory."""
    from entroplain import EntropyMonitor, NVIDIAProvider
    
    provider = NVIDIAProvider()
    monitor = EntropyMonitor()
    
    print(f"Analyzing: {args.prompt[:50]}{'...' if len(args.prompt) > 50 else ''}")
    print(f"Model: {args.model}")
    print("-" * 60)
    
    messages = [{"role": "user", "content": args.prompt}]
    
    full_response = ""
    for token_data in provider.stream_with_entropy(model=args.model, messages=messages, max_tokens=args.max_tokens):
        monitor.track(token_data.token, token_data.entropy)
        full_response += token_data.token
        print(token_data.token, end="", flush=True)
    
    print("\n")
    print("-" * 60)
    print("ENTROPY ANALYSIS")
    print("-" * 60)
    
    stats = monitor.get_stats()
    print(f"Total tokens: {stats['token_count']}")
    print(f"Valleys: {stats['valley_count']}")
    print(f"Mean entropy: {stats['mean_entropy']:.4f}")
    print(f"Min entropy: {stats['min_entropy']:.4f}")
    print(f"Max entropy: {stats['max_entropy']:.4f}")
    print(f"Final entropy: {stats['current_entropy']:.4f}")
    print(f"Final velocity: {stats['current_velocity']:.4f}")
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump({
                "prompt": args.prompt,
                "model": args.model,
                "response": full_response,
                "stats": stats,
                "trajectory": monitor.get_trajectory()
            }, f, indent=2)
        print(f"\nResults saved to: {args.output}")


def stream_command(args):
    """Stream with early exit."""
    from entroplain import EntropyMonitor, NVIDIAProvider
    
    provider = NVIDIAProvider()
    monitor = EntropyMonitor(
        entropy_threshold=args.threshold,
        min_valleys=args.min_valleys
    )
    
    print(f"Streaming: {args.prompt[:50]}{'...' if len(args.prompt) > 50 else ''}")
    print(f"Exit threshold: {args.threshold}, min valleys: {args.min_valleys}")
    print("-" * 60)
    
    messages = [{"role": "user", "content": args.prompt}]
    
    full_response = ""
    exited_early = False
    
    for token_data in provider.stream_with_entropy(model=args.model, messages=messages, max_tokens=args.max_tokens):
        monitor.track(token_data.token, token_data.entropy)
        full_response += token_data.token
        print(token_data.token, end="", flush=True)
        
        if args.exit_on_converge and monitor.should_exit():
            print("\n\n[EARLY EXIT] Reasoning converged")
            exited_early = True
            break
    
    if not exited_early:
        print("\n\n[COMPLETE] Full response generated")
    
    stats = monitor.get_stats()
    print(f"Tokens: {stats['token_count']}, Valleys: {stats['valley_count']}, Entropy: {stats['current_entropy']:.4f}")


def benchmark_command(args):
    """Run benchmark tests."""
    print("Benchmark mode not yet implemented")
    print("Coming soon: GSM8K, HotpotQA, custom problem sets")


def visualize_command(args):
    """Visualize entropy trajectory."""
    print("Visualization mode not yet implemented")
    print("Coming soon: matplotlib plots, interactive charts")


def main():
    parser = argparse.ArgumentParser(
        description="Entroplain — Entropy-based early exit for efficient agent reasoning"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a prompt's entropy trajectory")
    analyze_parser.add_argument("prompt", help="The prompt to analyze")
    analyze_parser.add_argument("--model", default="meta/llama-3.1-70b-instruct", help="Model to use")
    analyze_parser.add_argument("--max-tokens", type=int, default=512, help="Maximum tokens")
    analyze_parser.add_argument("--output", help="Output file for results (JSON)")
    
    # Stream command
    stream_parser = subparsers.add_parser("stream", help="Stream with early exit")
    stream_parser.add_argument("prompt", help="The prompt to stream")
    stream_parser.add_argument("--model", default="meta/llama-3.1-70b-instruct", help="Model to use")
    stream_parser.add_argument("--max-tokens", type=int, default=1024, help="Maximum tokens")
    stream_parser.add_argument("--threshold", type=float, default=0.15, help="Entropy exit threshold")
    stream_parser.add_argument("--min-valleys", type=int, default=2, help="Minimum valleys before exit")
    stream_parser.add_argument("--exit-on-converge", action="store_true", help="Exit when reasoning converges")
    
    # Benchmark command
    benchmark_parser = subparsers.add_parser("benchmark", help="Run benchmark tests")
    benchmark_parser.add_argument("--problems", default="gsm8k", help="Problem set to use")
    benchmark_parser.add_argument("--output", default="results.json", help="Output file")
    
    # Visualize command
    visualize_parser = subparsers.add_parser("visualize", help="Visualize entropy trajectory")
    visualize_parser.add_argument("input", help="Input JSON file from analyze")
    visualize_parser.add_argument("--output", default="entropy_plot.png", help="Output image file")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        analyze_command(args)
    elif args.command == "stream":
        stream_command(args)
    elif args.command == "benchmark":
        benchmark_command(args)
    elif args.command == "visualize":
        visualize_command(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
