export interface EmbeddingProvider {
  embed(text: string): Promise<number[]>;
  embedBatch(texts: string[]): Promise<number[][]>;
  status(): Promise<EmbeddingProviderStatus>;
  readonly dims: number;
  readonly name: string;
}

export interface EmbeddingProviderStatus {
  available: boolean;
  provider: string;
  model: string;
  dims: number;
  error?: string;
}
