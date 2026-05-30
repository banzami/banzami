import type { EmbeddingProvider, EmbeddingProviderStatus } from './provider.js';

interface OpenAIEmbeddingResponse {
  data: Array<{ embedding: number[]; index: number }>;
  usage: { total_tokens: number };
}

export class RemoteEmbeddingProvider implements EmbeddingProvider {
  readonly name = 'remote';

  constructor(
    readonly url: string,
    readonly model: string,
    readonly dims: number,
  ) {}

  private async call(texts: string[]): Promise<number[][]> {
    const response = await fetch(this.url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: texts, model: this.model }),
    });

    if (!response.ok) {
      const body = await response.text();
      throw new Error(`Remote embedding endpoint returned ${response.status}: ${body}`);
    }

    const json: OpenAIEmbeddingResponse = await response.json() as OpenAIEmbeddingResponse;
    return json.data
      .sort((a, b) => a.index - b.index)
      .map((d) => d.embedding);
  }

  async embed(text: string): Promise<number[]> {
    const [vec] = await this.call([text]);
    return vec;
  }

  async embedBatch(texts: string[]): Promise<number[][]> {
    const BATCH = 32;
    const results: number[][] = [];
    for (let i = 0; i < texts.length; i += BATCH) {
      results.push(...await this.call(texts.slice(i, i + BATCH)));
    }
    return results;
  }

  async status(): Promise<EmbeddingProviderStatus> {
    try {
      await this.embed('ping');
      return { available: true, provider: 'remote', model: this.model, dims: this.dims };
    } catch (e) {
      return {
        available: false,
        provider: 'remote',
        model: this.model,
        dims: this.dims,
        error: String(e),
      };
    }
  }
}
