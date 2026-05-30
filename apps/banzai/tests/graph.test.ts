import { describe, it, expect, beforeEach } from 'vitest';
import type { ProtocolGraph, GraphNode, GraphEdge } from '../src/graph/types.js';
import {
  findNode,
  findNodeByPath,
  findNodeByTitle,
  getNeighbours,
  getRelated,
  findPath,
  graphStats,
  setGraph,
} from '../src/graph/store.js';
import { enrichWithGraph } from '../src/graph/retrieval.js';
import type { SearchResult } from '../src/rag/types.js';

function makeNode(id: string, path: string, title: string, authority = 0.9, type: GraphNode['type'] = 'rfc'): GraphNode {
  return { id, type, title, path, status: 'accepted', summary: '', authority };
}

function makeEdge(from: string, to: string, rel: GraphEdge['relationship']): GraphEdge {
  return { from, to, relationship: rel };
}

const RFC_0001: GraphNode = makeNode('rfc:RFC-0001', 'docs/rfc/RFC-0001-identity.md', 'RFC-0001 Identity', 0.95, 'rfc');
const RFC_0002: GraphNode = makeNode('rfc:RFC-0002', 'docs/rfc/RFC-0002-ledger.md', 'RFC-0002 Ledger', 0.95, 'rfc');
const ADR_002: GraphNode = makeNode('adr:ADR-002', 'docs/adr/ADR-002-double-entry.md', 'ADR-002 Double Entry', 0.90, 'adr');
const OPENAPI: GraphNode = makeNode('openapi:transfers', 'contracts/openapi/transfers.yaml', 'Transfers API', 0.90, 'openapi');
const VECTOR: GraphNode = makeNode('vector:transfers', 'conformance/vectors/transfers.yaml', 'Transfer Vectors', 0.85, 'conformance_vector');

const TEST_EDGES: GraphEdge[] = [
  makeEdge('adr:ADR-002', 'rfc:RFC-0002', 'IMPLEMENTS'),
  makeEdge('vector:transfers', 'rfc:RFC-0002', 'VALIDATES'),
  makeEdge('rfc:RFC-0002', 'rfc:RFC-0001', 'REQUIRES'),
  makeEdge('openapi:transfers', 'rfc:RFC-0002', 'REFERENCES'),
];

const TEST_GRAPH: ProtocolGraph = {
  nodes: [RFC_0001, RFC_0002, ADR_002, OPENAPI, VECTOR],
  edges: TEST_EDGES,
  indexed_at: '2026-01-01T00:00:00Z',
  version: '1',
};

describe('graph/store — findNode', () => {
  it('finds by exact id', () => {
    const n = findNode(TEST_GRAPH, 'rfc:RFC-0001');
    expect(n?.id).toBe('rfc:RFC-0001');
  });

  it('finds by path fragment', () => {
    const n = findNode(TEST_GRAPH, 'RFC-0002-ledger');
    expect(n?.id).toBe('rfc:RFC-0002');
  });

  it('returns null for unknown id', () => {
    expect(findNode(TEST_GRAPH, 'rfc:RFC-9999')).toBeNull();
  });
});

describe('graph/store — findNodeByPath', () => {
  it('matches path fragment case-insensitively', () => {
    const nodes = findNodeByPath(TEST_GRAPH, 'docs/rfc');
    expect(nodes).toHaveLength(2);
  });

  it('matches openapi path', () => {
    const nodes = findNodeByPath(TEST_GRAPH, 'transfers.yaml');
    expect(nodes.length).toBeGreaterThanOrEqual(1);
    expect(nodes.some((n) => n.id === 'openapi:transfers')).toBe(true);
  });

  it('returns empty for no match', () => {
    expect(findNodeByPath(TEST_GRAPH, 'nonexistent')).toHaveLength(0);
  });
});

describe('graph/store — findNodeByTitle', () => {
  it('finds by title fragment', () => {
    const nodes = findNodeByTitle(TEST_GRAPH, 'ledger');
    expect(nodes.some((n) => n.id === 'rfc:RFC-0002')).toBe(true);
  });

  it('is case-insensitive', () => {
    const nodes = findNodeByTitle(TEST_GRAPH, 'DOUBLE ENTRY');
    expect(nodes.some((n) => n.id === 'adr:ADR-002')).toBe(true);
  });
});

describe('graph/store — getNeighbours', () => {
  it('returns outbound neighbours', () => {
    const neighbours = getNeighbours(TEST_GRAPH, 'adr:ADR-002');
    expect(neighbours.some((n) => n.node.id === 'rfc:RFC-0002' && n.direction === 'outbound')).toBe(true);
  });

  it('returns inbound neighbours', () => {
    // RFC-0002 is pointed to by ADR-002 (IMPLEMENTS), VECTOR (VALIDATES), OPENAPI (REFERENCES)
    const neighbours = getNeighbours(TEST_GRAPH, 'rfc:RFC-0002');
    const inbound = neighbours.filter((n) => n.direction === 'inbound');
    expect(inbound.length).toBeGreaterThanOrEqual(3);
  });

  it('filters by relationship type', () => {
    const neighbours = getNeighbours(TEST_GRAPH, 'rfc:RFC-0002', ['VALIDATES']);
    expect(neighbours.every((n) => n.relationship === 'VALIDATES')).toBe(true);
    expect(neighbours.some((n) => n.node.id === 'vector:transfers')).toBe(true);
  });

  it('returns empty for isolated node', () => {
    const isolated: GraphNode = makeNode('doc:orphan', 'docs/orphan.md', 'Orphan', 0.5);
    const g: ProtocolGraph = { ...TEST_GRAPH, nodes: [...TEST_GRAPH.nodes, isolated] };
    expect(getNeighbours(g, 'doc:orphan')).toHaveLength(0);
  });
});

describe('graph/store — getRelated (BFS)', () => {
  it('returns transitively related nodes within depth', () => {
    // RFC-0002 → REQUIRES → RFC-0001; ADR-002 → IMPLEMENTS → RFC-0002
    // From ADR-002 at depth 2: RFC-0002 (depth 1) and RFC-0001 (depth 2)
    const related = getRelated(TEST_GRAPH, 'adr:ADR-002', 2);
    expect(related.some((n) => n.id === 'rfc:RFC-0002')).toBe(true);
    expect(related.some((n) => n.id === 'rfc:RFC-0001')).toBe(true);
  });

  it('respects depth limit', () => {
    const related = getRelated(TEST_GRAPH, 'adr:ADR-002', 1);
    // Only RFC-0002 is 1 hop away from ADR-002
    expect(related.some((n) => n.id === 'rfc:RFC-0002')).toBe(true);
    // RFC-0001 is 2 hops; at depth 1 it should not be included
    expect(related.some((n) => n.id === 'rfc:RFC-0001')).toBe(false);
  });

  it('does not include the starting node', () => {
    const related = getRelated(TEST_GRAPH, 'rfc:RFC-0002', 2);
    expect(related.some((n) => n.id === 'rfc:RFC-0002')).toBe(false);
  });

  it('is sorted by authority descending', () => {
    const related = getRelated(TEST_GRAPH, 'adr:ADR-002', 3);
    for (let i = 1; i < related.length; i++) {
      expect(related[i - 1].authority).toBeGreaterThanOrEqual(related[i].authority);
    }
  });
});

describe('graph/store — findPath', () => {
  it('finds a path between connected nodes', () => {
    const path = findPath(TEST_GRAPH, 'adr:ADR-002', 'rfc:RFC-0001');
    expect(path).not.toBeNull();
    expect(path!.nodes[0].id).toBe('adr:ADR-002');
    expect(path!.nodes[path!.nodes.length - 1].id).toBe('rfc:RFC-0001');
    expect(path!.length).toBeGreaterThan(0);
  });

  it('returns trivial path for same node', () => {
    const path = findPath(TEST_GRAPH, 'rfc:RFC-0001', 'rfc:RFC-0001');
    expect(path).not.toBeNull();
    expect(path!.length).toBe(0);
    expect(path!.nodes).toHaveLength(1);
  });

  it('returns null for unreachable nodes', () => {
    const isolated: GraphNode = makeNode('doc:island', 'docs/island.md', 'Island', 0.5);
    const g: ProtocolGraph = { ...TEST_GRAPH, nodes: [...TEST_GRAPH.nodes, isolated] };
    expect(findPath(g, 'rfc:RFC-0001', 'doc:island')).toBeNull();
  });

  it('returns null when from node not found', () => {
    expect(findPath(TEST_GRAPH, 'rfc:RFC-9999', 'rfc:RFC-0001')).toBeNull();
  });
});

describe('graph/store — graphStats', () => {
  it('returns correct node and edge counts', () => {
    const stats = graphStats(TEST_GRAPH);
    expect(stats.node_count).toBe(5);
    expect(stats.edge_count).toBe(4);
  });

  it('counts nodes by type', () => {
    const stats = graphStats(TEST_GRAPH);
    const byType = stats.nodes_by_type as Record<string, number>;
    expect(byType['rfc']).toBe(2);
    expect(byType['adr']).toBe(1);
  });

  it('counts edges by relationship', () => {
    const stats = graphStats(TEST_GRAPH);
    const byRel = stats.edges_by_relationship as Record<string, number>;
    expect(byRel['IMPLEMENTS']).toBe(1);
    expect(byRel['VALIDATES']).toBe(1);
    expect(byRel['REQUIRES']).toBe(1);
    expect(byRel['REFERENCES']).toBe(1);
  });
});

describe('graph/store — setGraph (module singleton)', () => {
  it('allows injecting a test graph', () => {
    setGraph(TEST_GRAPH);
    // getGraph() returns the injected graph without hitting the filesystem
    // We just verify setGraph doesn't throw
    expect(true).toBe(true);
  });
});

describe('graph/retrieval — enrichWithGraph', () => {
  function makeResult(path: string, score = 0.8): SearchResult {
    return {
      text: `Content from ${path}`,
      citation: {
        title: path,
        path,
        section: '',
        source_type: 'accepted_rfc',
        start_line: 0,
        end_line: 10,
        authority: 0.95,
        score,
      },
      score,
      semantic_score: score,
      authority_weight: 0.95,
    };
  }

  it('adds graph-enriched neighbours', () => {
    const results = [makeResult('docs/rfc/RFC-0002-ledger.md')];
    const { enrichedResults, enrichment } = enrichWithGraph(TEST_GRAPH, results, 3);
    // Should have enriched with neighbours of RFC-0002
    expect(enrichedResults.length).toBeGreaterThan(1);
    expect(enrichment.enriched).toBe(true);
    expect(enrichment.added_nodes.length).toBeGreaterThan(0);
  });

  it('does not add duplicates from existing results', () => {
    const results = [
      makeResult('docs/rfc/RFC-0002-ledger.md'),
      makeResult('docs/adr/ADR-002-double-entry.md'),
    ];
    const { enrichedResults } = enrichWithGraph(TEST_GRAPH, results, 5);
    const paths = enrichedResults.map((r) => r.citation.path);
    const unique = new Set(paths);
    expect(paths.length).toBe(unique.size);
  });

  it('respects the limit', () => {
    const results = [makeResult('docs/rfc/RFC-0002-ledger.md')];
    const { enrichment } = enrichWithGraph(TEST_GRAPH, results, 1);
    expect(enrichment.added_nodes.length).toBeLessThanOrEqual(1);
  });

  it('returns original results unchanged when no graph nodes match', () => {
    const results = [makeResult('docs/some-unrelated-file.md')];
    const { enrichedResults, enrichment } = enrichWithGraph(TEST_GRAPH, results, 3);
    expect(enrichedResults).toHaveLength(1);
    expect(enrichment.enriched).toBe(false);
  });

  it('assigns score 0.4 to graph-enriched results', () => {
    const results = [makeResult('docs/rfc/RFC-0002-ledger.md')];
    const { enrichedResults } = enrichWithGraph(TEST_GRAPH, results, 3);
    const enriched = enrichedResults.slice(1);
    for (const r of enriched) {
      expect(r.score).toBe(0.4);
    }
  });
});
