import type { EmbeddingProvider } from './embedding/provider.js';
import { finalScore, authorityWeight } from './authority.js';
import {
  vectorSearch,
  keywordSearch,
  type ScoredChunk,
  type ScrollFilter,
} from '../store/qdrant.js';
import type { Config } from '../config.js';
import type { SearchResult, SearchResponse, SearchFilters, Citation, SourceType } from './types.js';

const WEAK_THRESHOLD = 0.45;
const SEMANTIC_LIMIT_MULTIPLIER = 3;

function toFilter(f: SearchFilters): ScrollFilter {
  return {
    source_type: f.source_type,
    status: f.status,
    language: f.language,
    repo: f.repo,
  };
}

function toCitation(chunk: ScoredChunk, score: number): Citation {
  const p = chunk.payload;
  return {
    title: p.title,
    path: p.path,
    section: p.section,
    source_type: p.source_type,
    start_line: p.start_line,
    end_line: p.end_line,
    authority: p.authority,
    score,
  };
}

function deduplicateByPath(results: SearchResult[], limit: number): SearchResult[] {
  const seen = new Set<string>();
  const out: SearchResult[] = [];
  for (const r of results) {
    const key = `${r.citation.path}:${r.citation.start_line}`;
    if (!seen.has(key)) {
      seen.add(key);
      out.push(r);
      if (out.length >= limit) break;
    }
  }
  return out;
}

export async function search(
  cfg: Config,
  embedder: EmbeddingProvider,
  query: string,
  limit: number = 8,
  filters: SearchFilters = {},
): Promise<SearchResponse> {
  const scrollFilter = toFilter(filters);
  const semanticLimit = limit * SEMANTIC_LIMIT_MULTIPLIER;

  let vector: number[];
  try {
    vector = await embedder.embed(query);
  } catch {
    return { results: [], mode: 'mock', weak_retrieval: true };
  }

  const vectorResults = await vectorSearch(cfg, vector, semanticLimit, scrollFilter);
  const maxSemanticScore = vectorResults[0]?.score ?? 0;
  const isWeak = maxSemanticScore < WEAK_THRESHOLD;

  let keywordResults: ScoredChunk[] = [];
  if (isWeak) {
    keywordResults = await keywordSearch(cfg, query, limit, scrollFilter);
  }

  const allRaw = new Map<string, ScoredChunk & { semanticScore: number }>();

  for (const r of vectorResults) {
    allRaw.set(r.payload.chunk_id, { ...r, semanticScore: r.score });
  }

  for (const r of keywordResults) {
    if (!allRaw.has(r.payload.chunk_id)) {
      allRaw.set(r.payload.chunk_id, { ...r, semanticScore: 0 });
    }
  }

  const scored: SearchResult[] = [...allRaw.values()].map((r) => {
    const authWeight = authorityWeight(r.payload.source_type as SourceType);
    const fs = finalScore(r.semanticScore, r.payload.source_type as SourceType, r.payload.updated_at);
    return {
      text: r.payload.text,
      citation: toCitation(r, fs),
      score: fs,
      semantic_score: r.semanticScore,
      authority_weight: authWeight,
    };
  });

  scored.sort((a, b) => b.score - a.score);

  const mode = isWeak && keywordResults.length > 0 ? 'hybrid' : 'vector';
  return {
    results: deduplicateByPath(scored, limit),
    mode,
    weak_retrieval: isWeak,
  };
}
