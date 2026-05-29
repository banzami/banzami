import { describe, it, expect } from 'vitest';
import { authorityWeight, finalScore } from '../src/rag/authority.js';

describe('authorityWeight', () => {
  it('gives reference the highest weight', () => {
    expect(authorityWeight('reference')).toBe(1.0);
  });

  it('gives draft_rfc the lowest defined weight', () => {
    expect(authorityWeight('draft_rfc')).toBe(0.5);
  });

  it('accepted_rfc > accepted_adr', () => {
    expect(authorityWeight('accepted_rfc')).toBeGreaterThan(authorityWeight('accepted_adr'));
  });

  it('openapi = accepted_adr', () => {
    expect(authorityWeight('openapi')).toBe(authorityWeight('accepted_adr'));
  });

  it('conformance, certification, invariant are equal and above glossary', () => {
    const w = authorityWeight('conformance');
    expect(authorityWeight('certification')).toBe(w);
    expect(authorityWeight('invariant')).toBe(w);
    expect(w).toBeGreaterThan(authorityWeight('glossary'));
  });

  it('readme < sdk_doc weight is equal', () => {
    expect(authorityWeight('readme')).toBe(authorityWeight('sdk_doc'));
  });

  it('returns fallback 0.5 for unknown type', () => {
    expect(authorityWeight('unknown_type' as never)).toBe(0.5);
  });
});

describe('finalScore', () => {
  it('scales semantic score by authority', () => {
    const score = finalScore(1.0, 'reference', new Date().toISOString());
    expect(score).toBeGreaterThan(0.8);
    expect(score).toBeLessThanOrEqual(1.0);
  });

  it('lower authority type yields lower final score for same semantic score', () => {
    const now = new Date().toISOString();
    const refScore = finalScore(0.9, 'reference', now);
    const draftScore = finalScore(0.9, 'draft_rfc', now);
    expect(refScore).toBeGreaterThan(draftScore);
  });

  it('old documents score lower than fresh ones', () => {
    const freshScore = finalScore(0.9, 'reference', new Date().toISOString());
    const oldDate = new Date(Date.now() - 365 * 24 * 60 * 60 * 1000).toISOString();
    const oldScore = finalScore(0.9, 'reference', oldDate);
    expect(freshScore).toBeGreaterThan(oldScore);
  });

  it('invalid date falls back gracefully', () => {
    const score = finalScore(0.8, 'reference', 'not-a-date');
    expect(score).toBeGreaterThan(0);
    expect(Number.isFinite(score)).toBe(true);
  });

  it('zero semantic score always yields zero final score', () => {
    expect(finalScore(0, 'reference', new Date().toISOString())).toBe(0);
  });
});
