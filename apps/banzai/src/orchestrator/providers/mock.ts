import type {
  ModelProvider,
  ModelProviderStatus,
  ChatMessage,
  ModelResponse,
  TaskType,
} from './provider.js';

const MOCK_RESPONSES: Record<TaskType, string> = {
  docs: 'Based on the Banza protocol documentation, I can answer your question. [mock response — configure BANZAI_MODE=live-ai and a vLLM endpoint for real model inference]',
  code: '```typescript\n// Mock code response — configure BANZAI_VLLM_URL for Qwen Coder inference\nconsole.log("BanzAI code generation requires a configured vLLM endpoint");\n```',
  reasoning: 'This requires deep reasoning about the Banza protocol. [mock response — configure DeepSeek via BANZAI_VLLM_URL for reasoning tasks]',
  validation: 'Manifest validation is deterministic and does not require a model. Check the /tools/validate endpoint.',
  certification: 'Certification analysis requires deterministic conformance tools plus model reasoning. [mock response]',
  trace: 'Trace analysis is available via the /tools/trace endpoint. [mock response]',
};

export class MockModelProvider implements ModelProvider {
  readonly name = 'mock';

  async generate(messages: ChatMessage[], taskType: TaskType): Promise<ModelResponse> {
    const userMessage = [...messages].reverse().find((m: ChatMessage) => m.role === 'user')?.content ?? '';
    const base = MOCK_RESPONSES[taskType];
    return {
      content: `${base}\n\n**Your question:** ${userMessage.slice(0, 200)}`,
      model: `mock-${taskType}`,
      task_type: taskType,
    };
  }

  async generateStream(
    messages: ChatMessage[],
    taskType: TaskType,
    onToken: (token: string) => void,
  ): Promise<ModelResponse> {
    const response = await this.generate(messages, taskType);
    const words = response.content.split(' ');
    for (let i = 0; i < words.length; i++) {
      onToken(words[i] + (i < words.length - 1 ? ' ' : ''));
      await new Promise((r) => setTimeout(r, 5));
    }
    return response;
  }

  async status(): Promise<ModelProviderStatus> {
    return {
      available: true,
      provider: 'mock',
      models: {
        qwen: 'mock-docs',
        qwenCoder: 'mock-code',
        deepseek: 'mock-reasoning',
      },
    };
  }
}
