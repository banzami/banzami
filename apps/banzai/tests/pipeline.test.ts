import { describe, it, expect, vi } from 'vitest';
import { MockModelProvider } from '../src/orchestrator/providers/mock.js';
import { MockEmbeddingProvider } from '../src/rag/embedding/mock.js';

describe('MockModelProvider', () => {
  const provider = new MockModelProvider();

  it('returns a response for all task types', async () => {
    const types = ['docs', 'code', 'reasoning', 'validation', 'certification', 'trace'] as const;
    for (const t of types) {
      const response = await provider.generate(
        [{ role: 'user', content: 'test question' }],
        t,
      );
      expect(response.content.length).toBeGreaterThan(0);
      expect(response.task_type).toBe(t);
    }
  });

  it('streams tokens in generateStream', async () => {
    const tokens: string[] = [];
    const response = await provider.generateStream(
      [{ role: 'user', content: 'What is the reference operator?' }],
      'docs',
      (token) => tokens.push(token),
    );
    expect(tokens.length).toBeGreaterThan(0);
    expect(response.content).toBe(tokens.join(''));
  });

  it('status reports available', async () => {
    const status = await provider.status();
    expect(status.available).toBe(true);
    expect(status.provider).toBe('mock');
  });
});

describe('embedding + router integration', () => {
  it('mock embedder returns consistent vectors for RAG', async () => {
    const embedder = new MockEmbeddingProvider(384);
    const query = 'What is gross_minor in ledger postings?';
    const v1 = await embedder.embed(query);
    const v2 = await embedder.embed(query);
    expect(v1).toEqual(v2);
    expect(v1.length).toBe(384);
  });
});
