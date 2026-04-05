"use strict";
/**
 * Hooks for agent framework integration
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.EntropyHook = void 0;
exports.initHooks = initHooks;
exports.trackEntropy = trackEntropy;
exports.earlyExit = earlyExit;
exports.resetHooks = resetHooks;
exports.getMonitor = getMonitor;
const monitor_1 = require("./monitor");
// Global monitor instance
let monitor = null;
let config = {};
/**
 * Initialize entropy hooks
 */
function initHooks(userConfig = {}) {
    config = userConfig;
    monitor = new monitor_1.EntropyMonitor({
        entropyThreshold: config.entropyThreshold ?? 0.15,
        minValleys: config.minValleys ?? 2,
        velocityThreshold: config.velocityThreshold ?? 0.05,
        minTokens: config.minTokens ?? 50,
    });
}
/**
 * Hook to track entropy for each token
 */
function trackEntropy(token, entropy) {
    if (!monitor) {
        initHooks();
    }
    const point = monitor.track(token, entropy);
    return {
        token,
        entropy,
        index: point.index,
        isValley: point.isValley,
        velocity: point.velocity,
        shouldExit: monitor.shouldExit(),
        stats: monitor.getStats(),
    };
}
/**
 * Hook to check if reasoning has converged
 */
function earlyExit() {
    if (!monitor) {
        return false;
    }
    return monitor.shouldExit();
}
/**
 * Reset the global monitor state
 */
function resetHooks() {
    if (monitor) {
        monitor.reset();
    }
}
/**
 * Get the current monitor instance
 */
function getMonitor() {
    return monitor;
}
/**
 * Class-based hook for frameworks that prefer class instances
 */
class EntropyHook {
    constructor(userConfig = {}) {
        this.config = userConfig;
        this.monitor = new monitor_1.EntropyMonitor({
            entropyThreshold: this.config.entropyThreshold ?? 0.15,
            minValleys: this.config.minValleys ?? 2,
            velocityThreshold: this.config.velocityThreshold ?? 0.05,
            minTokens: this.config.minTokens ?? 50,
        });
    }
    onToken(token, entropy) {
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
    shouldExit() {
        return this.monitor.shouldExit();
    }
    reset() {
        this.monitor.reset();
    }
    getStats() {
        return this.monitor.getStats();
    }
}
exports.EntropyHook = EntropyHook;
//# sourceMappingURL=hooks.js.map