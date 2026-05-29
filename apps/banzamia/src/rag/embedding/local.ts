import type { EmbeddingProvider, EmbeddingProviderStatus } from './provider.js';

type HFPipeline = (
  texts: string | string[],
  opts: { pooling: string; normalize: boolean },
) => Promise<{ data: Float32Array }>;

export class LocalEmbeddingProvider implements EmbeddingProvider {
  readonly name = 'local';
  private pipe: HFPipeline | null = null;
  private initError: string | null = null;

  constructor(
    readonly model: string,
    readonly dims: number,
  ) {}

  private async init(): Promise<HFPipeline | null> {
    if (this.pipe) return this.pipe;
    if (this.initError) return null;
    try {
      const { pipeline } = await import('@huggingface/transformers');
      this.pipe = (await pipeline('feature-extraction', this.model)) as unknown as HFPipeline;
      return this.pipe;
    } catch (e) {
      this.initError = String(e);
      return null;
    }
  }

  async embed(text: string): Promise<number[]> {
    const [vec] = await this.embedBatch([text]);
    return vec;
  }

  async embedBatch(texts: string[]): Promise<number[][]> {
    const pipe = await this.init();
    if (!pipe) throw new Error(`Local embedding provider unavailable: ${this.initError}`);

    const results: number[][] = [];
    for (const text of texts) {
      const out = await pipe(text, { pooling: 'mean', normalize: true });
      results.push(Array.from(out.data));
    }
    return results;
  }

  async status(): Promise<EmbeddingProviderStatus> {
    const pipe = await this.init();
    return {
      available: pipe !== null,
      provider: 'local',
      model: this.model,
      dims: this.dims,
      ...(this.initError ? { error: this.initError } : {}),
    };
  }
}
