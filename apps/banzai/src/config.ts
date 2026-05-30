export type EmbeddingProviderType = 'mock' | 'local' | 'remote';
export type BanzAIMode = 'demo' | 'live-api-no-model' | 'live-ai';

export interface Config {
  mode: BanzAIMode;
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

// Read BANZAI_* first; fall back to BANZAMIA_* for backward compatibility with existing deployments
function env(key: string, legacyKey: string, fallback = ''): string {
  return process.env[key] ?? process.env[legacyKey] ?? fallback;
}

function envInt(key: string, legacyKey: string, fallback: number): number {
  const v = process.env[key] ?? process.env[legacyKey];
  return v ? parseInt(v, 10) : fallback;
}

export const config: Config = {
  mode: (env('BANZAI_MODE', 'BANZAMIA_MODE', 'live-api-no-model')) as BanzAIMode,
  port: envInt('BANZAI_PORT', 'BANZAMIA_PORT', 4200),
  qdrant: {
    url: env('BANZAI_QDRANT_URL', 'BANZAMIA_QDRANT_URL', 'http://localhost:6333'),
    collection: env('BANZAI_COLLECTION', 'BANZAMIA_COLLECTION', 'banzai_knowledge'),
    dims: envInt('BANZAI_EMBEDDING_DIMS', 'BANZAMIA_EMBEDDING_DIMS', 1024),
  },
  embedding: {
    provider: (env('BANZAI_EMBEDDING_PROVIDER', 'BANZAMIA_EMBEDDING_PROVIDER', 'mock')) as EmbeddingProviderType,
    model: env('BANZAI_EMBEDDING_MODEL', 'BANZAMIA_EMBEDDING_MODEL', 'Xenova/bge-large-en-v1.5'),
    url: env('BANZAI_EMBEDDING_URL', 'BANZAMIA_EMBEDDING_URL', 'http://localhost:8000/v1/embeddings'),
    remoteModel: env('BANZAI_EMBEDDING_REMOTE_MODEL', 'BANZAMIA_EMBEDDING_REMOTE_MODEL', 'bge-large-en-v1.5'),
    dims: envInt('BANZAI_EMBEDDING_DIMS', 'BANZAMIA_EMBEDDING_DIMS', 1024),
  },
  vllm: {
    url: env('BANZAI_VLLM_URL', 'BANZAMIA_VLLM_URL', 'http://localhost:8000/v1'),
    models: {
      qwen: env('BANZAI_MODEL_QWEN', 'BANZAMIA_MODEL_QWEN', 'Qwen/Qwen2.5-7B-Instruct'),
      qwenCoder: env('BANZAI_MODEL_QWEN_CODER', 'BANZAMIA_MODEL_QWEN_CODER', 'Qwen/Qwen2.5-Coder-7B-Instruct'),
      deepseek: env('BANZAI_MODEL_DEEPSEEK', 'BANZAMIA_MODEL_DEEPSEEK', 'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B'),
    },
  },
  docsRoot: env('BANZAI_DOCS_ROOT', 'BANZAMIA_DOCS_ROOT', '../../'),
};
