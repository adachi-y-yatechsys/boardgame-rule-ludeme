#!/usr/bin/env node
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { readFile, writeFile, mkdir, readdir, stat } from 'node:fs/promises';
import crypto from 'node:crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, '..', '..');

async function collectModelFiles() {
  const baseDir = path.join(repoRoot, 'models');
  let baseStat;
  try {
    baseStat = await stat(baseDir);
  } catch {
    return [];
  }
  if (!baseStat.isDirectory()) {
    return [];
  }

  const results = [];
  const queue = [baseDir];
  while (queue.length) {
    const current = queue.pop();
    const entries = await readdir(current, { withFileTypes: true });
    for (const entry of entries) {
      const entryPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        queue.push(entryPath);
      } else if (entry.isFile() && entry.name.endsWith('.json')) {
        results.push(entryPath);
      }
    }
  }
  return results;
}

async function loadModels() {
  const files = await collectModelFiles();
  const entries = [];
  for (const file of files) {
    const raw = await readFile(file, 'utf8');
    const data = JSON.parse(raw);
    entries.push({
      source: path.relative(repoRoot, file),
      data,
    });
  }

  entries.sort((a, b) => a.data.id.localeCompare(b.data.id));
  return entries;
}

async function main() {
  const models = await loadModels();
  const generatedAt = new Date().toISOString();

  const hash = crypto.createHash('sha256');
  for (const entry of models) {
    hash.update(JSON.stringify(entry.data));
  }
  const checksum = hash.digest('hex');

  const payload = {
    generatedAt,
    modelCount: models.length,
    checksum,
    models: models.map((entry) => ({
      ...entry.data,
      source: entry.source,
    })),
  };

  const distDir = path.join(repoRoot, 'dist', 'qa');
  await mkdir(distDir, { recursive: true });
  const distPath = path.join(distDir, 'ludeme-qa-package.json');
  await writeFile(distPath, JSON.stringify(payload, null, 2));

  const logsDir = path.join(repoRoot, 'logs');
  await mkdir(logsDir, { recursive: true });
  const logPath = path.join(logsDir, 'build-summary.json');
  await writeFile(
    logPath,
    JSON.stringify(
      {
        generatedAt,
        modelSources: models.map((entry) => entry.source),
        distPath: path.relative(repoRoot, distPath),
        checksum,
      },
      null,
      2,
    ),
  );

  console.log(`Build completed. Dist artifact: ${path.relative(repoRoot, distPath)}`);
  console.log(`Build summary written to ${path.relative(repoRoot, logPath)}`);
}

main().catch((error) => {
  console.error('Build failed');
  console.error(error);
  process.exit(1);
});
