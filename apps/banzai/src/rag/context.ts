import type { SearchResult, PromptContext, ContextChunk } from './types.js';

const TOKEN_BUDGET = 3000;
const CHARS_PER_TOKEN = 4;

function estimateTokens(text: string): number {
  return Math.ceil(text.length / CHARS_PER_TOKEN);
}

function sourceSummary(chunks: ContextChunk[]): string {
  const types = [...new Set(chunks.map((c) => c.citation.source_type))];
  const paths = [...new Set(chunks.map((c) => c.citation.path))].slice(0, 5);
  return `${types.join(', ')} — ${paths.join(', ')}`;
}

export function buildContext(results: SearchResult[]): PromptContext {
  const included: ContextChunk[] = [];
  let totalTokens = 0;

  for (const r of results) {
    const tokens = estimateTokens(r.text);
    if (totalTokens + tokens > TOKEN_BUDGET) break;
    included.push({ text: r.text, citation: r.citation });
    totalTokens += tokens;
  }

  return {
    chunks: included,
    citations: included.map((c) => c.citation),
    source_summary: included.length > 0 ? sourceSummary(included) : 'no sources',
    weak_retrieval: results.length === 0 || (results[0]?.score ?? 0) < 0.3,
    token_estimate: totalTokens,
  };
}

export function renderContextBlock(ctx: PromptContext): string {
  if (ctx.chunks.length === 0) {
    return '<!-- No protocol context found for this query -->';
  }

  const blocks = ctx.chunks.map((c, i) => {
    const ref = `[${i + 1}] ${c.citation.path}${c.citation.section ? ' § ' + c.citation.section : ''}`;
    return `### Source ${i + 1}: ${ref}\n\n${c.text}`;
  });

  return blocks.join('\n\n---\n\n');
}
