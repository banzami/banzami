import type { SourceType } from './types.js';

const AUTHORITY_BASE: Record<SourceType, number> = {
  reference: 1.00,
  accepted_rfc: 0.95,
  accepted_adr: 0.90,
  openapi: 0.90,
  conformance: 0.85,
  certification: 0.85,
  invariant: 0.85,
  manifest_schema: 0.85,
  glossary: 0.80,
  banzamia_doc: 0.80,
  architecture_doc: 0.75,
  readme: 0.70,
  sdk_doc: 0.70,
  website: 0.60,
  draft_rfc: 0.50,
};

const FRESHNESS_HALF_LIFE_DAYS = 180;
const FRESHNESS_FLOOR = 0.80;

function freshnessWeight(updatedAt: string): number {
  try {
    const ts = new Date(updatedAt).getTime();
    if (!Number.isFinite(ts)) return FRESHNESS_FLOOR;
    const ms = Date.now() - ts;
    const days = ms / 86_400_000;
    const decay = Math.exp((-Math.LN2 * days) / FRESHNESS_HALF_LIFE_DAYS);
    return FRESHNESS_FLOOR + (1 - FRESHNESS_FLOOR) * decay;
  } catch {
    return FRESHNESS_FLOOR;
  }
}

export function authorityWeight(sourceType: SourceType): number {
  return AUTHORITY_BASE[sourceType] ?? 0.50;
}

export function finalScore(
  semanticScore: number,
  sourceType: SourceType,
  updatedAt: string,
): number {
  return semanticScore * authorityWeight(sourceType) * freshnessWeight(updatedAt);
}
