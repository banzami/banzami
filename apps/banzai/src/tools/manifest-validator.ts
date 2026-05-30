export interface ManifestValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
  manifest_type: string | null;
}

export interface ValidationError {
  path: string;
  message: string;
  code: string;
}

export interface ValidationWarning {
  path: string;
  message: string;
}

const REQUIRED_OPERATOR_FIELDS = [
  'operator_id',
  'protocol_version',
  'capabilities',
  'settlement_currency',
];

const REQUIRED_QR_FIELDS = [
  'version',
  'operator_id',
  'amount',
  'currency',
  'reference',
];

const REQUIRED_PAYMENT_LINK_FIELDS = [
  'link_id',
  'operator_id',
  'amount',
  'currency',
  'description',
];

function detectManifestType(data: Record<string, unknown>): string | null {
  if ('link_id' in data) return 'payment_link';
  if ('reference' in data && 'amount' in data && 'version' in data) return 'qr_payload';
  if ('operator_id' in data || 'capabilities' in data || 'settlement_currency' in data) return 'operator';
  return null;
}

function validateRequired(
  data: Record<string, unknown>,
  required: string[],
): ValidationError[] {
  return required
    .filter((field) => !(field in data) || data[field] === null || data[field] === undefined)
    .map((field) => ({
      path: field,
      message: `Required field '${field}' is missing or null`,
      code: 'MISSING_REQUIRED_FIELD',
    }));
}

function validateProtocolVersion(version: unknown): ValidationError | null {
  if (typeof version !== 'string') {
    return { path: 'protocol_version', message: 'Must be a string', code: 'INVALID_TYPE' };
  }
  if (!/^\d+\.\d+(\.\d+)?$/.test(version)) {
    return {
      path: 'protocol_version',
      message: `Invalid protocol version format '${version}' — expected semver like 1.0 or 1.0.0`,
      code: 'INVALID_PROTOCOL_VERSION',
    };
  }
  return null;
}

function validateCurrency(value: unknown, path: string): ValidationError | null {
  if (typeof value !== 'string' || !/^[A-Z]{3}$/.test(value)) {
    return {
      path,
      message: `'${path}' must be a 3-letter ISO 4217 currency code`,
      code: 'INVALID_CURRENCY',
    };
  }
  return null;
}

function validateAmount(value: unknown, path: string): ValidationError | null {
  if (typeof value !== 'number' || value < 0 || !Number.isFinite(value)) {
    return {
      path,
      message: `'${path}' must be a non-negative finite number`,
      code: 'INVALID_AMOUNT',
    };
  }
  return null;
}

export function validateManifest(raw: unknown): ManifestValidationResult {
  if (typeof raw !== 'object' || raw === null || Array.isArray(raw)) {
    return {
      valid: false,
      errors: [{ path: '$', message: 'Manifest must be a JSON object', code: 'INVALID_TYPE' }],
      warnings: [],
      manifest_type: null,
    };
  }

  const data = raw as Record<string, unknown>;
  const manifestType = detectManifestType(data);
  const errors: ValidationError[] = [];
  const warnings: ValidationWarning[] = [];

  if (manifestType === 'operator') {
    errors.push(...validateRequired(data, REQUIRED_OPERATOR_FIELDS));
    const vErr = validateProtocolVersion(data.protocol_version);
    if (vErr) errors.push(vErr);
    const cErr = validateCurrency(data.settlement_currency, 'settlement_currency');
    if (cErr) errors.push(cErr);

    if (!Array.isArray(data.capabilities) || data.capabilities.length === 0) {
      errors.push({
        path: 'capabilities',
        message: 'capabilities must be a non-empty array',
        code: 'INVALID_CAPABILITIES',
      });
    }
  } else if (manifestType === 'qr_payload') {
    errors.push(...validateRequired(data, REQUIRED_QR_FIELDS));
    const aErr = validateAmount(data.amount, 'amount');
    if (aErr) errors.push(aErr);
    const cErr = validateCurrency(data.currency, 'currency');
    if (cErr) errors.push(cErr);
  } else if (manifestType === 'payment_link') {
    errors.push(...validateRequired(data, REQUIRED_PAYMENT_LINK_FIELDS));
    const aErr = validateAmount(data.amount, 'amount');
    if (aErr) errors.push(aErr);
    const cErr = validateCurrency(data.currency, 'currency');
    if (cErr) errors.push(cErr);
  } else {
    warnings.push({
      path: '$',
      message: 'Unknown manifest type — could not determine schema for full validation',
    });
  }

  return { valid: errors.length === 0, errors, warnings, manifest_type: manifestType };
}
