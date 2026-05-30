export interface TimelineEvent {
  date: string;
  type: 'assessment' | 'certification' | 'federation' | 'conformance' | 'research' | 'manifest_change';
  title: string;
  detail?: string;
  level?: number;
  score?: number;
}

export interface AssessmentSnapshot {
  timestamp: string;
  target_level: number;
  readiness_score: number;
  current_level: number;
  missing_count: number;
  capabilities: string[];
}

export interface OperatorMemory {
  operator_id: string;
  created_at: string;
  updated_at: string;
  current_manifest: Record<string, unknown>;
  current_capabilities: string[];
  current_level: number;
  assessments: AssessmentSnapshot[];
  timeline: TimelineEvent[];
  research_history: Array<{ question: string; timestamp: string }>;
  notes: string[];
}

const store = new Map<string, OperatorMemory>();

export function getOrCreate(operatorId: string): OperatorMemory {
  if (!store.has(operatorId)) {
    const now = new Date().toISOString();
    store.set(operatorId, {
      operator_id: operatorId,
      created_at: now,
      updated_at: now,
      current_manifest: {},
      current_capabilities: [],
      current_level: -1,
      assessments: [],
      timeline: [],
      research_history: [],
      notes: [],
    });
  }
  return store.get(operatorId)!;
}

export function recordAssessment(
  operatorId: string,
  snapshot: Omit<AssessmentSnapshot, 'timestamp'>,
  manifest: Record<string, unknown>,
  capabilities: string[],
): void {
  const mem = getOrCreate(operatorId);
  const now = new Date().toISOString();
  const ts: AssessmentSnapshot = { ...snapshot, timestamp: now };
  mem.assessments.push(ts);
  mem.current_manifest = manifest;
  mem.current_capabilities = capabilities;

  // Timeline event
  const prev = mem.assessments.at(-2);
  let detail = `Readiness score: ${snapshot.readiness_score}%`;
  if (prev) {
    const delta = snapshot.readiness_score - prev.readiness_score;
    if (delta !== 0) detail += ` (${delta > 0 ? '+' : ''}${delta} pts from last assessment)`;
  }
  if (snapshot.current_level !== mem.current_level) {
    const oldLevel = mem.current_level;
    mem.current_level = snapshot.current_level;
    if (snapshot.current_level > oldLevel) {
      mem.timeline.push({
        date: now.slice(0, 10),
        type: 'certification',
        title: `Reached Level ${snapshot.current_level}`,
        detail: `Upgraded from Level ${oldLevel < 0 ? 'none' : oldLevel} to Level ${snapshot.current_level}.`,
        level: snapshot.current_level,
        score: snapshot.readiness_score,
      });
    }
  }
  mem.timeline.push({
    date: now.slice(0, 10),
    type: 'assessment',
    title: `Certification assessment (target L${snapshot.target_level})`,
    detail,
    score: snapshot.readiness_score,
  });
  mem.updated_at = now;
}

export function recordResearch(operatorId: string, question: string): void {
  const mem = getOrCreate(operatorId);
  mem.research_history.push({ question, timestamp: new Date().toISOString() });
  mem.updated_at = new Date().toISOString();
}

export function recordFederation(operatorId: string, partnerOperatorId: string, compatible: boolean): void {
  const mem = getOrCreate(operatorId);
  const now = new Date().toISOString();
  mem.timeline.push({
    date: now.slice(0, 10),
    type: 'federation',
    title: `Federation analysis with ${partnerOperatorId}`,
    detail: compatible
      ? `Federation eligible — both operators cleared all requirements.`
      : `Federation not yet eligible — review compatibility report.`,
  });
  mem.updated_at = now;
}

export function addNote(operatorId: string, note: string): void {
  const mem = getOrCreate(operatorId);
  mem.notes.push(note);
  mem.updated_at = new Date().toISOString();
}

export function getMemory(operatorId: string): OperatorMemory | null {
  return store.get(operatorId) ?? null;
}

export function listOperatorIds(): string[] {
  return [...store.keys()];
}

export function deleteMemory(operatorId: string): void {
  store.delete(operatorId);
}
