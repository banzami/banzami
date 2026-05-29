import { readdir, readFile, stat } from 'node:fs/promises';
import { join, relative, extname, basename } from 'node:path';
import type { Document, SourceType } from './types.js';
import { authorityWeight } from './authority.js';

const SUPPORTED_EXTENSIONS = new Set(['.md', '.yaml', '.yml', '.json']);

const EXCLUDE_DIRS = new Set([
  'node_modules', '.git', 'dist', 'target', 'build',
  '__pycache__', '.cache', 'coverage', '.next',
]);

const EXCLUDE_FILES = new Set([
  'CHANGELOG.md', 'CODE_OF_CONDUCT.md', 'CONTRIBUTING.md',
  'SECURITY.md', 'LICENSE',
]);

interface PathPattern {
  test: (rel: string) => boolean;
  sourceType: (rel: string, content: string) => SourceType;
  language?: string;
}

const PATH_PATTERNS: PathPattern[] = [
  {
    test: (r) => r === 'docs/BANZAMI_REFERENCE.md',
    sourceType: () => 'reference',
  },
  {
    test: (r) => r.startsWith('docs/rfc/') && r.endsWith('.md') && r !== 'docs/rfc/README.md',
    sourceType: (_, content) => detectRfcStatus(content),
  },
  {
    test: (r) => r.startsWith('docs/adr/') && r.endsWith('.md'),
    sourceType: () => 'accepted_adr',
  },
  {
    test: (r) => r.startsWith('contracts/openapi/') && (r.endsWith('.yaml') || r.endsWith('.yml')),
    sourceType: () => 'openapi',
  },
  {
    test: (r) => r.startsWith('conformance/vectors/') && r.endsWith('.json'),
    sourceType: () => 'conformance',
  },
  {
    test: (r) => r === 'docs/conformance.md',
    sourceType: () => 'conformance',
  },
  {
    test: (r) => r === 'docs/certification.md',
    sourceType: () => 'certification',
  },
  {
    test: (r) => r === 'docs/glossary.md' || r.includes('glossary'),
    sourceType: () => 'glossary',
  },
  {
    test: (r) => r.startsWith('manifests/schemas/') && r.endsWith('.json'),
    sourceType: () => 'manifest_schema',
  },
  {
    test: (r) => r.startsWith('docs/banzamia/') && r.endsWith('.md'),
    sourceType: () => 'banzamia_doc',
  },
  {
    test: (r) => r.startsWith('docs/architecture/') && r.endsWith('.md'),
    sourceType: () => 'architecture_doc',
  },
  {
    test: (r) => r.startsWith('docs/') && r.endsWith('.md'),
    sourceType: () => 'architecture_doc',
  },
  {
    test: (r) => r.startsWith('sdk/') && r.endsWith('.md'),
    sourceType: () => 'sdk_doc',
  },
  {
    test: (r) => r === 'README.md',
    sourceType: () => 'readme',
  },
];

function detectRfcStatus(content: string): SourceType {
  const lower = content.slice(0, 2000).toLowerCase();
  if (lower.includes('status: accepted') || lower.includes('**status**: accepted')) {
    return 'accepted_rfc';
  }
  return 'draft_rfc';
}

function detectSourceType(relPath: string, content: string): SourceType {
  for (const p of PATH_PATTERNS) {
    if (p.test(relPath)) return p.sourceType(relPath, content);
  }
  return 'readme';
}

function extractTitle(content: string, filePath: string): string {
  const h1 = content.match(/^#\s+(.+)/m);
  if (h1) return h1[1].trim();
  return basename(filePath, extname(filePath));
}

function extractVersion(content: string): string {
  const m = content.match(/version[:\s]+(\d+\.\d+[\.\d]*)/i);
  return m ? m[1] : '1.0';
}

function extractStatus(content: string, sourceType: SourceType): string {
  if (sourceType === 'accepted_rfc' || sourceType === 'accepted_adr') return 'accepted';
  if (sourceType === 'draft_rfc') return 'draft';
  const m = content.match(/\*\*status\*\*[:\s]+([a-z-]+)/i);
  return m ? m[1].toLowerCase() : 'active';
}

function shouldInclude(relPath: string): boolean {
  const parts = relPath.split('/');
  for (const part of parts) {
    if (EXCLUDE_DIRS.has(part)) return false;
  }
  const file = basename(relPath);
  if (EXCLUDE_FILES.has(file)) return false;
  return SUPPORTED_EXTENSIONS.has(extname(relPath));
}

async function walkDir(dir: string, root: string): Promise<string[]> {
  const entries = await readdir(dir, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!EXCLUDE_DIRS.has(entry.name)) {
        files.push(...await walkDir(full, root));
      }
    } else if (entry.isFile()) {
      const rel = relative(root, full);
      if (shouldInclude(rel)) {
        files.push(full);
      }
    }
  }
  return files;
}

export async function loadDocuments(repoRoot: string): Promise<Document[]> {
  const files = await walkDir(repoRoot, repoRoot);
  const docs: Document[] = [];

  for (const filePath of files) {
    try {
      const content = await readFile(filePath, 'utf-8');
      const relPath = relative(repoRoot, filePath);
      const sourceType = detectSourceType(relPath, content);
      const title = extractTitle(content, filePath);
      const s = await stat(filePath);

      docs.push({
        path: relPath,
        title,
        section: title,
        source_type: sourceType,
        status: extractStatus(content, sourceType),
        version: extractVersion(content),
        authority: authorityWeight(sourceType),
        language: 'pt',
        repo: 'banzami/banzami',
        updated_at: s.mtime.toISOString(),
        content,
      });
    } catch {
      // Skip unreadable files silently
    }
  }

  return docs;
}
