export type EmbeddingProviderType = 'mock' | 'local' | 'remote';
export type BanzamIAMode = 'demo' | 'live-api-no-model' | 'live-ai';

export interface Config {
  mode: BanzamIAMode;
  port: number;
  qdrant: {
    url: string;
    collection: string;
    dims: number;
  };
  embedding: {
    provider: EmbeddingProviderType;
    model: string;
    url: string;
    remoteModel: string;
    dims: number;
  };
  vllm: {
    url: string;
    models: {
      qwen: string;
      qwenCoder: string;
      deepseek: string;
    };
  };
  docsRoot: string;
}

function env(key: string, fallback = ''): string {
  return process.env[key] ?? fallback;
}

function envInt(key: string, fallback: number): number {
  const v = process.env[key];
  return v ? parseInt(v, 10) : fallback;
}

export const config: Config = {
  mode: (env('BANZAMIA_MODE', 'live-api-no-model')) as BanzamIAMode,
  port: envInt('BANZAMIA_PORT', 4200),
  qdrant: {
    url: env('BANZAMIA_QDRANT_URL', 'http://localhost:6333'),
    collection: env('BANZAMIA_COLLECTION', 'banzamia_knowledge'),
    dims: envInt('BANZAMIA_EMBEDDING_DIMS', 1024),
  },
  embedding: {
    provider: (env('BANZAMIA_EMBEDDING_PROVIDER', 'mock')) as EmbeddingProviderType,
    model: env('BANZAMIA_EMBEDDING_MODEL', 'Xenova/bge-large-en-v1.5'),
    url: env('BANZAMIA_EMBEDDING_URL', 'http://localhost:8000/v1/embeddings'),
    remoteModel: env('BANZAMIA_EMBEDDING_REMOTE_MODEL', 'bge-large-en-v1.5'),
    dims: envInt('BANZAMIA_EMBEDDING_DIMS', 1024),
  },
  vllm: {
    url: env('BANZAMIA_VLLM_URL', 'http://localhost:8000/v1'),
    models: {
      qwen: env('BANZAMIA_MODEL_QWEN', 'Qwen/Qwen2.5-7B-Instruct'),
      qwenCoder: env('BANZAMIA_MODEL_QWEN_CODER', 'Qwen/Qwen2.5-Coder-7B-Instruct'),
      deepseek: env('BANZAMIA_MODEL_DEEPSEEK', 'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B'),
    },
  },
  docsRoot: env('BANZAMIA_DOCS_ROOT', '../../'),
};
