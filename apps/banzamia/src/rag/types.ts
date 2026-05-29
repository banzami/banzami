export type SourceType =
  | 'reference'
  | 'accepted_rfc'
  | 'draft_rfc'
  | 'accepted_adr'
  | 'openapi'
  | 'conformance'
  | 'certification'
  | 'manifest_schema'
  | 'invariant'
  | 'glossary'
  | 'architecture_doc'
  | 'sdk_doc'
  | 'banzamia_doc'
  | 'readme'
  | 'website';

export interface DocumentMeta {
  path: string;
  title: string;
  section: string;
  source_type: SourceType;
  status: string;
  version: string;
  authority: number;
  language: string;
  repo: string;
  updated_at: string;
}

export interface Document extends DocumentMeta {
  content: string;
}

export interface ChunkPayload extends DocumentMeta {
  chunk_id: string;
  document_id: string;
  heading_path: string;
  start_line: number;
  end_line: number;
  text: string;
}

export interface Citation {
  title: string;
  path: string;
  section: string;
  source_type: SourceType;
  start_line: number;
  end_line: number;
  authority: number;
  score: number;
}

export interface SearchResult {
  text: string;
  citation: Citation;
  score: number;
  semantic_score: number;
  authority_weight: number;
}

export interface SearchResponse {
  results: SearchResult[];
  mode: 'vector' | 'hybrid' | 'keyword' | 'mock';
  weak_retrieval: boolean;
}

export interface SearchFilters {
  source_type?: SourceType | SourceType[];
  status?: string;
  language?: string;
  repo?: string;
  path_prefix?: string;
}

export interface ContextChunk {
  text: string;
  citation: Citation;
}

export interface PromptContext {
  chunks: ContextChunk[];
  citations: Citation[];
  source_summary: string;
  weak_retrieval: boolean;
  token_estimate: number;
}

export interface RagStatus {
  qdrant: 'available' | 'unavailable';
  collection: string;
  documents_indexed: number;
  chunks_indexed: number;
  embedding_provider: string;
  last_indexed_at: string | null;
  hybrid_search: 'available' | 'unavailable';
  authority_ranking: 'available';
}
