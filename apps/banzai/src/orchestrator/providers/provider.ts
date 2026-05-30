export type TaskType =
  | 'docs'
  | 'code'
  | 'reasoning'
  | 'validation'
  | 'certification'
  | 'trace';

export interface ChatMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface ModelResponse {
  content: string;
  model: string;
  task_type: TaskType;
  input_tokens?: number;
  output_tokens?: number;
}

export interface ModelProvider {
  generate(messages: ChatMessage[], taskType: TaskType): Promise<ModelResponse>;
  generateStream(
    messages: ChatMessage[],
    taskType: TaskType,
    onToken: (token: string) => void,
  ): Promise<ModelResponse>;
  status(): Promise<ModelProviderStatus>;
  readonly name: string;
}

export interface ModelProviderStatus {
  available: boolean;
  provider: string;
  models: Record<string, string>;
  error?: string;
}
