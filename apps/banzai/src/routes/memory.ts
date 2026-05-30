import type { FastifyInstance } from 'fastify';
import {
  getMemory,
  getOrCreate,
  addNote,
  recordAssessment,
  listOperatorIds,
  deleteMemory,
} from '../memory/operator-memory.js';

export async function memoryRoute(fastify: FastifyInstance) {
  // List all operators with memory
  fastify.get('/memory', async () => {
    return { operator_ids: listOperatorIds() };
  });

  // Get operator memory
  fastify.get('/memory/:operatorId', async (req, reply) => {
    const { operatorId } = req.params as { operatorId: string };
    const mem = getMemory(operatorId);
    if (!mem) return reply.code(404).send({ error: `No memory found for operator: ${operatorId}` });
    return mem;
  });

  // Init / upsert operator memory
  fastify.post('/memory/:operatorId', async (req, reply) => {
    const { operatorId } = req.params as { operatorId: string };
    const body = req.body as {
      note?: string;
      assessment?: {
        target_level: number;
        readiness_score: number;
        current_level: number;
        missing_count: number;
        capabilities: string[];
        manifest: Record<string, unknown>;
      };
    };
    if (!body || typeof body !== 'object') return reply.code(400).send({ error: 'Body required' });
    if (body.note) addNote(operatorId, body.note);
    if (body.assessment) {
      const { manifest, ...snap } = body.assessment;
      recordAssessment(operatorId, snap, manifest, snap.capabilities);
    }
    return getOrCreate(operatorId);
  });

  // Delete operator memory
  fastify.delete('/memory/:operatorId', async (req) => {
    const { operatorId } = req.params as { operatorId: string };
    deleteMemory(operatorId);
    return { deleted: operatorId };
  });
}
