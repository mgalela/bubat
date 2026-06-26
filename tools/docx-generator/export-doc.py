#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
import shutil
import struct
import subprocess
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATE_DIR = SCRIPT_DIR / "templates"
DEFAULT_OUT_DIR = Path.cwd() / "output" / "documents"

DEFAULT_TEMPLATES = {
    "architecture": DEFAULT_TEMPLATE_DIR / "architecture-template.md",
    "fsd": DEFAULT_TEMPLATE_DIR / "fsd-template.md",
}
FORMATS = {"md", "html", "docx"}
PAGE_WIDTH_TWIPS = 11906
PAGE_HEIGHT_TWIPS = 16838
PAGE_MARGIN_TWIPS = 900
PAGE_HEADER_FOOTER_TWIPS = 420
PORTRAIT_CONTENT_WIDTH_TWIPS = PAGE_WIDTH_TWIPS - (2 * PAGE_MARGIN_TWIPS)
LANDSCAPE_CONTENT_WIDTH_TWIPS = PAGE_HEIGHT_TWIPS - (2 * PAGE_MARGIN_TWIPS)
MAX_IMAGE_WIDTH_EMU = int(7.0 * 914400)
MAX_IMAGE_HEIGHT_EMU = int(8.6 * 914400)
LARGE_IMAGE_HEIGHT_EMU = int(6.8 * 914400)
PNG_DPI = 96


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "template"


def inline_format(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text


def table_to_html(lines: list[str]) -> str:
    rows = []
    for line in lines:
        if not line.strip().startswith("|"):
            continue
        cells = [inline_format(cell.strip()) for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return ""
    header = rows[0]
    body = rows[2:] if len(rows) > 2 else []
    parts = ["<table>", "<thead><tr>"]
    parts.extend(f"<th>{cell}</th>" for cell in header)
    parts.append("</tr></thead>")
    if body:
        parts.append("<tbody>")
        for row in body:
            parts.append("<tr>")
            parts.extend(f"<td>{cell}</td>" for cell in row)
            parts.append("</tr>")
        parts.append("</tbody>")
    parts.append("</table>")
    return "".join(parts)


def render_mermaid(mermaid_text: str, asset_dir: Path, stem: str, fmt: str = "svg") -> Path:
    asset_dir.mkdir(parents=True, exist_ok=True)
    input_path = asset_dir / f"{slugify(stem)}.mmd"
    output_path = asset_dir / f"{slugify(stem)}.{fmt}"
    input_path.write_text(mermaid_text, encoding="utf-8")
    subprocess.run([
        "npx",
        "-y",
        "@mermaid-js/mermaid-cli",
        "-q",
        "-i",
        str(input_path),
        "-o",
        str(output_path),
        "-b",
        "transparent",
    ], check=True)
    return output_path


def markdown_to_html(markdown_text: str, title: str, asset_dir: Path | None = None) -> str:
    lines = markdown_text.splitlines()
    body: list[str] = []
    i = 0
    in_code = False
    code_lines: list[str] = []
    code_lang = ""
    mermaid_index = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                code_text = "\n".join(code_lines)
                if code_lang == "mermaid" and asset_dir is not None:
                    mermaid_index += 1
                    svg_path = render_mermaid(code_text, asset_dir, f"mermaid-{mermaid_index}")
                    body.append(f"<p><img src=\"{svg_path.resolve().as_uri()}\" alt=\"Mermaid diagram {mermaid_index}\" /></p>")
                else:
                    body.append(f"<pre><code>{html.escape(code_text)}</code></pre>")
                code_lines = []
                code_lang = ""
                in_code = False
            else:
                in_code = True
                code_lang = stripped[3:].strip().lower()
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            body.append("<hr />")
            i += 1
            continue

        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            table_html = table_to_html(table_lines)
            if table_html:
                body.append(table_html)
            continue

        if stripped.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(inline_format(lines[i].strip()[1:].strip()))
                i += 1
            body.append(f"<blockquote>{'<br />'.join(quote_lines)}</blockquote>")
            continue

        if re.match(r"^#{1,6}\s+", stripped):
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped[level:].strip()
            body.append(f"<h{level}>{inline_format(text)}</h{level}>")
            i += 1
            continue

        if re.match(r"^[-*]\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                item = re.sub(r"^\s*[-*]\s+", "", lines[i].strip())
                items.append(f"<li>{inline_format(item)}</li>")
                i += 1
            body.append("<ul>" + "".join(items) + "</ul>")
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                item = re.sub(r"^\s*\d+\.\s+", "", lines[i].strip())
                items.append(f"<li>{inline_format(item)}</li>")
                i += 1
            body.append("<ol>" + "".join(items) + "</ol>")
            continue

        para_lines = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt:
                break
            if nxt == "---" or nxt.startswith("|") or nxt.startswith(">") or nxt.startswith("```"):
                break
            if re.match(r"^#{1,6}\s+", nxt) or re.match(r"^[-*]\s+", nxt) or re.match(r"^\d+\.\s+", nxt):
                break
            para_lines.append(nxt)
            i += 1
        body.append(f"<p>{inline_format(' '.join(para_lines))}</p>")

    css = """
    body { font-family: Helvetica, Arial, sans-serif; font-size: 11pt; line-height: 1.4; color: #111; margin: 36pt; }
    h1 { font-size: 22pt; margin: 0 0 12pt; text-align: center; }
    h2 { font-size: 16pt; margin: 20pt 0 8pt; border-bottom: 1px solid #999; padding-bottom: 3pt; }
    h3 { font-size: 13pt; margin: 16pt 0 6pt; }
    h4 { font-size: 11pt; margin: 12pt 0 4pt; }
    p, li, blockquote { margin: 0 0 8pt; }
    ul, ol { margin: 0 0 8pt 18pt; }
    blockquote { border-left: 3px solid #999; padding-left: 10pt; color: #333; }
    table { width: 100%; border-collapse: collapse; margin: 8pt 0 12pt; }
    th, td { border: 1px solid #777; padding: 6pt; vertical-align: top; }
    th { background: #efefef; }
    code { font-family: Menlo, Consolas, monospace; font-size: 9pt; }
    pre { background: #f7f7f7; padding: 8pt; border: 1px solid #ddd; white-space: pre-wrap; }
    hr { border: none; border-top: 1px solid #aaa; margin: 14pt 0; }
    img { max-width: 100%; }
    """
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{html.escape(title)}</title><style>{css}</style></head><body>{''.join(body)}</body></html>"


def parse_markdown_table(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    rows = []
    for line in lines:
        if line.strip().startswith("|"):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    if len(rows) < 2:
        return [], []
    return rows[0], rows[2:]


def parse_markdown(markdown_text: str, asset_dir: Path | None = None, render_mermaid_fmt: str = "png") -> list[dict]:
    blocks: list[dict] = []
    lines = markdown_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            lang = stripped[3:].strip().lower()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            code_text = "\n".join(code_lines)
            if lang == "mermaid" and asset_dir is not None:
                idx = 1 + sum(1 for b in blocks if b["type"] == "image")
                img_path = render_mermaid(code_text, asset_dir, f"mermaid-{idx}", render_mermaid_fmt)
                blocks.append({"type": "image", "path": img_path, "alt": f"Mermaid diagram {idx}"})
            else:
                blocks.append({"type": "code", "text": code_text})
            continue

        if stripped == "---":
            blocks.append({"type": "hr"})
            i += 1
            continue

        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            header, rows = parse_markdown_table(table_lines)
            if header:
                blocks.append({"type": "table", "header": header, "rows": rows})
            continue

        if re.match(r"^#{1,6}\s+", stripped):
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped[level:].strip()
            blocks.append({"type": "heading", "level": level, "text": text})
            i += 1
            continue

        if stripped.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            blocks.append({"type": "quote", "text": "\n".join(quote_lines)})
            continue

        if re.match(r"^[-*]\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i].strip()))
                i += 1
            blocks.append({"type": "ul", "items": items})
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i].strip()))
                i += 1
            blocks.append({"type": "ol", "items": items})
            continue

        para = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt:
                break
            if nxt == "---" or nxt.startswith("|") or nxt.startswith(">") or nxt.startswith("```"):
                break
            if re.match(r"^#{1,6}\s+", nxt) or re.match(r"^[-*]\s+", nxt) or re.match(r"^\d+\.\s+", nxt):
                break
            para.append(nxt)
            i += 1
        blocks.append({"type": "p", "text": " ".join(para)})
    return blocks


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Not PNG: {path}")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def emu_size_from_png(path: Path) -> tuple[int, int]:
    width_px, height_px = png_dimensions(path)
    width_emu = int(width_px / PNG_DPI * 914400)
    height_emu = int(height_px / PNG_DPI * 914400)
    ratio = min(MAX_IMAGE_WIDTH_EMU / width_emu, MAX_IMAGE_HEIGHT_EMU / height_emu, 1)
    width_emu = int(width_emu * ratio)
    height_emu = int(height_emu * ratio)
    return width_emu, height_emu


def xml_text_runs(text: str, bold: bool = False, italic: bool = False, code: bool = False, font_size: int | None = None) -> str:
    parts: list[str] = []
    pattern = re.compile(r"(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)")
    pos = 0
    for match in pattern.finditer(text):
        if match.start() > pos:
            parts.append(run_xml(text[pos:match.start()], bold=bold, italic=italic, code=code, font_size=font_size))
        token = match.group(0)
        if token.startswith("`"):
            parts.append(run_xml(token[1:-1], code=True, font_size=font_size))
        elif token.startswith("**"):
            parts.append(run_xml(token[2:-2], bold=True, font_size=font_size))
        elif token.startswith("*"):
            parts.append(run_xml(token[1:-1], italic=True, font_size=font_size))
        pos = match.end()
    if pos < len(text):
        parts.append(run_xml(text[pos:], bold=bold, italic=italic, code=code, font_size=font_size))
    return "".join(parts) or run_xml("", font_size=font_size)


def run_xml(text: str, bold: bool = False, italic: bool = False, code: bool = False, font_size: int | None = None) -> str:
    props = []
    if bold:
        props.append("<w:b/>")
    if italic:
        props.append("<w:i/>")
    if code:
        props.append("<w:rFonts w:ascii=\"Consolas\" w:hAnsi=\"Consolas\"/>")
    if font_size is not None:
        props.append(f"<w:sz w:val=\"{font_size}\"/>")
    prop_xml = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    safe = xml_escape(text)
    preserve = ' xml:space="preserve"' if text.startswith(" ") or text.endswith(" ") or "  " in text else ""
    return f"<w:r>{prop_xml}<w:t{preserve}>{safe}</w:t></w:r>"


def paragraph_xml(text: str = "", style: str | None = None, align: str | None = None, indent_left: int | None = None, spacing_after: int | None = 120, page_break_before: bool = False, outline_level: int | None = None, num_level: int | None = None, keep_next: bool = False, bold: bool = False, font_size: int | None = None) -> str:
    ppr = []
    if style:
        ppr.append(f"<w:pStyle w:val=\"{style}\"/>")
    if align:
        ppr.append(f"<w:jc w:val=\"{align}\"/>")
    if indent_left is not None:
        ppr.append(f"<w:ind w:left=\"{indent_left}\"/>")
    if spacing_after is not None:
        ppr.append(f"<w:spacing w:after=\"{spacing_after}\"/>")
    if page_break_before:
        ppr.append("<w:pageBreakBefore/>")
    if keep_next:
        ppr.append("<w:keepNext/>")
    if outline_level is not None:
        ppr.append(f"<w:outlineLvl w:val=\"{outline_level}\"/>")
    if num_level is not None:
        ppr.append(f"<w:numPr><w:ilvl w:val=\"{num_level}\"/><w:numId w:val=\"1\"/></w:numPr>")
    ppr_xml = f"<w:pPr>{''.join(ppr)}</w:pPr>" if ppr else ""
    content_xml = xml_text_runs(text, bold=bold, font_size=font_size)
    return f"<w:p>{ppr_xml}{content_xml}</w:p>"


def page_break_xml() -> str:
    return "<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>"


def toc_paragraph_xml() -> str:
    return (
        '<w:p><w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        '<w:r><w:t></w:t></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
    )


def heading_display_text(text: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", text).strip()


def hr_paragraph_xml() -> str:
    return (
        "<w:p><w:pPr><w:pBdr><w:bottom w:val=\"single\" w:sz=\"8\" w:space=\"1\" w:color=\"A0A0A0\"/>"
        "</w:pBdr><w:spacing w:after=\"120\"/></w:pPr></w:p>"
    )


def code_paragraph_xml(text: str) -> str:
    runs = []
    for idx, line in enumerate(text.splitlines() or [""]):
        if idx:
            runs.append("<w:r><w:br/></w:r>")
        runs.append(run_xml(line, code=True))
    return (
        "<w:p><w:pPr><w:spacing w:after=\"120\"/><w:shd w:fill=\"F7F7F7\"/>"
        "</w:pPr>" + "".join(runs) + "</w:p>"
    )


def estimate_col_widths(header: list[str], rows: list[list[str]], usable_width_twips: int) -> list[int]:
    col_count = max(len(header), 1)
    min_col_width = 560 if col_count >= 6 else 720
    weights = []
    sample_rows = rows[:20]
    for idx in range(col_count):
        texts = [header[idx] if idx < len(header) else ""]
        texts.extend(row[idx] if idx < len(row) else "" for row in sample_rows)
        max_len = max(len(t.strip()) for t in texts) if texts else 0
        avg_len = sum(len(t.strip()) for t in texts) / max(len(texts), 1)
        header_len = len((header[idx] if idx < len(header) else "").strip())
        weight = max(6, min(32, int(max_len * 0.45 + avg_len * 0.35 + header_len * 0.20)))
        weights.append(weight)
    total_weight = sum(weights) or col_count
    widths = [max(min_col_width, int(usable_width_twips * w / total_weight)) for w in weights]
    if sum(widths) > usable_width_twips:
        scale = usable_width_twips / sum(widths)
        widths = [max(min_col_width, int(w * scale)) for w in widths]
    if sum(widths) > usable_width_twips:
        overflow = sum(widths) - usable_width_twips
        reducible = [max(0, w - min_col_width) for w in widths]
        total_reducible = sum(reducible)
        if total_reducible > 0:
            adjusted = []
            for w, r in zip(widths, reducible):
                cut = int(overflow * (r / total_reducible)) if r else 0
                adjusted.append(max(min_col_width, w - cut))
            widths = adjusted
    diff = usable_width_twips - sum(widths)
    widths[-1] += diff
    return widths


def table_needs_landscape(header: list[str], rows: list[list[str]]) -> bool:
    col_count = len(header)
    lengths = [len(c.strip()) for c in header] + [len(cell.strip()) for row in rows[:20] for cell in row]
    longest = max(lengths, default=0)
    avg_len = (sum(lengths) / len(lengths)) if lengths else 0
    return col_count >= 8 or (col_count >= 6 and longest >= 140) or (col_count >= 7 and avg_len >= 45)


def table_cell_xml(text: str, width: int, header: bool = False) -> str:
    shading = '<w:shd w:fill="EFEFEF"/>' if header else ''
    return (
        f"<w:tc><w:tcPr>{shading}<w:tcW w:w=\"{width}\" w:type=\"dxa\"/><w:noWrap w:val=\"0\"/><w:tcFitText w:val=\"0\"/></w:tcPr>"
        f"{paragraph_xml(text, spacing_after=60)}</w:tc>"
    )


def table_xml(header: list[str], rows: list[list[str]], usable_width_twips: int) -> str:
    col_widths = estimate_col_widths(header, rows, usable_width_twips)
    tbl_pr = (
        f"<w:tblPr><w:tblW w:w=\"{usable_width_twips}\" w:type=\"dxa\"/><w:tblLayout w:type=\"fixed\"/>"
        "<w:tblBorders>"
        "<w:top w:val=\"single\" w:sz=\"8\" w:color=\"777777\"/>"
        "<w:left w:val=\"single\" w:sz=\"8\" w:color=\"777777\"/>"
        "<w:bottom w:val=\"single\" w:sz=\"8\" w:color=\"777777\"/>"
        "<w:right w:val=\"single\" w:sz=\"8\" w:color=\"777777\"/>"
        "<w:insideH w:val=\"single\" w:sz=\"6\" w:color=\"777777\"/>"
        "<w:insideV w:val=\"single\" w:sz=\"6\" w:color=\"777777\"/>"
        "</w:tblBorders></w:tblPr>"
    )
    grid = "<w:tblGrid>" + "".join(f"<w:gridCol w:w=\"{w}\"/>" for w in col_widths) + "</w:tblGrid>"
    header_row = "<w:tr>" + "".join(table_cell_xml(cell, col_widths[idx], header=True) for idx, cell in enumerate(header)) + "</w:tr>"
    body_rows = []
    for row in rows:
        if len(row) < len(header):
            row = row + [""] * (len(header) - len(row))
        body_rows.append("<w:tr>" + "".join(table_cell_xml(cell, col_widths[idx]) for idx, cell in enumerate(row[:len(header)])) + "</w:tr>")
    return f"<w:tbl>{tbl_pr}{grid}{header_row}{''.join(body_rows)}</w:tbl>"


def section_props_xml(landscape: bool = False, include_title_pg: bool = False) -> str:
    width = PAGE_HEIGHT_TWIPS if landscape else PAGE_WIDTH_TWIPS
    height = PAGE_WIDTH_TWIPS if landscape else PAGE_HEIGHT_TWIPS
    orient = ' w:orient="landscape"' if landscape else ''
    title_pg = "<w:titlePg/>" if include_title_pg else ""
    return (
        "<w:sectPr>"
        "<w:headerReference w:type=\"default\" r:id=\"rIdHeader1\"/>"
        "<w:footerReference w:type=\"default\" r:id=\"rIdFooter1\"/>"
        f"{title_pg}"
        f"<w:pgSz w:w=\"{width}\" w:h=\"{height}\"{orient}/>"
        f"<w:pgMar w:top=\"{PAGE_MARGIN_TWIPS}\" w:right=\"{PAGE_MARGIN_TWIPS}\" w:bottom=\"{PAGE_MARGIN_TWIPS}\" w:left=\"{PAGE_MARGIN_TWIPS}\" w:header=\"{PAGE_HEADER_FOOTER_TWIPS}\" w:footer=\"{PAGE_HEADER_FOOTER_TWIPS}\" w:gutter=\"0\"/>"
        "</w:sectPr>"
    )


def section_break_paragraph_xml(landscape: bool = False) -> str:
    return f"<w:p><w:pPr>{section_props_xml(landscape=landscape)}</w:pPr></w:p>"


def image_paragraph_xml(rel_id: str, name: str, width_emu: int, height_emu: int, docpr_id: int, page_break_before: bool = False) -> str:
    page_break = "<w:pageBreakBefore/>" if page_break_before else ""
    return f'''<w:p><w:pPr>{page_break}<w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr><w:r><w:drawing>
    <wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
      <wp:extent cx="{width_emu}" cy="{height_emu}"/>
      <wp:docPr id="{docpr_id}" name="{xml_escape(name)}"/>
      <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
          <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:nvPicPr><pic:cNvPr id="0" name="{xml_escape(name)}"/><pic:cNvPicPr/></pic:nvPicPr>
            <pic:blipFill><a:blip r:embed="{rel_id}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
            <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{width_emu}" cy="{height_emu}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
          </pic:pic>
        </a:graphicData>
      </a:graphic>
    </wp:inline>
    </w:drawing></w:r></w:p>'''


def extract_doc_number(markdown_text: str) -> str:
    m = re.search(r"^\|\s*Nomor Dokumen\s*\|\s*([^|]+?)\s*\|$", markdown_text, re.M)
    return m.group(1).strip() if m else "DOC-NUMBER-TBD"


def build_docx_from_markdown(markdown_text: str, output: Path, title: str) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        asset_dir = tmp / "assets"
        blocks = parse_markdown(markdown_text, asset_dir=asset_dir, render_mermaid_fmt="png")

        body_parts: list[str] = []
        image_rels: list[tuple[str, Path]] = []
        rel_counter = 1
        docpr_id = 1
        doc_number = extract_doc_number(markdown_text)
        major_heading_count = 0

        cover_mode = True
        toc_mode = False
        pending_page_break_after_toc = False
        for block in blocks:
            t = block["type"]
            if t == "heading":
                if block["text"].strip().lower() == "daftar isi":
                    body_parts.append(paragraph_xml(block["text"], style="Heading1", spacing_after=120, page_break_before=True))
                    body_parts.append(toc_paragraph_xml())
                    toc_mode = True
                    pending_page_break_after_toc = True
                elif cover_mode:
                    if block["level"] == 1:
                        body_parts.append(paragraph_xml(block["text"], style="Title", align="center", spacing_after=220, bold=True, font_size=40))
                    else:
                        body_parts.append(paragraph_xml(block["text"], style="Subtitle", align="center", spacing_after=140, bold=True, font_size=26))
                else:
                    style_map = {2: "Heading1", 3: "Heading2", 4: "Heading3", 5: "Heading4"}
                    level_map = {2: 0, 3: 1, 4: 2, 5: 3}
                    style = style_map.get(block["level"], "Heading4")
                    level = level_map.get(block["level"], 3)
                    page_break_before = False
                    if block["level"] == 2:
                        major_heading_count += 1
                        page_break_before = major_heading_count > 1
                    font_size_map = {0: 32, 1: 28, 2: 24, 3: 22}
                    body_parts.append(paragraph_xml(heading_display_text(block["text"]), style=style, spacing_after=160, page_break_before=page_break_before, outline_level=level, num_level=level, keep_next=True, bold=True, font_size=font_size_map.get(level, 22)))
            elif t == "p":
                if toc_mode:
                    toc_mode = False
                    continue
                if pending_page_break_after_toc:
                    body_parts.append(page_break_xml())
                    pending_page_break_after_toc = False
                align = "center" if cover_mode and (block["text"].startswith("**Dipersiapkan oleh:**") or block["text"].startswith("Dipersiapkan oleh:")) else None
                body_parts.append(paragraph_xml(block["text"], align=align))
            elif t == "quote":
                body_parts.append(paragraph_xml(block["text"], indent_left=720))
            elif t == "ul":
                for item in block["items"]:
                    body_parts.append(paragraph_xml(f"• {item}", indent_left=360, spacing_after=60))
            elif t == "ol":
                for idx, item in enumerate(block["items"], start=1):
                    body_parts.append(paragraph_xml(f"{idx}. {item}", indent_left=360, spacing_after=60))
            elif t == "code":
                body_parts.append(code_paragraph_xml(block["text"]))
            elif t == "table":
                use_landscape = table_needs_landscape(block["header"], block["rows"])
                if use_landscape:
                    body_parts.append(section_break_paragraph_xml(landscape=True))
                body_parts.append(table_xml(block["header"], block["rows"], LANDSCAPE_CONTENT_WIDTH_TWIPS if use_landscape else PORTRAIT_CONTENT_WIDTH_TWIPS))
                body_parts.append(paragraph_xml("", spacing_after=60))
                if use_landscape:
                    body_parts.append(section_break_paragraph_xml(landscape=False))
            elif t == "hr":
                cover_mode = False
                body_parts.append(hr_paragraph_xml())
            elif t == "image":
                rel_id = f"rId{rel_counter}"
                rel_counter += 1
                image_rels.append((rel_id, block["path"]))
                width_emu, height_emu = emu_size_from_png(block["path"])
                page_break_before = (not cover_mode) and height_emu >= LARGE_IMAGE_HEIGHT_EMU
                body_parts.append(image_paragraph_xml(rel_id, block.get("alt", block["path"].name), width_emu, height_emu, docpr_id, page_break_before=page_break_before))
                docpr_id += 1

        section = section_props_xml(include_title_pg=True)
        document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
 xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
 xmlns:v="urn:schemas-microsoft-com:vml"
 xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:w10="urn:schemas-microsoft-com:office:word"
 xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
 xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
 xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
 xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
 xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
 mc:Ignorable="w14 wp14">
  <w:body>{''.join(body_parts)}{section}</w:body>
</w:document>'''

        rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
        rels.append('<Relationship Id="rIdHeader1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>')
        rels.append('<Relationship Id="rIdFooter1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>')
        rels.append('<Relationship Id="rIdNumbering1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>')
        for idx, (rel_id, img_path) in enumerate(image_rels, start=1):
            rels.append(f'<Relationship Id="{rel_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{img_path.name}"/>')
        rels.append('</Relationships>')
        document_rels_xml = ''.join(rels)

        header_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p><w:pPr><w:tabs><w:tab w:val="right" w:pos="9000"/></w:tabs><w:spacing w:after="0"/></w:pPr><w:r><w:rPr><w:b/></w:rPr><w:t>{xml_escape(doc_number)}</w:t></w:r><w:r><w:tab/></w:r><w:r><w:t>{xml_escape(title)}</w:t></w:r></w:p>
</w:hdr>'''

        footer_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p><w:pPr><w:tabs><w:tab w:val="center" w:pos="4680"/><w:tab w:val="right" w:pos="9360"/></w:tabs><w:spacing w:after="0"/></w:pPr><w:r><w:t>Halaman </w:t></w:r><w:fldSimple w:instr=" PAGE "><w:r><w:t>1</w:t></w:r></w:fldSimple><w:r><w:tab/></w:r><w:r><w:t>Generated by Markdown DOCX Generator</w:t></w:r></w:p>
</w:ftr>'''

        styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/></w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="120"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:jc w:val="center"/><w:spacing w:before="240" w:after="260"/></w:pPr><w:rPr><w:b/><w:sz w:val="40"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:before="40" w:after="120"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:qFormat/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:pPr><w:outlineLvl w:val="0"/><w:spacing w:before="120" w:after="220"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:qFormat/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:pPr><w:outlineLvl w:val="1"/><w:spacing w:before="120" w:after="140"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:qFormat/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:pPr><w:outlineLvl w:val="2"/><w:spacing w:before="100" w:after="120"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading4"><w:name w:val="heading 4"/><w:basedOn w:val="Normal"/><w:qFormat/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:pPr><w:outlineLvl w:val="3"/><w:spacing w:before="80" w:after="100"/></w:pPr><w:rPr><w:b/><w:sz w:val="22"/></w:rPr></w:style>
</w:styles>'''

        content_types = ['''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
  <Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
  <Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>''']
        content_types_xml = ''.join(content_types)

        package_rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''

        core_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{xml_escape(title)}</dc:title>
  <dc:creator>Pi Coding Agent</dc:creator>
  <cp:lastModifiedBy>Pi Coding Agent</cp:lastModifiedBy>
</cp:coreProperties>'''

        app_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Pi Coding Agent</Application>
</Properties>'''

        numbering_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="0">
    <w:multiLevelType w:val="multilevel"/>
    <w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/><w:lvlJc w:val="left"/></w:lvl>
    <w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1.%2."/><w:lvlJc w:val="left"/></w:lvl>
    <w:lvl w:ilvl="2"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1.%2.%3."/><w:lvlJc w:val="left"/></w:lvl>
    <w:lvl w:ilvl="3"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1.%2.%3.%4."/><w:lvlJc w:val="left"/></w:lvl>
  </w:abstractNum>
  <w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>'''

        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", content_types_xml)
            zf.writestr("_rels/.rels", package_rels_xml)
            zf.writestr("word/document.xml", document_xml)
            zf.writestr("word/_rels/document.xml.rels", document_rels_xml)
            zf.writestr("word/styles.xml", styles_xml)
            zf.writestr("word/numbering.xml", numbering_xml)
            zf.writestr("word/header1.xml", header_xml)
            zf.writestr("word/footer1.xml", footer_xml)
            zf.writestr("docProps/core.xml", core_xml)
            zf.writestr("docProps/app.xml", app_xml)
            for _, img_path in image_rels:
                zf.write(img_path, f"word/media/{img_path.name}")
    return output


def export_markdown(source: Path, fmt: str, output: Path, title: str | None = None) -> Path:
    if not source.exists():
        raise FileNotFoundError(f"Markdown source missing: {source}")

    output.parent.mkdir(parents=True, exist_ok=True)

    if fmt == "md":
        shutil.copyfile(source, output)
        return output

    markdown_text = source.read_text(encoding="utf-8")

    if fmt == "html":
        asset_dir = output.parent / f"{output.stem}-assets"
        html_text = markdown_to_html(markdown_text, title or source.stem, asset_dir)
        output.write_text(html_text, encoding="utf-8")
        return output

    return build_docx_from_markdown(markdown_text, output, title or source.stem)


def export_template(template_name: str, fmt: str, output: Path | None, templates: dict[str, Path]) -> Path:
    source = templates[template_name]
    if not source.exists():
        raise FileNotFoundError(f"Template source missing: {source}")

    if output is None:
        DEFAULT_OUT_DIR.mkdir(parents=True, exist_ok=True)
        output = DEFAULT_OUT_DIR / f"{slugify(template_name)}-template.{fmt}"

    return export_markdown(source, fmt, output, f"{template_name.title()} Template")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Markdown or a named template into md/html/docx")
    parser.add_argument("--template", choices=sorted(DEFAULT_TEMPLATES), help="Template name")
    parser.add_argument("--template-dir", type=Path, default=DEFAULT_TEMPLATE_DIR, help="Directory containing architecture-template.md and fsd-template.md")
    parser.add_argument("--source", type=Path, help="Markdown source file")
    parser.add_argument("--title", help="Document title for HTML/DOCX export")
    parser.add_argument("--format", choices=sorted(FORMATS), help="Target format")
    parser.add_argument("--output", type=Path, help="Target file path")
    parser.add_argument("--list", action="store_true", help="List available templates and formats")
    args = parser.parse_args()

    if args.list:
        print("templates:", ", ".join(sorted(DEFAULT_TEMPLATES)))
        print("formats:", ", ".join(sorted(FORMATS)))
        return 0

    if not args.format:
        parser.error("--format required unless --list used")
    if bool(args.template) == bool(args.source):
        parser.error("choose exactly one of --template or --source")
    if args.output is None:
        parser.error("--output required")

    templates = {
        "architecture": args.template_dir / "architecture-template.md",
        "fsd": args.template_dir / "fsd-template.md",
    }
    output = export_template(args.template, args.format, args.output, templates) if args.template else export_markdown(args.source, args.format, args.output, args.title)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
