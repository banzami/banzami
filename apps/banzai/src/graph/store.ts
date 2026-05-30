import { resolve } from 'node:path';
import { loadGraph } from './indexer.js';
import type { ProtocolGraph, GraphNode, GraphEdge, GraphNeighbour, GraphPath, RelationshipType } from './types.js';
import type { Config } from '../config.js';

let _graph: ProtocolGraph | null = null;
let _repoRoot: string | null = null;

export function setGraph(graph: ProtocolGraph): void {
  _graph = graph;
}

function repoRoot(cfg: Config): string {
  if (!_repoRoot) {
    _repoRoot = resolve(new URL(import.meta.url).pathname, '../../../', cfg.docsRoot);
  }
  return _repoRoot;
}

export async function getGraph(cfg: Config): Promise<ProtocolGraph | null> {
  if (_graph) return _graph;
  const root = repoRoot(cfg);
  _graph = await loadGraph(root);
  return _graph;
}

export function findNode(graph: ProtocolGraph, id: string): GraphNode | null {
  return graph.nodes.find((n) => n.id === id || n.path.includes(id)) ?? null;
}

export function findNodeByPath(graph: ProtocolGraph, pathFragment: string): GraphNode[] {
  const lower = pathFragment.toLowerCase();
  return graph.nodes.filter((n) => n.path.toLowerCase().includes(lower));
}

export function findNodeByTitle(graph: ProtocolGraph, titleFragment: string): GraphNode[] {
  const lower = titleFragment.toLowerCase();
  return graph.nodes.filter((n) => n.title.toLowerCase().includes(lower));
}

export function getNeighbours(
  graph: ProtocolGraph,
  nodeId: string,
  relationshipFilter?: RelationshipType[],
): GraphNeighbour[] {
  const neighbours: GraphNeighbour[] = [];

  for (const edge of graph.edges) {
    if (relationshipFilter && !relationshipFilter.includes(edge.relationship)) continue;

    if (edge.from === nodeId) {
      const node = findNode(graph, edge.to);
      if (node) neighbours.push({ node, relationship: edge.relationship, direction: 'outbound' });
    }
    if (edge.to === nodeId) {
      const node = findNode(graph, edge.from);
      if (node) neighbours.push({ node, relationship: edge.relationship, direction: 'inbound' });
    }
  }

  return neighbours;
}

export function getRelated(
  graph: ProtocolGraph,
  nodeId: string,
  maxDepth = 2,
): GraphNode[] {
  const visited = new Set<string>([nodeId]);
  const result: GraphNode[] = [];
  const queue: Array<{ id: string; depth: number }> = [{ id: nodeId, depth: 0 }];

  while (queue.length > 0) {
    const current = queue.shift()!;
    if (current.depth >= maxDepth) continue;

    for (const edge of graph.edges) {
      let neighbourId: string | null = null;
      if (edge.from === current.id) neighbourId = edge.to;
      else if (edge.to === current.id) neighbourId = edge.from;

      if (neighbourId && !visited.has(neighbourId)) {
        visited.add(neighbourId);
        const node = findNode(graph, neighbourId);
        if (node) {
          result.push(node);
          queue.push({ id: neighbourId, depth: current.depth + 1 });
        }
      }
    }
  }

  return result.sort((a, b) => b.authority - a.authority);
}

export function findPath(
  graph: ProtocolGraph,
  fromId: string,
  toId: string,
): GraphPath | null {
  if (fromId === toId) {
    const node = findNode(graph, fromId);
    return node ? { nodes: [node], edges: [], length: 0 } : null;
  }

  type QueueEntry = { id: string; nodes: GraphNode[]; edges: GraphEdge[] };
  const visited = new Set<string>([fromId]);
  const queue: QueueEntry[] = [];
  const startNode = findNode(graph, fromId);
  if (!startNode) return null;
  queue.push({ id: fromId, nodes: [startNode], edges: [] });

  while (queue.length > 0) {
    const current = queue.shift()!;
    if (current.nodes.length > 6) continue;

    for (const edge of graph.edges) {
      let nextId: string | null = null;
      if (edge.from === current.id) nextId = edge.to;
      else if (edge.to === current.id) nextId = edge.from;

      if (!nextId || visited.has(nextId)) continue;
      visited.add(nextId);

      const nextNode = findNode(graph, nextId);
      if (!nextNode) continue;

      const newNodes = [...current.nodes, nextNode];
      const newEdges = [...current.edges, edge];

      if (nextId === toId) {
        return { nodes: newNodes, edges: newEdges, length: newEdges.length };
      }

      queue.push({ id: nextId, nodes: newNodes, edges: newEdges });
    }
  }

  return null;
}

export function graphStats(graph: ProtocolGraph): Record<string, unknown> {
  const nodesByType: Record<string, number> = {};
  const edgesByRel: Record<string, number> = {};

  for (const n of graph.nodes) nodesByType[n.type] = (nodesByType[n.type] ?? 0) + 1;
  for (const e of graph.edges) edgesByRel[e.relationship] = (edgesByRel[e.relationship] ?? 0) + 1;

  return {
    node_count: graph.nodes.length,
    edge_count: graph.edges.length,
    indexed_at: graph.indexed_at,
    nodes_by_type: nodesByType,
    edges_by_relationship: edgesByRel,
  };
}
