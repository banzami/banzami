#!/usr/bin/env tsx
import { config } from '../src/config.js';
import { createEmbeddingProvider } from '../src/rag/embedding/factory.js';
import { indexDocuments, getIndexState } from '../src/rag/indexer.js';
import { search } from '../src/rag/search.js';
import { qdrantHealthy, collectionInfo, ensureCollection } from '../src/store/qdrant.js';

const [, , command, ...args] = process.argv;

async function cmdIndex() {
  const incremental = args.includes('--incremental') || args.includes('-i');
  const verbose = args.includes('--verbose') || args.includes('-v') || !args.includes('--quiet');
  const embedder = createEmbeddingProvider(config);

  console.log(`BanzamIA Indexer`);
  console.log(`  Mode:     ${config.mode}`);
  console.log(`  Embedder: ${config.embedding.provider} (${config.embedding.dims} dims)`);
  console.log(`  Qdrant:   ${config.qdrant.url}`);
  console.log(`  Docs:     ${config.docsRoot}`);
  console.log(`  Incremental: ${incremental}`);
  console.log('');

  const alive = await qdrantHealthy(config);
  if (!alive) {
    console.error(`✗ Qdrant not reachable at ${config.qdrant.url}`);
    console.error('  Start Qdrant: docker run -p 6333:6333 qdrant/qdrant');
    process.exit(1);
  }

  await ensureCollection(config);
  console.log(`  Collection '${config.qdrant.collection}' ready`);
  console.log('');

  const result = await indexDocuments(config, embedder, { incremental, verbose });
  console.log('');
  console.log('Indexing complete:');
  console.log(`  Documents found:   ${result.total_documents}`);
  console.log(`  Documents indexed: ${result.indexed_documents}`);
  console.log(`  Documents skipped: ${result.skipped_documents}`);
  console.log(`  Chunks created:    ${result.total_chunks}`);
  console.log(`  Duration:          ${result.duration_ms}ms`);

  if (result.errors.length > 0) {
    console.error(`\n  Errors (${result.errors.length}):`);
    for (const e of result.errors) {
      console.error(`    - ${e}`);
    }
  }
}

async function cmdSearch() {
  const query = args.filter((a) => !a.startsWith('-')).join(' ');
  if (!query) {
    console.error('Usage: rag-cli search <query>');
    process.exit(1);
  }

  const embedder = createEmbeddingProvider(config);
  const alive = await qdrantHealthy(config);
  if (!alive) {
    console.error(`✗ Qdrant not reachable at ${config.qdrant.url}`);
    process.exit(1);
  }

  console.log(`Searching: "${query}"\n`);
  const response = await search(config, embedder, query, 5);

  console.log(`Mode: ${response.mode}  Weak: ${response.weak_retrieval}`);
  console.log(`Results: ${response.results.length}\n`);

  for (let i = 0; i < response.results.length; i++) {
    const r = response.results[i];
    console.log(`[${i + 1}] Score: ${r.score.toFixed(3)} (semantic: ${r.semantic_score.toFixed(3)}, authority: ${r.authority_weight.toFixed(2)})`);
    console.log(`    ${r.citation.source_type} — ${r.citation.path}`);
    if (r.citation.section) console.log(`    § ${r.citation.section}`);
    console.log(`    ${r.text.slice(0, 200).replace(/\n/g, ' ')}...`);
    console.log('');
  }

  if (response.results.length === 0) {
    console.log('No results. Run `rag-cli index` to index documents first.');
  }
}

async function cmdStatus() {
  const alive = await qdrantHealthy(config);
  const embedder = createEmbeddingProvider(config);
  const embStatus = await embedder.status();
  const state = await getIndexState(config);
  const colInfo = alive ? await collectionInfo(config) : { points_count: 0 };

  console.log('BanzamIA RAG Status');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`  Mode:             ${config.mode}`);
  console.log(`  Qdrant:           ${alive ? '✓ available' : '✗ unavailable'} (${config.qdrant.url})`);
  console.log(`  Collection:       ${config.qdrant.collection}`);
  console.log(`  Chunks indexed:   ${colInfo.points_count}`);
  console.log(`  Documents:        ${state?.document_count ?? 0}`);
  console.log(`  Last indexed:     ${state?.last_indexed_at ?? 'never'}`);
  console.log(`  Embedding:        ${embStatus.available ? '✓' : '✗'} ${embStatus.provider} (${embStatus.model})`);
  console.log(`  Dims:             ${embStatus.dims}`);
  console.log(`  Hybrid search:    ${alive ? '✓ available' : '✗ unavailable'}`);
  console.log(`  Authority rank:   ✓ available`);
  if (!alive) {
    console.log('\n  Start Qdrant: docker run -p 6333:6333 qdrant/qdrant');
  }
}

const commands: Record<string, () => Promise<void>> = {
  index: cmdIndex,
  search: cmdSearch,
  status: cmdStatus,
};

const handler = commands[command];
if (!handler) {
  console.error(`Unknown command: ${command ?? '(none)'}`);
  console.error('Available commands: index, search, status');
  console.error('');
  console.error('Examples:');
  console.error('  npm run rag:index            # index all documents');
  console.error('  npm run rag:index -- -i      # incremental (skip unchanged files)');
  console.error('  npm run rag:search gross_minor');
  console.error('  npm run rag:status');
  process.exit(1);
}

handler().catch((e) => {
  console.error('Fatal:', e);
  process.exit(1);
});
