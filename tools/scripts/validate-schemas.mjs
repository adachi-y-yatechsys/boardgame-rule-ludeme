#!/usr/bin/env node
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { readFile, readdir, stat } from 'node:fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, '..', '..');

async function loadModule(request, fallback) {
  try {
    return await import(request);
  } catch (error) {
    if (fallback) {
      return import(fallback);
    }
    throw error;
  }
}

const AjvModule = await loadModule('ajv', '../vendor/ajv/index.js');
const AjvExport = AjvModule.default ?? AjvModule.Ajv ?? AjvModule;
const addFormatsModule = await loadModule('ajv-formats', '../vendor/ajv-formats/index.js');
const addFormats = addFormatsModule.default ?? addFormatsModule.addFormats ?? addFormatsModule;

const groups = {
  models: [
    {
      name: 'Ludeme model entries',
      schema: 'schemas/models/ludeme-model.schema.json',
      directories: ['models'],
    },
  ],
  dist: [
    {
      name: 'QA package outputs',
      schema: 'schemas/dist/qa-package.schema.json',
      directories: ['dist'],
    },
  ],
};

const target = process.argv[2] ?? 'models';
if (!Object.prototype.hasOwnProperty.call(groups, target)) {
  console.error(`Unknown validation target: ${target}`);
  console.error(`Available targets: ${Object.keys(groups).join(', ')}`);
  process.exit(1);
}

const ajv = new AjvExport({
  allErrors: true,
  strict: false,
  allowUnionTypes: true,
});
if (typeof addFormats === 'function') {
  addFormats(ajv);
}

async function collectJsonFiles(relativeDir) {
  const absDir = path.resolve(repoRoot, relativeDir);
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
      } else if (entry.isFile() && entry.name.endsWith('.json')) {
        results.push(entryPath);
      }
    }
  }
  return results;
}

let hasFailures = false;

for (const task of groups[target]) {
  const schemaPath = path.resolve(repoRoot, task.schema);
  let schema;
  try {
    schema = JSON.parse(await readFile(schemaPath, 'utf8'));
  } catch (error) {
    console.error(`Failed to read schema for ${task.name}: ${schemaPath}`);
    console.error(error);
    hasFailures = true;
    continue;
  }

  const validate = ajv.compile(schema);
  const files = [];
  for (const dir of task.directories) {
    const dirFiles = await collectJsonFiles(dir);
    files.push(...dirFiles);
  }

  if (!files.length) {
    console.warn(`No files matched for ${task.name}; skipping.`);
    continue;
  }

  console.log(`\nValidating ${files.length} file(s) for ${task.name}`);

  for (const file of files) {
    let data;
    try {
      data = JSON.parse(await readFile(file, 'utf8'));
    } catch (error) {
      console.error(`  ✖ Failed to parse JSON: ${path.relative(repoRoot, file)}`);
      console.error(error);
      hasFailures = true;
      continue;
    }

    const valid = validate(data);
    if (!valid) {
      console.error(`  ✖ Validation failed: ${path.relative(repoRoot, file)}`);
      for (const err of validate.errors ?? []) {
        console.error(`    - ${err.instancePath || '/'} ${err.message}`);
      }
      hasFailures = true;
    } else {
      console.log(`  ✔ ${path.relative(repoRoot, file)}`);
    }
  }
}

if (hasFailures) {
  console.error('\nSchema validation completed with failures.');
  process.exit(1);
}

console.log('\nSchema validation completed successfully.');
