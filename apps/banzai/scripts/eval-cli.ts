import { runBenchmark } from '../evals/benchmark-runner.js';

const args = process.argv.slice(2);
const skipAdversarial = args.includes('--skip-adversarial');
const verbose = args.includes('--verbose');

await runBenchmark({ skipAdversarial, verbose });
