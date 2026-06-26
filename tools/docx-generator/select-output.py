#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
EXPORT_TOOL = SCRIPT_DIR / "export-doc.py"
DEFAULT_TEMPLATE_DIR = SCRIPT_DIR / "templates"

MODE_TO_TEMPLATE = {
    "architecture": "architecture",
    "fsd": "fsd",
}

MODE_TO_SOURCE_STEM = {
    "architecture": "architecture",
    "fsd": "fsd",
}


def read_system_slug(root: Path) -> str:
    meta = root / "shared" / "system-meta.md"
    if not meta.exists():
        return "system"
    marker = "- **System slug:**"
    for line in meta.read_text(encoding="utf-8").splitlines():
        if line.startswith(marker):
            return line[len(marker):].strip() or "system"
    return "system"


def default_output_path(output_dir: Path, mode: str, fmt: str, slug: str) -> Path:
    stem = f"{slug}-{MODE_TO_SOURCE_STEM[mode]}"
    if fmt == "md":
        return output_dir / f"{stem}.md"
    return output_dir / "templates" / f"{stem}.{fmt}"


def source_markdown_path(source_dir: Path, mode: str, slug: str) -> Path:
    return source_dir / f"{slug}-{MODE_TO_SOURCE_STEM[mode]}.md"


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def main() -> int:
    parser = argparse.ArgumentParser(description="Select document mode and export template or final Markdown")
    parser.add_argument("--mode", choices=sorted(MODE_TO_TEMPLATE), required=True, help="Output mode")
    parser.add_argument("--format", choices=["md", "html", "docx"], default="md", help="Output format")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Workspace root; used for shared/system-meta.md slug lookup")
    parser.add_argument("--source-dir", type=Path, help="Directory containing final Markdown sources; default: <root>/stages/05-document/output if present, else <root>/output/documents")
    parser.add_argument("--output-dir", type=Path, help="Output directory; default: <source-dir>")
    parser.add_argument("--template-dir", type=Path, default=DEFAULT_TEMPLATE_DIR, help="Directory containing built-in-compatible templates")
    parser.add_argument("--slug", help="Override system slug")
    parser.add_argument("--output", type=Path, help="Override output path")
    parser.add_argument("--template-only", action="store_true", help="Force export from template, not final Markdown source")
    parser.add_argument("--require-source", action="store_true", help="Fail if final Markdown source is missing instead of falling back to template")
    args = parser.parse_args()

    root = args.root.resolve()
    legacy_stage_out = root / "stages" / "05-document" / "output"
    source_dir = args.source_dir or (legacy_stage_out if legacy_stage_out.exists() else root / "output" / "documents")
    output_dir = args.output_dir or source_dir

    slug = args.slug or read_system_slug(root)
    output = args.output or default_output_path(output_dir, args.mode, args.format, slug)
    output.parent.mkdir(parents=True, exist_ok=True)

    source_md = source_markdown_path(source_dir, args.mode, slug)
    use_source = (not args.template_only) and source_md.exists()
    if args.require_source and not use_source:
        raise FileNotFoundError(
            f"Final Markdown source missing for mode '{args.mode}': {source_md}. "
            f"Generate/save final content first, pass --source-dir, or use --template-only for template DOCX."
        )

    cmd = ["python3", str(EXPORT_TOOL)]
    if use_source:
        cmd.extend(["--source", str(source_md), "--title", f"{slug} {args.mode.upper()} Document"])
    else:
        cmd.extend(["--template", MODE_TO_TEMPLATE[args.mode], "--template-dir", str(args.template_dir)])
    cmd.extend(["--format", args.format, "--output", str(output)])
    subprocess.run(cmd, check=True)

    mode_note = output_dir / "selected-mode.md"
    source_ref = rel(source_md, root) if use_source else rel(args.template_dir / f"{MODE_TO_TEMPLATE[args.mode]}-template.md", root)
    mode_note.write_text(
        "# Selected Document Output Mode\n\n"
        f"- Mode: `{args.mode}`\n"
        f"- Template: `{MODE_TO_TEMPLATE[args.mode]}`\n"
        f"- Format: `{args.format}`\n"
        f"- Export source: `{'final markdown' if use_source else 'template'}`\n"
        f"- Source path: `{source_ref}`\n"
        f"- Output: `{rel(output, root)}`\n",
        encoding="utf-8",
    )

    print(output)
    print(mode_note)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
