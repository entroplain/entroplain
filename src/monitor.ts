/**
 * Entropy Monitor — Core entropy tracking and early exit logic
 */

import { EntropyPoint, MonitorConfig, MonitorStats, ExitCondition } from './types';

export class EntropyMonitor {
  private config: MonitorConfig;
  private trajectory: EntropyPoint[] = [];
  private valleys: EntropyPoint[] = [];
  private index: number = 0;

  constructor(options: Partial<MonitorConfig> = {}) {
    this.config = {
      entropyThreshold: options.entropyThreshold ?? 0.15,
      minValleys: options.minValleys ?? 2,
      velocityThreshold: options.velocityThreshold ?? 0.05,
      minTokens: options.minTokens ?? 50,
      valleyWindow: options.valleyWindow ?? 5,
      plateauThreshold: options.plateauThreshold ?? 3,
      exitCondition: options.exitCondition ?? 'combined',
    };
  }

  /**
   * Calculate Shannon entropy from log probabilities
   */
  calculateEntropy(logprobs: number[], fromProbs: boolean = false): number {
    if (!logprobs || logprobs.length === 0) {
      return 0.0;
    }

    let entropy = 0.0;
    for (const lp of logprobs) {
      const prob = fromProbs ? lp : Math.exp(lp);
      if (prob > 0) {
        entropy -= prob * Math.log2(prob + 1e-10);
      }
    }

    return entropy;
  }

  /**
   * Track a token and its entropy value
   */
  track(token: string, entropy: number): EntropyPoint {
    const point: EntropyPoint = {
      index: this.index,
      token,
      entropy,
      isValley: false,
      velocity: 0.0,
    };

    // Calculate velocity
    if (this.trajectory.length > 0) {
      const prev = this.trajectory[this.trajectory.length - 1];
      point.velocity = Math.abs(entropy - prev.entropy);
    }

    // Detect valley (local minimum)
    if (this.trajectory.length >= 2) {
      const prev2 = this.trajectory[this.trajectory.length - 2];
      const prev1 = this.trajectory[this.trajectory.length - 1];
      if (prev1.entropy < prev2.entropy && prev1.entropy < entropy) {
        prev1.isValley = true;
        this.valleys.push(prev1);
      }
    }

    this.trajectory.push(point);
    this.index++;

    return point;
  }

  /**
   * Get all entropy valleys (local minima)
   */
  getValleys(): Array<[number, number]> {
    return this.valleys.map(v => [v.index, v.entropy]);
  }

  /**
   * Get current entropy velocity
   */
  getVelocity(): number {
    if (this.trajectory.length < 2) {
      return 0.0;
    }
    return this.trajectory[this.trajectory.length - 1].velocity;
  }

  /**
   * Get mean entropy over the trajectory
   */
  getMeanEntropy(): number {
    if (this.trajectory.length === 0) {
      return 0.0;
    }
    const sum = this.trajectory.reduce((acc, p) => acc + p.entropy, 0);
    return sum / this.trajectory.length;
  }

  /**
   * Get the number of detected valleys
   */
  getValleyCount(): number {
    return this.valleys.length;
  }

  /**
   * Check if valley count has plateaued
   */
  isValleysPlateau(): boolean {
    if (this.valleys.length < this.config.minValleys) {
      return false;
    }

    if (this.valleys.length < this.config.plateauThreshold) {
      return false;
    }

    const recent = this.valleys.slice(-this.config.plateauThreshold);
    const spacings: number[] = [];
    for (let i = 0; i < recent.length - 1; i++) {
      spacings.push(recent[i + 1].index - recent[i].index);
    }

    if (spacings.length === 0) return false;

    const meanSpacing = spacings.reduce((a, b) => a + b, 0) / spacings.length;
    const variance = spacings.reduce((acc, s) => acc + (s - meanSpacing) ** 2, 0) / spacings.length;

    return variance < 10;
  }

  /**
   * Check if current entropy is below threshold
   */
  isEntropyLow(): boolean {
    if (this.trajectory.length === 0) {
      return false;
    }
    return this.trajectory[this.trajectory.length - 1].entropy < this.config.entropyThreshold;
  }

  /**
   * Check if velocity is below threshold
   */
  isVelocityStable(): boolean {
    return this.getVelocity() < this.config.velocityThreshold;
  }

  /**
   * Determine if reasoning has converged
   */
  shouldExit(): boolean {
    // Always require minimum tokens
    if (this.trajectory.length < this.config.minTokens) {
      return false;
    }

    // Always require minimum valleys
    if (this.valleys.length < this.config.minValleys) {
      return false;
    }

    switch (this.config.exitCondition) {
      case 'valleys_plateau':
        return this.isValleysPlateau();
      case 'entropy_drop':
        return this.isEntropyLow();
      case 'velocity_zero':
        return this.isVelocityStable();
      case 'combined':
        return (this.isEntropyLow() || this.isValleysPlateau()) && this.isVelocityStable();
      default:
        return false;
    }
  }

  /**
   * Alias for shouldExit()
   */
  isConverged(): boolean {
    return this.shouldExit();
  }

  /**
   * Get full entropy trajectory
   */
  getTrajectory(): number[] {
    return this.trajectory.map(p => p.entropy);
  }

  /**
   * Get all tracked tokens
   */
  getTokens(): string[] {
    return this.trajectory.map(p => p.token);
  }

  /**
   * Get summary statistics
   */
  getStats(): MonitorStats {
    if (this.trajectory.length === 0) {
      return {
        tokenCount: 0,
        valleyCount: 0,
        meanEntropy: 0,
        minEntropy: 0,
        maxEntropy: 0,
        currentEntropy: 0,
        currentVelocity: 0,
        isConverged: false,
      };
    }

    const entropies = this.trajectory.map(p => p.entropy);

    return {
      tokenCount: this.trajectory.length,
      valleyCount: this.valleys.length,
      meanEntropy: this.getMeanEntropy(),
      minEntropy: Math.min(...entropies),
      maxEntropy: Math.max(...entropies),
      currentEntropy: entropies[entropies.length - 1],
      currentVelocity: this.getVelocity(),
      isConverged: this.shouldExit(),
    };
  }

  /**
   * Clear all tracked data
   */
  reset(): void {
    this.trajectory = [];
    this.valleys = [];
    this.index = 0;
  }
}

/**
 * Standalone function to calculate Shannon entropy
 */
export function calculateEntropy(logprobs: number[], fromProbs: boolean = false): number {
  const monitor = new EntropyMonitor();
  return monitor.calculateEntropy(logprobs, fromProbs);
}
