import { resolve } from 'node:path';
import { config } from '../src/config.js';
import { buildProtocolGraph, saveGraph } from '../src/graph/indexer.js';
import { graphStats } from '../src/graph/store.js';

const repoRoot = resolve(new URL(import.meta.url).pathname, '../../../', config.docsRoot);

console.log('');
console.log('BanzAI — Protocol Graph Indexer');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log(`  Repo root: ${repoRoot}`);
console.log('');

console.log('Scanning protocol documents...');
const t0 = Date.now();
const graph = await buildProtocolGraph(repoRoot);
const elapsed = ((Date.now() - t0) / 1000).toFixed(2);

const stats = graphStats(graph);
console.log(`  Nodes:     ${stats.node_count}`);
console.log(`  Edges:     ${stats.edge_count}`);
console.log(`  Duration:  ${elapsed}s`);
console.log('');

if (stats.nodes_by_type && typeof stats.nodes_by_type === 'object') {
  console.log('Node types:');
  for (const [type, count] of Object.entries(stats.nodes_by_type as Record<string, number>)) {
    console.log(`  ${type.padEnd(22)} ${count}`);
  }
  console.log('');
}

if (stats.edges_by_relationship && typeof stats.edges_by_relationship === 'object') {
  console.log('Relationship types:');
  for (const [rel, count] of Object.entries(stats.edges_by_relationship as Record<string, number>)) {
    console.log(`  ${rel.padEnd(22)} ${count}`);
  }
  console.log('');
}

await saveGraph(graph, repoRoot);
console.log('✓ Graph saved to .banzai-graph.json');
console.log('');
