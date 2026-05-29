export type NodeType =
  | 'rfc'
  | 'adr'
  | 'invariant'
  | 'openapi'
  | 'conformance_vector'
  | 'certification_rule'
  | 'manifest_schema'
  | 'sdk_doc'
  | 'architecture_doc'
  | 'glossary_term'
  | 'operator'
  | 'capability'
  | 'federation_profile'
  | 'digital_twin'
  | 'timeline_event'
  | 'simulation_result';

export type RelationshipType =
  | 'REFERENCES'
  | 'IMPLEMENTS'
  | 'SUPERSEDES'
  | 'REQUIRES'
  | 'VALIDATES'
  | 'EXPLAINS'
  | 'DEPENDS_ON'
  | 'RELATED_TO'
  | 'CAN_FEDERATE_WITH'
  | 'REQUIRES_CAPABILITY'
  | 'BLOCKED_BY'
  | 'CERTIFIED_FOR';

export interface GraphNode {
  id: string;
  type: NodeType;
  title: string;
  path: string;
  status: string;
  summary: string;
  authority: number;
}

export interface GraphEdge {
  from: string;
  to: string;
  relationship: RelationshipType;
  reason?: string;
}

export interface ProtocolGraph {
  nodes: GraphNode[];
  edges: GraphEdge[];
  indexed_at: string;
  version: string;
}

export interface GraphNeighbour {
  node: GraphNode;
  relationship: RelationshipType;
  direction: 'outbound' | 'inbound';
}

export interface GraphPath {
  nodes: GraphNode[];
  edges: GraphEdge[];
  length: number;
}
