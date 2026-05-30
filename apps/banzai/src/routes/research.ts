import type { FastifyPluginAsync } from 'fastify';
import type { Config } from '../config.js';
import type { EmbeddingProvider } from '../rag/embedding/provider.js';
import type { ModelProvider } from '../orchestrator/providers/provider.js';
import { runResearch } from '../agent/researcher.js';

interface ResearchDeps {
  cfg: Config;
  embedder: EmbeddingProvider;
  model: ModelProvider;
}

export const researchRoute: FastifyPluginAsync<ResearchDeps> = async (fastify, opts) => {
  const { cfg, embedder, model } = opts;

  fastify.post<{ Body: { question: string } }>(
    '/research',
    {
      schema: {
        body: {
          type: 'object',
          required: ['question'],
          properties: {
            question: { type: 'string', minLength: 3, maxLength: 2000 },
          },
        },
      },
    },
    async (req, reply) => {
      const { question } = req.body;
      const report = await runResearch(cfg, embedder, model, question);
      return reply.send(report);
    },
  );
};
