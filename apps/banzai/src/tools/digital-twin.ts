import { analyzeCertificationReadiness, type CopilotResult } from './certification-copilot.js';
import { analyzeFederation, type FederationAnalysisResult } from './federation-intelligence.js';
import { getOrCreate, type OperatorMemory } from '../memory/operator-memory.js';

export interface DigitalTwinInput {
  operator_id: string;
  manifest: Record<string, unknown>;
  capabilities: string[];
  target_level?: number;
  partner_manifests?: Array<{ operator_id: string; manifest: Record<string, unknown>; capabilities: string[] }>;
}

export interface InvariantImpact {
  invariant_id: string;
  description: string;
  relevant: boolean;
  reason: string;
}

export interface RFCReference {
  rfc_id: string;
  title: string;
  relevance: string;
}

export interface DigitalTwin {
  operator_id: string;
  snapshot_at: string;
  manifest: Record<string, unknown>;
  capabilities: string[];
  certification: CopilotResult;
  federation_profiles: FederationAnalysisResult[];
  memory: OperatorMemory;
  relevant_invariants: InvariantImpact[];
  relevant_rfcs: RFCReference[];
  recommendations: string[];
  capability_gap_summary: string;
  readiness_trajectory: string;
}

const INVARIANTS: InvariantImpact[] = [
  { invariant_id: 'INV-LEDGER-001', description: 'Conservation: sum of all balances is constant', relevant: false, reason: '' },
  { invariant_id: 'INV-LEDGER-002', description: 'Double-entry: every transfer has 1 DEBIT + 1 CREDIT', relevant: false, reason: '' },
  { invariant_id: 'INV-LEDGER-003', description: 'Non-negativity: no balance below zero for settlement', relevant: false, reason: '' },
  { invariant_id: 'INV-TRACE-001', description: 'trace_id propagates to all entities in a flow', relevant: false, reason: '' },
  { invariant_id: 'INV-STL-001', description: 'net + fee = gross for all settlement transfers', relevant: false, reason: '' },
  { invariant_id: 'INV-STL-002', description: 'Settlement batches close before next open', relevant: false, reason: '' },
];

const RFCS: RFCReference[] = [
  { rfc_id: 'RFC-0001', title: 'Wallet Model', relevance: 'wallet' },
  { rfc_id: 'RFC-0002', title: 'Transfer Model', relevance: 'transfer' },
  { rfc_id: 'RFC-0003', title: 'Ledger Invariants', relevance: 'ledger' },
  { rfc_id: 'RFC-0004', title: 'QR Payment Protocol', relevance: 'qr' },
  { rfc_id: 'RFC-0005', title: 'Settlement Model', relevance: 'settlement' },
  { rfc_id: 'RFC-0006', title: 'Operator Manifest', relevance: 'manifest' },
  { rfc_id: 'RFC-0007', title: 'Trace Model', relevance: 'trace' },
  { rfc_id: 'RFC-0008', title: 'Federation Protocol', relevance: 'federation' },
  { rfc_id: 'RFC-0009', title: 'Payment Request Model', relevance: 'payment' },
];

export function buildDigitalTwin(input: DigitalTwinInput): DigitalTwin {
  const targetLevel = input.target_level ?? 4;

  const certification = analyzeCertificationReadiness({
    manifest: input.manifest,
    capabilities: input.capabilities,
    target_level: targetLevel,
  });

  const federationProfiles: FederationAnalysisResult[] = (input.partner_manifests ?? []).map(p =>
    analyzeFederation(
      { operator_id: input.operator_id, manifest: input.manifest, capabilities: input.capabilities },
      { operator_id: p.operator_id, manifest: p.manifest, capabilities: p.capabilities },
    )
  );

  const memory = getOrCreate(input.operator_id);
  const capSet = new Set(input.capabilities);

  // Relevant invariants based on capabilities + level
  const relevantInvs = INVARIANTS.map(inv => {
    let relevant = false;
    let reason = '';
    if (inv.invariant_id.startsWith('INV-LEDGER') && (capSet.has('supports_wallets') || capSet.has('supports_transfers'))) {
      relevant = true; reason = 'Operator handles transfers and wallets.';
    }
    if (inv.invariant_id === 'INV-TRACE-001' && capSet.has('supports_traces')) {
      relevant = true; reason = 'Operator supports trace propagation.';
    }
    if (inv.invariant_id.startsWith('INV-STL') && certification.current_level >= 3) {
      relevant = true; reason = 'Operator is Level 3+ and approaching settlement compatibility.';
    }
    return { ...inv, relevant, reason };
  }).filter(inv => inv.relevant);

  // Relevant RFCs based on capabilities + missing requirements
  const missingRFCs = new Set(certification.missing_for_target.map(r => r.rfc).filter(Boolean));
  const relevantRFCs = RFCS.filter(rfc => {
    const cap = input.capabilities.join(' ').toLowerCase();
    return cap.includes(rfc.relevance) || missingRFCs.has(rfc.rfc_id);
  });

  // Recommendations
  const recs: string[] = [];
  if (certification.current_level < 0) {
    recs.push('Run conformance suite (Level 0) to establish baseline: health, wallets, transfers.');
  }
  if (certification.blocking_issues.length > 0) {
    recs.push(`Resolve ${certification.blocking_issues.length} blocking issue(s) before proceeding.`);
  }
  if (certification.missing_for_target.length > 0) {
    recs.push(`Implement ${certification.missing_for_target.length} requirement(s) to reach Level ${targetLevel}.`);
  }
  if (!capSet.has('supports_webhooks') && certification.current_level >= 1) {
    recs.push('Add webhook support (supports_webhooks) — required for Level 2 Trace-compatible.');
  }
  if (!capSet.has('supports_federation') && certification.current_level >= 2) {
    recs.push('Add federation support to unlock Level 3 and cross-operator capabilities.');
  }
  if (federationProfiles.some(fp => !fp.federation_ready)) {
    recs.push('One or more federation partners are not yet ready. Review federation compatibility reports.');
  }
  if (memory.assessments.length > 1) {
    const prev = memory.assessments.at(-2)!;
    const curr = memory.assessments.at(-1)!;
    const delta = curr.readiness_score - prev.readiness_score;
    if (delta < 0) recs.push(`Readiness declined by ${Math.abs(delta)} points since last assessment — review recent changes.`);
  }
  if (recs.length === 0) {
    recs.push('All requirements met. Submit manifest to Banzami network for formal certification.');
  }

  // Trajectory
  let trajectory = 'Steady';
  if (memory.assessments.length >= 2) {
    const scores = memory.assessments.slice(-3).map(a => a.readiness_score);
    const trend = scores.at(-1)! - scores[0];
    if (trend > 10) trajectory = 'Improving rapidly';
    else if (trend > 0) trajectory = 'Improving';
    else if (trend < -10) trajectory = 'Declining';
    else if (trend < 0) trajectory = 'Slight decline';
  } else if (memory.assessments.length === 0) {
    trajectory = 'No history yet';
  }

  const gapCount = certification.missing_for_target.length;
  const gapSummary = gapCount === 0
    ? 'All requirements for the target level are satisfied.'
    : `${gapCount} requirement(s) remain before reaching Level ${targetLevel}: ${certification.missing_for_target.slice(0, 3).map(r => r.id).join(', ')}${gapCount > 3 ? '…' : ''}.`;

  return {
    operator_id: input.operator_id,
    snapshot_at: new Date().toISOString(),
    manifest: input.manifest,
    capabilities: input.capabilities,
    certification,
    federation_profiles: federationProfiles,
    memory,
    relevant_invariants: relevantInvs,
    relevant_rfcs: relevantRFCs,
    recommendations: recs,
    capability_gap_summary: gapSummary,
    readiness_trajectory: trajectory,
  };
}
