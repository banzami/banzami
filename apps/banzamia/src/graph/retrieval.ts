import type { ProtocolGraph } from './types.js';
import { getNeighbours, findNodeByPath } from './store.js';
import type { SearchResult, SourceType } from '../rag/types.js';
import { authorityWeight } from '../rag/authority.js';

const ENRICHMENT_RELATIONSHIPS = ['IMPLEMENTS', 'SUPERSEDES', 'VALIDATES', 'REQUIRES'] as const;

export interface GraphEnrichment {
  added_nodes: Array<{ id: string; title: string; path: string; relationship: string; reason: string }>;
  enriched: boolean;
}

export function enrichWithGraph(
  graph: ProtocolGraph,
  results: SearchResult[],
  limit = 3,
): { enrichedResults: SearchResult[]; enrichment: GraphEnrichment } {
  const existingPaths = new Set(results.map((r) => r.citation.path));
  const addedNodes: GraphEnrichment['added_nodes'] = [];

  for (const result of results.slice(0, 5)) {
    const graphNodes = findNodeByPath(graph, result.citation.path);
    for (const graphNode of graphNodes) {
      const neighbours = getNeighbours(
        graph,
        graphNode.id,
        ENRICHMENT_RELATIONSHIPS as unknown as import('./types.js').RelationshipType[],
      );

      for (const neighbour of neighbours.slice(0, 2)) {
        if (existingPaths.has(neighbour.node.path)) continue;
        if (addedNodes.length >= limit) break;

        existingPaths.add(neighbour.node.path);
        addedNodes.push({
          id: neighbour.node.id,
          title: neighbour.node.title,
          path: neighbour.node.path,
          relationship: neighbour.relationship,
          reason: `${neighbour.relationship} from ${result.citation.path}`,
        });
      }
    }
    if (addedNodes.length >= limit) break;
  }

  const additionalResults: SearchResult[] = addedNodes
    .filter((node) => node.path.endsWith('.md') || node.path.endsWith('.yaml'))
    .map((node) => {
      const sourceType = (
        node.id.startsWith('rfc:') ? 'accepted_rfc' :
        node.id.startsWith('adr:') ? 'accepted_adr' :
        node.id.startsWith('openapi:') ? 'openapi' :
        node.id.startsWith('vector:') ? 'conformance' :
        'architecture_doc'
      ) as SourceType;

      return {
        text: `[Graph-enriched context from ${node.relationship}] ${node.title} — see ${node.path} for full content`,
        citation: {
          title: node.title,
          path: node.path,
          section: node.title,
          source_type: sourceType,
          start_line: 0,
          end_line: 0,
          authority: authorityWeight(sourceType),
          score: 0.4,
        },
        score: 0.4,
        semantic_score: 0,
        authority_weight: authorityWeight(sourceType),
      };
    });

  return {
    enrichedResults: [...results, ...additionalResults],
    enrichment: { added_nodes: addedNodes, enriched: addedNodes.length > 0 },
  };
}
