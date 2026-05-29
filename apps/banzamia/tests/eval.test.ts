import { describe, it, expect } from 'vitest';
import { computeRetrievalMetrics } from '../evals/retrieval-eval.js';
import { evaluateCitations, buildCitationReport } from '../evals/citation-eval.js';
import { detectForbiddenClaims, detectRequiredConcepts, validateProtocolTruth } from '../evals/adversarial-eval.js';
import type { Citation } from '../src/rag/types.js';

// ── Retrieval metrics ────────────────────────────────────────────────────────

describe('retrieval eval — computeRetrievalMetrics', () => {
  it('scores perfect retrieval', () => {
    const runs = [
      { expected: ['docs/rfc/RFC-0001.md'], retrieved: ['docs/rfc/RFC-0001.md', 'docs/adr/ADR-002.md'] },
    ];
    const m = computeRetrievalMetrics(runs, 5);
    expect(m.top_1_accuracy).toBe(1);
    expect(m.top_3_accuracy).toBe(1);
    expect(m.mrr).toBe(1);
    expect(m.recall_at_5).toBe(1);
  });

  it('scores zero when nothing retrieved', () => {
    const runs = [
      { expected: ['docs/rfc/RFC-0001.md'], retrieved: [] },
    ];
    const m = computeRetrievalMetrics(runs, 5);
    expect(m.top_1_accuracy).toBe(0);
    expect(m.mrr).toBe(0);
    expect(m.recall_at_5).toBe(0);
    expect(m.weak_retrieval_rate).toBe(1);
  });

  it('computes MRR correctly for rank-2 hit', () => {
    const runs = [
      { expected: ['docs/rfc/RFC-0002.md'], retrieved: ['docs/unrelated.md', 'docs/rfc/RFC-0002.md'] },
    ];
    const m = computeRetrievalMetrics(runs, 5);
    expect(m.top_1_accuracy).toBe(0);
    expect(m.top_3_accuracy).toBe(1);
    expect(m.mrr).toBeCloseTo(0.5, 5);
  });

  it('computes recall with partial expected sources found', () => {
    const runs = [
      {
        expected: ['docs/rfc/RFC-0001.md', 'docs/adr/ADR-002.md'],
        retrieved: ['docs/rfc/RFC-0001.md', 'docs/unrelated.md'],
      },
    ];
    const m = computeRetrievalMetrics(runs, 5);
    expect(m.recall_at_5).toBeCloseTo(0.5, 5);
  });

  it('uses normalized path matching (partial path match)', () => {
    const runs = [
      {
        expected: ['RFC-0001'],
        retrieved: ['docs/rfc/RFC-0001.md'],
      },
    ];
    const m = computeRetrievalMetrics(runs, 5);
    expect(m.top_1_accuracy).toBe(1);
  });

  it('averages metrics across multiple questions', () => {
    const runs = [
      { expected: ['docs/a.md'], retrieved: ['docs/a.md'] },
      { expected: ['docs/b.md'], retrieved: ['docs/c.md'] },
    ];
    const m = computeRetrievalMetrics(runs, 5);
    expect(m.top_1_accuracy).toBeCloseTo(0.5, 5);
    expect(m.mrr).toBeCloseTo(0.5, 5);
  });

  it('flags weak retrieval when top score would be low (no retrieved results)', () => {
    const runs = [
      { expected: ['docs/a.md'], retrieved: [] },
      { expected: ['docs/b.md'], retrieved: ['docs/b.md'] },
    ];
    const m = computeRetrievalMetrics(runs, 5);
    expect(m.weak_retrieval_rate).toBeGreaterThan(0);
  });
});

// ── Citation quality ─────────────────────────────────────────────────────────

function makeCitation(path: string, authority: number, source_type = 'accepted_rfc'): Citation {
  return {
    title: path,
    path,
    section: 'Section 1',
    source_type: source_type as Citation['source_type'],
    start_line: 0,
    end_line: 10,
    authority,
    score: 0.8,
  };
}

describe('citation eval — evaluateCitations', () => {
  it('scores perfect citation coverage', () => {
    const citations = [makeCitation('docs/rfc/RFC-0001.md', 0.95)];
    const result = evaluateCitations('Q1', citations, ['docs/rfc/RFC-0001.md']);
    expect(result.missing_expected_sources).toHaveLength(0);
    expect(result.quality_score).toBeGreaterThan(0.8);
  });

  it('penalises missing expected sources', () => {
    const citations = [makeCitation('docs/unrelated.md', 0.70)];
    const result = evaluateCitations('Q2', citations, ['docs/rfc/RFC-0001.md']);
    expect(result.missing_expected_sources).toHaveLength(1);
    expect(result.quality_score).toBeLessThan(0.7);
  });

  it('penalises duplicate citations', () => {
    const citations = [
      makeCitation('docs/rfc/RFC-0001.md', 0.95),
      makeCitation('docs/rfc/RFC-0001.md', 0.95),
    ];
    const result = evaluateCitations('Q3', citations, ['docs/rfc/RFC-0001.md']);
    expect(result.duplicate_paths).toHaveLength(1);
    // quality_score should be less than a non-duplicate set
    const clean = evaluateCitations('Q3b', [makeCitation('docs/rfc/RFC-0001.md', 0.95)], ['docs/rfc/RFC-0001.md']);
    expect(result.quality_score).toBeLessThanOrEqual(clean.quality_score);
  });

  it('flags weak authority citations', () => {
    // draft_rfc has authority 0.50 which is below WEAK_AUTHORITY_THRESHOLD (0.60)
    const citations = [makeCitation('docs/rfc/RFC-DRAFT.md', 0.50, 'draft_rfc')];
    const result = evaluateCitations('Q4', citations, ['docs/rfc/RFC-DRAFT.md']);
    expect(result.weak_citations).toHaveLength(1);
  });

  it('handles empty citations', () => {
    const result = evaluateCitations('Q5', [], ['docs/rfc/RFC-0001.md']);
    expect(result.has_citations).toBe(false);
    expect(result.quality_score).toBe(0);
  });

  it('handles no expected sources', () => {
    const citations = [makeCitation('docs/rfc/RFC-0001.md', 0.95)];
    const result = evaluateCitations('Q6', citations, []);
    expect(result.missing_expected_sources).toHaveLength(0);
    expect(result.quality_score).toBeGreaterThan(0);
  });
});

describe('citation eval — buildCitationReport', () => {
  it('computes aggregate metrics', () => {
    const results = [
      evaluateCitations('Q1', [makeCitation('docs/rfc/RFC-0001.md', 0.95)], ['docs/rfc/RFC-0001.md']),
      evaluateCitations('Q2', [], ['docs/rfc/RFC-0002.md']),
    ];
    const report = buildCitationReport(results);
    expect(report.citation_rate).toBe(0.5);
    expect(report.avg_quality_score).toBeGreaterThanOrEqual(0);
    expect(report.total_evaluated).toBe(2);
  });

  it('computes weak citation rate', () => {
    const results = [
      evaluateCitations('Q1', [makeCitation('docs/rfc/RFC-DRAFT.md', 0.50, 'draft_rfc')], []),
      evaluateCitations('Q2', [makeCitation('docs/rfc/RFC-0001.md', 0.95)], []),
    ];
    const report = buildCitationReport(results);
    expect(report.weak_citation_rate).toBeGreaterThan(0);
    expect(report.weak_citation_rate).toBeLessThanOrEqual(1);
  });
});

// ── Adversarial eval ─────────────────────────────────────────────────────────

describe('adversarial eval — detectForbiddenClaims', () => {
  it('detects forbidden claim in answer', () => {
    const found = detectForbiddenClaims(
      'An operator at level 1 can perform cross-operator settlement.',
      ['cross-operator settlement'],
    );
    expect(found).toHaveLength(1);
    expect(found[0]).toContain('cross-operator settlement');
  });

  it('returns empty when no forbidden claims', () => {
    const found = detectForbiddenClaims(
      'An operator at level 0 must implement a valid manifest.',
      ['cross-operator settlement', 'sandbox environment can'],
    );
    expect(found).toHaveLength(0);
  });

  it('is case-insensitive', () => {
    const found = detectForbiddenClaims(
      'You can SKIP LEVELS to reach level 3 faster.',
      ['skip levels'],
    );
    expect(found).toHaveLength(1);
  });
});

describe('adversarial eval — detectRequiredConcepts', () => {
  it('detects missing required concept', () => {
    const missing = detectRequiredConcepts(
      'You must implement the protocol properly.',
      ['certification', 'level 0'],
    );
    expect(missing.length).toBeGreaterThan(0);
  });

  it('returns empty when all concepts present', () => {
    const missing = detectRequiredConcepts(
      'Certification requires passing all level 0 conformance tests.',
      ['certification', 'level 0'],
    );
    expect(missing).toHaveLength(0);
  });
});

describe('adversarial eval — validateProtocolTruth', () => {
  it('passes when tool and model agree', () => {
    const result = validateProtocolTruth(
      { type: 'conformance_result', level_achieved: 2 },
      'The conformance check shows level 2 achieved.',
    );
    expect(result.conflict).toBe(false);
    expect(result.winner).toBe('agreement');
  });

  it('detects conflict when model claims higher level than tool', () => {
    const result = validateProtocolTruth(
      { type: 'conformance_result', level_achieved: 1 },
      'The operator has achieved certification level 3.',
    );
    expect(result.conflict).toBe(true);
    expect(result.winner).toBe('tool');
  });

  it('detects conflict when model claims validation passed but tool says failed', () => {
    const result = validateProtocolTruth(
      { type: 'validation_result', valid: false, errors: ['missing operator_id'] },
      'The manifest is valid and passes all checks.',
    );
    expect(result.conflict).toBe(true);
    expect(result.winner).toBe('tool');
  });

  it('passes when model correctly reports validation failure', () => {
    const result = validateProtocolTruth(
      { type: 'validation_result', valid: false, errors: ['missing operator_id'] },
      'The manifest is invalid. The operator_id field is missing.',
    );
    expect(result.conflict).toBe(false);
  });

  it('handles unknown tool result type gracefully', () => {
    const result = validateProtocolTruth(
      { type: 'trace_analysis', events: 3 },
      'The trace contains 3 events in the audit log.',
    );
    expect(result.conflict).toBe(false);
  });
});
