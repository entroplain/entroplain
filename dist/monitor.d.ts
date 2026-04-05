/**
 * Entropy Monitor — Core entropy tracking and early exit logic
 */
import { EntropyPoint, MonitorConfig, MonitorStats } from './types';
export declare class EntropyMonitor {
    private config;
    private trajectory;
    private valleys;
    private index;
    constructor(options?: Partial<MonitorConfig>);
    /**
     * Calculate Shannon entropy from log probabilities
     */
    calculateEntropy(logprobs: number[], fromProbs?: boolean): number;
    /**
     * Track a token and its entropy value
     */
    track(token: string, entropy: number): EntropyPoint;
    /**
     * Get all entropy valleys (local minima)
     */
    getValleys(): Array<[number, number]>;
    /**
     * Get current entropy velocity
     */
    getVelocity(): number;
    /**
     * Get mean entropy over the trajectory
     */
    getMeanEntropy(): number;
    /**
     * Get the number of detected valleys
     */
    getValleyCount(): number;
    /**
     * Check if valley count has plateaued
     */
    isValleysPlateau(): boolean;
    /**
     * Check if current entropy is below threshold
     */
    isEntropyLow(): boolean;
    /**
     * Check if velocity is below threshold
     */
    isVelocityStable(): boolean;
    /**
     * Determine if reasoning has converged
     */
    shouldExit(): boolean;
    /**
     * Alias for shouldExit()
     */
    isConverged(): boolean;
    /**
     * Get full entropy trajectory
     */
    getTrajectory(): number[];
    /**
     * Get all tracked tokens
     */
    getTokens(): string[];
    /**
     * Get summary statistics
     */
    getStats(): MonitorStats;
    /**
     * Clear all tracked data
     */
    reset(): void;
}
/**
 * Standalone function to calculate Shannon entropy
 */
export declare function calculateEntropy(logprobs: number[], fromProbs?: boolean): number;
//# sourceMappingURL=monitor.d.ts.map