#!/usr/bin/env node
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { access, readdir, stat } from 'node:fs/promises';
import { constants } from 'node:fs';
import { spawn } from 'node:child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, '..', '..');

const jarPath = path.join(repoRoot, 'tools', 'vendor', 'alloy', 'alloy6.jar');

async function jarExists() {
  try {
    await access(jarPath, constants.R_OK);
    return true;
  } catch {
    return false;
  }
}

async function collectAlsFiles(relativeDir) {
  const absDir = path.join(repoRoot, relativeDir);
  let dirStat;
  try {
    dirStat = await stat(absDir);
  } catch {
    return [];
  }
  if (!dirStat.isDirectory()) {
    return [];
  }

  const results = [];
  const queue = [absDir];
  while (queue.length) {
    const current = queue.pop();
    const entries = await readdir(current, { withFileTypes: true });
    for (const entry of entries) {
      const entryPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        queue.push(entryPath);
      } else if (entry.isFile() && entry.name.endsWith('.als')) {
        results.push(entryPath);
      }
    }
  }
  return results;
}

async function runAlloy(specPath) {
  return new Promise((resolve, reject) => {
    const child = spawn('java', ['-jar', jarPath, specPath], {
      stdio: 'inherit',
      cwd: repoRoot,
    });

    child.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Alloy exited with code ${code}`));
      }
    });
  });
}

async function main() {
  const allowMissing = ['1', 'true', 'yes'].includes(
    String(process.env.ALLOW_ALLOY_SKIP ?? '').toLowerCase(),
  );

  if (!(await jarExists())) {
    const message =
      'Alloy CLI (tools/vendor/alloy/alloy6.jar) is required but not present. Failing Alloy checks.';

    if (allowMissing) {
      console.warn(`${message} ALLOW_ALLOY_SKIP is set, so the step will be skipped.`);
      console.warn('See docs/requirements/13_tooling_and_commands.md for installation instructions.');
      return;
    }

    throw new Error(
      `${message} Set ALLOW_ALLOY_SKIP=1 if you intend to bypass Alloy execution intentionally.`,
    );
  }

  const specs = [
    ...(await collectAlsFiles('spec').catch(() => [])),
    ...(await collectAlsFiles('docs').catch(() => [])),
  ];

  if (!specs.length) {
    console.warn('No Alloy specification (*.als) files found.');
    return;
  }

  for (const spec of specs) {
    const relPath = path.relative(repoRoot, spec);
    console.log(`Running Alloy solver for ${relPath}`);
    await runAlloy(spec);
  }

  console.log('Alloy checks completed successfully.');
}

main().catch((error) => {
  console.error('Alloy check failed.');
  console.error(error);
  process.exit(1);
});
