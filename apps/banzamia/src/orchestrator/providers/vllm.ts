import type {
  ModelProvider,
  ModelProviderStatus,
  ChatMessage,
  ModelResponse,
  TaskType,
} from './provider.js';

interface VLLMConfig {
  url: string;
  models: {
    qwen: string;
    qwenCoder: string;
    deepseek: string;
  };
}

interface OpenAIChatResponse {
  choices: Array<{
    message: { content: string };
    finish_reason: string;
  }>;
  usage?: { prompt_tokens: number; completion_tokens: number };
  model: string;
}

interface OpenAIChatStreamChunk {
  choices: Array<{
    delta: { content?: string };
    finish_reason: string | null;
  }>;
}

const TASK_MODEL: Record<TaskType, keyof VLLMConfig['models']> = {
  docs: 'qwen',
  code: 'qwenCoder',
  reasoning: 'deepseek',
  validation: 'deepseek',
  certification: 'deepseek',
  trace: 'deepseek',
};

const MAX_TOKENS: Record<TaskType, number> = {
  docs: 2048,
  code: 4096,
  reasoning: 4096,
  validation: 2048,
  certification: 2048,
  trace: 2048,
};

export class VLLMProvider implements ModelProvider {
  readonly name = 'vllm';

  constructor(private readonly cfg: VLLMConfig) {}

  private modelFor(taskType: TaskType): string {
    return this.cfg.models[TASK_MODEL[taskType]];
  }

  private chatUrl(): string {
    return `${this.cfg.url}/chat/completions`;
  }

  async generate(messages: ChatMessage[], taskType: TaskType): Promise<ModelResponse> {
    const model = this.modelFor(taskType);
    const response = await fetch(this.chatUrl(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model,
        messages,
        max_tokens: MAX_TOKENS[taskType],
        temperature: taskType === 'code' ? 0.1 : 0.3,
        stream: false,
      }),
    });

    if (!response.ok) {
      const body = await response.text();
      throw new Error(`vLLM returned ${response.status}: ${body}`);
    }

    const data: OpenAIChatResponse = await response.json() as OpenAIChatResponse;
    return {
      content: data.choices[0]?.message.content ?? '',
      model: data.model,
      task_type: taskType,
      input_tokens: data.usage?.prompt_tokens,
      output_tokens: data.usage?.completion_tokens,
    };
  }

  async generateStream(
    messages: ChatMessage[],
    taskType: TaskType,
    onToken: (token: string) => void,
  ): Promise<ModelResponse> {
    const model = this.modelFor(taskType);
    const response = await fetch(this.chatUrl(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model,
        messages,
        max_tokens: MAX_TOKENS[taskType],
        temperature: taskType === 'code' ? 0.1 : 0.3,
        stream: true,
      }),
    });

    if (!response.ok || !response.body) {
      throw new Error(`vLLM stream failed: ${response.status}`);
    }

    const decoder = new TextDecoder();
    let fullContent = '';
    const reader = response.body.getReader();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const text = decoder.decode(value, { stream: true });
      for (const line of text.split('\n')) {
        if (!line.startsWith('data: ')) continue;
        const data = line.slice(6).trim();
        if (data === '[DONE]') break;
        try {
          const chunk: OpenAIChatStreamChunk = JSON.parse(data) as OpenAIChatStreamChunk;
          const token = chunk.choices[0]?.delta.content ?? '';
          if (token) {
            fullContent += token;
            onToken(token);
          }
        } catch {
          // Ignore malformed SSE chunks
        }
      }
    }

    return { content: fullContent, model, task_type: taskType };
  }

  async status(): Promise<ModelProviderStatus> {
    try {
      const response = await fetch(`${this.cfg.url}/models`);
      if (!response.ok) throw new Error(`${response.status}`);
      return {
        available: true,
        provider: 'vllm',
        models: {
          qwen: this.cfg.models.qwen,
          qwenCoder: this.cfg.models.qwenCoder,
          deepseek: this.cfg.models.deepseek,
        },
      };
    } catch (e) {
      return {
        available: false,
        provider: 'vllm',
        models: this.cfg.models,
        error: String(e),
      };
    }
  }
}
