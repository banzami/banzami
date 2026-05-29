export interface CopilotInput {
  manifest?: Record<string, unknown>;
  capabilities?: string[];
  conformance_results?: Array<{ id: string; status: 'PASS' | 'FAIL' | 'SKIP'; level: number }>;
  declared_level?: number;
  target_level?: number;
}

export interface LevelRequirement {
  id: string;
  description: string;
  capability?: string;
  conformance_check?: string;
  manifest_field?: string;
  rfc?: string;
  adr?: string;
}

export interface LevelStatus {
  level: number;
  name: string;
  status: 'achieved' | 'partial' | 'blocked';
  missing: LevelRequirement[];
  achieved_count: number;
  total_count: number;
}

export interface CopilotResult {
  current_level: number;
  target_level: number;
  readiness_score: number;
  level_statuses: LevelStatus[];
  missing_for_target: LevelRequirement[];
  next_actions: string[];
  roadmap: Array<{ from_level: number; to_level: number; steps: string[]; estimated_effort: string }>;
  certification_ready: boolean;
  blocking_issues: string[];
}

const LEVEL_DEFINITIONS: Array<{ level: number; name: string; requirements: LevelRequirement[] }> = [
  {
    level: 0,
    name: 'Reference-compatible',
    requirements: [
      { id: 'L0-001', description: 'GET /health returns 200', conformance_check: 'health', rfc: 'RFC-0006' },
      { id: 'L0-002', description: 'POST /wallets creates wallet with minor-unit balance', conformance_check: 'wallets', rfc: 'RFC-0001', adr: 'ADR-001' },
      { id: 'L0-003', description: 'POST /transfers executes double-entry transfer', conformance_check: 'transfers', rfc: 'RFC-0002', adr: 'ADR-002' },
    ],
  },
  {
    level: 1,
    name: 'Protocol-compatible',
    requirements: [
      { id: 'L1-001', description: 'QR payment lifecycle (create, scan, pay, expire)', conformance_check: 'qr', rfc: 'RFC-0004', capability: 'supports_qr' },
      { id: 'L1-002', description: 'Payment requests (e-commerce flow)', conformance_check: 'payment-requests', rfc: 'RFC-0009', capability: 'supports_payment_requests' },
      { id: 'L1-003', description: 'Ledger invariants (INV-LEDGER-001 through INV-LEDGER-003)', conformance_check: 'ledger', rfc: 'RFC-0003', adr: 'ADR-002' },
      { id: 'L1-004', description: 'Settlement model (INV-STL-001 and INV-STL-002)', conformance_check: 'settlement', rfc: 'RFC-0005' },
    ],
  },
  {
    level: 2,
    name: 'Trace-compatible',
    requirements: [
      { id: 'L2-001', description: 'GET /v1/traces/:trace_id reconstructs causal flow', conformance_check: 'traces', rfc: 'RFC-0007', capability: 'supports_traces' },
      { id: 'L2-002', description: 'INV-TRACE-001: trace_id propagates to all flow entities', conformance_check: 'trace-propagation', rfc: 'RFC-0007' },
      { id: 'L2-003', description: 'Webhook event delivery with correlation_id', conformance_check: 'webhooks', capability: 'supports_webhooks' },
    ],
  },
  {
    level: 3,
    name: 'Federation-ready',
    requirements: [
      { id: 'L3-001', description: 'Valid /.well-known/banzami/operator.json manifest', conformance_check: 'manifest', rfc: 'RFC-0006', manifest_field: 'operator_id', capability: 'supports_manifest' },
      { id: 'L3-002', description: 'Federation discovery endpoint', conformance_check: 'federation-discovery', rfc: 'RFC-0008', capability: 'supports_federation' },
      { id: 'L3-003', description: 'Cross-operator event exchange', conformance_check: 'event-exchange', rfc: 'RFC-0008', capability: 'supports_cross_operator' },
    ],
  },
  {
    level: 4,
    name: 'Settlement-compatible',
    requirements: [
      { id: 'L4-001', description: 'Settlement batch lifecycle (open, close, settle)', conformance_check: 'settlement-lifecycle', rfc: 'RFC-0005' },
      { id: 'L4-002', description: 'INV-STL-001: net + fee = gross for all transfers', conformance_check: 'settlement-invariants', rfc: 'RFC-0005' },
    ],
  },
];

const ROADMAP_STEPS: Array<{ from_level: number; to_level: number; steps: string[]; estimated_effort: string }> = [
  {
    from_level: 0, to_level: 1,
    steps: [
      'Implement QR payment lifecycle (RFC-0004): POST /v1/qr, GET /v1/qr/:id, PATCH /v1/qr/:id/pay',
      'Add payment request support (RFC-0009): POST /v1/payment-requests',
      'Validate ledger double-entry (ADR-002): every transfer = 1 DEBIT + 1 CREDIT',
      'Implement settlement batches (RFC-0005): POST /v1/settlement-batches',
      'Run Level 1 conformance suite and fix all FAIL checks',
    ],
    estimated_effort: '2–4 weeks',
  },
  {
    from_level: 1, to_level: 2,
    steps: [
      'Implement GET /v1/traces/:trace_id endpoint',
      'Propagate trace_id to all flow entities (RFC-0007, INV-TRACE-001)',
      'Add webhook delivery with correlation_id and retry logic',
      'Run Level 2 conformance suite and verify INV-TRACE-001 passes',
    ],
    estimated_effort: '1–2 weeks',
  },
  {
    from_level: 2, to_level: 3,
    steps: [
      'Publish /.well-known/banzami/operator.json with all required fields (RFC-0006)',
      'Implement federation discovery endpoint',
      'Add cross-operator event exchange capability',
      'Submit manifest for Banzami network review',
    ],
    estimated_effort: '3–6 weeks',
  },
  {
    from_level: 3, to_level: 4,
    steps: [
      'Implement full settlement batch lifecycle (RFC-0005)',
      'Enforce INV-STL-001 in all transfer logic: net + fee = gross',
      'Add settlement invariant validation to your CI pipeline',
      'Run Level 4 conformance suite — all settlement checks must PASS',
    ],
    estimated_effort: '2–4 weeks',
  },
];

export function analyzeCertificationReadiness(input: CopilotInput): CopilotResult {
  const passedChecks = new Set<string>(
    (input.conformance_results ?? [])
      .filter(r => r.status === 'PASS')
      .map(r => r.id.toLowerCase().replace('l', 'l').replace('-', '-')),
  );

  const capabilities = new Set<string>(input.capabilities ?? []);
  const manifest = input.manifest ?? {};

  function requirementMet(req: LevelRequirement): boolean {
    if (req.conformance_check) {
      const checkKey = req.conformance_check.toLowerCase();
      if ([...passedChecks].some(p => p.includes(checkKey))) return true;
    }
    if (req.capability && !capabilities.has(req.capability)) return false;
    if (req.manifest_field && !manifest[req.manifest_field]) return false;
    if (req.conformance_check && passedChecks.size === 0 && !input.conformance_results) {
      // No conformance data — cannot confirm
      return false;
    }
    return req.conformance_check ? false : true;
  }

  const levelStatuses: LevelStatus[] = LEVEL_DEFINITIONS.map(def => {
    const missing = def.requirements.filter(r => !requirementMet(r));
    const achieved = def.requirements.length - missing.length;
    const status: LevelStatus['status'] =
      missing.length === 0 ? 'achieved' :
      achieved > 0 ? 'partial' : 'blocked';
    return {
      level: def.level,
      name: def.name,
      status,
      missing,
      achieved_count: achieved,
      total_count: def.requirements.length,
    };
  });

  // Current level: highest where ALL requirements met
  let currentLevel = -1;
  for (const ls of levelStatuses) {
    if (ls.status === 'achieved') currentLevel = ls.level;
    else break;
  }

  const targetLevel = input.target_level ?? Math.min(currentLevel + 1, 4);

  // Missing for target
  const missingForTarget = levelStatuses
    .filter(ls => ls.level <= targetLevel && ls.status !== 'achieved')
    .flatMap(ls => ls.missing);

  // Blocking issues
  const blockingIssues: string[] = [];
  if (manifest['environment'] === 'sandbox' && manifest['production_allowed'] === true) {
    blockingIssues.push('SANDBOX SAFETY VIOLATION: production_allowed must be false in sandbox environment (RFC-006)');
  }
  if (manifest['environment'] === 'production' && manifest['simulated'] === true) {
    blockingIssues.push('PRODUCTION SAFETY VIOLATION: simulated must be false in production environment (RFC-006)');
  }

  // Readiness score
  const totalReqs = levelStatuses
    .filter(ls => ls.level <= targetLevel)
    .reduce((s, ls) => s + ls.total_count, 0);
  const metReqs = levelStatuses
    .filter(ls => ls.level <= targetLevel)
    .reduce((s, ls) => s + ls.achieved_count, 0);
  const readinessScore = totalReqs > 0
    ? Math.round((metReqs / totalReqs) * 100) - (blockingIssues.length * 15)
    : 0;

  // Next actions
  const nextActions: string[] = [
    ...blockingIssues.map(i => `[CRITICAL] Fix: ${i}`),
    ...missingForTarget.slice(0, 5).map(r => `Implement ${r.id}: ${r.description}${r.rfc ? ` (${r.rfc})` : ''}`),
  ];
  if (missingForTarget.length === 0 && blockingIssues.length === 0) {
    nextActions.push('Submit operator manifest to Banzami network for Level 3+ review');
    nextActions.push('Run full conformance suite against your production endpoint');
  }

  // Roadmap
  const roadmap = ROADMAP_STEPS.filter(r => r.from_level >= Math.max(0, currentLevel));

  return {
    current_level: currentLevel,
    target_level: targetLevel,
    readiness_score: Math.max(0, Math.min(100, readinessScore)),
    level_statuses: levelStatuses,
    missing_for_target: missingForTarget,
    next_actions: nextActions,
    roadmap,
    certification_ready: missingForTarget.length === 0 && blockingIssues.length === 0,
    blocking_issues: blockingIssues,
  };
}
