import Fastify from 'fastify';
import cors from '@fastify/cors';
import { config } from './config.js';
import { createEmbeddingProvider } from './rag/embedding/factory.js';
import { MockModelProvider } from './orchestrator/providers/mock.js';
import { VLLMProvider } from './orchestrator/providers/vllm.js';
import { statusRoute } from './routes/status.js';
import { knowledgeRoute } from './routes/knowledge.js';
import { askRoute } from './routes/ask.js';
import { chatRoute } from './routes/chat.js';
import { graphRoute } from './routes/graph.js';
import { ragStatsRoute } from './routes/rag-stats.js';
import { researchRoute } from './routes/research.js';
import { certificationCopilotRoute } from './routes/certification-copilot.js';
import { simulateRoute } from './routes/simulate.js';
import { federationRoute } from './routes/federation.js';
import { memoryRoute } from './routes/memory.js';
import { digitalTwinRoute } from './routes/digital-twin.js';
import type { ModelProvider } from './orchestrator/providers/provider.js';

const fastify = Fastify({
  logger: {
    transport: {
      target: 'pino-pretty',
      options: { colorize: true },
    },
  },
});

await fastify.register(cors, { origin: true });

const embedder = createEmbeddingProvider(config);

const model: ModelProvider = config.mode === 'live-ai'
  ? new VLLMProvider({ url: config.vllm.url, models: config.vllm.models })
  : new MockModelProvider();

const deps = { cfg: config, embedder, model };

await fastify.register(statusRoute, deps);
await fastify.register(knowledgeRoute, deps);
await fastify.register(askRoute, deps);
await fastify.register(chatRoute, deps);
await fastify.register(graphRoute, { cfg: config });
await fastify.register(ragStatsRoute, deps);
await fastify.register(researchRoute, deps);
await fastify.register(certificationCopilotRoute);
await fastify.register(simulateRoute);
await fastify.register(federationRoute);
await fastify.register(memoryRoute);
await fastify.register(digitalTwinRoute);

fastify.get('/health', async () => ({ ok: true }));

try {
  await fastify.listen({ port: config.port, host: '0.0.0.0' });
  fastify.log.info(`BanzAI running on port ${config.port} [mode: ${config.mode}]`);
} catch (err) {
  fastify.log.error(err);
  process.exit(1);
}
