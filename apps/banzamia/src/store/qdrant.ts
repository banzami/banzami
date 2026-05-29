import { QdrantClient } from '@qdrant/js-client-rest';
import type { ChunkPayload } from '../rag/types.js';
import type { Config } from '../config.js';

export interface ScoredChunk {
  payload: ChunkPayload;
  score: number;
}

export interface ScrollFilter {
  source_type?: string | string[];
  status?: string;
  language?: string;
  repo?: string;
}

let _client: QdrantClient | null = null;

export function getClient(cfg: Config): QdrantClient {
  if (!_client) {
    _client = new QdrantClient({ url: cfg.qdrant.url });
  }
  return _client;
}

export async function ensureCollection(cfg: Config): Promise<void> {
  const client = getClient(cfg);
  const exists = await collectionExists(cfg);

  if (!exists) {
    await client.createCollection(cfg.qdrant.collection, {
      vectors: { size: cfg.qdrant.dims, distance: 'Cosine' },
    });

    await Promise.all([
      client.createPayloadIndex(cfg.qdrant.collection, {
        field_name: 'document_id',
        field_schema: 'keyword',
      }),
      client.createPayloadIndex(cfg.qdrant.collection, {
        field_name: 'source_type',
        field_schema: 'keyword',
      }),
      client.createPayloadIndex(cfg.qdrant.collection, {
        field_name: 'status',
        field_schema: 'keyword',
      }),
      client.createPayloadIndex(cfg.qdrant.collection, {
        field_name: 'text',
        field_schema: { type: 'text', tokenizer: 'word', lowercase: true, min_token_len: 2, max_token_len: 40 },
      }),
    ]);
  }
}

async function collectionExists(cfg: Config): Promise<boolean> {
  const client = getClient(cfg);
  try {
    const info = await client.getCollections();
    return info.collections.some((c) => c.name === cfg.qdrant.collection);
  } catch {
    return false;
  }
}

export async function qdrantHealthy(cfg: Config): Promise<boolean> {
  try {
    const client = getClient(cfg);
    await client.getCollections();
    return true;
  } catch {
    return false;
  }
}

export async function collectionInfo(cfg: Config): Promise<{ points_count: number }> {
  try {
    const client = getClient(cfg);
    const info = await client.getCollection(cfg.qdrant.collection);
    return { points_count: info.points_count ?? 0 };
  } catch {
    return { points_count: 0 };
  }
}

export async function deleteByDocumentId(cfg: Config, documentId: string): Promise<void> {
  const client = getClient(cfg);
  await client.delete(cfg.qdrant.collection, {
    wait: true,
    filter: {
      must: [{ key: 'document_id', match: { value: documentId } }],
    },
  });
}

const UPSERT_BATCH = 100;

export async function upsertChunks(
  cfg: Config,
  chunks: ChunkPayload[],
  vectors: number[][],
): Promise<void> {
  const client = getClient(cfg);
  for (let i = 0; i < chunks.length; i += UPSERT_BATCH) {
    const batch = chunks.slice(i, i + UPSERT_BATCH);
    const vecs = vectors.slice(i, i + UPSERT_BATCH);
    await client.upsert(cfg.qdrant.collection, {
      wait: true,
      points: batch.map((chunk, idx) => ({
        id: chunk.chunk_id,
        vector: vecs[idx],
        payload: chunk as unknown as Record<string, unknown>,
      })),
    });
  }
}

export async function vectorSearch(
  cfg: Config,
  vector: number[],
  limit: number,
  filter?: ScrollFilter,
): Promise<ScoredChunk[]> {
  const client = getClient(cfg);
  const must: unknown[] = [];

  if (filter?.source_type) {
    const types = Array.isArray(filter.source_type)
      ? filter.source_type
      : [filter.source_type];
    must.push({ key: 'source_type', match: { any: types } });
  }
  if (filter?.status) must.push({ key: 'status', match: { value: filter.status } });
  if (filter?.language) must.push({ key: 'language', match: { value: filter.language } });
  if (filter?.repo) must.push({ key: 'repo', match: { value: filter.repo } });

  const results = await client.search(cfg.qdrant.collection, {
    vector,
    limit,
    with_payload: true,
    ...(must.length > 0 ? { filter: { must } } : {}),
  });

  return results.map((r) => ({
    payload: r.payload as unknown as ChunkPayload,
    score: r.score,
  }));
}

export async function keywordSearch(
  cfg: Config,
  query: string,
  limit: number,
  filter?: ScrollFilter,
): Promise<ScoredChunk[]> {
  const client = getClient(cfg);
  const must: unknown[] = [
    { key: 'text', match: { text: query } },
  ];

  if (filter?.source_type) {
    const types = Array.isArray(filter.source_type)
      ? filter.source_type
      : [filter.source_type];
    must.push({ key: 'source_type', match: { any: types } });
  }

  try {
    const result = await client.scroll(cfg.qdrant.collection, {
      filter: { must },
      limit,
      with_payload: true,
      with_vector: false,
    });

    return result.points.map((p) => ({
      payload: p.payload as unknown as ChunkPayload,
      score: 0.5,
    }));
  } catch {
    return [];
  }
}
