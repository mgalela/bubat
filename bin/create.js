#!/usr/bin/env node

'use strict';

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  console.log('Usage:');
  console.log('  npx create-bubat <dir>         standalone workspace (open dir in Claude Code)');
  console.log('  npx create-bubat --dir <dir>   embed in existing project (patches paths + @import hint)');
  console.log('');
  console.log('Examples:');
  console.log('  npx create-bubat my-arch');
  console.log('  npx create-bubat --dir .bubat');
  process.exit(0);
}

let targetDir = null;
let isEmbed = false;

const dirIdx = args.indexOf('--dir');
if (dirIdx !== -1) {
  isEmbed = true;
  targetDir = args[dirIdx + 1];
  if (!targetDir || targetDir.startsWith('--')) {
    console.error('Error: --dir requires a directory argument');
    process.exit(1);
  }
} else {
  targetDir = args.find(a => !a.startsWith('--'));
  if (!targetDir) {
    console.error('Error: directory argument required');
    process.exit(1);
  }
}

const templateSrc = path.join(__dirname, '..');
const dest = path.resolve(process.cwd(), targetDir);
const relFromCwd = path.relative(process.cwd(), dest).replace(/\\/g, '/');

// prefix used to rewrite BUBAT-root-relative paths in instruction files
const prefix = isEmbed && relFromCwd ? relFromCwd + '/' : '';

const COPY_EXCLUDE = new Set([
  'bin', 'package.json', 'package-lock.json',
  'node_modules', '.git', '.npmignore', '.claude',
  'example', 'ref-ICM', 'C4ICM.zip',
]);

function copyDir(srcDir, destDir) {
  fs.mkdirSync(destDir, { recursive: true });
  for (const entry of fs.readdirSync(srcDir)) {
    if (COPY_EXCLUDE.has(entry)) continue;
    const srcPath = path.join(srcDir, entry);
    const destPath = path.join(destDir, entry);
    if (fs.lstatSync(srcPath).isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// Rewrite BUBAT-root-relative path references in markdown instruction files.
// Skips fenced code blocks (documentation, not instructions).
// Uses (?<!\/) lookbehind so ../../shared/ patterns in stage files are left alone
// (the ../../ paths are resolved by Claude relative to the file's own location).
function patchPaths(content, pfx) {
  const lines = content.split('\n');
  let inFence = false;
  return lines.map(line => {
    if (/^```/.test(line.trimStart())) {
      inFence = !inFence;
      return line;
    }
    if (inFence) return line;
    return line.replace(/(?<!\/)(?<!\w)(stages|shared|raw|setup)\//g, `${pfx}$1/`);
  }).join('\n');
}

// Root instruction files + shared gates file (all have BUBAT-root-relative bare paths).
// README.md is documentation — excluded.
const PATCH_FILES_BASE = [
  'CLAUDE.md',
  'CONTEXT.md',
  path.join('shared', 'stage-gates.md'),
];

// Stage CONTEXT.md files also have a handful of bare shared/ references in
// their Process steps. ../../shared/ references are left intact by patchPaths.
function collectStagePatchFiles(destDir) {
  const stagesDir = path.join(destDir, 'stages');
  if (!fs.existsSync(stagesDir)) return [];
  return fs.readdirSync(stagesDir)
    .map(s => path.join('stages', s, 'CONTEXT.md'))
    .filter(rel => fs.existsSync(path.join(destDir, rel)));
}

// --- run ---

if (fs.existsSync(dest)) {
  console.error(`Error: directory already exists: ${dest}`);
  process.exit(1);
}

copyDir(templateSrc, dest);

if (isEmbed && prefix) {
  const allPatchFiles = [...PATCH_FILES_BASE, ...collectStagePatchFiles(dest)];
  for (const rel of allPatchFiles) {
    const fpath = path.join(dest, rel);
    if (fs.existsSync(fpath)) {
      fs.writeFileSync(fpath, patchPaths(fs.readFileSync(fpath, 'utf8'), prefix));
    }
  }
}

console.log(`\nBUBAT scaffolded at: ${dest}`);

if (isEmbed) {
  const importLine = `@${relFromCwd}/CLAUDE.md`;
  const projectClaudeMd = path.join(process.cwd(), 'CLAUDE.md');

  console.log('');
  if (fs.existsSync(projectClaudeMd)) {
    const existing = fs.readFileSync(projectClaudeMd, 'utf8');
    if (existing.includes(importLine)) {
      console.log(`@import already present in project CLAUDE.md.`);
    } else {
      console.log(`Add to your project CLAUDE.md:\n\n  ${importLine}\n`);
    }
  } else {
    console.log(`No CLAUDE.md at project root. Create one:\n\n  echo '${importLine}' > CLAUDE.md\n`);
  }
  console.log(`Then open project in Claude Code and type: setup`);
} else {
  console.log(`Open ${dest} in Claude Code and type: setup`);
}
