import type { EmbeddingProvider } from '../rag/embedding/provider.js';
import type { ModelProvider, ChatMessage, TaskType } from './providers/provider.js';
import { classifyTask } from './router.js';
import { search } from '../rag/search.js';
import { buildContext, renderContextBlock } from '../rag/context.js';
import type { Config } from '../config.js';
import type { Citation, SearchFilters } from '../rag/types.js';

export interface AskRequest {
  question: string;
  filters?: SearchFilters;
  context_limit?: number;
}

export interface AskResponse {
  answer: string;
  citations: Citation[];
  task_type: TaskType;
  model: string;
  weak_retrieval: boolean;
  retrieval_mode: string;
}

const SYSTEM_PROMPTS: Record<TaskType, string> = {
  docs: `You are BanzamIA, the AI-native agent for the Banzami open payment protocol.
You answer questions about the protocol using only the provided protocol sources.
Principle: Tools determine truth. AI explains truth.
Rules:
- Never invent protocol facts, certification results, or regulatory claims.
- Ground every claim in the provided sources.
- If a source does not cover the question, say so clearly.
- Cite sources by their path and section.
- Respond in the same language as the user's question.`,

  code: `You are BanzamIA, specialising in Banzami SDK code generation.
Generate working code examples using the official Banzami SDKs (TypeScript, Dart, PHP, Go).
Rules:
- Use only the API patterns shown in the provided protocol sources.
- Never invent endpoint paths, field names, or SDK methods not present in the sources.
- Always include the correct imports and error handling.
- Prefer TypeScript examples unless the user specifies a different SDK.`,

  reasoning: `You are BanzamIA, performing deep protocol reasoning for the Banzami payment network.
Analyse the provided protocol sources carefully before answering.
Rules:
- Reason step by step from first principles shown in the sources.
- Identify relevant RFCs, ADRs, and invariants by ID.
- Flag any ambiguity or gaps in the protocol specification.
- Never extrapolate beyond what the sources state.`,

  validation: `You are BanzamIA, helping with Banzami protocol validation.
The manifest validator and conformance runner are deterministic tools — they determine ground truth.
Your role is to explain validation failures clearly, not to override the deterministic result.
Rules:
- Explain what the error means in plain language.
- Point to the relevant schema rule or RFC.
- Suggest the correct fix based on the specification.`,

  certification: `You are BanzamIA, assisting with Banzami operator certification.
Certification levels (0–4) are determined by the conformance test suite — deterministic and authoritative.
Your role is to explain what a level requires and how to pass the tests.
Rules:
- Never claim an operator is certified without a conformance runner result.
- Explain each certification requirement from the provided sources.
- Guide operators through the certification path step by step.`,

  trace: `You are BanzamIA, analysing Banzami protocol traces and audit logs.
Traces contain causation, correlation, and event chains across the financial kernel.
Rules:
- Identify the event sequence and any breaks in the causal chain.
- Flag any invariant violations visible in the trace.
- Explain what each event means in the context of the protocol state machine.`,
};

function buildMessages(
  question: string,
  taskType: TaskType,
  contextBlock: string,
): ChatMessage[] {
  return [
    { role: 'system', content: SYSTEM_PROMPTS[taskType] },
    {
      role: 'user',
      content: contextBlock
        ? `## Protocol Context\n\n${contextBlock}\n\n## Question\n\n${question}`
        : question,
    },
  ];
}

export async function ask(
  cfg: Config,
  embedder: EmbeddingProvider,
  model: ModelProvider,
  req: AskRequest,
): Promise<AskResponse> {
  const routing = classifyTask(req.question);
  const limit = req.context_limit ?? 8;

  const searchResponse = await search(cfg, embedder, req.question, limit, req.filters ?? {});
  const ctx = buildContext(searchResponse.results);
  const contextBlock = renderContextBlock(ctx);

  const messages = buildMessages(req.question, routing.task_type, contextBlock);
  const modelResponse = await model.generate(messages, routing.task_type);

  return {
    answer: modelResponse.content,
    citations: ctx.citations,
    task_type: routing.task_type,
    model: modelResponse.model,
    weak_retrieval: ctx.weak_retrieval,
    retrieval_mode: searchResponse.mode,
  };
}

export async function askStream(
  cfg: Config,
  embedder: EmbeddingProvider,
  model: ModelProvider,
  req: AskRequest,
  onToken: (token: string) => void,
): Promise<AskResponse> {
  const routing = classifyTask(req.question);
  const limit = req.context_limit ?? 8;

  const searchResponse = await search(cfg, embedder, req.question, limit, req.filters ?? {});
  const ctx = buildContext(searchResponse.results);
  const contextBlock = renderContextBlock(ctx);

  const messages = buildMessages(req.question, routing.task_type, contextBlock);
  const modelResponse = await model.generateStream(messages, routing.task_type, onToken);

  return {
    answer: modelResponse.content,
    citations: ctx.citations,
    task_type: routing.task_type,
    model: modelResponse.model,
    weak_retrieval: ctx.weak_retrieval,
    retrieval_mode: searchResponse.mode,
  };
}
