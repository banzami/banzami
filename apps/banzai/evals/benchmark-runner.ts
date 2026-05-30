import { writeFile, mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import { config } from '../src/config.js';
import { createEmbeddingProvider } from '../src/rag/embedding/factory.js';
import { MockModelProvider } from '../src/orchestrator/providers/mock.js';
import { evaluateRetrieval, type GoldenQuestion } from './retrieval-eval.js';
import { evaluateCitations, buildCitationReport } from './citation-eval.js';
import { runAdversarialEval, TRAP_QUESTIONS } from './adversarial-eval.js';
import { authorityWeight } from '../src/rag/authority.js';
import { ask } from '../src/orchestrator/pipeline.js';
import { qdrantHealthy } from '../src/store/qdrant.js';

const REPORTS_DIR = new URL('../reports/', import.meta.url).pathname;

async function loadQuestions(): Promise<GoldenQuestion[]> {
  const { readFile } = await import('node:fs/promises');
  const raw = await readFile(
    new URL('./datasets/protocol-questions.json', import.meta.url).pathname,
    'utf-8',
  );
  return JSON.parse(raw) as GoldenQuestion[];
}

async function writeReport(name: string, data: unknown): Promise<void> {
  await mkdir(REPORTS_DIR, { recursive: true });
  const path = join(REPORTS_DIR, name);
  await writeFile(path, JSON.stringify(data, null, 2), 'utf-8');
  console.log(`  ✓ ${path}`);
}

async function runAuthorityRankingValidation() {
  const checks = [
    { high: 'reference', low: 'readme', label: 'BANZA_REFERENCE > README' },
    { high: 'accepted_rfc', low: 'draft_rfc', label: 'accepted_rfc > draft_rfc' },
    { high: 'accepted_adr', low: 'readme', label: 'accepted_adr > readme' },
    { high: 'openapi', low: 'website', label: 'openapi > website' },
    { high: 'conformance', low: 'website', label: 'conformance > website' },
  ] as const;

  const results = checks.map((c) => ({
    rule: c.label,
    high_type: c.high,
    high_weight: authorityWeight(c.high),
    low_type: c.low,
    low_weight: authorityWeight(c.low),
    passes: authorityWeight(c.high) > authorityWeight(c.low),
  }));

  const allPass = results.every((r) => r.passes);
  return { passes: allPass, checks: results, generated_at: new Date().toISOString() };
}

export async function runBenchmark(options: {
  skipAdversarial?: boolean;
  questions?: GoldenQuestion[];
  verbose?: boolean;
} = {}): Promise<void> {
  const embedder = createEmbeddingProvider(config);
  const model = new MockModelProvider();
  const questions = options.questions ?? await loadQuestions();

  console.log('');
  console.log('BanzamIA Evaluation Benchmark');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`  Questions:   ${questions.length}`);
  console.log(`  Embedder:    ${config.embedding.provider}`);
  console.log(`  Mode:        ${config.mode}`);

  const alive = await qdrantHealthy(config);
  console.log(`  Qdrant:      ${alive ? 'available' : 'unavailable (using mock results)'}`);
  console.log('');

  console.log('1. Authority Ranking Validation');
  const authorityReport = await runAuthorityRankingValidation();
  await writeReport('authority-ranking-report.json', authorityReport);
  console.log(`   ${authorityReport.passes ? '✓ All authority ranking rules pass' : '✗ Authority ranking failures detected'}`);
  console.log('');

  console.log('2. Retrieval Quality Evaluation');
  const subset = questions.slice(0, alive ? questions.length : 20);
  console.log(`   Evaluating ${subset.length} questions...`);
  const retrievalReport = await evaluateRetrieval(config, embedder, subset);
  await writeReport('retrieval-report.json', retrievalReport);
  const m = retrievalReport.metrics;
  console.log(`   Top-1:  ${(m.top_1_accuracy * 100).toFixed(1)}%`);
  console.log(`   Top-3:  ${(m.top_3_accuracy * 100).toFixed(1)}%`);
  console.log(`   Top-5:  ${(m.top_5_accuracy * 100).toFixed(1)}%`);
  console.log(`   MRR:    ${m.mrr.toFixed(3)}`);
  console.log(`   Recall@5: ${(m.recall_at_5 * 100).toFixed(1)}%`);
  console.log(`   Weak retrieval rate: ${(m.weak_retrieval_rate * 100).toFixed(1)}%`);
  console.log('');

  console.log('3. Citation Quality Evaluation');
  const citResults = [];
  for (const q of subset.slice(0, 20)) {
    const resp = await ask(config, embedder, model, { question: q.question });
    citResults.push(evaluateCitations(q.id, resp.citations, q.expected_sources));
  }
  const citReport = buildCitationReport(citResults);
  await writeReport('citation-report.json', citReport);
  console.log(`   Citation rate:    ${(citReport.citation_rate * 100).toFixed(1)}%`);
  console.log(`   Avg quality:      ${citReport.avg_quality_score.toFixed(3)}`);
  console.log(`   Avg authority:    ${citReport.avg_authority.toFixed(3)}`);
  console.log(`   Weak citations:   ${(citReport.weak_citation_rate * 100).toFixed(1)}%`);
  console.log('');

  if (!options.skipAdversarial) {
    console.log('4. Adversarial Protocol Tests');
    console.log(`   Running ${TRAP_QUESTIONS.length} trap questions...`);
    const adversarialReport = await runAdversarialEval(config, embedder, model);
    await writeReport('adversarial-report.json', adversarialReport);
    console.log(`   Passed: ${adversarialReport.passed}/${adversarialReport.total} (${(adversarialReport.pass_rate * 100).toFixed(0)}%)`);
    if (adversarialReport.failed > 0) {
      const failures = adversarialReport.results.filter((r) => !r.passed);
      for (const f of failures) {
        console.log(`   ✗ ${f.id}: ${f.trap_description}`);
      }
    }
    console.log('');
  }

  const summary = {
    generated_at: new Date().toISOString(),
    retrieval: {
      top_3_accuracy: retrievalReport.metrics.top_3_accuracy,
      mrr: retrievalReport.metrics.mrr,
      weak_retrieval_rate: retrievalReport.metrics.weak_retrieval_rate,
    },
    citations: {
      citation_rate: citReport.citation_rate,
      avg_quality: citReport.avg_quality_score,
      avg_authority: citReport.avg_authority,
    },
    authority_ranking: { all_rules_pass: authorityReport.passes },
    questions_evaluated: subset.length,
  };
  await writeReport('benchmark-summary.json', summary);

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('Reports written to reports/');
}
