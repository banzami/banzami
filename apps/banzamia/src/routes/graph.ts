import type { FastifyPluginAsync } from 'fastify';
import type { Config } from '../config.js';
import { getGraph } from '../graph/store.js';
import { findNode, findNodeByPath, findNodeByTitle, getNeighbours, getRelated, findPath, graphStats } from '../graph/store.js';

interface GraphDeps {
  cfg: Config;
}

export const graphRoute: FastifyPluginAsync<GraphDeps> = async (fastify, opts) => {
  const { cfg } = opts;

  fastify.get('/graph/stats', async (_req, reply) => {
    const graph = await getGraph(cfg);
    if (!graph) return reply.status(503).send({ error: 'Graph not indexed. Run: npm run graph:index' });
    return reply.send(graphStats(graph));
  });

  fastify.get<{ Params: { id: string } }>('/graph/node/:id', async (req, reply) => {
    const graph = await getGraph(cfg);
    if (!graph) return reply.status(503).send({ error: 'Graph not indexed' });

    const id = decodeURIComponent(req.params.id);
    const node = findNode(graph, id);
    if (!node) return reply.status(404).send({ error: `Node not found: ${id}` });

    const neighbours = getNeighbours(graph, node.id);
    return reply.send({ node, neighbours });
  });

  fastify.get<{ Querystring: { q: string; type?: string } }>('/graph/search', async (req, reply) => {
    const graph = await getGraph(cfg);
    if (!graph) return reply.status(503).send({ error: 'Graph not indexed' });

    const q = req.query.q ?? '';
    if (!q) return reply.status(400).send({ error: 'q parameter required' });

    const byPath = findNodeByPath(graph, q);
    const byTitle = findNodeByTitle(graph, q);

    const seen = new Set<string>();
    const results = [];
    for (const n of [...byPath, ...byTitle]) {
      if (!seen.has(n.id)) {
        seen.add(n.id);
        results.push(n);
      }
    }

    return reply.send({ query: q, count: results.length, nodes: results.slice(0, 20) });
  });

  fastify.get<{ Params: { id: string }; Querystring: { depth?: string } }>('/graph/related/:id', async (req, reply) => {
    const graph = await getGraph(cfg);
    if (!graph) return reply.status(503).send({ error: 'Graph not indexed' });

    const id = decodeURIComponent(req.params.id);
    const depth = Math.min(parseInt(req.query.depth ?? '2', 10), 4);

    const node = findNode(graph, id);
    if (!node) return reply.status(404).send({ error: `Node not found: ${id}` });

    const related = getRelated(graph, node.id, depth);
    return reply.send({ node, depth, related_count: related.length, related });
  });

  fastify.get<{ Querystring: { from: string; to: string } }>('/graph/path', async (req, reply) => {
    const graph = await getGraph(cfg);
    if (!graph) return reply.status(503).send({ error: 'Graph not indexed' });

    const { from, to } = req.query;
    if (!from || !to) return reply.status(400).send({ error: 'from and to parameters required' });

    const fromNode = findNode(graph, from);
    const toNode = findNode(graph, to);

    if (!fromNode) return reply.status(404).send({ error: `Node not found: ${from}` });
    if (!toNode) return reply.status(404).send({ error: `Node not found: ${to}` });

    const path = findPath(graph, fromNode.id, toNode.id);
    if (!path) return reply.send({ from: fromNode, to: toNode, path: null, reachable: false });

    return reply.send({ from: fromNode, to: toNode, path, reachable: true });
  });
};
