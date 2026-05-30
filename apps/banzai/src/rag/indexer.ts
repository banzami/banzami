import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { readFile, writeFile, access } from 'node:fs/promises';
import type { Config } from '../config.js';
import type { EmbeddingProvider } from './embedding/provider.js';
import { loadDocuments } from './loader.js';
import { chunkDocument } from './chunker.js';
import { ensureCollection, deleteByDocumentId, upsertChunks } from '../store/qdrant.js';
import type { ChunkPayload } from './types.js';

const INDEX_STATE_FILE = '.banzamia-index-state.json';

interface IndexState {
  last_indexed_at: string;
  document_count: number;
  chunk_count: number;
  file_hashes: Record<string, string>;
}

async function loadState(stateFile: string): Promise<IndexState> {
  try {
    await access(stateFile);
    const raw = await readFile(stateFile, 'utf-8');
    return JSON.parse(raw) as IndexState;
  } catch {
    return {
      last_indexed_at: '',
      document_count: 0,
      chunk_count: 0,
      file_hashes: {},
    };
  }
}

async function saveState(stateFile: string, state: IndexState): Promise<void> {
  await writeFile(stateFile, JSON.stringify(state, null, 2), 'utf-8');
}

function contentHash(content: string): string {
  return createHash('sha256').update(content).digest('hex').slice(0, 16);
}

function documentId(path: string): string {
  return createHash('sha256').update(path).digest('hex').slice(0, 32);
}

export interface IndexResult {
  total_documents: number;
  indexed_documents: number;
  skipped_documents: number;
  total_chunks: number;
  duration_ms: number;
  errors: string[];
}

export async function indexDocuments(
  cfg: Config,
  embedder: EmbeddingProvider,
  options: { incremental?: boolean; verbose?: boolean } = {},
): Promise<IndexResult> {
  const start = Date.now();
  const repoRoot = resolve(new URL(import.meta.url).pathname, '../../', cfg.docsRoot);
  const stateFile = resolve(repoRoot, INDEX_STATE_FILE);

  await ensureCollection(cfg);

  const state = await loadState(stateFile);
  const docs = await loadDocuments(repoRoot);

  let indexed = 0;
  let skipped = 0;
  let totalChunks = 0;
  const errors: string[] = [];

  for (const doc of docs) {
    const hash = contentHash(doc.content);
    const docId = documentId(doc.path);

    if (options.incremental && state.file_hashes[doc.path] === hash) {
      skipped++;
      continue;
    }

    try {
      const chunks = chunkDocument(doc);
      if (chunks.length === 0) continue;

      const texts = chunks.map((c) => c.text);
      const vectors = await embedder.embedBatch(texts);

      if (options.incremental) {
        await deleteByDocumentId(cfg, docId);
      }

      await upsertChunks(cfg, chunks, vectors);

      state.file_hashes[doc.path] = hash;
      totalChunks += chunks.length;
      indexed++;

      if (options.verbose) {
        process.stdout.write(`  ✓ ${doc.path} (${chunks.length} chunks)\n`);
      }
    } catch (e) {
      errors.push(`${doc.path}: ${String(e)}`);
    }
  }

  state.last_indexed_at = new Date().toISOString();
  state.document_count = docs.length;
  state.chunk_count = (state.chunk_count ?? 0) + totalChunks;
  await saveState(stateFile, state);

  return {
    total_documents: docs.length,
    indexed_documents: indexed,
    skipped_documents: skipped,
    total_chunks: totalChunks,
    duration_ms: Date.now() - start,
    errors,
  };
}

export async function getIndexState(cfg: Config): Promise<IndexState | null> {
  const repoRoot = resolve(new URL(import.meta.url).pathname, '../../', cfg.docsRoot);
  const stateFile = resolve(repoRoot, INDEX_STATE_FILE);
  try {
    return await loadState(stateFile);
  } catch {
    return null;
  }
}
