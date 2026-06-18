#!/usr/bin/env node

'use strict';

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  console.log('Usage:');
  console.log('  npx create-bubat <dir>                standalone workspace (open dir in Claude Code)');
  console.log('  npx create-bubat --dir <dir>          embed in existing project (patches paths + @import hint)');
  console.log('  npx create-bubat --update <dir>       update framework files, preserve user data');
  console.log('  npx create-bubat --update --dir <dir> update embedded workspace');
  console.log('');
  console.log('Examples:');
  console.log('  npx create-bubat my-arch');
  console.log('  npx create-bubat --dir .bubat');
  console.log('  npx create-bubat --update my-arch');
  console.log('  npx create-bubat --update --dir .bubat');
  console.log('');
  console.log('Update preserves: shared/system-meta.md, raw/MANIFEST.md, stages/*/output/*');
  process.exit(0);
}

const isUpdate = args.includes('--update');
let isEmbed = false;
let targetDir = null;

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

// User-owned files — never overwritten on --update.
// Paths are relative to the BUBAT root (dest), using OS path.join separators.
const USER_DATA_FILES = new Set([
  path.join('shared', 'system-meta.md'),
  path.join('raw', 'MANIFEST.md'),
]);

// Returns true for files inside stages/*/output/ that are NOT .gitkeep.
// .gitkeep is allowed through so new stages get their output/ placeholder.
function isOutputFile(relPath) {
  const parts = relPath.split(path.sep);
  return (
    parts.length >= 4 &&
    parts[0] === 'stages' &&
    parts[2] === 'output' &&
    parts[3] !== '.gitkeep'
  );
}

function isUserData(relPath) {
  return USER_DATA_FILES.has(relPath) || isOutputFile(relPath);
}

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

// Walk src, copy framework files to dest, skip user data.
// Returns { updated, added, skipped } counts.
function updateDir(srcDir, destDir, pfx, relBase) {
  let updated = 0, added = 0, skipped = 0;
  fs.mkdirSync(destDir, { recursive: true });

  for (const entry of fs.readdirSync(srcDir)) {
    if (COPY_EXCLUDE.has(entry)) continue;
    const srcPath = path.join(srcDir, entry);
    const destPath = path.join(destDir, entry);
    const relPath = relBase ? path.join(relBase, entry) : entry;

    if (fs.lstatSync(srcPath).isDirectory()) {
      const counts = updateDir(srcPath, destPath, pfx, relPath);
      updated += counts.updated;
      added   += counts.added;
      skipped += counts.skipped;
    } else {
      if (isUserData(relPath)) {
        skipped++;
        continue;
      }
      const existed = fs.existsSync(destPath);
      fs.copyFileSync(srcPath, destPath);
      if (existed) updated++; else added++;
    }
  }
  return { updated, added, skipped };
}

// --- run ---

if (isUpdate) {
  if (!fs.existsSync(dest)) {
    console.error(`Error: directory does not exist: ${dest}`);
    console.error(`Run without --update to create a new workspace.`);
    process.exit(1);
  }

  const { updated, added, skipped } = updateDir(templateSrc, dest, prefix, '');

  if (isEmbed && prefix) {
    const allPatchFiles = [...PATCH_FILES_BASE, ...collectStagePatchFiles(dest)];
    for (const rel of allPatchFiles) {
      const fpath = path.join(dest, rel);
      if (fs.existsSync(fpath)) {
        fs.writeFileSync(fpath, patchPaths(fs.readFileSync(fpath, 'utf8'), prefix));
      }
    }
  }

  console.log(`\nBUBAT updated at: ${dest}`);
  console.log(`  ${updated} files updated, ${added} files added, ${skipped} files preserved (user data)`);
  console.log('');
  console.log('Review changes, then open in Claude Code and continue your pipeline.');

} else {
  if (fs.existsSync(dest)) {
    console.error(`Error: directory already exists: ${dest}`);
    console.error(`Use --update to update an existing workspace.`);
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
}
