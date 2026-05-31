import { describe, it, expect } from 'vitest';
import { chunkDocument } from '../src/rag/chunker.js';
import type { Document } from '../src/rag/types.js';

const baseDoc: Omit<Document, 'content'> = {
  path: 'docs/test.md',
  title: 'Test Document',
  section: 'Test Document',
  source_type: 'reference',
  status: 'active',
  version: '1.0',
  authority: 1.0,
  language: 'pt',
  repo: 'banza-protocols/banza',
  updated_at: '2026-01-01T00:00:00.000Z',
};

function doc(content: string): Document {
  return { ...baseDoc, content };
}

describe('chunkDocument', () => {
  it('splits a document on h2 headings', () => {
    const content = `# Document Title

Some intro text that is long enough to trigger a split.
This text needs to be long enough so that the minimum token count is met.
Adding more content here to ensure we have enough tokens before the heading.
Even more text to make sure the chunk is large enough to be finalized.

## Section One

Content of section one.
This section has enough content to form a proper chunk.
We need at least 100 tokens worth of content here.
Adding more sentences to ensure the minimum is met for testing purposes.

## Section Two

Content of section two.
This section also has enough content to form a proper chunk.
We need at least 100 tokens worth of content here too.
Adding more sentences to ensure the minimum is met.
`;

    const chunks = chunkDocument(doc(content));
    expect(chunks.length).toBeGreaterThan(0);
    expect(chunks.every((c) => c.text.length > 0)).toBe(true);
  });

  it('does not split code blocks', () => {
    const content = `# Guide

Some introductory text that is long enough.
Adding more content here so we reach the minimum token threshold.
We need quite a bit of text before the code block appears here.

\`\`\`typescript
const x = 1;
const y = 2;
// This code should never be split
function add(a: number, b: number): number {
  return a + b;
}
\`\`\`

More text after the code block.
`;

    const chunks = chunkDocument(doc(content));
    const codeChunks = chunks.filter((c) => c.text.includes('```typescript'));
    for (const chunk of codeChunks) {
      const opens = (chunk.text.match(/```/g) ?? []).length;
      expect(opens % 2).toBe(0);
    }
  });

  it('preserves heading path in metadata', () => {
    const content = `# Top Level

## Sub Section

### Deep Section

This is content in the deep section with enough text to be a real chunk.
Adding more content to ensure we have enough tokens for this chunk.
Even more text to make the test reliable and deterministic.
`;

    const chunks = chunkDocument(doc(content));
    const deepChunk = chunks.find((c) => c.heading_path.includes('Deep Section'));
    expect(deepChunk).toBeDefined();
    expect(deepChunk!.heading_path).toContain('Top Level');
    expect(deepChunk!.heading_path).toContain('Sub Section');
    expect(deepChunk!.heading_path).toContain('Deep Section');
  });

  it('generates unique chunk_ids', () => {
    const content = `# Doc\n\n${'Word '.repeat(300)}\n\n## Section B\n\n${'Word '.repeat(300)}`;
    const chunks = chunkDocument(doc(content));
    const ids = chunks.map((c) => c.chunk_id);
    const unique = new Set(ids);
    expect(unique.size).toBe(ids.length);
  });

  it('handles JSON files as single chunks', () => {
    const jsonDoc: Document = {
      ...baseDoc,
      path: 'conformance/vectors/test.json',
      content: JSON.stringify({ type: 'test', data: [1, 2, 3] }),
    };
    const chunks = chunkDocument(jsonDoc);
    expect(chunks.length).toBe(1);
    expect(chunks[0].source_type).toBe('reference');
  });

  it('skips nearly empty documents', () => {
    const chunks = chunkDocument(doc('# Title\n\n'));
    expect(chunks.length).toBe(0);
  });

  it('preserves table content within a chunk', () => {
    const content = `# Reference

Intro paragraph with enough text to ensure we meet the minimum token count.
Adding more content here to make sure we have enough.

| Field | Type | Required |
|-------|------|----------|
| id | string | yes |
| amount | number | yes |
| currency | string | yes |

Post-table text.
`;

    const chunks = chunkDocument(doc(content));
    const tableChunk = chunks.find((c) => c.text.includes('| Field |'));
    expect(tableChunk).toBeDefined();
    expect(tableChunk!.text).toContain('| id |');
    expect(tableChunk!.text).toContain('| amount |');
  });
});
