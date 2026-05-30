import type { FastifyInstance } from 'fastify';
import { runSimulation, type SimulatorInput } from '../tools/protocol-simulator.js';

export async function simulateRoute(fastify: FastifyInstance) {
  fastify.post('/simulate', async (req, reply) => {
    const body = req.body as Partial<SimulatorInput>;
    if (!body.manifest || !Array.isArray(body.capabilities) || !Array.isArray(body.proposed_changes)) {
      return reply.code(400).send({ error: 'manifest, capabilities, and proposed_changes are required' });
    }
    const result = runSimulation({
      manifest: body.manifest,
      capabilities: body.capabilities,
      target_level: typeof body.target_level === 'number' ? body.target_level : 2,
      proposed_changes: body.proposed_changes,
    });
    return result;
  });
}
