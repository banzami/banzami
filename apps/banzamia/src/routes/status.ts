import type { FastifyPluginAsync } from 'fastify';
import type { Config } from '../config.js';
import type { EmbeddingProvider } from '../rag/embedding/provider.js';
import type { ModelProvider } from '../orchestrator/providers/provider.js';
import { qdrantHealthy, collectionInfo } from '../store/qdrant.js';
import { getIndexState } from '../rag/indexer.js';
import type { RagStatus } from '../rag/types.js';

interface StatusDeps {
  cfg: Config;
  embedder: EmbeddingProvider;
  model: ModelProvider;
}

export const statusRoute: FastifyPluginAsync<StatusDeps> = async (fastify, opts) => {
  const { cfg, embedder, model } = opts;

  fastify.get('/status', async (_request, reply) => {
    const [healthy, embStatus, modelStatus, colInfo, indexState] = await Promise.allSettled([
      qdrantHealthy(cfg),
      embedder.status(),
      model.status(),
      collectionInfo(cfg),
      getIndexState(cfg),
    ]);

    const qdrantAvailable = healthy.status === 'fulfilled' && healthy.value;
    const colPoints = colInfo.status === 'fulfilled' ? colInfo.value.points_count : 0;
    const state = indexState.status === 'fulfilled' ? indexState.value : null;
    const emb = embStatus.status === 'fulfilled' ? embStatus.value : null;
    const mod = modelStatus.status === 'fulfilled' ? modelStatus.value : null;

    const rag: RagStatus = {
      qdrant: qdrantAvailable ? 'available' : 'unavailable',
      collection: cfg.qdrant.collection,
      documents_indexed: state?.document_count ?? 0,
      chunks_indexed: colPoints,
      embedding_provider: emb?.model ?? cfg.embedding.provider,
      last_indexed_at: state?.last_indexed_at ?? null,
      hybrid_search: qdrantAvailable ? 'available' : 'unavailable',
      authority_ranking: 'available',
    };

    return reply.send({
      status: 'ok',
      mode: cfg.mode,
      version: '1.0.0',
      rag,
      embedding: emb ?? { available: false, provider: cfg.embedding.provider, model: 'unknown', dims: cfg.embedding.dims },
      model: mod ?? { available: false, provider: 'unknown', models: {} },
    });
  });
};
