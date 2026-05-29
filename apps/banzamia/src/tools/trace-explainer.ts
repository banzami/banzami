export interface TraceEvent {
  event_id: string;
  event_type: string;
  timestamp: string;
  trace_id: string;
  correlation_id?: string;
  causation_id?: string;
  payload?: Record<string, unknown>;
}

export interface TraceAnalysis {
  trace_id: string;
  event_count: number;
  timeline: TraceEventExplained[];
  causal_chain: string[];
  anomalies: TraceAnomaly[];
  summary: string;
}

export interface TraceEventExplained {
  event: TraceEvent;
  explanation: string;
  state_transition?: string;
}

export interface TraceAnomaly {
  type: 'broken_causal_chain' | 'duplicate_event_id' | 'out_of_order' | 'unknown_event_type';
  description: string;
  event_id?: string;
}

const EVENT_EXPLANATIONS: Record<string, string> = {
  'wallet.created': 'A new wallet was initialised in the ledger with zero balance',
  'wallet.credited': 'Funds were added to a wallet (debit from external source, credit to wallet)',
  'wallet.debited': 'Funds were removed from a wallet',
  'transfer.initiated': 'A P2P transfer was requested between wallets',
  'transfer.completed': 'A P2P transfer settled successfully with double-entry postings applied',
  'transfer.failed': 'A P2P transfer could not be completed; no ledger mutation occurred',
  'transfer.reversed': 'A previously settled transfer was reversed; compensating postings applied',
  'payment.requested': 'A payment request (QR or link) was created',
  'payment.fulfilled': 'A payment request was fulfilled by a payer',
  'payment.expired': 'A payment request expired before being fulfilled',
  'settlement.initiated': 'Cross-operator settlement batch was opened',
  'settlement.completed': 'Settlement batch closed; net positions applied',
  'settlement.failed': 'Settlement batch could not complete; positions reversed',
  'ledger.posting': 'A double-entry ledger posting was recorded',
};

function explainEvent(event: TraceEvent): TraceEventExplained {
  const explanation = EVENT_EXPLANATIONS[event.event_type]
    ?? `Unknown event type '${event.event_type}' — not in protocol specification`;

  let stateTransition: string | undefined;
  if (event.event_type.includes('initiated')) stateTransition = '→ PENDING';
  else if (event.event_type.includes('completed')) stateTransition = 'PENDING → SETTLED';
  else if (event.event_type.includes('failed')) stateTransition = 'PENDING → FAILED';
  else if (event.event_type.includes('reversed')) stateTransition = 'SETTLED → REVERSED';
  else if (event.event_type.includes('created')) stateTransition = '→ ACTIVE';

  return { event, explanation, ...(stateTransition ? { state_transition: stateTransition } : {}) };
}

function detectAnomalies(events: TraceEvent[]): TraceAnomaly[] {
  const anomalies: TraceAnomaly[] = [];
  const seenIds = new Set<string>();
  const knownTypes = new Set(Object.keys(EVENT_EXPLANATIONS));

  for (const event of events) {
    if (seenIds.has(event.event_id)) {
      anomalies.push({
        type: 'duplicate_event_id',
        description: `Duplicate event_id '${event.event_id}'`,
        event_id: event.event_id,
      });
    }
    seenIds.add(event.event_id);

    if (!knownTypes.has(event.event_type)) {
      anomalies.push({
        type: 'unknown_event_type',
        description: `Event type '${event.event_type}' is not in the Banzami protocol specification`,
        event_id: event.event_id,
      });
    }
  }

  const sorted = [...events].sort((a, b) => a.timestamp.localeCompare(b.timestamp));
  for (let i = 0; i < events.length; i++) {
    if (events[i].event_id !== sorted[i].event_id) {
      anomalies.push({
        type: 'out_of_order',
        description: 'Events are not in chronological order',
      });
      break;
    }
  }

  const causeMap = new Map<string, string>();
  for (const event of events) {
    if (event.causation_id && !seenIds.has(event.causation_id) && event.causation_id !== event.trace_id) {
      anomalies.push({
        type: 'broken_causal_chain',
        description: `Event '${event.event_id}' references causation_id '${event.causation_id}' which does not exist in this trace`,
        event_id: event.event_id,
      });
    }
    if (event.causation_id) causeMap.set(event.causation_id, event.event_id);
  }

  return anomalies;
}

export function explainTrace(events: TraceEvent[]): TraceAnalysis {
  if (events.length === 0) {
    return {
      trace_id: '',
      event_count: 0,
      timeline: [],
      causal_chain: [],
      anomalies: [],
      summary: 'Empty trace — no events to analyse',
    };
  }

  const traceId = events[0].trace_id;
  const sorted = [...events].sort((a, b) => a.timestamp.localeCompare(b.timestamp));
  const timeline = sorted.map(explainEvent);
  const anomalies = detectAnomalies(sorted);

  const causalChain = sorted.map((e) => {
    const parts = [e.event_type];
    if (e.causation_id && e.causation_id !== traceId) {
      parts.push(`← caused by ${e.causation_id.slice(0, 8)}...`);
    }
    return parts.join(' ');
  });

  const summary = anomalies.length > 0
    ? `Trace ${traceId.slice(0, 8)}... — ${events.length} events — ${anomalies.length} anomaly(ies) detected`
    : `Trace ${traceId.slice(0, 8)}... — ${events.length} events — no anomalies`;

  return { trace_id: traceId, event_count: events.length, timeline, causal_chain: causalChain, anomalies, summary };
}
