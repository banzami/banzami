import type { FastifyPluginAsync } from 'fastify';
import type { Config } from '../config.js';
import type { EmbeddingProvider } from '../rag/embedding/provider.js';
import { search } from '../rag/search.js';
import type { SearchFilters } from '../rag/types.js';

interface KnowledgeDeps {
  cfg: Config;
  embedder: EmbeddingProvider;
}

interface SearchBody {
  query: string;
  filters?: SearchFilters;
  limit?: number;
}

export const knowledgeRoute: FastifyPluginAsync<KnowledgeDeps> = async (fastify, opts) => {
  const { cfg, embedder } = opts;

  fastify.post<{ Body: SearchBody }>('/knowledge/search', {
    schema: {
      body: {
        type: 'object',
        required: ['query'],
        properties: {
          query: { type: 'string', minLength: 1, maxLength: 2000 },
          filters: { type: 'object' },
          limit: { type: 'integer', minimum: 1, maximum: 50 },
        },
      },
    },
  }, async (request, reply) => {
    const { query, filters = {}, limit = 8 } = request.body;

    const response = await search(cfg, embedder, query, limit, filters as SearchFilters);
    return reply.send(response);
  });
};
