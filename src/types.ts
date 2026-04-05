/**
 * Type definitions for Entroplain
 */

export interface EntropyPoint {
  index: number;
  token: string;
  entropy: number;
  isValley: boolean;
  velocity: number;
}

export interface MonitorConfig {
  entropyThreshold: number;
  minValleys: number;
  velocityThreshold: number;
  minTokens: number;
  valleyWindow: number;
  plateauThreshold: number;
  exitCondition: ExitCondition;
}

export type ExitCondition = 
  | 'valleys_plateau' 
  | 'entropy_drop' 
  | 'velocity_zero' 
  | 'combined';

export interface MonitorStats {
  tokenCount: number;
  valleyCount: number;
  meanEntropy: number;
  minEntropy: number;
  maxEntropy: number;
  currentEntropy: number;
  currentVelocity: number;
  isConverged: boolean;
}

export interface TokenWithEntropy {
  token: string;
  entropy: number;
  logprob: number;
  topLogprobs: Array<{ token: string; logprob: number }>;
}

export interface ProviderConfig {
  apiKey?: string;
  baseUrl?: string;
  model?: string;
}

export interface StreamOptions {
  model?: string;
  messages?: Array<{ role: string; content: string }>;
  maxTokens?: number;
  topLogprobs?: number;
}
