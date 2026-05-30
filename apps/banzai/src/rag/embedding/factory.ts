import type { EmbeddingProvider } from './provider.js';
import { MockEmbeddingProvider } from './mock.js';
import { LocalEmbeddingProvider } from './local.js';
import { RemoteEmbeddingProvider } from './remote.js';
import type { Config } from '../../config.js';

export function createEmbeddingProvider(cfg: Config): EmbeddingProvider {
  const { provider, model, url, remoteModel, dims } = cfg.embedding;
  switch (provider) {
    case 'local':
      return new LocalEmbeddingProvider(model, dims);
    case 'remote':
      return new RemoteEmbeddingProvider(url, remoteModel, dims);
    case 'mock':
    default:
      return new MockEmbeddingProvider(dims);
  }
}
