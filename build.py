#!/usr/bin/env python3
"""Build the Tidy Byte Tools static website into this folder."""
from __future__ import annotations

import html
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
ASSETS = ROOT / "assets"
BRAND = Path("/workspace/design/brand")
PRODUCTS_DIR = Path("/workspace/products")
BASE = "https://tidybytetools.github.io"
YEAR = "2026"

# ---------------------------------------------------------------------------
# Live catalog. Only include public, working listings.
# Rechecked at build time for the two Apify actors that may still be unpublished.
# ---------------------------------------------------------------------------

CATEGORIES = [
    ("pdf", "PDF & docs"),
    ("data", "CSV & data"),
    ("web", "Links & web"),
    ("ai", "AI / RAG"),
    ("media", "Images & video"),
]


def V(place, label, price, url=None, urls=None, note=None, cta=None, card_price=None):
    return {
        "place": place,
        "label": label,
        "price": price,
        "url": url,
        "urls": urls or [],
        "note": note,
        "cta": cta,
        "card_price": card_price or price,
    }


TOOLS = [
    {
        "slug": "pdf-table-pull",
        "name": "PDF Table Pull",
        "category": "pdf",
        "tagline": "Pull tables out of PDFs into Excel, CSV, or JSON.",
        "summary": (
            "Copying tables out of a PDF by hand is slow, and pasting them into Excel "
            "often wrecks the columns. This tool finds the tables and saves clean rows."
        ),
        "does": [
            "Finds tables in a PDF, including tables that run across pages (paid and Apify).",
            "Saves Excel, CSV, or JSON (the free lite version saves CSV only).",
            "Reads scanned pages with OCR in the paid and Apify versions.",
            "The free lite tool also works as an MCP server for AI apps.",
        ],
        "thumb": PRODUCTS_DIR / "pdf-table-pull" / "thumb.png",
        "cover": PRODUCTS_DIR / "pdf-table-pull" / "cover.png",
        "versions": [
            V(
                "Apify",
                "Pay per use",
                "$0.003 per page with a table",
                "https://apify.com/tidybytetools/pdf-table-pull",
                card_price="$0.003/page",
                note="Pages with no tables are free. Scanned pages read with OCR are $0.01 each.",
                cta="Open in Apify",
            ),
            V(
                "Gumroad",
                "For your computer",
                "$12",
                "https://tidybyte.gumroad.com/l/hkxqxh",
                note="Excel, CSV and JSON output, scanned PDFs, and tables that run across pages.",
                cta="Buy on Gumroad",
            ),
            V(
                "GitHub & PyPI",
                "Free lite",
                "Free",
                urls=[
                    ("GitHub", "https://github.com/tidybytetools/pdf-table-pull-lite"),
                    ("PyPI", "https://pypi.org/project/pdf-table-pull-lite/"),
                    ("Gumroad", "https://tidybyte.gumroad.com/l/qrbzvo"),
                ],
                note="Text PDFs to CSV. CLI and MCP server. No Excel, no OCR, no joining tables across pages.",
            ),
        ],
        "repos": ["pdf-table-pull-lite"],
    },
    {
        "slug": "doc2md",
        "name": "Doc to Markdown",
        "category": "pdf",
        "tagline": "Turn PDFs, Word files, and web pages into clean Markdown.",
        "summary": (
            "Get Markdown you can use in notes, docs, or AI apps. Tables stay as "
            "Markdown tables. The paid version also writes chunks for AI search."
        ),
        "does": [
            "Turns text PDFs and HTML into clean Markdown (all versions).",
            "Keeps tables as real Markdown tables.",
            "The paid version also reads Word files, whole folders, and writes RAG chunks.",
            "The Apify version can read scanned PDFs with OCR.",
            "The free lite tool includes an MCP server for AI apps.",
        ],
        "thumb": PRODUCTS_DIR / "doc2md" / "thumb.png",
        "cover": PRODUCTS_DIR / "doc2md" / "cover.png",
        "versions": [
            V(
                "Apify",
                "Pay per use",
                "$0.003 per file",
                "https://apify.com/tidybytetools/doc-to-markdown",
                note="First 20 PDF pages are included. Extra PDF pages are $0.0003 each. Scanned pages with OCR are $0.005. Failed files are free.",
                cta="Open in Apify",
            ),
            V(
                "Gumroad",
                "For your computer",
                "$12",
                "https://tidybyte.gumroad.com/l/frlkv",
                note="PDF, Word and HTML, plus RAG chunks with heading paths and page numbers. Runs offline.",
                cta="Buy on Gumroad",
            ),
            V(
                "GitHub & PyPI",
                "Free lite",
                "Free",
                urls=[
                    ("GitHub", "https://github.com/tidybytetools/doc2md-lite"),
                    ("PyPI", "https://pypi.org/project/doc2md-lite/"),
                ],
                note="Text PDF or HTML, one file at a time. No Word files, no folders, no RAG chunks, no OCR.",
            ),
        ],
        "repos": ["doc2md-lite"],
    },
    {
        "slug": "sheet-scrub",
        "name": "CSV & spreadsheet cleanup",
        "category": "data",
        "tagline": "Clean messy CSV and Excel files: dates, phones, emails, and duplicates.",
        "summary": (
            "Got a sheet full of extra spaces, mixed date styles, and repeat rows? "
            "These tools tidy the file and give you a clean table back."
        ),
        "does": [
            "Fixes messy column names and extra spaces.",
            "Makes dates, emails, and phone numbers look the same.",
            "Removes duplicate and empty rows.",
            "Works on CSV and Excel (the Apify tool also reads JSON tables).",
        ],
        "thumb": PRODUCTS_DIR / "sheet-scrub" / "thumb.png",
        "cover": PRODUCTS_DIR / "sheet-scrub" / "cover.png",
        "versions": [
            V(
                "Apify",
                "Pay per use",
                "$0.0005 per clean row",
                "https://apify.com/tidybytetools/csv-excel-data-cleaner",
                card_price="$0.0005/row",
                note="Removed rows are free. Gives you a clean CSV and a short report of what changed.",
                cta="Open in Apify",
            ),
            V(
                "Gumroad",
                "For your computer",
                "$9",
                "https://tidybyte.gumroad.com/l/cknndc",
                note="sheet-scrub: one command for messy Excel and CSV files. Runs on your computer.",
                cta="Buy on Gumroad",
            ),
        ],
        "repos": [],
    },
    {
        "slug": "json-shaper",
        "name": "JSON Shaper",
        "category": "data",
        "tagline": "Turn messy notes, CSV, and Markdown tables into clean JSON.",
        "summary": (
            "Free converters do well with neat CSV. JSON Shaper is for the messy stuff: "
            "pasted notes, key: value lists, and tables."
        ),
        "does": [
            "Turns key: value notes, CSV/TSV, and Markdown tables into typed JSON.",
            "The paid version also parses app logs and splits a one-line US address.",
            "The free lite tool is a CLI and an MCP server, and runs with no extra packages for the core tool.",
        ],
        "thumb": PRODUCTS_DIR / "json-shaper" / "thumb.png",
        "cover": PRODUCTS_DIR / "json-shaper" / "cover.png",
        "versions": [
            V(
                "Gumroad",
                "For your computer",
                "From $5",
                "https://tidybyte.gumroad.com/l/cznmeo",
                note="Pay what you want, $5 minimum. Adds app logs and a US address splitter.",
                cta="Buy on Gumroad",
            ),
            V(
                "GitHub & PyPI",
                "Free lite",
                "Free",
                urls=[
                    ("GitHub", "https://github.com/tidybytetools/json-shaper-lite"),
                    ("PyPI", "https://pypi.org/project/json-shaper-lite/"),
                    ("Gumroad", "https://tidybyte.gumroad.com/l/txytmi"),
                ],
                note="Notes, CSV/TSV and Markdown tables. CLI and MCP server. No log parsing, no address splitter.",
            ),
        ],
        "repos": ["json-shaper-lite"],
    },
    {
        "slug": "lead-sheet-fixer",
        "name": "Lead Sheet Fixer",
        "category": "data",
        "tagline": "Clean a lead list: fix phones, check emails, and merge duplicates.",
        "summary": (
            "Clean the lead list you already have. Phones are formatted, bad emails "
            "are flagged, names can be split, and duplicate rows can be merged."
        ),
        "does": [
            "Fixes and formats phone numbers.",
            "Flags bad or odd email addresses.",
            "Merges duplicate rows.",
            "Works on CSV and Excel. Runs on your computer.",
        ],
        "thumb": PRODUCTS_DIR / "lead-sheet-fixer" / "thumb.png",
        "cover": PRODUCTS_DIR / "lead-sheet-fixer" / "cover.png",
        "versions": [
            V(
                "Gumroad",
                "For your computer",
                "$9",
                "https://tidybyte.gumroad.com/l/iaiacv",
                cta="Buy on Gumroad",
            ),
        ],
        "repos": [],
    },
    {
        "slug": "phone-validator",
        "name": "Phone Number Validator",
        "category": "data",
        "tagline": "Check phone numbers and format them as E.164, in bulk, offline.",
        "summary": (
            "See if each number is valid and write it in three common formats. "
            "The tool also shows country, line type, area, and time zone. "
            "It works offline and never calls or texts anyone."
        ),
        "does": [
            "Says if each number is valid and possible.",
            "Writes the number as E.164, international, and national.",
            "Shows country, line type, area, and time zones.",
            "Removes repeats for free.",
            "Uses Google's open phone rules. Nothing is called or texted.",
        ],
        "thumb": None,  # generated
        "cover": None,
        "gen_art": {
            "title": "phone-validator",
            "sub": "Bulk phones to E.164, offline",
            "badge": "PAY PER USE",
            "vis": "phone",
        },
        "versions": [
            V(
                "Apify",
                "Pay per use",
                "$0.001 per number",
                "https://apify.com/tidybytetools/phone-number-validator-formatter",
                card_price="$0.001/number",
                cta="Open in Apify",
            ),
        ],
        "repos": [],
    },
    {
        "slug": "data-cleanup-bundle",
        "name": "Data Cleanup Bundle",
        "category": "data",
        "tagline": "Three desktop tools together: PDF tables, sheet cleanup, and JSON Shaper.",
        "summary": (
            "Get pdf-table-pull, sheet-scrub, and json-shaper in one purchase. "
            "Bought one by one they cost at least $26. The bundle is $19, so you save $7."
        ),
        "does": [
            "pdf-table-pull: PDF tables to Excel, CSV, or JSON, including scans.",
            "sheet-scrub: clean messy Excel and CSV files.",
            "json-shaper: notes, tables, and logs into clean JSON.",
            "All three run on your computer.",
        ],
        "thumb": PRODUCTS_DIR / "data-cleanup-bundle" / "thumb.png",
        "cover": PRODUCTS_DIR / "data-cleanup-bundle" / "cover.png",
        "versions": [
            V(
                "Gumroad",
                "For your computer",
                "$19",
                "https://tidybyte.gumroad.com/l/qnlxiy",
                note="Saves $7 versus buying the three tools separately at their listed prices ($12 + $9 + $5).",
                cta="Buy on Gumroad",
            ),
        ],
        "repos": [],
    },
    {
        "slug": "link-check",
        "name": "Broken Link Checker",
        "category": "web",
        "tagline": "Check a list of links for status codes, redirects, and broken pages.",
        "summary": (
            "Paste a list, give a sitemap, or scan pages for their links. "
            "Get a clear report of what works, what is broken, and where redirects end up."
        ),
        "does": [
            "Shows the status code, redirect chain, and final URL for each link.",
            "The Apify version can also read a sitemap or scan pages for links, and follows robots.txt.",
            "The free lite tool checks a text file of links on your computer, includes an MCP server, and is also on the GitHub Marketplace as an Action.",
        ],
        "thumb": PRODUCTS_DIR / "link-check" / "thumb.png",
        "cover": PRODUCTS_DIR / "link-check" / "cover.png",
        "versions": [
            V(
                "Apify",
                "Pay per use",
                "$0.001 per link",
                "https://apify.com/tidybytetools/broken-link-checker",
                card_price="$0.001/link",
                note="Scanning a page for links is $0.002 per page. Duplicates and links skipped by robots.txt are free.",
                cta="Open in Apify",
            ),
            V(
                "GitHub & PyPI",
                "Free lite",
                "Free",
                urls=[
                    ("GitHub", "https://github.com/tidybytetools/link-check-lite"),
                    ("PyPI", "https://pypi.org/project/link-check-lite/"),
                    ("GitHub Action", "https://github.com/marketplace/actions/link-check-lite"),
                ],
                note="Checks a text file of links. CLI, MCP server, and a GitHub Action. No sitemap input, no speed flags, no CSV report in the lite version.",
            ),
        ],
        "repos": ["link-check-lite"],
    },
    {
        "slug": "server-pulse",
        "name": "Server Pulse",
        "category": "web",
        "tagline": "Get a Discord alert when a website or server goes down.",
        "summary": (
            "Server Pulse watches a site or server and sends a Discord message if it goes down. "
            "It can also post Stripe and PayPal donation alerts to Discord."
        ),
        "does": [
            "Watches a website or server and alerts you in Discord when it is down.",
            "Can also send Stripe and PayPal donation alerts to Discord.",
            "Runs on your computer.",
        ],
        "thumb": PRODUCTS_DIR / "server-pulse" / "thumb.png",
        "cover": PRODUCTS_DIR / "server-pulse" / "cover.png",
        "versions": [
            V(
                "Gumroad",
                "For your computer",
                "$19",
                "https://tidybyte.gumroad.com/l/cjatbj",
                cta="Buy on Gumroad",
            ),
        ],
        "repos": [],
    },
    {
        "slug": "markdown-chunker",
        "name": "Markdown Chunker for RAG",
        "category": "ai",
        "tagline": "Split Markdown into chunks for AI search, with heading paths kept.",
        "summary": (
            "Split a Markdown file by heading so each chunk stays on one topic. "
            "Code blocks and tables stay whole when they fit. Each chunk keeps its heading path and line numbers. "
            "This is plain code, not an AI model, so the same file always gives the same chunks."
        ),
        "does": [
            "Splits by headings first, so each chunk stays on one topic.",
            "Avoids cutting a code block or table in the middle when it fits.",
            "Gives each chunk an id, heading path, and line numbers.",
            "The free lite tool is a CLI and an MCP server you run on your computer.",
        ],
        "thumb": None,
        "cover": None,
        "gen_art": {
            "title": "markdown-chunker",
            "sub": "Split Markdown by heading for RAG",
            "badge": None,
            "vis": "chunk",
        },
        "versions": [
            V(
                "Apify",
                "Pay per use",
                "$0.0001 per chunk",
                "https://apify.com/tidybytetools/markdown-rag-chunker",
                card_price="$0.0001/chunk",
                cta="Open in Apify",
            ),
            V(
                "GitHub & PyPI",
                "Free lite",
                "Free",
                urls=[
                    ("GitHub", "https://github.com/tidybytetools/md-chunk-lite"),
                    ("PyPI", "https://pypi.org/project/md-chunk-lite/"),
                ],
                note="Markdown and plain text. CLI and MCP server. It does not read PDF or Word files.",
            ),
        ],
        "repos": ["md-chunk-lite"],
    },
    {
        "slug": "gif-forge",
        "name": "GIF Forge",
        "category": "media",
        "tagline": "Turn a folder of videos into small, sharp GIFs, offline.",
        "summary": (
            "Drop in a folder of clips and get a folder of small, sharp, looping GIFs. "
            "It can also remove solid image backgrounds, all on your computer."
        ),
        "does": [
            "Turns videos into small, sharp GIFs in batches.",
            "Can remove solid backgrounds from images.",
            "Runs offline on your computer.",
        ],
        "thumb": PRODUCTS_DIR / "gif-forge" / "thumb.png",
        "cover": PRODUCTS_DIR / "gif-forge" / "cover.png",
        "versions": [
            V(
                "Gumroad",
                "For your computer",
                "$7",
                "https://tidybyte.gumroad.com/l/vjbsqs",
                cta="Buy on Gumroad",
            ),
        ],
        "repos": [],
    },
]

# Optional Apify actors: include only if the public store page returns 200.
OPTIONAL_APIFY = [
    {
        "slug": "json-to-csv",
        "name": "JSON to CSV Converter",
        "category": "data",
        "tagline": "Flatten nested JSON or JSON Lines into a CSV table.",
        "summary": (
            "Turn nested JSON into a flat table for Excel and Google Sheets. "
            "You pick how lists are handled."
        ),
        "does": [
            "Flattens nested objects, such as user.name and user.address.city.",
            "Reads JSON, JSON Lines, and Apify dataset links.",
            "Saves a CSV file and also puts rows in the dataset.",
        ],
        "thumb": None,
        "cover": None,
        "gen_art": {
            "title": "json-to-csv",
            "sub": "Flatten nested JSON for Excel",
            "badge": "PAY PER USE",
        },
        "versions": [
            V(
                "Apify",
                "Pay per use",
                "$0.0001 per row",
                "https://apify.com/tidybytetools/json-to-csv-flattener",
                cta="Open in Apify",
            ),
        ],
        "repos": [],
        "apify_url": "https://apify.com/tidybytetools/json-to-csv-flattener",
    },
    {
        "slug": "csv-encoding-fixer",
        "name": "CSV Encoding Fixer",
        "category": "data",
        "tagline": "Fix broken characters in CSV files and split large files.",
        "summary": (
            "Fixes garbled letters such as Ã© instead of é, then saves clean UTF-8 "
            "that opens right in Excel. Can also split a large file and keep the header on every part."
        ),
        "does": [
            "Finds and fixes garbled letters like Ã©, â€™ and Ã¼.",
            "Reads UTF-8, UTF-16, and old Windows files.",
            "Can split big files into parts that each keep the header.",
        ],
        "thumb": None,
        "cover": None,
        "gen_art": {
            "title": "csv-encoding-fixer",
            "sub": "Fix mojibake, split big CSVs",
            "badge": "PAY PER USE",
        },
        "versions": [
            V(
                "Apify",
                "Pay per use",
                "$0.01 per file",
                "https://apify.com/tidybytetools/csv-encoding-fixer-splitter",
                cta="Open in Apify",
            ),
        ],
        "repos": [],
        "apify_url": "https://apify.com/tidybytetools/csv-encoding-fixer-splitter",
    },
]


def e(text: str) -> str:
    return html.escape(text, quote=True)


def http_ok(url: str, timeout: int = 20) -> bool:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "TidyByteToolsSiteBot/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return 200 <= res.status < 400
    except Exception:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "TidyByteToolsSiteBot/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as res:
                return 200 <= res.status < 400
        except Exception:
            return False


def live_tools() -> list[dict]:
    tools = list(TOOLS)
    for item in OPTIONAL_APIFY:
        url = item["apify_url"]
        if http_ok(url):
            print(f"including optional {item['slug']} (live)")
            tools.append(item)
        else:
            print(f"skipping optional {item['slug']} (not a public 200)")
    return tools


def subset_fonts() -> None:
    from fontTools.subset import Subsetter, Options
    from fontTools.ttLib import TTFont

    outdir = ASSETS / "fonts"
    outdir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(BRAND / "fonts" / "OFL.txt", outdir / "OFL.txt")

    # Basic Latin, Latin-1, Latin Extended-A, plus common punctuation and arrows.
    unicodes = set()
    for start, end in (
        (0x0009, 0x000D),
        (0x0020, 0x007E),
        (0x00A0, 0x00FF),
        (0x0100, 0x017F),
        (0x2010, 0x2027),
        (0x2030, 0x203A),
        (0x2044, 0x2044),
        (0x20AC, 0x20AC),  # euro
        (0x2190, 0x2193),
        (0x2212, 0x2212),
    ):
        unicodes.update(range(start, end + 1))

    sources = {
        "geist-latin.woff2": BRAND / "fonts" / "Geist-VariableFont_wght.ttf",
        "geist-mono-latin.woff2": BRAND / "fonts" / "GeistMono-VariableFont_wght.ttf",
    }
    for name, src in sources.items():
        dest = outdir / name
        font = TTFont(src)
        options = Options()
        options.layout_features = ["*"]
        options.hinting = False
        options.desubroutinize = True
        options.retain_gids = False
        subsetter = Subsetter(options=options)
        subsetter.populate(unicodes=unicodes)
        subsetter.subset(font)
        font.flavor = "woff2"
        font.save(dest)
        print(f"font {name} {dest.stat().st_size // 1024}KB")


def optimize_image(src: Path, dest_stem: Path, max_side: int, quality: int = 82) -> None:
    im = Image.open(src)
    if im.mode in ("P", "RGBA"):
        # Keep transparency only if needed; product thumbs are RGB.
        if im.mode == "P":
            im = im.convert("RGBA")
        if dest_stem.name.endswith("lockup") or "mark" in dest_stem.name:
            pass
        background = Image.new("RGB", im.size, (244, 247, 245))
        if im.mode == "RGBA":
            background.paste(im, mask=im.split()[-1])
            im = background
        else:
            im = im.convert("RGB")
    elif im.mode != "RGB":
        im = im.convert("RGB")
    im = im.copy()
    im.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    dest_stem.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest_stem.with_suffix(".webp"), "WEBP", quality=quality, method=6)
    im.save(dest_stem.with_suffix(".png"), "PNG", optimize=True)


def generate_missing_art(tools: list[dict]) -> None:
    """Make on-brand thumbs for tools that have no existing cover art."""
    sys.path.insert(0, str(BRAND))
    from brand_kit import page  # type: ignore
    from importlib.machinery import SourceFileLoader

    render = SourceFileLoader("tb_render", "/workspace/design/render.py").load_module()
    shot = render.shot
    art_dir = ASSETS / "img" / "generated"
    art_dir.mkdir(parents=True, exist_ok=True)
    for tool in tools:
        if tool.get("thumb") and Path(tool["thumb"]).exists() and tool.get("cover") and Path(tool["cover"]).exists():
            continue
        info = tool.get("gen_art") or {"title": tool["slug"], "sub": tool["tagline"], "badge": None}
        kind = info.get("vis")
        if kind == "phone":
            vis = (
                '<div style="display:flex;flex-direction:column;gap:10px;align-items:center;font-family:Geist,sans-serif;color:#0D1512">'
                '<div style="background:#fff;border:1px solid #DCE4E0;border-radius:12px;padding:14px 18px;min-width:230px">'
                '<div style="font-size:13px;color:#56645E;margin-bottom:8px">+1 (555) 123-4567</div>'
                '<div style="font-size:13px;color:#0A7F4C;font-weight:650">→ +15551234567</div>'
                '<div style="font-size:13px;color:#0A7F4C;font-weight:650">→ +1 555 123 4567</div>'
                '<div style="margin-top:8px;font-size:11px;color:#56645E">US · mobile · valid</div>'
                '</div></div>'
            )
        elif kind == "chunk":
            vis = (
                '<div style="background:#fff;border:1px solid #DCE4E0;border-radius:12px;padding:14px 16px;min-width:250px;font-family:Geist,sans-serif;color:#0D1512">'
                '<div style="font-size:12px;padding:7px 0;border-bottom:1px solid #DCE4E0"><strong>Install</strong> <span style="color:#56645E;float:right">lines 1–20</span></div>'
                '<div style="font-size:12px;padding:7px 0;border-bottom:1px solid #DCE4E0"><strong>Install / Setup</strong> <span style="color:#56645E;float:right">21–54</span></div>'
                '<div style="font-size:12px;padding:7px 0"><strong>Install / Use it</strong> <span style="color:#56645E;float:right">55–102</span></div>'
                '</div>'
            )
        else:
            vis = (
                '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center">'
                '<div style="width:72%;max-width:280px;border:1px solid #DCE4E0;border-radius:12px;'
                'background:#fff;padding:18px 16px;font-family:Geist,sans-serif">'
                f'<div style="font-size:22px;font-weight:700;letter-spacing:-0.03em;color:#0D1512">{html.escape(info["title"])}</div>'
                "</div></div>"
            )
        if not tool.get("thumb") or not Path(tool.get("thumb") or "").exists():
            html_thumb = page(
                600, 600,
                title=info["title"],
                sub=info["sub"],
                tag=None,
                vis=vis,
                mode="thumb",
                theme="light",
                badge=info.get("badge"),
            )
            dest = art_dir / f"{tool['slug']}-thumb.png"
            shot(html_thumb, str(dest), 600, 600)
            tool["thumb"] = dest
            print("generated thumb", dest)
        if not tool.get("cover") or not Path(tool.get("cover") or "").exists():
            html_cover = page(
                1280, 720,
                title=info["title"],
                sub=info["sub"],
                tag="pay per use · tidy byte tools" if info.get("badge") == "PAY PER USE" else "tidy byte tools",
                vis=vis,
                mode="cover",
                theme="light",
                badge=info.get("badge"),
            )
            dest = art_dir / f"{tool['slug']}-cover.png"
            shot(html_cover, str(dest), 1280, 720)
            tool["cover"] = dest
            print("generated cover", dest)



GALLERIES = {
    "pdf-table-pull": {
        "src": Path("/tmp/tbt-galleries/assets/img/tools/pdf-table-pull-gallery.png"),
        "alt": "A real run of pdf-table-pull: a sample PDF goes in, and an Excel file comes out with real numbers. The value (40) became -40, and a table that ran across two pages was joined.",
    },
    "doc2md": {
        "src": Path("/tmp/tbt-galleries/assets/img/tools/doc2md-gallery.png"),
        "alt": "A real run of doc2md turning a sample file into clean Markdown with a table kept as a table.",
    },
    "gif-forge": {
        "src": Path("/tmp/tbt-galleries/assets/img/tools/gif-forge-gallery.png"),
        "alt": "A sample of gif-forge turning a short clip into a GIF and removing a solid background from a sprite.",
    },
    "json-shaper": {
        "src": Path("/tmp/tbt-galleries/assets/img/tools/json-shaper-gallery.png"),
        "alt": "A real run of json-shaper turning a sample log file and a Markdown table into clean JSON.",
    },
    "lead-sheet-fixer": {
        "src": Path("/tmp/tbt-galleries/assets/img/tools/lead-sheet-fixer-gallery.png"),
        "alt": "A real run of lead-sheet-fixer cleaning a messy lead list: names split, phones made consistent, and duplicates merged.",
    },
    "link-check": {
        "src": Path("/tmp/tbt-galleries/assets/img/tools/link-check-gallery.png"),
        "alt": "A sample run of link-check showing status codes and redirect results for a list of URLs.",
    },
    "server-pulse": {
        "src": Path("/tmp/tbt-galleries/assets/img/tools/server-pulse-gallery.png"),
        "alt": "Sample Discord alerts from server-pulse: a down alert, an up alert, and a donation alert.",
    },
    "sheet-scrub": {
        "src": Path("/tmp/tbt-galleries/assets/img/tools/sheet-scrub-gallery.png"),
        "alt": "A before and after of sheet-scrub cleaning a messy contact list: names cased, phones and dates made consistent, a duplicate row removed, and a bad email flagged.",
    },
}

ALIASES = {
    "phone-number-validator": "phone-validator",
    "csv-excel-data-cleaner": "sheet-scrub",
}


def copy_galleries(tools):
    dest_dir = ASSETS / "img" / "galleries"
    dest_dir.mkdir(parents=True, exist_ok=True)
    by_slug = {tool["slug"]: tool for tool in tools}
    for slug, info in GALLERIES.items():
        if slug not in by_slug:
            continue
        src = Path(info["src"])
        if not src.exists():
            print("missing gallery", src)
            continue
        optimize_image(src, dest_dir / slug, 1280, 80)
        by_slug[slug]["gallery_src"] = "/assets/img/galleries/%s.webp" % slug
        by_slug[slug]["gallery_png"] = "/assets/img/galleries/%s.png" % slug
        by_slug[slug]["gallery_alt"] = info["alt"]
        print("gallery", slug)


def write_aliases(tools):
    slugs = {tool["slug"] for tool in tools}
    for alias, target in ALIASES.items():
        if target not in slugs:
            continue
        dest = "/tools/%s/" % target
        html_text = (
            "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
            "  <meta charset=\"utf-8\">\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "  <title>This page has moved \u2014 Tidy Byte Tools</title>\n"
            "  <link rel=\"canonical\" href=\"%s\">\n"
            "  <meta http-equiv=\"refresh\" content=\"0; url=%s\">\n"
            "  <meta name=\"robots\" content=\"noindex\">\n"
            "</head>\n<body>\n"
            "  <p>This page has moved to <a href=\"%s\">%s</a>.</p>\n"
            "</body>\n</html>\n"
        ) % (e(BASE + dest), e(dest), e(dest), e(BASE + dest))
        write_page("tools/%s/index.html" % alias, html_text)


def copy_brand_assets(tools: list[dict]) -> None:
    img = ASSETS / "img"
    img.mkdir(parents=True, exist_ok=True)
    # Icons
    shutil.copyfile(BRAND / "favicon.ico", ROOT / "favicon.ico")
    shutil.copyfile(BRAND / "png" / "favicon-32.png", img / "favicon-32.png")
    shutil.copyfile(BRAND / "png" / "favicon-16.png", img / "favicon-16.png")
    shutil.copyfile(BRAND / "png" / "apple-touch-icon-180.png", ROOT / "apple-touch-icon.png")
    shutil.copyfile(BRAND / "png" / "mark-512.png", img / "mark-512.png")
    shutil.copyfile(BRAND / "mark.svg", img / "mark.svg")
    shutil.copyfile(BRAND / "lockup-horizontal-light.svg", img / "lockup-horizontal-light.svg")
    shutil.copyfile(BRAND / "lockup-horizontal-dark.svg", img / "lockup-horizontal-dark.svg")
    shutil.copyfile(BRAND / "mark.svg", img / "favicon.svg")
    shutil.copyfile(BRAND / "png" / "apple-touch-icon-180.png", img / "apple-touch-icon.png")
    # OG: 1200x630 from the existing 1280x640 social preview.
    og_src = Image.open(BRAND / "png" / "github-social-preview-1280x640.png").convert("RGB")
    # Center-crop slightly then resize
    w, h = og_src.size
    target_ratio = 1200 / 630
    src_ratio = w / h
    if src_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        og_src = og_src.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        og_src = og_src.crop((0, top, w, top + new_h))
    og = og_src.resize((1200, 630), Image.Resampling.LANCZOS)
    og.save(img / "og.png", "PNG", optimize=True)
    og.save(img / "og.webp", "WEBP", quality=84, method=6)

    thumbs = img / "thumbs"
    covers = img / "covers"
    thumbs.mkdir(exist_ok=True)
    covers.mkdir(exist_ok=True)
    for tool in tools:
        thumb = Path(tool["thumb"])
        cover = Path(tool["cover"])
        optimize_image(thumb, thumbs / tool["slug"], 480, 82)
        optimize_image(cover, covers / tool["slug"], 1280, 80)
        tool["thumb_src"] = f"/assets/img/thumbs/{tool['slug']}.webp"
        tool["thumb_png"] = f"/assets/img/thumbs/{tool['slug']}.png"
        tool["cover_src"] = f"/assets/img/covers/{tool['slug']}.webp"
        tool["cover_png"] = f"/assets/img/covers/{tool['slug']}.png"


def write_css() -> None:
    css_src = (SRC / "site.css").read_text()
    font_css = """
@font-face {
  font-family: "Geist";
  src: url("/assets/fonts/geist-latin.woff2") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "Geist Mono";
  src: url("/assets/fonts/geist-mono-latin.woff2") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}
"""
    dest = ASSETS / "css"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "site.css").write_text(font_css.strip() + "\n\n" + css_src)


def version_links(ver: dict) -> str:
    items = []
    if ver.get("url"):
        items.append((ver.get("cta") or "Open", ver["url"]))
    items.extend(ver.get("urls") or [])
    if not items:
        return ""
    parts = []
    for label, url in items:
        parts.append(f'<a class="btn btn-secondary btn-sm" href="{e(url)}">{e(label)}</a>')
    return '<div class="btn-row">' + "".join(parts) + "</div>"


def versions_list(tool: dict, compact: bool = True) -> str:
    rows = []
    for ver in tool["versions"]:
        price = ver["price"]
        shown = ver.get("card_price") or price
        if price.lower() == "free":
            price_html = '<span class="badge-free">FREE</span>'
        else:
            price_html = f'<span class="price">{e(shown if compact else price)}</span>'
        place = f'<div class="ver-place"><strong>{e(ver["label"])}</strong><span>{e(ver["place"])}</span></div>'
        note = f'<p class="note">{e(ver["note"])}</p>' if ver.get("note") and not compact else ""
        rows.append(
            f"<li>{place}{price_html}{version_links(ver)}</li>" + (f"<li style='border:0;padding-top:0;display:block'>{note}</li>" if note else "")
        )
    return '<ul class="versions">' + "".join(rows) + "</ul>"


def card(tool: dict) -> str:
    return f'''
<article class="card" id="tool-{e(tool["slug"])}">
  <div class="card-top">
    <a class="card-thumb" href="/tools/{e(tool["slug"])}/" aria-hidden="true" tabindex="-1">
      <picture>
        <source type="image/webp" srcset="{e(tool["thumb_src"])}">
        <img src="{e(tool["thumb_png"])}" alt="" width="96" height="96">
      </picture>
    </a>
    <div>
      <p class="cat-label">{e(dict(CATEGORIES)[tool["category"]])}</p>
      <h3><a href="/tools/{e(tool["slug"])}/">{e(tool["name"])}</a></h3>
      <p class="tagline">{e(tool["tagline"])}</p>
    </div>
  </div>
  {versions_list(tool, compact=True)}
</article>
'''


def logo_html() -> str:
    return '''
    <a class="logo" href="/">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="/assets/img/lockup-horizontal-dark.svg">
        <img src="/assets/img/lockup-horizontal-light.svg" alt="Tidy Byte Tools" height="32" width="118">
      </picture>
    </a>
    '''


def nav_html(page: str) -> str:
    links = [
        ("/tools/", "Tools", "tools"),
        ("/#how", "How it works", "how"),
        ("/#faq", "FAQ", "faq"),
        ("https://github.com/tidybytetools", "GitHub", "github"),
    ]
    items = []
    for href, label, key in links:
        cur = ' aria-current="page"' if page == key else ""
        items.append(f'<li><a href="{e(href)}"{cur}>{e(label)}</a></li>')
    return "<nav aria-label=\"Primary\"><ul>" + "".join(items) + "</ul></nav>"


def footer_html(tools: list[dict]) -> str:
    tool_links = "\n".join(
        f'<li><a href="/tools/{e(t["slug"])}/">{e(t["name"])}</a></li>' for t in tools
    )
    return f'''
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      {logo_html()}
      <p>Small tools that clean up messy data. Each one does one job and does it well.</p>
    </div>
    <div>
      <h2>Tools</h2>
      <ul>{tool_links}</ul>
    </div>
    <div>
      <h2>Shops</h2>
      <ul>
        <li><a href="https://apify.com/tidybytetools">Apify</a></li>
        <li><a href="https://tidybyte.gumroad.com">Gumroad</a></li>
        <li><a href="https://github.com/tidybytetools">GitHub</a></li>
      </ul>
    </div>
    <div>
      <h2>This site</h2>
      <ul>
        <li><a href="/privacy/">Privacy</a></li>
        <li><a href="/llms.txt">llms.txt</a></li>
        <li><a href="/sitemap.xml">Sitemap</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap legal">
    <p>© {YEAR} Tidy Byte Tools. This site does not use tracking cookies.</p>
  </div>
</footer>
'''


def head_html(
    title: str,
    description: str,
    path: str,
    page_type: str = "website",
    extra: str = "",
) -> str:
    canon = BASE + path
    og_img = BASE + "/assets/img/og.png"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{e(canon)}">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <meta name="theme-color" content="#F4F7F5" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0D1512" media="(prefers-color-scheme: dark)">
  <meta property="og:type" content="{e(page_type)}">
  <meta property="og:site_name" content="Tidy Byte Tools">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{e(canon)}">
  <meta property="og:image" content="{e(og_img)}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(description)}">
  <meta name="twitter:image" content="{e(og_img)}">
  <link rel="stylesheet" href="/assets/css/site.css">
  {extra}
</head>
'''


ORG_LD = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Tidy Byte Tools",
    "url": BASE,
    "logo": BASE + "/assets/img/mark-512.png",
    "description": "Small tools that clean up messy data.",
    "sameAs": [
        "https://github.com/tidybytetools",
        "https://apify.com/tidybytetools",
        "https://tidybyte.gumroad.com",
    ],
}


def ld_script(data) -> str:
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=True) + "</script>"


def page_shell(title, description, path, body, nav_page, tools, extra_head=""):
    return "\n".join([
        head_html(title, description, path, extra=extra_head),
        "<body>",
        '<a class="skip" href="#main">Skip to content</a>',
        '<header class="site-header"><div class="header-inner">',
        logo_html(),
        nav_html(nav_page),
        "</div></header>",
        f'<main id="main">{body}</main>',
        footer_html(tools),
        "</body></html>\n",
    ])


def write_page(rel: str, html_text: str) -> None:
    dest = ROOT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html_text)
    print("wrote", dest.relative_to(ROOT))


def home_page(tools: list[dict]) -> None:
    groups = []
    for key, label in CATEGORIES:
        items = [t for t in tools if t["category"] == key]
        if not items:
            continue
        cards = "\n".join(card(t) for t in items)
        groups.append(f'''
        <section id="{e(key)}" aria-labelledby="h-{e(key)}">
          <div class="wrap">
            <div class="section-head">
              <h2 id="h-{e(key)}">{e(label)}</h2>
            </div>
            <div class="grid">{cards}</div>
          </div>
        </section>
        ''')
    chips = "\n".join(
        f'<a class="chip" href="#{e(key)}">{e(label)}</a>'
        for key, label in CATEGORIES
        if any(t["category"] == key for t in tools)
    )
    desc = "Small tools that clean up messy data. Run them on your computer, or pay only for what you use in the cloud."
    body = f'''
    <section class="hero">
      <div class="wrap hero-inner">
        <p class="eyebrow">Developer tools</p>
        <h1>Small tools that clean up messy data.</h1>
        <p class="lede">Each one does one job and does it well. Run it on your computer, or pay only for what you use in the cloud.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="#tools">See the tools</a>
          <a class="btn btn-secondary" href="https://github.com/tidybytetools">Free tools on GitHub</a>
        </div>
        <div class="cat-nav" role="navigation" aria-label="Tool groups">{chips}</div>
      </div>
    </section>
    <div id="tools">{"".join(groups)}</div>
    <section id="how">
      <div class="wrap">
        <h2>How it works</h2>
        <p class="section-intro">Pick the tool that matches your file. You can run it yourself, or start a run in the cloud.</p>
        <div class="steps">
          <div class="step">
            <p class="step-num">01</p>
            <h3>Pick a tool</h3>
            <p>Every tool does one job, like pulling tables from a PDF or checking a list of links.</p>
          </div>
          <div class="step">
            <p class="step-num">02</p>
            <h3>Run it where you want</h3>
            <p>Download a tool and run it on your computer, or use the Apify version and pay only for what it does.</p>
          </div>
          <div class="step">
            <p class="step-num">03</p>
            <h3>Get a clean file back</h3>
            <p>You get CSV, Excel, JSON, or Markdown you can use in a sheet, a script, or an AI app.</p>
          </div>
        </div>
        <p class="section-intro" style="margin-top:28px">The free lite tools include an MCP server, so you can use them from Cursor, Claude Desktop, and other AI apps. No API key is needed.</p>
      </div>
    </section>
    <section id="faq">
      <div class="wrap">
        <h2>FAQ</h2>
        <div class="faq">
          <div class="faq-item">
            <h3>What is Tidy Byte Tools?</h3>
            <p>A small shop of tools that clean up messy data. We sell downloads you run on your computer, and pay-per-use tools on Apify. Free lite tools are on GitHub and PyPI.</p>
          </div>
          <div class="faq-item">
            <h3>Will you see my files?</h3>
            <p>The download tools run on your computer, so those files stay with you. The Apify tools run in your own Apify account. This website does not take uploads.</p>
          </div>
          <div class="faq-item">
            <h3>What is the difference between free and paid?</h3>
            <p>The free lite tools cover the common case, like a text PDF or a simple list of links. Paid versions add things like Excel output, scanned pages, Word files, or folder support. Each tool page lists the difference.</p>
          </div>
          <div class="faq-item">
            <h3>What does pay per use mean?</h3>
            <p>On Apify you pay for what the tool does, such as each page with a table or each link checked. Failed or skipped items are free. The exact price is on the tool page and on Apify.</p>
          </div>
          <div class="faq-item">
            <h3>Do the free tools work with AI apps?</h3>
            <p>Yes. The free lite tools include a small MCP server. You can use them from Cursor, Claude Desktop, and other apps that support MCP. No API key is needed.</p>
          </div>
          <div class="faq-item">
            <h3>How do I get help?</h3>
            <p>Open an issue on the GitHub page for that tool. For a Gumroad or Apify purchase, you can also use the support option on that site.</p>
          </div>
        </div>
      </div>
    </section>
    '''
    extra = ld_script(ORG_LD)
    html_text = page_shell(
        "Tidy Byte Tools — small tools that clean up messy data",
        desc,
        "/",
        body,
        "home",
        tools,
        extra_head=extra,
    )
    write_page("index.html", html_text)


def tools_index(tools: list[dict]) -> None:
    cards = "\n".join(card(t) for t in tools)
    body = f'''
    <section class="page-hero">
      <div class="wrap">
        <p class="crumb"><a href="/">Home</a> / Tools</p>
        <h1>All tools</h1>
        <p class="lede">Downloads for your computer, free lite tools, and pay-per-use tools on Apify.</p>
      </div>
    </section>
    <section>
      <div class="wrap">
        <div class="grid">{cards}</div>
      </div>
    </section>
    '''
    html_text = page_shell(
        "All tools — Tidy Byte Tools",
        "Every Tidy Byte Tools product: PDF and docs, CSV and data, links, and AI chunking.",
        "/tools/",
        body,
        "tools",
        tools,
    )
    write_page("tools/index.html", html_text)


def tool_page(tool: dict, tools: list[dict]) -> None:
    bullets = "".join(f"<li>{e(x)}</li>" for x in tool["does"])
    version_blocks = []
    offers = []
    for ver in tool["versions"]:
        note = f'<p>{e(ver["note"])}</p>' if ver.get("note") else ""
        version_blocks.append(
            f'''<div class="version-block">
              <h3>{e(ver["label"])} · {e(ver["place"])} · {e(ver["price"])}</h3>
              {note}
              {version_links(ver)}
            </div>'''
        )
        url = ver.get("url") or (ver.get("urls") or [[None, None]])[0][1]
        if url:
            offer = {
                "@type": "Offer",
                "url": url,
                "availability": "https://schema.org/InStock",
            }
            if ver["price"].lower() == "free":
                offer["price"] = "0"
                offer["priceCurrency"] = "USD"
            offers.append(offer)
    ld = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": tool["name"],
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Windows, macOS, Linux",
        "description": tool["tagline"],
        "url": f"{BASE}/tools/{tool['slug']}/",
        "image": BASE + tool["cover_png"],
        "author": {"@type": "Organization", "name": "Tidy Byte Tools", "url": BASE},
    }
    if offers:
        ld["offers"] = offers if len(offers) > 1 else offers[0]
    gallery_html = ""
    if tool.get("gallery_src"):
        gallery_html = (
            '<div class="cover"><picture>'
            f'<source type="image/webp" srcset="{e(tool["gallery_src"])}">'
            f'<img src="{e(tool["gallery_png"])}" alt="{e(tool["gallery_alt"])}" width="1280" height="720">'
            '</picture></div>'
        )
    body = f'''
    <article class="page-hero">
      <div class="wrap">
        <p class="crumb"><a href="/">Home</a> / <a href="/tools/">Tools</a> / {e(tool["name"])}</p>
        <p class="cat-label">{e(dict(CATEGORIES)[tool["category"]])}</p>
        <h1>{e(tool["name"])}</h1>
        <p class="lede">{e(tool["tagline"])}</p>
        <div class="cover">
          <picture>
            <source type="image/webp" srcset="{e(tool["cover_src"])}">
            <img src="{e(tool["cover_png"])}" alt="{e(tool["name"] + " — " + tool["tagline"])}" width="1280" height="720">
          </picture>
        </div>
        {gallery_html}
        <div class="prose">
          <p>{e(tool["summary"])}</p>
          <h2>What it does</h2>
          <ul>{bullets}</ul>
          <h2>Get it</h2>
        </div>
        {"".join(version_blocks)}
      </div>
    </article>
    '''
    html_text = page_shell(
        f"{tool['name']} — Tidy Byte Tools",
        tool["tagline"],
        f"/tools/{tool['slug']}/",
        body,
        "tools",
        tools,
        extra_head=ld_script(ld),
    )
    write_page(f"tools/{tool['slug']}/index.html", html_text)


def privacy_page(tools: list[dict]) -> None:
    body = f'''
    <section class="page-hero">
      <div class="wrap prose">
        <p class="crumb"><a href="/">Home</a> / Privacy</p>
        <h1>Privacy</h1>
        <p>This is a static website. It has no accounts, no contact forms, and no tracking cookies. We do not run analytics on this site.</p>
        <p>Links on this site go to other places, such as GitHub, Gumroad, Apify, and PyPI. Those sites have their own privacy policies. If you buy a tool or start a run there, your data is handled by that site.</p>
        <p>The download tools sold on Gumroad run on your own computer. Those tools do not send your files to us. The tools on Apify run in your Apify account.</p>
        <p>If you open a GitHub issue, GitHub will have the information you post there.</p>
        <p>This site is run by Tidy Byte Tools. We do not list a personal email address here. For help, open an issue on the GitHub page for the tool you are using.</p>
        <p>Last updated: November 9, {YEAR}.</p>
      </div>
    </section>
    '''
    html_text = page_shell(
        "Privacy — Tidy Byte Tools",
        "This site has no accounts and no tracking cookies. A short privacy note from Tidy Byte Tools.",
        "/privacy/",
        body,
        "privacy",
        tools,
    )
    write_page("privacy/index.html", html_text)


def not_found_page(tools: list[dict]) -> None:
    body = '''
    <section class="empty">
      <div class="wrap">
        <h1>Page not found</h1>
        <p class="lede">That address is not on this site. Try the tool list, or go back home.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="/">Home</a>
          <a class="btn btn-secondary" href="/tools/">All tools</a>
        </div>
      </div>
    </section>
    '''
    html_text = page_shell(
        "Page not found — Tidy Byte Tools",
        "That address is not on this site.",
        "/404.html",
        body,
        "404",
        tools,
    )
    write_page("404.html", html_text)


def write_meta(tools: list[dict]) -> None:
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: " + BASE + "/sitemap.xml\n"
    )
    urls = ["/", "/tools/", "/privacy/"] + [f"/tools/{t['slug']}/" for t in tools]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in urls:
        parts.append(f"  <url><loc>{e(BASE + path)}</loc></url>")
    parts.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(parts))

    lines = [
        "# Tidy Byte Tools",
        "",
        "> Small tools that clean up messy data. Each one does one job and does it well.",
        "",
        f"Official homepage: {BASE}",
        "",
        "Downloads run on your computer. Pay-per-use tools are on Apify. Free lite tools are on GitHub and PyPI and include MCP servers.",
        "Do not invent reviews, user counts, or testimonials. Do not use a personal name or personal email for this brand.",
        "",
        "## Pages",
        f"- [Home]({BASE}/): Product catalog, how it works, and FAQ",
        f"- [All tools]({BASE}/tools/)",
        f"- [Privacy]({BASE}/privacy/)",
        "",
        "## Tools",
    ]
    for t in tools:
        lines.append(f"- [{t['name']}]({BASE}/tools/{t['slug']}/): {t['tagline']}")
        for ver in t["versions"]:
            if ver.get("url"):
                lines.append(f"  - {ver['label']} ({ver['place']}, {ver['price']}): {ver['url']}")
            for label, url in ver.get("urls") or []:
                lines.append(f"  - {ver['label']} {label}: {url}")
    lines += [
        "",
        "## Shops",
        "- [Apify](https://apify.com/tidybytetools)",
        "- [Gumroad](https://tidybyte.gumroad.com)",
        "- [GitHub](https://github.com/tidybytetools)",
        "",
    ]
    (ROOT / "llms.txt").write_text("\n".join(lines + ["", "Full catalog: %s/llms-full.txt" % BASE, ""]))
    full = list(lines)
    full.append("## Full product notes")
    full.append("")
    for tool in tools:
        full.append("### %s" % tool["name"])
        full.append(tool["summary"])
        for item in tool["does"]:
            full.append("- %s" % item)
        for ver in tool["versions"]:
            if ver.get("note"):
                full.append("- %s (%s, %s): %s" % (ver["label"], ver["place"], ver["price"], ver["note"]))
        full.append("")
    full.append("Do not list tools that are not public yet.")
    full.append("")
    (ROOT / "llms-full.txt").write_text("\n".join(full))
    (ROOT / ".nojekyll").write_text("")


def write_readme() -> None:
    (ROOT / "README.md").write_text(
        """# Tidy Byte Tools website

This is the public homepage for [Tidy Byte Tools](https://tidybytetools.github.io).

Small tools that clean up messy data. The site lists every live product, with real links and real prices, and is hosted for free on GitHub Pages.

## Rebuild

```
python3 build.py
```

You need Pillow, fontTools, brotli, and (for generated product art) Google Chrome, which `build.py` uses through `/workspace/design/render.py` when a tool has no existing cover.

Fonts are a subset of [Geist](https://github.com/vercel/geist-font), SIL Open Font License 1.1. The license is in `assets/fonts/OFL.txt`.

The site itself is MIT licensed. See `LICENSE`.
"""
    )


def write_gitignore() -> None:
    (ROOT / ".gitignore").write_text(
        "\n".join(
            [
                ".DS_Store",
                "__pycache__/",
                "*.pyc",
                "screenshot.png",
                ".preview/",
                "",
            ]
        )
    )


def main() -> None:
    print("Building Tidy Byte Tools website…")
    tools = live_tools()
    subset_fonts()
    generate_missing_art(tools)
    copy_brand_assets(tools)
    copy_galleries(tools)
    write_css()
    home_page(tools)
    tools_index(tools)
    for tool in tools:
        tool_page(tool, tools)
    write_aliases(tools)
    privacy_page(tools)
    not_found_page(tools)
    write_meta(tools)
    write_readme()
    write_gitignore()
    print(f"done: {len(tools)} tools")


if __name__ == "__main__":
    main()
