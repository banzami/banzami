import type { Config } from '../config.js';
import { collectionInfo, scrollAll } from '../store/qdrant.js';
import type { SourceType } from '../rag/types.js';
import { authorityWeight } from '../rag/authority.js';

export interface SourceCoverage {
  source_type: SourceType;
  chunk_count: number;
  document_count: number;
  authority_weight: number;
  paths: string[];
}

export interface CoverageReport {
  generated_at: string;
  total_chunks: number;
  total_documents: number;
  coverage_by_source: SourceCoverage[];
  uncovered_source_types: SourceType[];
  top_documents: Array<{ path: string; chunk_count: number; source_type: string }>;
  health: 'good' | 'partial' | 'sparse';
}

const ALL_SOURCE_TYPES: SourceType[] = [
  'reference', 'accepted_rfc', 'accepted_adr', 'openapi', 'conformance',
  'certification', 'invariant', 'manifest_schema', 'glossary', 'banzamia_doc',
  'architecture_doc', 'readme', 'sdk_doc', 'website', 'draft_rfc',
];

export async function analyzeCoverage(cfg: Config): Promise<CoverageReport> {
  const [colInfo, chunks] = await Promise.all([
    collectionInfo(cfg),
    scrollAll(cfg),
  ]);

  const bySource = new Map<string, { chunks: number; docs: Set<string>; paths: Set<string> }>();
  const byPath = new Map<string, { count: number; source_type: string }>();

  for (const chunk of chunks) {
    const st = (chunk.source_type as SourceType) ?? 'architecture_doc';
    const path = chunk.path as string ?? '';

    if (!bySource.has(st)) bySource.set(st, { chunks: 0, docs: new Set(), paths: new Set() });
    const entry = bySource.get(st)!;
    entry.chunks++;
    if (chunk.document_id) entry.docs.add(chunk.document_id as string);
    if (path) entry.paths.add(path);

    if (!byPath.has(path)) byPath.set(path, { count: 0, source_type: st });
    byPath.get(path)!.count++;
  }

  const coverageBySource: SourceCoverage[] = ALL_SOURCE_TYPES
    .filter((st) => bySource.has(st))
    .map((st) => {
      const entry = bySource.get(st)!;
      return {
        source_type: st,
        chunk_count: entry.chunks,
        document_count: entry.docs.size,
        authority_weight: authorityWeight(st),
        paths: [...entry.paths].slice(0, 5),
      };
    })
    .sort((a, b) => b.authority_weight - a.authority_weight);

  const uncovered = ALL_SOURCE_TYPES.filter((st) => !bySource.has(st));

  const topDocuments = [...byPath.entries()]
    .sort((a, b) => b[1].count - a[1].count)
    .slice(0, 10)
    .map(([path, { count, source_type }]) => ({ path, chunk_count: count, source_type }));

  const total = colInfo.points_count ?? chunks.length;
  const health: CoverageReport['health'] =
    coverageBySource.length >= 8 && total >= 100 ? 'good' :
    coverageBySource.length >= 4 && total >= 20 ? 'partial' :
    'sparse';

  return {
    generated_at: new Date().toISOString(),
    total_chunks: total,
    total_documents: new Set(chunks.map((c) => c.document_id as string).filter(Boolean)).size,
    coverage_by_source: coverageBySource,
    uncovered_source_types: uncovered,
    top_documents: topDocuments,
    health,
  };
}
