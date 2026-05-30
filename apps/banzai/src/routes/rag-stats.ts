import type { FastifyPluginAsync } from 'fastify';
import type { Config } from '../config.js';
import type { EmbeddingProvider } from '../rag/embedding/provider.js';
import type { ModelProvider } from '../orchestrator/providers/provider.js';
import { getAnalyticsReport } from '../analytics/tracker.js';
import { collectionInfo } from '../store/qdrant.js';
import { getIndexState } from '../rag/indexer.js';
import { getGraph } from '../graph/store.js';
import { graphStats } from '../graph/store.js';

interface RagStatsDeps {
  cfg: Config;
  embedder: EmbeddingProvider;
  model: ModelProvider;
}

export const ragStatsRoute: FastifyPluginAsync<RagStatsDeps> = async (fastify, opts) => {
  const { cfg } = opts;

  fastify.get('/rag/stats', async (_req, reply) => {
    const [colInfo, indexState, analytics, graph] = await Promise.allSettled([
      collectionInfo(cfg),
      getIndexState(cfg),
      Promise.resolve(getAnalyticsReport()),
      getGraph(cfg),
    ]);

    const col = colInfo.status === 'fulfilled' ? colInfo.value : { points_count: 0 };
    const state = indexState.status === 'fulfilled' ? indexState.value : null;
    const stats = analytics.status === 'fulfilled' ? analytics.value : null;
    const g = graph.status === 'fulfilled' ? graph.value : null;

    return reply.send({
      generated_at: new Date().toISOString(),
      knowledge_base: {
        documents_indexed: state?.document_count ?? 0,
        chunks_indexed: col.points_count,
        last_indexed_at: state?.last_indexed_at ?? null,
        embedding_provider: cfg.embedding.provider,
        embedding_dims: cfg.qdrant.dims,
      },
      query_analytics: stats ? {
        total_queries: stats.total_queries,
        avg_latency_ms: stats.avg_latency_ms,
        weak_retrieval_rate: stats.weak_retrieval_rate,
        avg_citations: stats.avg_citations,
        avg_top_authority: stats.avg_top_authority,
        task_type_distribution: stats.task_type_distribution,
        retrieval_mode_distribution: stats.retrieval_mode_distribution,
        top_sources: stats.top_sources,
      } : null,
      protocol_graph: g ? graphStats(g) : null,
    });
  });
};
