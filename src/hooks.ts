/**
 * Hooks for agent framework integration
 */

import { EntropyMonitor } from './monitor';
import { EntropyPoint, MonitorStats } from './types';

// Global monitor instance
let monitor: EntropyMonitor | null = null;
let config: Record<string, unknown> = {};

/**
 * Initialize entropy hooks
 */
export function initHooks(userConfig: Record<string, unknown> = {}): void {
  config = userConfig;
  monitor = new EntropyMonitor({
    entropyThreshold: (config.entropyThreshold as number) ?? 0.15,
    minValleys: (config.minValleys as number) ?? 2,
    velocityThreshold: (config.velocityThreshold as number) ?? 0.05,
    minTokens: (config.minTokens as number) ?? 50,
  });
}

/**
 * Hook to track entropy for each token
 */
export function trackEntropy(token: string, entropy: number): {
  token: string;
  entropy: number;
  index: number;
  isValley: boolean;
  velocity: number;
  shouldExit: boolean;
  stats: MonitorStats;
} {
  if (!monitor) {
    initHooks();
  }

  const point = monitor!.track(token, entropy);

  return {
    token,
    entropy,
    index: point.index,
    isValley: point.isValley,
    velocity: point.velocity,
    shouldExit: monitor!.shouldExit(),
    stats: monitor!.getStats(),
  };
}

/**
 * Hook to check if reasoning has converged
 */
export function earlyExit(): boolean {
  if (!monitor) {
    return false;
  }
  return monitor.shouldExit();
}

/**
 * Reset the global monitor state
 */
export function resetHooks(): void {
  if (monitor) {
    monitor.reset();
  }
}

/**
 * Get the current monitor instance
 */
export function getMonitor(): EntropyMonitor | null {
  return monitor;
}

/**
 * Class-based hook for frameworks that prefer class instances
 */
export class EntropyHook {
  private monitor: EntropyMonitor;
  private config: Record<string, unknown>;

  constructor(userConfig: Record<string, unknown> = {}) {
    this.config = userConfig;
    this.monitor = new EntropyMonitor({
      entropyThreshold: (this.config.entropyThreshold as number) ?? 0.15,
      minValleys: (this.config.minValleys as number) ?? 2,
      velocityThreshold: (this.config.velocityThreshold as number) ?? 0.05,
      minTokens: (this.config.minTokens as number) ?? 50,
    });
  }

  onToken(token: string, entropy: number): {
    token: string;
    entropy: number;
    index: number;
    isValley: boolean;
    velocity: number;
    shouldExit: boolean;
    stats: MonitorStats;
  } {
    const point = this.monitor.track(token, entropy);

    return {
      token,
      entropy,
      index: point.index,
      isValley: point.isValley,
      velocity: point.velocity,
      shouldExit: this.monitor.shouldExit(),
      stats: this.monitor.getStats(),
    };
  }

  shouldExit(): boolean {
    return this.monitor.shouldExit();
  }

  reset(): void {
    this.monitor.reset();
  }

  getStats(): MonitorStats {
    return this.monitor.getStats();
  }
}
