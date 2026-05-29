import type { FastifyPluginAsync } from 'fastify';
import { analyzeCertificationReadiness } from '../tools/certification-copilot.js';

export const certificationCopilotRoute: FastifyPluginAsync = async (fastify) => {
  fastify.post<{
    Body: {
      manifest?: Record<string, unknown>;
      capabilities?: string[];
      conformance_results?: Array<{ id: string; status: 'PASS' | 'FAIL' | 'SKIP'; level: number }>;
      declared_level?: number;
      target_level?: number;
    };
  }>(
    '/certification/copilot',
    {
      schema: {
        body: {
          type: 'object',
          properties: {
            manifest:             { type: 'object' },
            capabilities:         { type: 'array', items: { type: 'string' } },
            conformance_results:  { type: 'array' },
            declared_level:       { type: 'number' },
            target_level:         { type: 'number' },
          },
        },
      },
    },
    async (req, reply) => {
      const result = analyzeCertificationReadiness(req.body);
      return reply.send(result);
    },
  );
};
