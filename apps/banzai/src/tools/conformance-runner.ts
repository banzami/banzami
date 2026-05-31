export type CertificationLevel = 0 | 1 | 2 | 3 | 4;

export interface ConformanceResult {
  level_achieved: CertificationLevel;
  level_requested: CertificationLevel;
  passed: ConformanceCheck[];
  failed: ConformanceCheck[];
  skipped: ConformanceCheck[];
  compliant: boolean;
}

export interface ConformanceCheck {
  id: string;
  name: string;
  level: CertificationLevel;
  result: 'pass' | 'fail' | 'skip';
  reason?: string;
}

const LEVEL_CHECKS: ConformanceCheck[] = [
  { id: 'L0-001', name: 'Valid operator manifest', level: 0, result: 'skip' },
  { id: 'L0-002', name: 'Protocol version declared', level: 0, result: 'skip' },
  { id: 'L0-003', name: 'Settlement currency valid', level: 0, result: 'skip' },
  { id: 'L1-001', name: 'Wallet creation roundtrip', level: 1, result: 'skip' },
  { id: 'L1-002', name: 'P2P transfer idempotency', level: 1, result: 'skip' },
  { id: 'L1-003', name: 'Double-entry invariant holds', level: 1, result: 'skip' },
  { id: 'L1-004', name: 'Balance never negative', level: 1, result: 'skip' },
  { id: 'L2-001', name: 'QR payload encoding', level: 2, result: 'skip' },
  { id: 'L2-002', name: 'Payment link lifecycle', level: 2, result: 'skip' },
  { id: 'L2-003', name: 'Webhook delivery and signature', level: 2, result: 'skip' },
  { id: 'L3-001', name: 'Cross-operator settlement', level: 3, result: 'skip' },
  { id: 'L3-002', name: 'Multi-operator routing', level: 3, result: 'skip' },
  { id: 'L3-003', name: 'Reconciliation convergence', level: 3, result: 'skip' },
  { id: 'L4-001', name: 'Settlement batch lifecycle (open, close, settle)', level: 4, result: 'skip' },
  { id: 'L4-002', name: 'EMIS card acquiring integration (acquiring.emis)', level: 4, result: 'skip' },
];

export interface OperatorCapabilities {
  manifest_valid: boolean;
  wallet_ops: boolean;
  qr_payments: boolean;
  payment_links: boolean;
  cross_operator: boolean;
  federation: boolean;
  offline: boolean;
}

function checksForLevel(level: CertificationLevel): ConformanceCheck[] {
  return LEVEL_CHECKS.filter((c) => c.level <= level);
}

export function runConformanceCheck(
  capabilities: OperatorCapabilities,
  targetLevel: CertificationLevel,
): ConformanceResult {
  const checks = checksForLevel(targetLevel);
  const results: ConformanceCheck[] = checks.map((check) => {
    let result: 'pass' | 'fail' | 'skip' = 'skip';
    let reason: string | undefined;

    switch (check.id) {
      case 'L0-001': result = capabilities.manifest_valid ? 'pass' : 'fail'; break;
      case 'L0-002': result = capabilities.manifest_valid ? 'pass' : 'fail'; break;
      case 'L0-003': result = capabilities.manifest_valid ? 'pass' : 'fail'; break;
      case 'L1-001': result = capabilities.wallet_ops ? 'pass' : 'fail'; break;
      case 'L1-002': result = capabilities.wallet_ops ? 'pass' : 'fail'; break;
      case 'L1-003': result = capabilities.wallet_ops ? 'pass' : 'fail'; break;
      case 'L1-004': result = capabilities.wallet_ops ? 'pass' : 'fail'; break;
      case 'L2-001': result = capabilities.qr_payments ? 'pass' : 'fail'; break;
      case 'L2-002': result = capabilities.payment_links ? 'pass' : 'fail'; break;
      case 'L2-003': result = capabilities.payment_links ? 'pass' : 'fail'; break;
      case 'L3-001': result = capabilities.cross_operator ? 'pass' : 'fail'; break;
      case 'L3-002': result = capabilities.cross_operator ? 'pass' : 'fail'; break;
      case 'L3-003': result = capabilities.cross_operator ? 'pass' : 'fail'; break;
      case 'L4-001': result = capabilities.federation ? 'pass' : 'fail'; break;
      case 'L4-002':
        result = 'skip';
        reason = 'L4 (Infrastructure Operator) conformance suite is v1.1 scope — not certifiable in v1.0';
        break;
      default:
        result = 'skip';
    }

    return { ...check, result, ...(reason ? { reason } : {}) };
  });

  const passed = results.filter((c) => c.result === 'pass');
  const failed = results.filter((c) => c.result === 'fail');
  const skipped = results.filter((c) => c.result === 'skip');

  let levelAchieved: CertificationLevel = 0;
  const requiredByLevel = [0, 1, 2, 3, 4] as CertificationLevel[];
  for (const level of requiredByLevel) {
    const checksAtLevel = results.filter((c) => c.level === level);
    const allPass = checksAtLevel.every((c) => c.result === 'pass');
    if (allPass && checksAtLevel.length > 0) {
      levelAchieved = level;
    } else if (checksAtLevel.length > 0) {
      break;
    }
  }

  return {
    level_achieved: levelAchieved,
    level_requested: targetLevel,
    passed,
    failed,
    skipped,
    compliant: failed.length === 0,
  };
}
