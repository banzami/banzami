import type { EmbeddingProvider } from '../src/rag/embedding/provider.js';
import type { Config } from '../src/config.js';
import { search } from '../src/rag/search.js';

export interface GoldenQuestion {
  id: string;
  question: string;
  expected_sources: string[];
  expected_answer_keywords: string[];
  difficulty: 'easy' | 'medium' | 'hard';
  category: string;
}

export interface RetrievalHit {
  question_id: string;
  hit_at_1: boolean;
  hit_at_3: boolean;
  hit_at_5: boolean;
  reciprocal_rank: number;
  retrieved_sources: string[];
  expected_sources: string[];
}

export interface RetrievalMetrics {
  top_1_accuracy: number;
  top_3_accuracy: number;
  top_5_accuracy: number;
  mrr: number;
  recall_at_5: number;
  total_questions: number;
  hits_by_category: Record<string, { total: number; hit_at_3: number }>;
  hits_by_difficulty: Record<string, { total: number; hit_at_3: number }>;
  weak_retrieval_rate: number;
  avg_result_count: number;
}

export interface RetrievalReport {
  generated_at: string;
  metrics: RetrievalMetrics;
  hits: RetrievalHit[];
  failures: Array<{ id: string; question: string; expected: string[]; retrieved: string[] }>;
}

function normalizeSource(path: string): string {
  return path.replace(/^\/+/, '').toLowerCase().trim();
}

function sourceMatches(retrieved: string[], expected: string[]): boolean {
  const normalizedRetrieved = retrieved.map(normalizeSource);
  return expected.some((exp) => {
    const normExp = normalizeSource(exp);
    return normalizedRetrieved.some((r) => r.includes(normExp) || normExp.includes(r));
  });
}

function findFirstMatchRank(retrieved: string[], expected: string[]): number {
  for (let i = 0; i < retrieved.length; i++) {
    if (sourceMatches([retrieved[i]], expected)) return i + 1;
  }
  return 0;
}

export interface RunInput {
  expected: string[];
  retrieved: string[];
}

export function computeRetrievalMetrics(runs: RunInput[], k: number): RetrievalMetrics {
  const hits: RetrievalHit[] = runs.map((run, i) => {
    const rank = findFirstMatchRank(run.retrieved, run.expected);

    const recallNumerator = run.expected.filter((exp) =>
      run.retrieved.some((r) => {
        const nr = normalizeSource(r);
        const ne = normalizeSource(exp);
        return nr.includes(ne) || ne.includes(nr);
      }),
    ).length;

    return {
      question_id: `Q${i + 1}`,
      hit_at_1: rank === 1,
      hit_at_3: rank > 0 && rank <= 3,
      hit_at_5: rank > 0 && rank <= k,
      reciprocal_rank: rank > 0 ? 1 / rank : 0,
      retrieved_sources: run.retrieved,
      expected_sources: run.expected,
      recall: run.expected.length > 0 ? recallNumerator / run.expected.length : 1,
    } as RetrievalHit & { recall: number };
  });

  const n = hits.length;
  const recall_at_5 = n > 0
    ? (hits as Array<RetrievalHit & { recall?: number }>).reduce((s, h) => s + (h.recall ?? (h.hit_at_5 ? 1 : 0)), 0) / n
    : 0;

  const weak = hits.filter((h) => h.retrieved_sources.length === 0).length;

  return {
    top_1_accuracy: n > 0 ? hits.filter((h) => h.hit_at_1).length / n : 0,
    top_3_accuracy: n > 0 ? hits.filter((h) => h.hit_at_3).length / n : 0,
    top_5_accuracy: n > 0 ? hits.filter((h) => h.hit_at_5).length / n : 0,
    mrr: n > 0 ? hits.reduce((s, h) => s + h.reciprocal_rank, 0) / n : 0,
    recall_at_5,
    total_questions: n,
    hits_by_category: {},
    hits_by_difficulty: {},
    weak_retrieval_rate: n > 0 ? weak / n : 0,
    avg_result_count: n > 0 ? hits.reduce((s, h) => s + h.retrieved_sources.length, 0) / n : 0,
  };
}

export async function evaluateRetrieval(
  cfg: Config,
  embedder: EmbeddingProvider,
  questions: GoldenQuestion[],
  k = 5,
): Promise<RetrievalReport> {
  const hits: RetrievalHit[] = [];
  const failures: RetrievalReport['failures'] = [];
  let totalWeakRetrieval = 0;
  let totalResultCount = 0;

  for (const q of questions) {
    const response = await search(cfg, embedder, q.question, k);
    const retrievedSources = response.results.map((r) => r.citation.path);

    if (response.weak_retrieval) totalWeakRetrieval++;
    totalResultCount += response.results.length;

    const rank = findFirstMatchRank(retrievedSources, q.expected_sources);
    const hitAt1 = rank === 1;
    const hitAt3 = rank > 0 && rank <= 3;
    const hitAt5 = rank > 0 && rank <= 5;
    const rr = rank > 0 ? 1 / rank : 0;

    hits.push({
      question_id: q.id,
      hit_at_1: hitAt1,
      hit_at_3: hitAt3,
      hit_at_5: hitAt5,
      reciprocal_rank: rr,
      retrieved_sources: retrievedSources,
      expected_sources: q.expected_sources,
    });

    if (!hitAt5) {
      failures.push({
        id: q.id,
        question: q.question,
        expected: q.expected_sources,
        retrieved: retrievedSources,
      });
    }
  }

  const n = hits.length;
  const hitsByCategory: Record<string, { total: number; hit_at_3: number }> = {};
  const hitsByDifficulty: Record<string, { total: number; hit_at_3: number }> = {};

  for (let i = 0; i < questions.length; i++) {
    const q = questions[i];
    const h = hits[i];

    hitsByCategory[q.category] ??= { total: 0, hit_at_3: 0 };
    hitsByCategory[q.category].total++;
    if (h.hit_at_3) hitsByCategory[q.category].hit_at_3++;

    hitsByDifficulty[q.difficulty] ??= { total: 0, hit_at_3: 0 };
    hitsByDifficulty[q.difficulty].total++;
    if (h.hit_at_3) hitsByDifficulty[q.difficulty].hit_at_3++;
  }

  const recallAt5 = n > 0 ? hits.filter((h) => h.hit_at_5).length / n : 0;

  return {
    generated_at: new Date().toISOString(),
    metrics: {
      top_1_accuracy: n > 0 ? hits.filter((h) => h.hit_at_1).length / n : 0,
      top_3_accuracy: n > 0 ? hits.filter((h) => h.hit_at_3).length / n : 0,
      top_5_accuracy: n > 0 ? hits.filter((h) => h.hit_at_5).length / n : 0,
      mrr: n > 0 ? hits.reduce((s, h) => s + h.reciprocal_rank, 0) / n : 0,
      recall_at_5: recallAt5,
      total_questions: n,
      hits_by_category: hitsByCategory,
      hits_by_difficulty: hitsByDifficulty,
      weak_retrieval_rate: n > 0 ? totalWeakRetrieval / n : 0,
      avg_result_count: n > 0 ? totalResultCount / n : 0,
    },
    hits,
    failures,
  };
}
