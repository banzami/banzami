import { writeFile, mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import { config } from '../src/config.js';
import { analyzeCoverage } from '../src/analytics/coverage.js';
import { qdrantHealthy } from '../src/store/qdrant.js';

const REPORTS_DIR = new URL('../reports/', import.meta.url).pathname;

console.log('');
console.log('BanzAI — Knowledge Coverage Analysis');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

const alive = await qdrantHealthy(config);
if (!alive) {
  console.error('  ✗ Qdrant unavailable. Start Qdrant and run rag:index first.');
  process.exit(1);
}

console.log('  Analyzing knowledge base coverage...');
const report = await analyzeCoverage(config);

console.log('');
console.log(`  Total chunks:    ${report.total_chunks}`);
console.log(`  Total documents: ${report.total_documents}`);
console.log(`  Health:          ${report.health.toUpperCase()}`);
console.log('');

console.log('Coverage by source type:');
for (const sc of report.coverage_by_source) {
  const bar = '█'.repeat(Math.round(sc.authority_weight * 10));
  console.log(`  ${sc.source_type.padEnd(20)} ${String(sc.chunk_count).padStart(4)} chunks  ${String(sc.document_count).padStart(3)} docs  [${bar.padEnd(10)}] auth=${sc.authority_weight.toFixed(2)}`);
}
console.log('');

if (report.uncovered_source_types.length > 0) {
  console.log(`Uncovered source types (${report.uncovered_source_types.length}):`);
  for (const st of report.uncovered_source_types) {
    console.log(`  ⚠ ${st}`);
  }
  console.log('');
}

console.log('Top documents by chunk count:');
for (const doc of report.top_documents) {
  console.log(`  ${String(doc.chunk_count).padStart(3)}  ${doc.source_type.padEnd(18)}  ${doc.path}`);
}
console.log('');

await mkdir(REPORTS_DIR, { recursive: true });
const outPath = join(REPORTS_DIR, 'coverage-report.json');
await writeFile(outPath, JSON.stringify(report, null, 2), 'utf-8');
console.log(`✓ Report written to ${outPath}`);
console.log('');
