import { readdir, readFile, stat } from 'node:fs/promises';
import { join, relative, basename, extname } from 'node:path';
import type { GraphNode, GraphEdge, ProtocolGraph, NodeType, RelationshipType } from './types.js';
import { authorityWeight } from '../rag/authority.js';

const RFC_ID_RE = /RFC-\d{4}/g;
const ADR_ID_RE = /ADR-\d{3}/gi;
const INV_RE = /\b(balance.never.negative|no.money.creation|double.entry|immutabilit|ledger.append)/gi;
const MD_LINK_RE = /\[([^\]]+)\]\(([^)]+)\)/g;

const SUPERSEDES_RE = /supersedes?\s+(?:RFC|ADR)-\d+/gi;
const IMPLEMENTS_RE = /implements?\s+RFC-\d{4}/gi;
const REQUIRES_RE = /requires?\s+(?:RFC|ADR)-\d+/gi;

function nodeIdFromPath(path: string): string {
  const name = basename(path, extname(path)).toLowerCase();
  const rfcMatch = name.match(/rfc-(\d{4})/);
  if (rfcMatch) return `rfc:RFC-${rfcMatch[1]}`;
  const adrMatch = name.match(/adr-(\d{3})/);
  if (adrMatch) return `adr:ADR-${adrMatch[1].padStart(3, '0')}`;
  if (path.startsWith('contracts/openapi/')) return `openapi:${name}`;
  if (path.startsWith('conformance/vectors/')) return `vector:${name}`;
  if (path === 'docs/BANZA_REFERENCE.md') return 'reference:main';
  if (path === 'docs/conformance.md') return 'certification:conformance';
  if (path === 'docs/certification.md') return 'certification:rules';
  if (path === 'docs/glossary.md') return 'glossary:main';
  return `doc:${name}`;
}

function detectNodeType(path: string): NodeType {
  if (path.startsWith('docs/rfc/')) return 'rfc';
  if (path.startsWith('docs/adr/')) return 'adr';
  if (path.startsWith('contracts/openapi/')) return 'openapi';
  if (path.startsWith('conformance/vectors/')) return 'conformance_vector';
  if (path === 'docs/conformance.md' || path === 'docs/certification.md') return 'certification_rule';
  if (path.startsWith('manifests/schemas/')) return 'manifest_schema';
  if (path.startsWith('sdk/')) return 'sdk_doc';
  if (path.startsWith('docs/architecture/')) return 'architecture_doc';
  if (path.includes('glossary')) return 'glossary_term';
  return 'architecture_doc';
}

function extractTitle(content: string, filePath: string): string {
  const h1 = content.match(/^#\s+(.+)/m);
  return h1 ? h1[1].trim() : basename(filePath, extname(filePath));
}

function extractSummary(content: string): string {
  const paras = content.split('\n\n').filter((p) => p.trim() && !p.startsWith('#'));
  return (paras[0] ?? '').replace(/[*_`]/g, '').slice(0, 200).trim();
}

function extractStatus(content: string): string {
  const m = content.match(/status[:\s]+([a-z-]+)/i);
  return m ? m[1].toLowerCase() : 'active';
}

function refToNodeId(ref: string): string {
  const rfcMatch = ref.match(/RFC-(\d{4})/i);
  if (rfcMatch) return `rfc:RFC-${rfcMatch[1]}`;
  const adrMatch = ref.match(/ADR-(\d{3})/i);
  if (adrMatch) return `adr:ADR-${adrMatch[1].padStart(3, '0')}`;
  return '';
}

function extractEdges(fromId: string, content: string, knownNodeIds: Set<string>): GraphEdge[] {
  const edges: GraphEdge[] = [];
  const addEdge = (to: string, rel: RelationshipType, reason?: string) => {
    if (to && to !== fromId && knownNodeIds.has(to)) {
      const exists = edges.some((e) => e.from === fromId && e.to === to && e.relationship === rel);
      if (!exists) edges.push({ from: fromId, to, relationship: rel, reason });
    }
  };

  const supersedes = content.matchAll(/supersedes?\s+(RFC-\d{4}|ADR-\d{3})/gi);
  for (const m of supersedes) {
    addEdge(refToNodeId(m[1]), 'SUPERSEDES', `Explicitly supersedes ${m[1]}`);
  }

  const implements_ = content.matchAll(/implements?\s+(RFC-\d{4})/gi);
  for (const m of implements_) {
    addEdge(refToNodeId(m[1]), 'IMPLEMENTS', `Implements ${m[1]}`);
  }

  const requires = content.matchAll(/requires?\s+(RFC-\d{4}|ADR-\d{3})/gi);
  for (const m of requires) {
    addEdge(refToNodeId(m[1]), 'REQUIRES', `Requires ${m[1]}`);
  }

  for (const m of content.matchAll(MD_LINK_RE)) {
    const href = m[2];
    if (href.startsWith('http')) continue;
    const rfcInHref = href.match(/RFC-(\d{4})/i);
    if (rfcInHref) addEdge(`rfc:RFC-${rfcInHref[1]}`, 'REFERENCES');
    const adrInHref = href.match(/ADR-(\d{3})/i);
    if (adrInHref) addEdge(`adr:ADR-${adrInHref[1].padStart(3, '0')}`, 'REFERENCES');
  }

  for (const m of content.matchAll(RFC_ID_RE)) {
    addEdge(refToNodeId(m[0]), 'REFERENCES');
  }
  for (const m of content.matchAll(ADR_ID_RE)) {
    addEdge(refToNodeId(m[0]), 'REFERENCES');
  }

  return edges;
}

const CONFORMANCE_VALIDATES: Array<[string, string]> = [
  ['vector:transfers', 'rfc:RFC-0002'],
  ['vector:ledger-postings', 'adr:ADR-002'],
  ['vector:settlement-batches', 'rfc:RFC-0002'],
  ['vector:qr-payloads', 'adr:ADR-006'],
  ['vector:operator-manifests', 'rfc:RFC-0005'],
  ['vector:payment-requests', 'adr:ADR-009'],
  ['vector:wallet-balances', 'adr:ADR-002'],
  ['certification:conformance', 'certification:rules'],
];

const CERTIFICATION_REQUIRES: Array<[string, string]> = [
  ['adr:ADR-002', 'rfc:RFC-0002'],
  ['adr:ADR-006', 'rfc:RFC-0001'],
];

const GRAPH_FILE = '.banzai-graph.json';

async function walkMarkdownFiles(dir: string, root: string): Promise<string[]> {
  const entries = await readdir(dir, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    if (entry.name.startsWith('.') || entry.name === 'node_modules' || entry.name === 'target') continue;
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...await walkMarkdownFiles(full, root));
    } else if (entry.isFile() && (entry.name.endsWith('.md') || entry.name.endsWith('.yaml') || entry.name.endsWith('.json'))) {
      files.push(full);
    }
  }
  return files;
}

const GRAPH_RELEVANT_PREFIXES = [
  'docs/rfc/', 'docs/adr/', 'contracts/openapi/', 'conformance/vectors/',
  'docs/conformance', 'docs/certification', 'docs/glossary',
];

function isGraphRelevant(relPath: string): boolean {
  return GRAPH_RELEVANT_PREFIXES.some((p) => relPath.startsWith(p));
}

export async function buildProtocolGraph(repoRoot: string): Promise<ProtocolGraph> {
  const files = await walkMarkdownFiles(repoRoot, repoRoot);
  const relevant = files
    .map((f) => ({ full: f, rel: relative(repoRoot, f) }))
    .filter(({ rel }) => isGraphRelevant(rel));

  const nodes: GraphNode[] = [];
  const nodeContents = new Map<string, string>();

  for (const { full, rel } of relevant) {
    try {
      const content = await readFile(full, 'utf-8');
      const id = nodeIdFromPath(rel);
      const type = detectNodeType(rel);
      const title = extractTitle(content, rel);
      const summary = extractSummary(content);
      const status = extractStatus(content);
      const sourceType = type === 'rfc' && status === 'accepted' ? 'accepted_rfc' as const
        : type === 'rfc' ? 'draft_rfc' as const
        : type === 'adr' ? 'accepted_adr' as const
        : type === 'openapi' ? 'openapi' as const
        : type === 'conformance_vector' ? 'conformance' as const
        : type === 'certification_rule' ? 'certification' as const
        : 'architecture_doc' as const;

      nodes.push({ id, type, title, path: rel, status, summary, authority: authorityWeight(sourceType) });
      nodeContents.set(id, content);
    } catch {
      continue;
    }
  }

  const knownIds = new Set(nodes.map((n) => n.id));
  const edges: GraphEdge[] = [];

  for (const [id, content] of nodeContents) {
    const extracted = extractEdges(id, content, knownIds);
    edges.push(...extracted);
  }

  for (const [from, to] of CONFORMANCE_VALIDATES) {
    if (knownIds.has(from) && knownIds.has(to)) {
      edges.push({ from, to, relationship: 'VALIDATES', reason: 'Static conformance mapping' });
    }
  }

  const deduped = [...new Map(edges.map((e) => [`${e.from}|${e.to}|${e.relationship}`, e])).values()];

  return {
    nodes,
    edges: deduped,
    indexed_at: new Date().toISOString(),
    version: '1',
  };
}

export async function saveGraph(graph: ProtocolGraph, repoRoot: string): Promise<void> {
  const { writeFile } = await import('node:fs/promises');
  const path = join(repoRoot, GRAPH_FILE);
  await writeFile(path, JSON.stringify(graph, null, 2), 'utf-8');
}

export async function loadGraph(repoRoot: string): Promise<ProtocolGraph | null> {
  try {
    const { readFile } = await import('node:fs/promises');
    const path = join(repoRoot, GRAPH_FILE);
    const raw = await readFile(path, 'utf-8');
    return JSON.parse(raw) as ProtocolGraph;
  } catch {
    return null;
  }
}
