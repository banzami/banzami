import { createHash } from 'node:crypto';
import type { EmbeddingProvider, EmbeddingProviderStatus } from './provider.js';

export class MockEmbeddingProvider implements EmbeddingProvider {
  readonly name = 'mock';

  constructor(readonly dims: number = 1024) {}

  private pseudoVector(text: string): number[] {
    const hash = createHash('sha256').update(text).digest();
    const vec: number[] = [];
    for (let i = 0; i < this.dims; i++) {
      const byte = hash[i % hash.length];
      vec.push((byte / 127.5) - 1.0);
    }
    const norm = Math.sqrt(vec.reduce((s, v) => s + v * v, 0));
    return vec.map((v) => v / (norm || 1));
  }

  async embed(text: string): Promise<number[]> {
    return this.pseudoVector(text);
  }

  async embedBatch(texts: string[]): Promise<number[][]> {
    return texts.map((t) => this.pseudoVector(t));
  }

  async status(): Promise<EmbeddingProviderStatus> {
    return {
      available: true,
      provider: 'mock',
      model: 'deterministic-pseudo-random',
      dims: this.dims,
    };
  }
}
