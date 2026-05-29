import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MockEmbeddingProvider } from '../src/rag/embedding/mock.js';
import { buildContext, renderContextBlock } from '../src/rag/context.js';
import { classifyTask } from '../src/orchestrator/router.js';
import { validateManifest } from '../src/tools/manifest-validator.js';
import { runConformanceCheck } from '../src/tools/conformance-runner.js';
import { explainTrace } from '../src/tools/trace-explainer.js';
import type { SearchResult } from '../src/rag/types.js';

describe('MockEmbeddingProvider', () => {
  const provider = new MockEmbeddingProvider(1024);

  it('returns vector of correct dimension', async () => {
    const vec = await provider.embed('hello world');
    expect(vec.length).toBe(1024);
  });

  it('returns unit vectors', async () => {
    const vec = await provider.embed('test');
    const norm = Math.sqrt(vec.reduce((s, v) => s + v * v, 0));
    expect(norm).toBeCloseTo(1.0, 5);
  });

  it('same input always yields same vector', async () => {
    const v1 = await provider.embed('deterministic');
    const v2 = await provider.embed('deterministic');
    expect(v1).toEqual(v2);
  });

  it('different inputs yield different vectors', async () => {
    const v1 = await provider.embed('gross_minor');
    const v2 = await provider.embed('settlement_currency');
    expect(v1).not.toEqual(v2);
  });

  it('embedBatch returns correct number of vectors', async () => {
    const vecs = await provider.embedBatch(['a', 'b', 'c']);
    expect(vecs.length).toBe(3);
  });

  it('status reports available', async () => {
    const status = await provider.status();
    expect(status.available).toBe(true);
    expect(status.dims).toBe(1024);
  });
});

describe('buildContext', () => {
  function makeResult(text: string, score = 0.8): SearchResult {
    return {
      text,
      citation: {
        title: 'Test Doc',
        path: 'docs/test.md',
        section: 'Section',
        source_type: 'reference',
        start_line: 0,
        end_line: 10,
        authority: 1.0,
        score,
      },
      score,
      semantic_score: score,
      authority_weight: 1.0,
    };
  }

  it('includes results within token budget', () => {
    const results = [makeResult('Short text'), makeResult('Another short text')];
    const ctx = buildContext(results);
    expect(ctx.chunks.length).toBe(2);
    expect(ctx.citations.length).toBe(2);
  });

  it('empty results yields weak_retrieval', () => {
    const ctx = buildContext([]);
    expect(ctx.weak_retrieval).toBe(true);
    expect(ctx.chunks.length).toBe(0);
  });

  it('high score result does not flag weak retrieval', () => {
    const ctx = buildContext([makeResult('text', 0.9)]);
    expect(ctx.weak_retrieval).toBe(false);
  });

  it('renderContextBlock includes source references', () => {
    const ctx = buildContext([makeResult('Protocol content about payments')]);
    const block = renderContextBlock(ctx);
    expect(block).toContain('docs/test.md');
    expect(block).toContain('Protocol content about payments');
  });
});

describe('classifyTask', () => {
  it('detects code questions', () => {
    expect(classifyTask('How do I install the TypeScript SDK?').task_type).toBe('code');
    expect(classifyTask('Show me an npm package example').task_type).toBe('code');
  });

  it('detects trace questions', () => {
    expect(classifyTask('Explain trace_id abc123').task_type).toBe('trace');
    expect(classifyTask('What happened in this audit log?').task_type).toBe('trace');
  });

  it('detects validation questions', () => {
    expect(classifyTask('Is this manifest valid JSON?').task_type).toBe('validation');
    expect(classifyTask('Validate my MON-001 schema').task_type).toBe('validation');
  });

  it('detects certification questions', () => {
    expect(classifyTask('How do I reach operator level 2?').task_type).toBe('certification');
    expect(classifyTask('What are the conformance requirements?').task_type).toBe('certification');
  });

  it('detects reasoning questions', () => {
    expect(classifyTask('Why does the double-entry ledger require two postings?').task_type).toBe('reasoning');
    expect(classifyTask('Explain RFC-0004 architecture decisions').task_type).toBe('reasoning');
  });

  it('defaults to docs for general questions', () => {
    expect(classifyTask('What is Banzami?').task_type).toBe('docs');
    expect(classifyTask('Como funciona o protocolo?').task_type).toBe('docs');
  });
});

describe('validateManifest', () => {
  it('validates a correct operator manifest', () => {
    const result = validateManifest({
      operator_id: 'op-001',
      protocol_version: '1.0',
      capabilities: ['wallets', 'transfers'],
      settlement_currency: 'AOA',
    });
    expect(result.valid).toBe(true);
    expect(result.errors.length).toBe(0);
    expect(result.manifest_type).toBe('operator');
  });

  it('fails on missing required fields', () => {
    const result = validateManifest({ operator_id: 'op-001' });
    expect(result.valid).toBe(false);
    expect(result.errors.some((e) => e.code === 'MISSING_REQUIRED_FIELD')).toBe(true);
  });

  it('fails on invalid currency', () => {
    const result = validateManifest({
      operator_id: 'op-001',
      protocol_version: '1.0',
      capabilities: ['wallets'],
      settlement_currency: 'invalid',
    });
    expect(result.valid).toBe(false);
    expect(result.errors.some((e) => e.code === 'INVALID_CURRENCY')).toBe(true);
  });

  it('fails on invalid protocol version', () => {
    const result = validateManifest({
      operator_id: 'op-001',
      protocol_version: 'not.valid.version.format.extra',
      capabilities: ['wallets'],
      settlement_currency: 'AOA',
    });
    expect(result.valid).toBe(false);
    expect(result.errors.some((e) => e.code === 'INVALID_PROTOCOL_VERSION')).toBe(true);
  });

  it('rejects non-object input', () => {
    expect(validateManifest(null).valid).toBe(false);
    expect(validateManifest('string').valid).toBe(false);
    expect(validateManifest([]).valid).toBe(false);
  });
});

describe('runConformanceCheck', () => {
  const fullCaps = {
    manifest_valid: true,
    wallet_ops: true,
    qr_payments: true,
    payment_links: true,
    cross_operator: true,
    federation: true,
    offline: true,
  };

  it('passes all checks for fully capable operator', () => {
    const result = runConformanceCheck(fullCaps, 4);
    expect(result.failed.length).toBe(0);
    expect(result.compliant).toBe(true);
    expect(result.level_achieved).toBe(4);
  });

  it('fails level 1 checks without wallet_ops', () => {
    const result = runConformanceCheck({ ...fullCaps, wallet_ops: false }, 1);
    expect(result.failed.length).toBeGreaterThan(0);
    expect(result.compliant).toBe(false);
  });

  it('level 0 passes with only manifest_valid', () => {
    const result = runConformanceCheck({
      manifest_valid: true,
      wallet_ops: false,
      qr_payments: false,
      payment_links: false,
      cross_operator: false,
      federation: false,
      offline: false,
    }, 0);
    expect(result.failed.length).toBe(0);
  });
});

describe('explainTrace', () => {
  const traceId = 'abc123def456';
  const events = [
    { event_id: 'evt-001', event_type: 'transfer.initiated', timestamp: '2026-01-01T10:00:00Z', trace_id: traceId },
    { event_id: 'evt-002', event_type: 'ledger.posting', timestamp: '2026-01-01T10:00:01Z', trace_id: traceId, causation_id: 'evt-001' },
    { event_id: 'evt-003', event_type: 'transfer.completed', timestamp: '2026-01-01T10:00:02Z', trace_id: traceId, causation_id: 'evt-001' },
  ];

  it('returns timeline with explanations', () => {
    const analysis = explainTrace(events);
    expect(analysis.timeline.length).toBe(3);
    expect(analysis.timeline.every((e) => e.explanation.length > 0)).toBe(true);
  });

  it('detects no anomalies in valid trace', () => {
    const analysis = explainTrace(events);
    const causalAnomalies = analysis.anomalies.filter((a) => a.type === 'broken_causal_chain');
    expect(causalAnomalies.length).toBe(0);
  });

  it('detects duplicate event_id', () => {
    const dupes = [
      ...events,
      { event_id: 'evt-001', event_type: 'transfer.initiated', timestamp: '2026-01-01T10:00:03Z', trace_id: traceId },
    ];
    const analysis = explainTrace(dupes);
    expect(analysis.anomalies.some((a) => a.type === 'duplicate_event_id')).toBe(true);
  });

  it('detects unknown event types', () => {
    const withUnknown = [...events, { event_id: 'evt-004', event_type: 'mystery.event', timestamp: '2026-01-01T10:00:03Z', trace_id: traceId }];
    const analysis = explainTrace(withUnknown);
    expect(analysis.anomalies.some((a) => a.type === 'unknown_event_type')).toBe(true);
  });

  it('handles empty trace', () => {
    const analysis = explainTrace([]);
    expect(analysis.event_count).toBe(0);
    expect(analysis.summary).toContain('Empty');
  });

  it('identifies state transitions', () => {
    const analysis = explainTrace(events);
    const completed = analysis.timeline.find((e) => e.event.event_type === 'transfer.completed');
    expect(completed?.state_transition).toContain('SETTLED');
  });
});
