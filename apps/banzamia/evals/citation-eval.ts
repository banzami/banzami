import type { Citation, SourceType } from '../src/rag/types.js';
import { authorityWeight } from '../src/rag/authority.js';

export interface CitationQualityResult {
  question_id: string;
  has_citations: boolean;
  citation_count: number;
  min_authority: number;
  avg_authority: number;
  weak_citations: string[];
  duplicate_paths: string[];
  missing_expected_sources: string[];
  quality_score: number;
}

export interface CitationReport {
  generated_at: string;
  total_evaluated: number;
  citation_rate: number;
  avg_quality_score: number;
  avg_authority: number;
  weak_citation_rate: number;
  duplicate_citation_rate: number;
  results: CitationQualityResult[];
}

const WEAK_AUTHORITY_THRESHOLD = 0.60;

export function evaluateCitations(
  questionId: string,
  citations: Citation[],
  expectedSources: string[],
): CitationQualityResult {
  if (citations.length === 0) {
    return {
      question_id: questionId,
      has_citations: false,
      citation_count: 0,
      min_authority: 0,
      avg_authority: 0,
      weak_citations: [],
      duplicate_paths: [],
      missing_expected_sources: expectedSources,
      quality_score: 0,
    };
  }

  const weakCitations = citations
    .filter((c) => authorityWeight(c.source_type) < WEAK_AUTHORITY_THRESHOLD)
    .map((c) => c.path);

  const pathCounts = new Map<string, number>();
  for (const c of citations) {
    pathCounts.set(c.path, (pathCounts.get(c.path) ?? 0) + 1);
  }
  const duplicatePaths = [...pathCounts.entries()]
    .filter(([, count]) => count > 1)
    .map(([path]) => path);

  const authorities = citations.map((c) => authorityWeight(c.source_type));
  const avgAuthority = authorities.reduce((s, a) => s + a, 0) / authorities.length;
  const minAuthority = Math.min(...authorities);

  const missingExpected = expectedSources.filter((exp) => {
    const normExp = exp.toLowerCase();
    return !citations.some((c) => c.path.toLowerCase().includes(normExp) || normExp.includes(c.path.toLowerCase()));
  });

  const coverageScore = expectedSources.length > 0
    ? 1 - (missingExpected.length / expectedSources.length)
    : 1;
  const authorityScore = avgAuthority;
  const deduplicationScore = duplicatePaths.length === 0 ? 1 : 0.7;
  const qualityScore = (coverageScore * 0.5) + (authorityScore * 0.3) + (deduplicationScore * 0.2);

  return {
    question_id: questionId,
    has_citations: true,
    citation_count: citations.length,
    min_authority: minAuthority,
    avg_authority: avgAuthority,
    weak_citations: weakCitations,
    duplicate_paths: duplicatePaths,
    missing_expected_sources: missingExpected,
    quality_score: Math.min(1, qualityScore),
  };
}

export function buildCitationReport(results: CitationQualityResult[]): CitationReport {
  const n = results.length;
  const withCitations = results.filter((r) => r.has_citations);
  const citationRate = n > 0 ? withCitations.length / n : 0;
  const avgQuality = withCitations.length > 0
    ? withCitations.reduce((s, r) => s + r.quality_score, 0) / withCitations.length
    : 0;
  const avgAuthority = withCitations.length > 0
    ? withCitations.reduce((s, r) => s + r.avg_authority, 0) / withCitations.length
    : 0;
  const weakRate = withCitations.length > 0
    ? withCitations.filter((r) => r.weak_citations.length > 0).length / withCitations.length
    : 0;
  const dupRate = withCitations.length > 0
    ? withCitations.filter((r) => r.duplicate_paths.length > 0).length / withCitations.length
    : 0;

  return {
    generated_at: new Date().toISOString(),
    total_evaluated: n,
    citation_rate: citationRate,
    avg_quality_score: avgQuality,
    avg_authority: avgAuthority,
    weak_citation_rate: weakRate,
    duplicate_citation_rate: dupRate,
    results,
  };
}

export function validateAuthorityRanking(
  highPriorityResult: Citation,
  lowPriorityResult: Citation,
): boolean {
  return highPriorityResult.authority >= lowPriorityResult.authority;
}
