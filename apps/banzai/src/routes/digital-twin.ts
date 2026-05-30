import type { FastifyInstance } from 'fastify';
import { buildDigitalTwin, type DigitalTwinInput } from '../tools/digital-twin.js';
import { recordAssessment } from '../memory/operator-memory.js';

export async function digitalTwinRoute(fastify: FastifyInstance) {
  fastify.post('/digital-twin', async (req, reply) => {
    const body = req.body as Partial<DigitalTwinInput>;
    if (!body.operator_id || !body.manifest || !Array.isArray(body.capabilities)) {
      return reply.code(400).send({ error: 'operator_id, manifest, and capabilities are required' });
    }
    const twin = buildDigitalTwin({
      operator_id: body.operator_id,
      manifest: body.manifest,
      capabilities: body.capabilities,
      target_level: typeof body.target_level === 'number' ? body.target_level : 4,
      partner_manifests: body.partner_manifests,
    });
    // Auto-record this as an assessment in memory
    recordAssessment(
      body.operator_id,
      {
        target_level: twin.certification.target_level,
        readiness_score: twin.certification.readiness_score,
        current_level: twin.certification.current_level,
        missing_count: twin.certification.missing_for_target.length,
        capabilities: body.capabilities,
      },
      body.manifest,
      body.capabilities,
    );
    return twin;
  });
}
