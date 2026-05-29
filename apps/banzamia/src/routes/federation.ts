import type { FastifyInstance } from 'fastify';
import { analyzeFederation } from '../tools/federation-intelligence.js';
import { recordFederation } from '../memory/operator-memory.js';

export async function federationRoute(fastify: FastifyInstance) {
  fastify.post('/federation/analyze', async (req, reply) => {
    const body = req.body as {
      operator_a?: { operator_id?: string; manifest?: Record<string, unknown>; capabilities?: string[] };
      operator_b?: { operator_id?: string; manifest?: Record<string, unknown>; capabilities?: string[] };
    };
    if (!body.operator_a?.manifest || !body.operator_b?.manifest) {
      return reply.code(400).send({ error: 'operator_a and operator_b with manifest are required' });
    }
    const a = {
      operator_id: body.operator_a.operator_id ?? 'operator_a',
      manifest: body.operator_a.manifest,
      capabilities: body.operator_a.capabilities ?? [],
    };
    const b = {
      operator_id: body.operator_b.operator_id ?? 'operator_b',
      manifest: body.operator_b.manifest,
      capabilities: body.operator_b.capabilities ?? [],
    };
    const result = analyzeFederation(a, b);
    // Record federation attempt in memory
    recordFederation(a.operator_id, b.operator_id, result.federation_ready);
    recordFederation(b.operator_id, a.operator_id, result.federation_ready);
    return result;
  });
}
