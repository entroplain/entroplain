/**
 * Hooks for agent framework integration
 */
import { EntropyMonitor } from './monitor';
import { MonitorStats } from './types';
/**
 * Initialize entropy hooks
 */
export declare function initHooks(userConfig?: Record<string, unknown>): void;
/**
 * Hook to track entropy for each token
 */
export declare function trackEntropy(token: string, entropy: number): {
    token: string;
    entropy: number;
    index: number;
    isValley: boolean;
    velocity: number;
    shouldExit: boolean;
    stats: MonitorStats;
};
/**
 * Hook to check if reasoning has converged
 */
export declare function earlyExit(): boolean;
/**
 * Reset the global monitor state
 */
export declare function resetHooks(): void;
/**
 * Get the current monitor instance
 */
export declare function getMonitor(): EntropyMonitor | null;
/**
 * Class-based hook for frameworks that prefer class instances
 */
export declare class EntropyHook {
    private monitor;
    private config;
    constructor(userConfig?: Record<string, unknown>);
    onToken(token: string, entropy: number): {
        token: string;
        entropy: number;
        index: number;
        isValley: boolean;
        velocity: number;
        shouldExit: boolean;
        stats: MonitorStats;
    };
    shouldExit(): boolean;
    reset(): void;
    getStats(): MonitorStats;
}
//# sourceMappingURL=hooks.d.ts.map