import type { FastifyPluginAsync } from 'fastify';
import type { Config } from '../config.js';
import type { EmbeddingProvider } from '../rag/embedding/provider.js';
import type { ModelProvider, ChatMessage } from '../orchestrator/providers/provider.js';
import { ask, askStream } from '../orchestrator/pipeline.js';
import { explainTrace } from '../tools/trace-explainer.js';
import type { TraceEvent } from '../tools/trace-explainer.js';

interface ChatDeps {
  cfg: Config;
  embedder: EmbeddingProvider;
  model: ModelProvider;
}

interface ChatBody {
  messages: ChatMessage[];
  filters?: Record<string, unknown>;
  stream?: boolean;
}

interface TraceBody {
  events: TraceEvent[];
}

export const chatRoute: FastifyPluginAsync<ChatDeps> = async (fastify, opts) => {
  const { cfg, embedder, model } = opts;

  fastify.post<{ Body: ChatBody }>('/chat', {
    schema: {
      body: {
        type: 'object',
        required: ['messages'],
        properties: {
          messages: { type: 'array', minItems: 1, maxItems: 50 },
          filters: { type: 'object' },
          stream: { type: 'boolean' },
        },
      },
    },
  }, async (request, reply) => {
    const { messages, filters } = request.body;
    const lastUser = [...messages].reverse().find((m: ChatMessage) => m.role === 'user');
    if (!lastUser) {
      return reply.status(400).send({ error: 'No user message in conversation' });
    }

    const response = await ask(cfg, embedder, model, {
      question: lastUser.content,
      filters: filters as never,
    });
    return reply.send(response);
  });

  fastify.get('/chat/stream', async (request, reply) => {
    const q = (request.query as Record<string, string>).q ?? '';
    if (!q) {
      reply.raw.writeHead(400, { 'Content-Type': 'text/plain' });
      reply.raw.end('Missing ?q= parameter');
      return reply;
    }

    reply.raw.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no',
    });

    const writeEvent = (data: unknown) => {
      reply.raw.write(`data: ${JSON.stringify(data)}\n\n`);
    };

    try {
      const result = await askStream(cfg, embedder, model, { question: q }, (token) => {
        writeEvent({ token });
      });

      writeEvent({ done: true, citations: result.citations, task_type: result.task_type });
    } catch (e) {
      writeEvent({ error: String(e) });
    }

    reply.raw.end();
    return reply;
  });

  fastify.post<{ Body: TraceBody }>('/tools/trace', {
    schema: {
      body: {
        type: 'object',
        required: ['events'],
        properties: {
          events: { type: 'array' },
        },
      },
    },
  }, async (request, reply) => {
    const analysis = explainTrace(request.body.events);
    return reply.send(analysis);
  });
};
