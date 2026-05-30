import type { TaskType } from '../orchestrator/providers/provider.js';
import type { SourceType } from '../rag/types.js';

export interface QueryEvent {
  timestamp: string;
  question_hash: string;
  task_type: TaskType;
  retrieval_mode: string;
  weak_retrieval: boolean;
  source_types: SourceType[];
  latency_ms: number;
  citation_count: number;
  top_authority: number;
}

interface AnalyticsState {
  total_queries: number;
  weak_retrieval_count: number;
  total_latency_ms: number;
  source_frequency: Map<string, number>;
  task_type_counts: Map<string, number>;
  retrieval_mode_counts: Map<string, number>;
  citation_total: number;
  authority_total: number;
  recent_events: QueryEvent[];
}

const MAX_RECENT = 100;

const state: AnalyticsState = {
  total_queries: 0,
  weak_retrieval_count: 0,
  total_latency_ms: 0,
  source_frequency: new Map(),
  task_type_counts: new Map(),
  retrieval_mode_counts: new Map(),
  citation_total: 0,
  authority_total: 0,
  recent_events: [],
};

export function trackQuery(event: QueryEvent): void {
  state.total_queries++;
  state.total_latency_ms += event.latency_ms;
  state.citation_total += event.citation_count;
  state.authority_total += event.top_authority;

  if (event.weak_retrieval) state.weak_retrieval_count++;

  const tt = state.task_type_counts.get(event.task_type) ?? 0;
  state.task_type_counts.set(event.task_type, tt + 1);

  const rm = state.retrieval_mode_counts.get(event.retrieval_mode) ?? 0;
  state.retrieval_mode_counts.set(event.retrieval_mode, rm + 1);

  for (const st of event.source_types) {
    const freq = state.source_frequency.get(st) ?? 0;
    state.source_frequency.set(st, freq + 1);
  }

  state.recent_events.push(event);
  if (state.recent_events.length > MAX_RECENT) {
    state.recent_events.shift();
  }
}

export interface AnalyticsReport {
  total_queries: number;
  avg_latency_ms: number;
  weak_retrieval_rate: number;
  avg_citations: number;
  avg_top_authority: number;
  task_type_distribution: Record<string, number>;
  retrieval_mode_distribution: Record<string, number>;
  top_sources: Array<{ source_type: string; count: number }>;
  recent_events: QueryEvent[];
}

export function getAnalyticsReport(): AnalyticsReport {
  const n = state.total_queries;
  const topSources = [...state.source_frequency.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([source_type, count]) => ({ source_type, count }));

  return {
    total_queries: n,
    avg_latency_ms: n > 0 ? Math.round(state.total_latency_ms / n) : 0,
    weak_retrieval_rate: n > 0 ? state.weak_retrieval_count / n : 0,
    avg_citations: n > 0 ? state.citation_total / n : 0,
    avg_top_authority: n > 0 ? state.authority_total / n : 0,
    task_type_distribution: Object.fromEntries(state.task_type_counts),
    retrieval_mode_distribution: Object.fromEntries(state.retrieval_mode_counts),
    top_sources: topSources,
    recent_events: [...state.recent_events].reverse().slice(0, 20),
  };
}

export function resetAnalytics(): void {
  state.total_queries = 0;
  state.weak_retrieval_count = 0;
  state.total_latency_ms = 0;
  state.source_frequency.clear();
  state.task_type_counts.clear();
  state.retrieval_mode_counts.clear();
  state.citation_total = 0;
  state.authority_total = 0;
  state.recent_events = [];
}
