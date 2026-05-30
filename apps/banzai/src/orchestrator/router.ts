import type { TaskType } from './providers/provider.js';

interface RoutingDecision {
  task_type: TaskType;
  reason: string;
  suggested_tools: string[];
}

const CODE_PATTERNS = [
  /\b(sdk|typescript|dart|php|go|npm|package|import|install|example|snippet|code|implement|integrate)\b/i,
  /`[^`]+`/,
  /\.(ts|js|dart|php|go)\b/,
];

const TRACE_PATTERNS = [
  /\b(trace|trace_id|causation|correlation|event|audit|log|span)\b/i,
  /[a-f0-9]{32}/,
];

const VALIDATION_PATTERNS = [
  /\b(manifest|schema|validate|invalid|malformed|json|yaml|openapi)\b/i,
  /MON-\d{3}/,
];

const CERTIFICATION_PATTERNS = [
  /\b(certif|operator level|level [0-4]|conformance|compliance|test suite|sdk-cert)\b/i,
];

const REASONING_PATTERNS = [
  /\b(why|reason|explain|how does|what is the difference|architecture|design|tradeoff|invariant|double.?entry|settlement|reconcil)\b/i,
  /RFC-\d{4}/,
  /ADR-\d{3}/,
  /INV-\d{3}/,
];

function matchesAny(text: string, patterns: RegExp[]): boolean {
  return patterns.some((p) => p.test(text));
}

export function classifyTask(question: string): RoutingDecision {
  if (matchesAny(question, TRACE_PATTERNS)) {
    return {
      task_type: 'trace',
      reason: 'Question contains trace ID or audit log keywords',
      suggested_tools: ['trace-explainer'],
    };
  }

  if (matchesAny(question, VALIDATION_PATTERNS)) {
    return {
      task_type: 'validation',
      reason: 'Question involves schema or manifest validation',
      suggested_tools: ['manifest-validator'],
    };
  }

  if (matchesAny(question, CERTIFICATION_PATTERNS)) {
    return {
      task_type: 'certification',
      reason: 'Question involves operator certification or conformance',
      suggested_tools: ['conformance-runner'],
    };
  }

  if (matchesAny(question, CODE_PATTERNS)) {
    return {
      task_type: 'code',
      reason: 'Question involves SDK integration or code examples',
      suggested_tools: [],
    };
  }

  if (matchesAny(question, REASONING_PATTERNS)) {
    return {
      task_type: 'reasoning',
      reason: 'Question requires architectural reasoning or protocol analysis',
      suggested_tools: [],
    };
  }

  return {
    task_type: 'docs',
    reason: 'General protocol documentation question',
    suggested_tools: [],
  };
}
