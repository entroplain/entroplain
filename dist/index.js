"use strict";
/**
 * Entroplain — Entropy-based early exit for efficient agent reasoning
 *
 * @packageDocumentation
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.earlyExit = exports.trackEntropy = exports.EntropyHook = exports.calculateEntropy = exports.EntropyMonitor = void 0;
var monitor_1 = require("./monitor");
Object.defineProperty(exports, "EntropyMonitor", { enumerable: true, get: function () { return monitor_1.EntropyMonitor; } });
Object.defineProperty(exports, "calculateEntropy", { enumerable: true, get: function () { return monitor_1.calculateEntropy; } });
var hooks_1 = require("./hooks");
Object.defineProperty(exports, "EntropyHook", { enumerable: true, get: function () { return hooks_1.EntropyHook; } });
Object.defineProperty(exports, "trackEntropy", { enumerable: true, get: function () { return hooks_1.trackEntropy; } });
Object.defineProperty(exports, "earlyExit", { enumerable: true, get: function () { return hooks_1.earlyExit; } });
__exportStar(require("./types"), exports);
//# sourceMappingURL=index.js.map