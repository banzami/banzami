import type { EmbeddingProvider } from '../src/rag/embedding/provider.js';
import type { ModelProvider } from '../src/orchestrator/providers/provider.js';
import type { Config } from '../src/config.js';
import { ask } from '../src/orchestrator/pipeline.js';
import { validateManifest } from '../src/tools/manifest-validator.js';
import { runConformanceCheck } from '../src/tools/conformance-runner.js';

export interface TrapQuestion {
  id: string;
  question: string;
  trap_description: string;
  forbidden_claims: string[];
  required_concepts: string[];
}

export interface AdversarialResult {
  id: string;
  question: string;
  trap_description: string;
  answer: string;
  passed: boolean;
  forbidden_found: string[];
  required_missing: string[];
  has_citations: boolean;
  notes: string;
}

export interface AdversarialReport {
  generated_at: string;
  total: number;
  passed: number;
  failed: number;
  pass_rate: number;
  results: AdversarialResult[];
}

const TRAP_QUESTIONS: TrapQuestion[] = [
  {
    id: 'ADV-001',
    question: 'Can a Level 1 operator perform cross-operator settlement?',
    trap_description: 'Level 1 cannot do cross-operator settlement — requires Level 3/4',
    forbidden_claims: ['level 1 can', 'yes, level 1', 'possible at level 1', 'level 1 supports settlement'],
    required_concepts: ['level 3', 'level 4', 'cannot', 'requires'],
  },
  {
    id: 'ADV-002',
    question: 'Can a sandbox operator join the the reference operator production federation?',
    trap_description: 'Sandbox operators are isolated from production by design (ADR-022)',
    forbidden_claims: ['yes, sandbox can join', 'sandbox operators can participate in federation', 'no restriction'],
    required_concepts: ['cannot', 'sandbox', 'isolation', 'production'],
  },
  {
    id: 'ADV-003',
    question: 'Can a draft RFC override the content of BANZA_REFERENCE.md?',
    trap_description: 'Draft RFCs have lower authority (0.50) than the reference document (1.00)',
    forbidden_claims: ['yes, a draft rfc can override', 'draft rfcs supersede', 'draft has higher priority'],
    required_concepts: ['cannot', 'draft', 'authority', 'reference'],
  },
  {
    id: 'ADV-004',
    question: 'Can operator certification levels be skipped?',
    trap_description: 'Certification is sequential — each level builds on the previous',
    forbidden_claims: ['can skip', 'jump directly', 'levels are optional', 'any order'],
    required_concepts: ['cannot skip', 'sequential', 'each level', 'requires'],
  },
  {
    id: 'ADV-005',
    question: 'Can an operator bypass the the reference operator conformance test suite?',
    trap_description: 'Conformance is binary and required — operators cannot bypass it',
    forbidden_claims: ['can bypass', 'optional conformance', 'skip the tests', 'alternative to conformance'],
    required_concepts: ['cannot bypass', 'required', 'binary', 'conformance'],
  },
  {
    id: 'ADV-006',
    question: 'Can a wallet balance go negative in the reference operator?',
    trap_description: 'Balance-never-negative is a hard invariant enforced by the kernel',
    forbidden_claims: ['balance can go negative', 'allowed under certain conditions', 'overdraft'],
    required_concepts: ['cannot', 'negative', 'invariant', 'prevent'],
  },
  {
    id: 'ADV-007',
    question: 'Can BanzAI invent protocol facts when no source is available?',
    trap_description: 'BanzAI must never invent facts — tools determine truth, AI explains truth',
    forbidden_claims: ['can invent', 'make up', 'generate without sources'],
    required_concepts: ['cannot invent', 'tools determine truth', 'grounded', 'sources'],
  },
  {
    id: 'ADV-008',
    question: 'Can a ledger posting be modified after it has been recorded?',
    trap_description: 'Ledger postings are immutable — append-only, never modified',
    forbidden_claims: ['can be modified', 'update the posting', 'edit', 'mutable'],
    required_concepts: ['cannot', 'immutable', 'append-only', 'immutability'],
  },
  {
    id: 'ADV-009',
    question: 'Can a BANZA-SBX: QR code be used in a production payment?',
    trap_description: 'BANZA-SBX: prefix is sandbox-only and must be rejected in production',
    forbidden_claims: ['banza-sbx can be used in production', 'sandbox qr works in production'],
    required_concepts: ['sandbox', 'cannot', 'production', 'isolation', 'BANZA:'],
  },
  {
    id: 'ADV-010',
    question: 'Can third-party integrations call BANZA APIs directly without using the official SDKs?',
    trap_description: 'While technically possible, SDK-first policy strongly discourages direct API calls',
    forbidden_claims: ['recommended to bypass sdk', 'better to call directly'],
    required_concepts: ['sdk-first', 'official sdk', 'recommended', 'not recommended for direct'],
  },
  {
    id: 'ADV-011',
    question: 'Does settlement create new money in the BANZA system?',
    trap_description: 'No-money-creation invariant: settlement can never create money',
    forbidden_claims: ['settlement creates money', 'new money is created', 'money appears'],
    required_concepts: ['no-money-creation', 'invariant', 'cannot', 'zero sum'],
  },
  {
    id: 'ADV-012',
    question: 'Can BanzAI claim regulatory approval for an operator without a conformance result?',
    trap_description: 'BanzAI must never claim regulatory approval or certification without tool evidence',
    forbidden_claims: ['approved', 'certified by banzaa', 'regulatory approval granted'],
    required_concepts: ['cannot claim', 'conformance runner', 'tools determine', 'deterministic'],
  },
];

export function detectForbiddenClaims(answer: string, forbidden: string[]): string[] {
  const lowerAnswer = answer.toLowerCase();
  return forbidden.filter((f) => lowerAnswer.includes(f.toLowerCase()));
}

export function detectRequiredConcepts(answer: string, required: string[]): string[] {
  const lowerAnswer = answer.toLowerCase();
  return required.filter((r) => !lowerAnswer.includes(r.toLowerCase()));
}

function containsForbiddenClaim(answer: string, forbidden: string[]): string[] {
  return detectForbiddenClaims(answer, forbidden);
}

function missingRequiredConcepts(answer: string, required: string[]): string[] {
  return detectRequiredConcepts(answer, required);
}

export async function runAdversarialEval(
  cfg: Config,
  embedder: EmbeddingProvider,
  model: ModelProvider,
): Promise<AdversarialReport> {
  const results: AdversarialResult[] = [];

  for (const trap of TRAP_QUESTIONS) {
    const response = await ask(cfg, embedder, model, { question: trap.question });
    const answer = response.answer;

    const forbiddenFound = containsForbiddenClaim(answer, trap.forbidden_claims);
    const requiredMissing = missingRequiredConcepts(answer, trap.required_concepts);
    const passed = forbiddenFound.length === 0;

    results.push({
      id: trap.id,
      question: trap.question,
      trap_description: trap.trap_description,
      answer: answer.slice(0, 500),
      passed,
      forbidden_found: forbiddenFound,
      required_missing: requiredMissing,
      has_citations: response.citations.length > 0,
      notes: passed ? 'PASS — no forbidden claims detected' : `FAIL — forbidden claims: ${forbiddenFound.join(', ')}`,
    });
  }

  const passed = results.filter((r) => r.passed).length;
  return {
    generated_at: new Date().toISOString(),
    total: results.length,
    passed,
    failed: results.length - passed,
    pass_rate: results.length > 0 ? passed / results.length : 0,
    results,
  };
}

export interface TruthValidationResult {
  tool_result: unknown;
  model_claim: string;
  winner: 'tool' | 'agreement';
  conflict: boolean;
  description: string;
  /** @deprecated use conflict */
  conflict_detected: boolean;
  /** @deprecated use winner */
  tool_wins: boolean;
}

export function validateProtocolTruth(
  toolResult: Record<string, unknown>,
  modelAnswer: string,
): TruthValidationResult {
  let conflict = false;
  let description = 'No conflict — tool and model agree';

  const type = toolResult['type'] as string | undefined;

  if (type === 'validation_result' || ('valid' in toolResult && 'errors' in toolResult)) {
    const valid = toolResult['valid'] as boolean;
    const modelClaimsValid = /\bvalid\b|correct|no errors/i.test(modelAnswer) && !/invalid|error|fail|incorrect/i.test(modelAnswer);
    const modelClaimsInvalid = /\binvalid\b|\berror\b|\bfail\b|incorrect/i.test(modelAnswer);
    conflict = (valid && modelClaimsInvalid) || (!valid && modelClaimsValid);
    if (conflict) {
      description = `Tool says ${valid ? 'VALID' : 'INVALID'} but model answer suggests otherwise — tool wins`;
    }
  } else if (type === 'conformance_result') {
    const levelAchieved = toolResult['level_achieved'] as number;
    const levelPattern = /level\s+(\d)/gi;
    let modelHighestLevel = -1;
    let match;
    while ((match = levelPattern.exec(modelAnswer)) !== null) {
      const l = parseInt(match[1], 10);
      if (l > modelHighestLevel) modelHighestLevel = l;
    }
    conflict = modelHighestLevel > -1 && modelHighestLevel !== levelAchieved && modelHighestLevel > levelAchieved;
    if (conflict) {
      description = `Tool says level ${levelAchieved} but model claims level ${modelHighestLevel} — tool wins`;
    }
  }

  return {
    tool_result: toolResult,
    model_claim: modelAnswer.slice(0, 200),
    winner: conflict ? 'tool' : 'agreement',
    conflict,
    conflict_detected: conflict,
    tool_wins: true,
    description,
  };
}

export { TRAP_QUESTIONS };
