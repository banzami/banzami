import { analyzeCertificationReadiness, type CopilotResult, type LevelRequirement } from './certification-copilot.js';

export interface SimulationChange {
  type: 'add_capability' | 'remove_capability' | 'update_manifest';
  capability?: string;
  manifest_patch?: Record<string, unknown>;
}

export interface SimulatorInput {
  manifest: Record<string, unknown>;
  capabilities: string[];
  target_level: number;
  proposed_changes: SimulationChange[];
}

export interface CertificationImpact {
  level_unlocked: boolean;
  new_level: number;
  requirements_satisfied: string[];
  requirements_still_missing: string[];
}

export interface FederationImpact {
  eligible_before: boolean;
  eligible_after: boolean;
  newly_eligible: boolean;
}

export interface SimulatorResult {
  before: CopilotResult;
  after: CopilotResult;
  readiness_delta: number;
  applied_changes: string[];
  new_capabilities: string[];
  removed_capabilities: string[];
  certification_impact: CertificationImpact;
  federation_impact: FederationImpact;
  estimated_effort: 'none' | 'minimal' | 'low' | 'medium' | 'high' | 'extensive';
  summary: string;
}

function estimateEffort(missingCount: number): SimulatorResult['estimated_effort'] {
  if (missingCount === 0) return 'none';
  if (missingCount === 1) return 'minimal';
  if (missingCount <= 3) return 'low';
  if (missingCount <= 5) return 'medium';
  if (missingCount <= 8) return 'high';
  return 'extensive';
}

export function runSimulation(input: SimulatorInput): SimulatorResult {
  const before = analyzeCertificationReadiness({
    manifest: input.manifest,
    capabilities: input.capabilities,
    target_level: input.target_level,
  });

  let newCapabilities = [...input.capabilities];
  let newManifest = { ...input.manifest };
  const appliedChanges: string[] = [];

  for (const change of input.proposed_changes) {
    if (change.type === 'add_capability' && change.capability) {
      if (!newCapabilities.includes(change.capability)) {
        newCapabilities.push(change.capability);
        appliedChanges.push(`+ Add capability: ${change.capability}`);
      }
    } else if (change.type === 'remove_capability' && change.capability) {
      newCapabilities = newCapabilities.filter(c => c !== change.capability);
      appliedChanges.push(`- Remove capability: ${change.capability}`);
    } else if (change.type === 'update_manifest' && change.manifest_patch) {
      newManifest = { ...newManifest, ...change.manifest_patch };
      appliedChanges.push(`~ Update manifest: ${Object.keys(change.manifest_patch).join(', ')}`);
    }
  }

  const after = analyzeCertificationReadiness({
    manifest: newManifest,
    capabilities: newCapabilities,
    target_level: input.target_level,
  });

  const addedCaps = newCapabilities.filter(c => !input.capabilities.includes(c));
  const removedCaps = input.capabilities.filter(c => !newCapabilities.includes(c));

  const beforeMissingIds = new Set(before.missing_for_target.map((r: LevelRequirement) => r.id));
  const afterMissingIds = new Set(after.missing_for_target.map((r: LevelRequirement) => r.id));
  const satisfied = [...beforeMissingIds].filter(id => !afterMissingIds.has(id));
  const stillMissing = [...afterMissingIds];

  const delta = after.readiness_score - before.readiness_score;
  const levelUnlocked = after.current_level > before.current_level;

  const fedEligibleBefore = before.level_statuses.find(ls => ls.level === 3)?.status === 'achieved';
  const fedEligibleAfter = after.level_statuses.find(ls => ls.level === 3)?.status === 'achieved';

  const parts: string[] = [];
  if (delta > 0) parts.push(`Readiness improves ${delta} points (${before.readiness_score}% → ${after.readiness_score}%).`);
  else if (delta < 0) parts.push(`Readiness drops ${Math.abs(delta)} points (${before.readiness_score}% → ${after.readiness_score}%).`);
  else parts.push(`Readiness unchanged at ${before.readiness_score}%.`);
  if (levelUnlocked) parts.push(`Level ${after.current_level} certification becomes achievable.`);
  if (!fedEligibleBefore && fedEligibleAfter) parts.push('Federation eligibility unlocked.');
  if (satisfied.length > 0) parts.push(`${satisfied.length} requirement(s) satisfied: ${satisfied.join(', ')}.`);

  return {
    before,
    after,
    readiness_delta: delta,
    applied_changes: appliedChanges,
    new_capabilities: addedCaps,
    removed_capabilities: removedCaps,
    certification_impact: {
      level_unlocked: levelUnlocked,
      new_level: after.current_level,
      requirements_satisfied: satisfied,
      requirements_still_missing: stillMissing,
    },
    federation_impact: {
      eligible_before: fedEligibleBefore ?? false,
      eligible_after: fedEligibleAfter ?? false,
      newly_eligible: !(fedEligibleBefore ?? false) && (fedEligibleAfter ?? false),
    },
    estimated_effort: estimateEffort(after.missing_for_target.length),
    summary: parts.join(' '),
  };
}
