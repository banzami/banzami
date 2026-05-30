import type { EmbeddingProvider } from '../rag/embedding/provider.js';
import type { ModelProvider } from '../orchestrator/providers/provider.js';
import type { Config } from '../config.js';
import { search } from '../rag/search.js';
import { getGraph } from '../graph/store.js';
import { findNodeByPath, getNeighbours, getRelated } from '../graph/store.js';
import type { SearchResult } from '../rag/types.js';
import type { GraphNode } from '../graph/types.js';

export interface ResearchStep {
  step: number;
  type: 'plan' | 'retrieval' | 'graph' | 'tool' | 'synthesis';
  description: string;
  sources_found?: number;
  nodes_found?: number;
  duration_ms?: number;
}

export interface Evidence {
  source_path: string;
  source_type: string;
  title: string;
  excerpt: string;
  authority: number;
  score: number;
  relationship_chain?: string[];
}

export interface ContradictionFlag {
  sources: string[];
  topic: string;
  description: string;
}

export interface ResearchReport {
  question: string;
  answer: string;
  steps: ResearchStep[];
  evidence: Evidence[];
  graph_nodes: Array<{ id: string; title: string; type: string; relationship?: string }>;
  relationship_chains: string[];
  contradictions: ContradictionFlag[];
  authority_summary: { highest: number; avg: number; sources_used: number };
  research_quality: 'high' | 'medium' | 'low';
  model: string;
  duration_ms: number;
}

const RESEARCH_SYSTEM_PROMPT = `You are BanzamIA performing deep protocol research for the Banzami payment network.
You have been given evidence collected from multiple sources: protocol documents, RFC/ADR specifications, graph relationships, and conformance rules.

Your task: synthesise the evidence into a comprehensive, grounded answer.

Rules:
- Ground every claim in the provided evidence.
- Cite sources by their path and type.
- Identify the dependency chain (e.g. "RFC-0004 → ADR-0002 → INV-STL-001 → CON-STL-004").
- If sources contradict, say so clearly.
- Never invent protocol facts not present in the evidence.
- Format your answer with clear sections, bullet points where appropriate.
- End with a "Source Chain" section listing the key dependency relationships.

Principle: Tools determine truth. AI explains truth.`;

function buildEvidenceBlock(evidence: Evidence[], graphNodes: GraphNode[]): string {
  const sourceBlocks = evidence.slice(0, 12).map((e, i) => (
    `[Source ${i + 1}] ${e.title} (${e.source_type}, authority=${e.authority.toFixed(2)})\nPath: ${e.source_path}\n${e.excerpt}`
  )).join('\n\n---\n\n');

  const graphBlock = graphNodes.length > 0
    ? `\n\nGraph context (${graphNodes.length} related protocol nodes):\n` +
      graphNodes.slice(0, 8).map(n => `- [${n.type.toUpperCase()}] ${n.id}: ${n.title}`).join('\n')
    : '';

  return sourceBlocks + graphBlock;
}

export async function runResearch(
  cfg: Config,
  embedder: EmbeddingProvider,
  model: ModelProvider,
  question: string,
): Promise<ResearchReport> {
  const t0 = Date.now();
  const steps: ResearchStep[] = [];
  let stepNum = 1;

  // Step 1: Plan
  steps.push({ step: stepNum++, type: 'plan', description: `Analysing question and planning research strategy for: "${question.slice(0, 80)}"` });

  // Step 2: Primary retrieval
  const tSearch1 = Date.now();
  const primaryResponse = await search(cfg, embedder, question, 10);
  steps.push({
    step: stepNum++,
    type: 'retrieval',
    description: `Primary vector search — ${primaryResponse.mode} mode`,
    sources_found: primaryResponse.results.length,
    duration_ms: Date.now() - tSearch1,
  });

  // Step 3: Graph traversal
  const tGraph = Date.now();
  const graph = await getGraph(cfg);
  const graphNodes: GraphNode[] = [];
  const relationshipChains: string[] = [];

  if (graph) {
    const seenIds = new Set<string>();
    for (const result of primaryResponse.results.slice(0, 5)) {
      const nodes = findNodeByPath(graph, result.citation.path);
      for (const node of nodes) {
        if (seenIds.has(node.id)) continue;
        seenIds.add(node.id);
        graphNodes.push(node);

        const neighbours = getNeighbours(graph, node.id);
        const chain = neighbours
          .filter(n => !seenIds.has(n.node.id))
          .slice(0, 3)
          .map(n => {
            seenIds.add(n.node.id);
            graphNodes.push(n.node);
            return `${node.id} —[${n.relationship}]→ ${n.node.id}`;
          });
        relationshipChains.push(...chain);
      }
    }

    // BFS related nodes for top result
    if (primaryResponse.results[0]) {
      const topNodes = findNodeByPath(graph, primaryResponse.results[0].citation.path);
      if (topNodes[0]) {
        const related = getRelated(graph, topNodes[0].id, 2);
        for (const n of related.slice(0, 5)) {
          if (!seenIds.has(n.id)) {
            seenIds.add(n.id);
            graphNodes.push(n);
          }
        }
      }
    }

    steps.push({
      step: stepNum++,
      type: 'graph',
      description: `Graph traversal — ${graphNodes.length} related protocol nodes found, ${relationshipChains.length} relationship chains`,
      nodes_found: graphNodes.length,
      duration_ms: Date.now() - tGraph,
    });
  } else {
    steps.push({ step: stepNum++, type: 'graph', description: 'Graph not indexed — skipping graph traversal', nodes_found: 0 });
  }

  // Step 4: Secondary retrieval on graph-discovered topics
  const additionalResults: SearchResult[] = [];
  if (graphNodes.length > 0) {
    const secondaryQueries = graphNodes
      .slice(0, 3)
      .map(n => n.title)
      .filter(Boolean);

    for (const q of secondaryQueries) {
      const tSearch2 = Date.now();
      const r = await search(cfg, embedder, q, 4);
      additionalResults.push(...r.results);
      steps.push({
        step: stepNum++,
        type: 'retrieval',
        description: `Secondary retrieval for "${q.slice(0, 50)}"`,
        sources_found: r.results.length,
        duration_ms: Date.now() - tSearch2,
      });
    }
  }

  // Merge + deduplicate all results
  const allResults: SearchResult[] = [...primaryResponse.results];
  const seenPaths = new Set(primaryResponse.results.map(r => `${r.citation.path}:${r.citation.start_line}`));
  for (const r of additionalResults) {
    const key = `${r.citation.path}:${r.citation.start_line}`;
    if (!seenPaths.has(key)) {
      seenPaths.add(key);
      allResults.push(r);
    }
  }

  // Build evidence list
  const evidence: Evidence[] = allResults
    .sort((a, b) => b.score - a.score)
    .slice(0, 12)
    .map(r => ({
      source_path: r.citation.path,
      source_type: r.citation.source_type,
      title: r.citation.title,
      excerpt: r.text.slice(0, 300),
      authority: r.citation.authority,
      score: r.score,
    }));

  // Contradiction detection
  const contradictions: ContradictionFlag[] = detectContradictions(evidence);
  if (contradictions.length > 0) {
    steps.push({ step: stepNum++, type: 'tool', description: `Contradiction analysis — ${contradictions.length} potential conflict(s) flagged` });
  }

  // Step N: Synthesis
  steps.push({ step: stepNum++, type: 'synthesis', description: 'Synthesising evidence into grounded protocol report' });

  const evidenceBlock = buildEvidenceBlock(evidence, graphNodes);
  const messages = [
    { role: 'system' as const, content: RESEARCH_SYSTEM_PROMPT },
    {
      role: 'user' as const,
      content: `## Research Question\n\n${question}\n\n## Collected Evidence\n\n${evidenceBlock}`,
    },
  ];

  const modelResponse = await model.generate(messages, 'reasoning');

  const authorities = evidence.map(e => e.authority);
  const authorityHighest = authorities.length > 0 ? Math.max(...authorities) : 0;
  const authorityAvg = authorities.length > 0 ? authorities.reduce((s, a) => s + a, 0) / authorities.length : 0;

  const quality: ResearchReport['research_quality'] =
    evidence.length >= 6 && authorityAvg >= 0.80 ? 'high' :
    evidence.length >= 3 && authorityAvg >= 0.65 ? 'medium' : 'low';

  return {
    question,
    answer: modelResponse.content,
    steps,
    evidence,
    graph_nodes: graphNodes.slice(0, 15).map(n => ({ id: n.id, title: n.title, type: n.type })),
    relationship_chains: relationshipChains.slice(0, 10),
    contradictions,
    authority_summary: { highest: authorityHighest, avg: authorityAvg, sources_used: evidence.length },
    research_quality: quality,
    model: modelResponse.model,
    duration_ms: Date.now() - t0,
  };
}

function detectContradictions(evidence: Evidence[]): ContradictionFlag[] {
  const contradictions: ContradictionFlag[] = [];
  const STATUS_RE = /\bstatus\s*[=:]\s*(\w+)/gi;

  const byTopic = new Map<string, Array<{ source: string; value: string }>>();
  for (const e of evidence) {
    for (const m of e.excerpt.matchAll(STATUS_RE)) {
      const key = 'status';
      if (!byTopic.has(key)) byTopic.set(key, []);
      byTopic.get(key)!.push({ source: e.source_path, value: m[1].toLowerCase() });
    }
  }

  for (const [topic, entries] of byTopic) {
    const values = new Set(entries.map(e => e.value));
    if (values.size > 1) {
      contradictions.push({
        topic,
        sources: entries.map(e => e.source),
        description: `Different values found: ${[...values].join(', ')}`,
      });
    }
  }

  return contradictions;
}
