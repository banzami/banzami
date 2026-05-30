import type { FastifyPluginAsync } from 'fastify';
import type { Config } from '../config.js';
import type { EmbeddingProvider } from '../rag/embedding/provider.js';
import type { ModelProvider } from '../orchestrator/providers/provider.js';
import { ask } from '../orchestrator/pipeline.js';
import { validateManifest } from '../tools/manifest-validator.js';
import { runConformanceCheck } from '../tools/conformance-runner.js';
import type { CertificationLevel, OperatorCapabilities } from '../tools/conformance-runner.js';

interface AskDeps {
  cfg: Config;
  embedder: EmbeddingProvider;
  model: ModelProvider;
}

interface AskBody {
  question: string;
  filters?: Record<string, unknown>;
  context_limit?: number;
}

interface ValidateBody {
  manifest: unknown;
}

interface ConformanceBody {
  capabilities: OperatorCapabilities;
  target_level: CertificationLevel;
}

export const askRoute: FastifyPluginAsync<AskDeps> = async (fastify, opts) => {
  const { cfg, embedder, model } = opts;

  fastify.post<{ Body: AskBody }>('/ask', {
    schema: {
      body: {
        type: 'object',
        required: ['question'],
        properties: {
          question: { type: 'string', minLength: 1, maxLength: 4000 },
          filters: { type: 'object' },
          context_limit: { type: 'integer', minimum: 1, maximum: 20 },
        },
      },
    },
  }, async (request, reply) => {
    const { question, filters, context_limit } = request.body;
    const response = await ask(cfg, embedder, model, {
      question,
      filters: filters as never,
      context_limit,
    });
    return reply.send(response);
  });

  fastify.post<{ Body: ValidateBody }>('/tools/validate', {
    schema: {
      body: {
        type: 'object',
        required: ['manifest'],
        properties: {
          manifest: {},
        },
      },
    },
  }, async (request, reply) => {
    const result = validateManifest(request.body.manifest);
    return reply.send(result);
  });

  fastify.post<{ Body: ConformanceBody }>('/tools/conformance', {
    schema: {
      body: {
        type: 'object',
        required: ['capabilities', 'target_level'],
        properties: {
          capabilities: { type: 'object' },
          target_level: { type: 'integer', minimum: 0, maximum: 4 },
        },
      },
    },
  }, async (request, reply) => {
    const { capabilities, target_level } = request.body;
    const result = runConformanceCheck(capabilities, target_level);
    return reply.send(result);
  });
};
