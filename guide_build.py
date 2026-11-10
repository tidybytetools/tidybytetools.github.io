"""Guide markdown → HTML helpers for the Tidy Byte Tools site."""
from __future__ import annotations

import html as htmlmod
import re
from pathlib import Path


def parse_guide(path: Path) -> dict:
    text = path.read_text()
    meta: dict[str, str] = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            body = parts[2].lstrip("\n")
    slug = meta.get("slug") or path.stem
    title = meta.get("title") or slug
    description = meta.get("description") or title
    return {
        "slug": slug,
        "title": title,
        "description": description,
        "body_md": body,
        "path": path,
    }


def md_to_html(md: str, path_prefix_fn) -> str:
    """Small Markdown subset → HTML for our how-to guides."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    in_code = False
    code_buf: list[str] = []
    in_ul = False
    table_rows: list[str] = []

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def flush_table() -> None:
        nonlocal table_rows
        if not table_rows:
            return
        out.append('<div class="table-wrap"><table>')
        for ri, row in enumerate(table_rows):
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            if ri == 1 and all(set(c) <= set("-: ") for c in cells):
                continue
            tag = "th" if ri == 0 else "td"
            out.append(
                "<tr>"
                + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells)
                + "</tr>"
            )
        out.append("</table></div>")
        table_rows = []

    def inline(s: str) -> str:
        def repl_code(m: re.Match) -> str:
            return "<code>" + htmlmod.escape(m.group(1)) + "</code>"

        s = re.sub(r"`([^`]+)`", repl_code, s)

        def repl_link(m: re.Match) -> str:
            label, url = m.group(1), m.group(2)
            if url.startswith("./") and url.endswith(".md"):
                stem = url[2:-3]
                url = "GUIDE_LINK:" + stem
            return f'<a href="{htmlmod.escape(url)}">{htmlmod.escape(label)}</a>'

        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl_link, s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        return s

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            close_ul()
            flush_table()
            if not in_code:
                in_code = True
                code_buf = []
            else:
                out.append(
                    "<pre><code>"
                    + htmlmod.escape("\n".join(code_buf))
                    + "</code></pre>"
                )
                in_code = False
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue
        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            close_ul()
            table_rows.append(line)
            i += 1
            continue
        flush_table()
        if line.startswith("# "):
            close_ul()
            out.append("<h1>" + inline(line[2:].strip()) + "</h1>")
            i += 1
            continue
        if line.startswith("## "):
            close_ul()
            out.append("<h2>" + inline(line[3:].strip()) + "</h2>")
            i += 1
            continue
        if line.startswith("### "):
            close_ul()
            out.append("<h3>" + inline(line[4:].strip()) + "</h3>")
            i += 1
            continue
        if re.match(r"^- ", line):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append("<li>" + inline(line[2:].strip()) + "</li>")
            i += 1
            continue
        close_ul()
        if not line.strip():
            i += 1
            continue
        out.append("<p>" + inline(line.strip()) + "</p>")
        i += 1
    close_ul()
    flush_table()
    if in_code:
        out.append(
            "<pre><code>" + htmlmod.escape("\n".join(code_buf)) + "</code></pre>"
        )
    return "\n".join(out)


def load_guides(guides_dir: Path) -> list[dict]:
    if not guides_dir.exists():
        return []
    return [parse_guide(p) for p in sorted(guides_dir.glob("how-to-*.md"))]


def rewrite_guide_links(html: str, guides: list[dict], path_prefix_fn) -> str:
    by_stem = {g["path"].stem: g for g in guides}

    def repl(m: re.Match) -> str:
        stem = m.group(1)
        g = by_stem.get(stem)
        if not g:
            return path_prefix_fn("/guides/")
        return path_prefix_fn(f"/guides/{g['slug']}/")

    return re.sub(r"GUIDE_LINK:([A-Za-z0-9_-]+)", repl, html)
