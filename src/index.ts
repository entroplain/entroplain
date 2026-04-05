/**
 * Entroplain — Entropy-based early exit for efficient agent reasoning
 * 
 * @packageDocumentation
 */

export { EntropyMonitor, calculateEntropy } from './monitor';
export { EntropyHook, trackEntropy, earlyExit } from './hooks';
export * from './types';
