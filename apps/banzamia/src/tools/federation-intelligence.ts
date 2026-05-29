import { analyzeCertificationReadiness } from './certification-copilot.js';

export interface OperatorProfile {
  operator_id: string;
  manifest: Record<string, unknown>;
  capabilities: string[];
}

export interface CompatibilityConflict {
  field: string;
  operator_a_value: unknown;
  operator_b_value: unknown;
  description: string;
}

export interface FederationAnalysisResult {
  operator_a_id: string;
  operator_b_id: string;
  compatibility_score: number;
  federation_ready: boolean;
  operator_a_level: number;
  operator_b_level: number;
  shared_capabilities: string[];
  missing_in_a: string[];
  missing_in_b: string[];
  conflicts: CompatibilityConflict[];
  blocking_issues: string[];
  suggested_next_actions: string[];
  analysis_notes: string[];
  estimated_effort_a: string;
  estimated_effort_b: string;
}

// Capabilities required for federation
const FEDERATION_REQUIRED_CAPS = [
  'supports_wallets',
  'supports_transfers',
  'supports_manifest',
  'supports_federation',
  'supports_cross_operator',
];

const PROTOCOL_VERSIONS_COMPATIBLE: Record<string, string[]> = {
  '1.0.0': ['1.0.0', '1.1.0'],
  '1.1.0': ['1.0.0', '1.1.0'],
};

function getCaps(profile: OperatorProfile): Set<string> {
  const capsList = profile.manifest['capabilities'] as Record<string, boolean> | undefined;
  const combined = new Set<string>(profile.capabilities);
  if (capsList) {
    for (const [k, v] of Object.entries(capsList)) {
      if (v) combined.add(k);
    }
  }
  return combined;
}

export function analyzeFederation(a: OperatorProfile, b: OperatorProfile): FederationAnalysisResult {
  const certA = analyzeCertificationReadiness({ manifest: a.manifest, capabilities: a.capabilities, target_level: 3 });
  const certB = analyzeCertificationReadiness({ manifest: b.manifest, capabilities: b.capabilities, target_level: 3 });

  const capsA = getCaps(a);
  const capsB = getCaps(b);

  const shared = [...capsA].filter(c => capsB.has(c));
  const missingInA = FEDERATION_REQUIRED_CAPS.filter(c => !capsA.has(c));
  const missingInB = FEDERATION_REQUIRED_CAPS.filter(c => !capsB.has(c));

  const conflicts: CompatibilityConflict[] = [];
  const blocking: string[] = [];

  // Protocol version compatibility
  const vA = (a.manifest['protocol_version'] as string | undefined) ?? '';
  const vB = (b.manifest['protocol_version'] as string | undefined) ?? '';
  if (vA && vB && !(PROTOCOL_VERSIONS_COMPATIBLE[vA] ?? []).includes(vB)) {
    conflicts.push({
      field: 'protocol_version',
      operator_a_value: vA,
      operator_b_value: vB,
      description: `Protocol versions ${vA} and ${vB} are not mutually compatible.`,
    });
    blocking.push(`Incompatible protocol versions: ${vA} vs ${vB}. Both operators must run a mutually compatible version.`);
  }

  // Environment conflicts (can't federate sandbox with production)
  const envA = (a.manifest['environment'] as string | undefined) ?? '';
  const envB = (b.manifest['environment'] as string | undefined) ?? '';
  if (envA && envB && envA !== envB) {
    conflicts.push({
      field: 'environment',
      operator_a_value: envA,
      operator_b_value: envB,
      description: 'Federation requires both operators to be in the same environment.',
    });
    blocking.push(`Environment mismatch: ${a.operator_id} is ${envA}, ${b.operator_id} is ${envB}. Federation requires same environment.`);
  }

  // Certification level checks (both must be L3+)
  if (certA.current_level < 3) {
    blocking.push(`${a.operator_id} has not reached Level 3 (Federation-ready). Current level: ${certA.current_level < 0 ? 'none' : certA.current_level}.`);
  }
  if (certB.current_level < 3) {
    blocking.push(`${b.operator_id} has not reached Level 3 (Federation-ready). Current level: ${certB.current_level < 0 ? 'none' : certB.current_level}.`);
  }

  // Missing federation capabilities
  if (missingInA.length > 0) {
    blocking.push(`${a.operator_id} missing federation capabilities: ${missingInA.join(', ')}.`);
  }
  if (missingInB.length > 0) {
    blocking.push(`${b.operator_id} missing federation capabilities: ${missingInB.join(', ')}.`);
  }

  const federationReady = blocking.length === 0;

  // Compatibility score (0–100)
  let score = 100;
  score -= conflicts.length * 20;
  score -= missingInA.length * 8;
  score -= missingInB.length * 8;
  if (certA.current_level < 3) score -= 25;
  if (certB.current_level < 3) score -= 25;
  score = Math.max(0, Math.min(100, score));

  // Next actions
  const nextActions: string[] = [...blocking.map(b => `[BLOCKER] ${b}`)];
  if (missingInA.length > 0) nextActions.push(`${a.operator_id}: add missing capabilities — ${missingInA.join(', ')}`);
  if (missingInB.length > 0) nextActions.push(`${b.operator_id}: add missing capabilities — ${missingInB.join(', ')}`);
  if (federationReady) {
    nextActions.push('Both operators are federation-eligible. Initiate federation handshake via RFC-0008 discovery endpoint.');
    nextActions.push('Exchange operator manifests and verify cross-operator event delivery.');
  }

  // Effort estimates
  const effortA = missingInA.length === 0 && certA.current_level >= 3
    ? 'None — already federation-ready'
    : missingInA.length <= 2 ? '1–2 weeks' : '3–6 weeks';
  const effortB = missingInB.length === 0 && certB.current_level >= 3
    ? 'None — already federation-ready'
    : missingInB.length <= 2 ? '1–2 weeks' : '3–6 weeks';

  const notes: string[] = [
    `Shared capabilities (${shared.length}): ${shared.slice(0, 5).join(', ')}${shared.length > 5 ? '…' : ''}.`,
    `${a.operator_id} readiness for L3: ${certA.readiness_score}%. ${b.operator_id} readiness: ${certB.readiness_score}%.`,
  ];
  if (conflicts.length === 0) notes.push('No protocol conflicts detected.');

  return {
    operator_a_id: a.operator_id,
    operator_b_id: b.operator_id,
    compatibility_score: score,
    federation_ready: federationReady,
    operator_a_level: certA.current_level,
    operator_b_level: certB.current_level,
    shared_capabilities: shared,
    missing_in_a: missingInA,
    missing_in_b: missingInB,
    conflicts,
    blocking_issues: blocking,
    suggested_next_actions: nextActions.slice(0, 6),
    analysis_notes: notes,
    estimated_effort_a: effortA,
    estimated_effort_b: effortB,
  };
}
