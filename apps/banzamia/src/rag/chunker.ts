import { createHash } from 'node:crypto';
import type { Document, ChunkPayload } from './types.js';

const TARGET_TOKENS = 800;
const MIN_TOKENS = 100;
const HARD_MAX_TOKENS = 1500;
const OVERLAP_CHARS = 400;
const CHARS_PER_TOKEN = 4;

function estimateTokens(text: string): number {
  return Math.ceil(text.length / CHARS_PER_TOKEN);
}

function headingLevel(line: string): number | null {
  const m = line.match(/^(#{1,6})\s+\S/);
  return m ? m[1].length : null;
}

function extractHeadingText(line: string): string {
  return line.replace(/^#{1,6}\s+/, '').trim();
}

function headingPath(headings: Map<number, string>): string {
  if (headings.size === 0) return '';
  return [...headings.keys()].sort((a, b) => a - b)
    .map((l) => headings.get(l)!)
    .join(' > ');
}

function deepestHeading(headings: Map<number, string>): string {
  if (headings.size === 0) return '';
  const maxLevel = Math.max(...headings.keys());
  return headings.get(maxLevel) ?? '';
}

function overlapLines(lines: string[]): string[] {
  let total = 0;
  const result: string[] = [];
  for (let i = lines.length - 1; i >= 0; i--) {
    total += lines[i].length + 1;
    if (total > OVERLAP_CHARS) break;
    result.unshift(lines[i]);
  }
  return result;
}

function documentId(path: string): string {
  return createHash('sha256').update(path).digest('hex').slice(0, 32);
}

function chunkId(path: string, startLine: number): string {
  const h = createHash('sha256').update(`${path}:${startLine}`).digest('hex');
  return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20, 32)}`;
}

function makeChunk(
  doc: Document,
  lines: string[],
  headings: Map<number, string>,
  startLine: number,
  endLine: number,
): ChunkPayload | null {
  const text = lines.join('\n').trim();
  if (estimateTokens(text) < 20) return null;
  const hPath = headingPath(headings);
  const section = deepestHeading(headings) || doc.title;
  return {
    chunk_id: chunkId(doc.path, startLine),
    document_id: documentId(doc.path),
    path: doc.path,
    title: doc.title,
    section,
    heading_path: hPath,
    source_type: doc.source_type,
    status: doc.status,
    version: doc.version,
    authority: doc.authority,
    language: doc.language,
    repo: doc.repo,
    updated_at: doc.updated_at,
    start_line: startLine,
    end_line: endLine,
    text,
  };
}

export function chunkDocument(doc: Document): ChunkPayload[] {
  const ext = doc.path.split('.').pop()?.toLowerCase();

  if (ext === 'json' || ext === 'yaml' || ext === 'yml') {
    return chunkStructured(doc);
  }
  return chunkMarkdown(doc);
}

function chunkStructured(doc: Document): ChunkPayload[] {
  if (estimateTokens(doc.content) <= HARD_MAX_TOKENS) {
    const lines = doc.content.split('\n');
    const text = doc.content.trim();
    if (text.length < 10) return [];
    const chunk = makeChunk(
      doc,
      [doc.content],
      new Map([[1, doc.title]]),
      0,
      lines.length - 1,
    );
    if (!chunk) {
      return [{
        chunk_id: chunkId(doc.path, 0),
        document_id: documentId(doc.path),
        path: doc.path,
        title: doc.title,
        section: doc.title,
        heading_path: doc.title,
        source_type: doc.source_type,
        status: doc.status,
        version: doc.version,
        authority: doc.authority,
        language: doc.language,
        repo: doc.repo,
        updated_at: doc.updated_at,
        start_line: 0,
        end_line: lines.length - 1,
        text,
      }];
    }
    return [chunk];
  }

  const lines = doc.content.split('\n');
  const chunks: ChunkPayload[] = [];
  let current: string[] = [];
  let startLine = 0;

  for (let i = 0; i < lines.length; i++) {
    current.push(lines[i]);
    if (estimateTokens(current.join('\n')) >= TARGET_TOKENS) {
      const chunk = makeChunk(doc, current, new Map([[1, doc.title]]), startLine, i);
      if (chunk) chunks.push(chunk);
      current = overlapLines(current);
      startLine = i - current.length + 1;
    }
  }

  if (current.length > 0) {
    const chunk = makeChunk(doc, current, new Map([[1, doc.title]]), startLine, lines.length - 1);
    if (chunk) chunks.push(chunk);
  }

  return chunks;
}

function chunkMarkdown(doc: Document): ChunkPayload[] {
  const lines = doc.content.split('\n');
  const chunks: ChunkPayload[] = [];

  const headings = new Map<number, string>();
  let currentLines: string[] = [];
  let startLine = 0;
  let inCodeBlock = false;
  let codeFence = '';
  let inTable = false;

  function flush(endLine: number) {
    const chunk = makeChunk(doc, currentLines, headings, startLine, endLine);
    if (chunk) chunks.push(chunk);
  }

  function startNewChunk(carryLines: string[], newStartLine: number) {
    currentLines = [...carryLines];
    startLine = newStartLine;
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    if (inCodeBlock) {
      currentLines.push(line);
      if (line.startsWith(codeFence)) {
        inCodeBlock = false;
        codeFence = '';
      }
      continue;
    }

    const fenceMatch = line.match(/^(`{3,}|~{3,})/);
    if (fenceMatch) {
      inCodeBlock = true;
      codeFence = fenceMatch[1];
      currentLines.push(line);
      continue;
    }

    if (line.startsWith('|')) {
      inTable = true;
      currentLines.push(line);
      continue;
    }

    if (inTable && !line.startsWith('|')) {
      inTable = false;
    }

    const level = headingLevel(line);
    if (level !== null) {
      const currentTokens = estimateTokens(currentLines.join('\n'));

      if (currentTokens >= MIN_TOKENS && level <= 3) {
        flush(i - 1);
        const carry = overlapLines(currentLines);
        startNewChunk([...carry, line], i - carry.length);
      } else {
        currentLines.push(line);
      }

      headings.set(level, extractHeadingText(line));
      for (const [l] of headings) {
        if (l > level) headings.delete(l);
      }
      continue;
    }

    currentLines.push(line);

    const tokens = estimateTokens(currentLines.join('\n'));
    if (tokens >= HARD_MAX_TOKENS && line.trim() === '') {
      flush(i);
      const carry = overlapLines(currentLines);
      startNewChunk(carry, i + 1 - carry.length);
    }
  }

  flush(lines.length - 1);
  return chunks;
}
