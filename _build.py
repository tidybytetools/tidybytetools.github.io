#!/usr/bin/env python3
"""Generate the Tidy Byte Tools static site."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path("/workspace/tidybytetools.github.io")
BASE = "https://tidybytetools.github.io"
YEAR = "2026"

# ---------------------------------------------------------------------------
# Catalog (only live products, honest copy)
# ---------------------------------------------------------------------------

FREE = [
    {
        "slug": "json-shaper",
        "name": "json-shaper-lite",
        "blurb": "Turns notes, CSV, and Markdown tables into clean JSON.",
        "who": "For people who paste messy notes into scripts or AI tools.",
        "price": "Free",
        "github": "https://github.com/tidybytetools/json-shaper-lite",
        "pypi": "https://pypi.org/project/json-shaper-lite/",
        "gumroad": "https://tidybyte.gumroad.com/l/txytmi",
        "page": "/tools/json-shaper/",
        "install": "pip install json-shaper-lite",
        "mcp": True,
    },
    {
        "slug": "pdf-table-pull",
        "name": "pdf-table-pull-lite",
        "blurb": "Pulls tables out of text PDFs and saves each one as a CSV file.",
        "who": "For people who are tired of copying tables out of PDFs by hand.",
        "price": "Free",
        "github": "https://github.com/tidybytetools/pdf-table-pull-lite",
        "pypi": "https://pypi.org/project/pdf-table-pull-lite/",
        "gumroad": "https://tidybyte.gumroad.com/l/qrbzvo",
        "page": "/tools/pdf-table-pull/",
        "install": "pip install pdf-table-pull-lite",
        "mcp": True,
    },
    {
        "slug": "doc2md",
        "name": "doc2md-lite",
        "blurb": "Turns a text PDF or a saved web page into clean Markdown. Tables stay as tables.",
        "who": "For people who want docs that AI tools can read well.",
        "price": "Free",
        "github": "https://github.com/tidybytetools/doc2md-lite",
        "pypi": "https://pypi.org/project/doc2md-lite/",
        "page": "/tools/doc2md/",
        "install": "pip install doc2md-lite",
        "mcp": True,
    },
    {
        "slug": "link-check",
        "name": "link-check-lite",
        "blurb": "Checks a list of links and shows which ones work, break, or redirect.",
        "who": "For people who keep a list of URLs and need to know which still work.",
        "price": "Free",
        "github": "https://github.com/tidybytetools/link-check-lite",
        "pypi": "https://pypi.org/project/link-check-lite/",
        "page": "/tools/link-check/",
        "install": "pip install link-check-lite",
        "mcp": True,
    },
    {
        "slug": "markdown-chunker",
        "name": "md-chunk-lite",
        "blurb": "Splits Markdown into chunks by heading, and keeps the heading path and line numbers.",
        "who": "For people building AI search (RAG) or a docs bot.",
        "price": "Free",
        "github": "https://github.com/tidybytetools/md-chunk-lite",
        "pypi": "https://pypi.org/project/md-chunk-lite/",
        "page": "/tools/markdown-chunker/",
        "install": "pip install md-chunk-lite",
        "mcp": True,
    },
]

APIFY = [
    {
        "slug": "pdf-table-pull-apify",
        "name": "PDF Table Extractor",
        "actor": "pdf-table-pull",
        "blurb": "Pulls tables out of PDFs, even tables that run across pages. Saves JSON, CSV, or Excel. Can read scans with OCR.",
        "who": "For people with invoices, bank statements, or reports to process in bulk.",
        "price": "$0.003 per page with a table; $0.01 per scanned OCR page. Pages with no tables are free.",
        "price_short": "$0.003 / page with a table",
        "url": "https://apify.com/tidybytetools/pdf-table-pull",
        "page": "/tools/pdf-table-pull/",
        "live": True,
    },
    {
        "slug": "doc-to-markdown",
        "name": "Doc to Markdown",
        "actor": "doc-to-markdown",
        "blurb": "Turns PDFs, Word files, and web pages into clean Markdown, plus chunks for AI search.",
        "who": "For people feeding many files to an AI search index.",
        "price": "$0.003 per file (first 20 PDF pages included). Extra PDF pages $0.0003. OCR $0.005 per scanned page.",
        "price_short": "$0.003 / file",
        "url": "https://apify.com/tidybytetools/doc-to-markdown",
        "page": "/tools/doc2md/",
        "live": True,
    },
    {
        "slug": "broken-link-checker",
        "name": "Broken Link Checker",
        "actor": "broken-link-checker",
        "blurb": "Checks lots of links at once. You get the status code, redirect chain, final URL, and speed.",
        "who": "For people who want to find 404s and redirect chains on a site or sitemap.",
        "price": "$0.001 per link checked. $0.002 per page scanned for links. Duplicates and robots.txt skips are free.",
        "price_short": "$0.001 / link",
        "url": "https://apify.com/tidybytetools/broken-link-checker",
        "page": "/tools/link-check/",
        "live": True,
    },
    {
        "slug": "markdown-rag-chunker",
        "name": "Markdown RAG Chunker",
        "actor": "markdown-rag-chunker",
        "blurb": "Splits Markdown into chunks for AI search. Keeps code blocks and tables whole when they fit. Each chunk has its heading path.",
        "who": "For people loading docs into a vector database.",
        "price": "$0.0001 per chunk.",
        "price_short": "$0.0001 / chunk",
        "url": "https://apify.com/tidybytetools/markdown-rag-chunker",
        "page": "/tools/markdown-chunker/",
        "live": True,
    },
    {
        "slug": "csv-excel-data-cleaner",
        "name": "CSV & Excel Data Cleaner",
        "actor": "csv-excel-data-cleaner",
        "blurb": "Cleans CSV, Excel, or JSON tables. Fixes headers, dates, emails, and phones, and removes duplicate and empty rows.",
        "who": "For people who get messy exports and need a clean file back.",
        "price": "$0.0005 per clean row. Removed rows are free.",
        "price_short": "$0.0005 / clean row",
        "url": "https://apify.com/tidybytetools/csv-excel-data-cleaner",
        "page": "/tools/csv-excel-data-cleaner/",
        "live": True,
    },
    {
        "slug": "phone-number-validator-formatter",
        "name": "Phone Number Validator & Formatter",
        "actor": "phone-number-validator-formatter",
        "blurb": "Checks if phone numbers are valid and writes them as E.164, international, and national. Shows country, line type, area, and time zone. Offline — nothing is called or texted.",
        "who": "For people cleaning a list of phone numbers.",
        "price": "$0.001 per number. Repeat numbers are free.",
        "price_short": "$0.001 / number",
        "url": "https://apify.com/tidybytetools/phone-number-validator-formatter",
        "page": "/tools/phone-number-validator/",
        "live": True,
    },
    {
        "slug": "json-to-csv-flattener",
        "name": "JSON to CSV Converter",
        "actor": "json-to-csv-flattener",
        "blurb": "Turns nested JSON or JSON Lines into a flat CSV table for Excel and Google Sheets.",
        "who": "For people who have nested JSON and need a spreadsheet.",
        "price": "$0.0001 per row.",
        "price_short": "$0.0001 / row",
        "url": "https://apify.com/tidybytetools/json-to-csv-flattener",
        "page": "/tools/json-to-csv/",
        "live": True,  # public in API; store page may still be catching up
    },
    {
        "slug": "csv-encoding-fixer-splitter",
        "name": "CSV Encoding Fixer & Splitter",
        "actor": "csv-encoding-fixer-splitter",
        "blurb": "Fixes broken characters in CSV files (like Ã© instead of é). Saves clean UTF-8, and can split big files while keeping the header.",
        "who": "For people whose CSVs look garbled in Excel.",
        "price": "$0.01 per file.",
        "price_short": "$0.01 / file",
        "url": "https://apify.com/tidybytetools/csv-encoding-fixer-splitter",
        "page": "/tools/csv-encoding-fixer/",
        "live": True,
    },
]

GUMROAD = [
    {
        "slug": "data-cleanup-bundle",
        "name": "Data Cleanup Bundle",
        "blurb": "Gets you pdf-table-pull, sheet-scrub, and json-shaper together.",
        "who": "For people who want the three data tools in one download and a lower price.",
        "price": "$19 (saves $7 vs buying the three tools one by one)",
        "price_short": "$19",
        "url": "https://tidybyte.gumroad.com/l/qnlxiy",
        "page": "/tools/data-cleanup-bundle/",
        "cover": "/assets/img/tools/data-cleanup-bundle-cover.png",
    },
    {
        "slug": "pdf-table-pull-paid",
        "name": "pdf-table-pull",
        "blurb": "Pulls tables out of PDFs into Excel, CSV, or JSON. Joins tables across pages and can read scanned pages.",
        "who": "For people with bank statements, invoices, or reports, including scans.",
        "price": "$12, pay once",
        "price_short": "$12",
        "url": "https://tidybyte.gumroad.com/l/hkxqxh",
        "page": "/tools/pdf-table-pull/",
        "cover": "/assets/img/tools/pdf-table-pull-cover.png",
    },
    {
        "slug": "doc2md-paid",
        "name": "doc2md",
        "blurb": "Turns PDF, Word, and HTML files into clean Markdown, plus chunks ready for AI search.",
        "who": "For people converting a folder of docs, including Word files.",
        "price": "$12, pay once",
        "price_short": "$12",
        "url": "https://tidybyte.gumroad.com/l/frlkv",
        "page": "/tools/doc2md/",
        "cover": "/assets/img/tools/doc2md-cover.png",
    },
    {
        "slug": "sheet-scrub",
        "name": "sheet-scrub",
        "blurb": "Cleans messy Excel and CSV files in one command: duplicates, dates, phones, and emails.",
        "who": "For people with messy contact lists or exports.",
        "price": "$9, pay once",
        "price_short": "$9",
        "url": "https://tidybyte.gumroad.com/l/cknndc",
        "page": "/tools/sheet-scrub/",
        "cover": "/assets/img/tools/sheet-scrub-cover.png",
        "gallery": "/assets/img/tools/sheet-scrub-gallery.png",
    },
    {
        "slug": "lead-sheet-fixer",
        "name": "lead-sheet-fixer",
        "blurb": "Cleans the lead list you already have: phones fixed, bad emails flagged, names split, duplicates merged.",
        "who": "For people working a list from a form, event, or CRM export.",
        "price": "$9, pay once",
        "price_short": "$9",
        "url": "https://tidybyte.gumroad.com/l/iaiacv",
        "page": "/tools/lead-sheet-fixer/",
        "cover": "/assets/img/tools/lead-sheet-fixer-cover.png",
        "gallery": "/assets/img/tools/lead-sheet-fixer-gallery.png",
    },
    {
        "slug": "json-shaper-paid",
        "name": "json-shaper",
        "blurb": "Turns messy text, CSV, Markdown tables, app logs, and US addresses into clean JSON.",
        "who": "For people who need more than plain CSV-to-JSON, including logs and addresses.",
        "price": "$5 minimum, pay what you want",
        "price_short": "$5+",
        "url": "https://tidybyte.gumroad.com/l/cznmeo",
        "page": "/tools/json-shaper/",
        "cover": "/assets/img/tools/json-shaper-cover.png",
        "gallery": "/assets/img/tools/json-shaper-gallery.png",
    },
    {
        "slug": "gif-forge",
        "name": "gif-forge",
        "blurb": "Turns a folder of videos into small, sharp GIFs, and can remove solid backgrounds from images. Runs offline.",
        "who": "For people making GIFs for docs, Discord, or store listings.",
        "price": "$7, pay once",
        "price_short": "$7",
        "url": "https://tidybyte.gumroad.com/l/vjbsqs",
        "page": "/tools/gif-forge/",
        "cover": "/assets/img/tools/gif-forge-cover.png",
        "gallery": "/assets/img/tools/gif-forge-gallery.png",
    },
    {
        "slug": "server-pulse",
        "name": "server-pulse",
        "blurb": "Sends Discord alerts when a website or game server goes down, plus Stripe and PayPal donation alerts.",
        "who": "For people who run a site or a game server and want alerts in Discord.",
        "price": "$19, pay once",
        "price_short": "$19",
        "url": "https://tidybyte.gumroad.com/l/cjatbj",
        "page": "/tools/server-pulse/",
        "cover": "/assets/img/tools/server-pulse-cover.png",
        "gallery": "/assets/img/tools/server-pulse-gallery.png",
    },
]

# Pages that need their own HTML, with longer copy
TOOL_PAGES = {
    "pdf-table-pull": {
        "title": "pdf-table-pull",
        "headline": "pdf-table-pull",
        "seo_title": "pdf-table-pull: PDF tables to CSV, Excel, or JSON",
        "seo_desc": "Pull tables out of PDFs into CSV, Excel, or JSON. Free lite tool on GitHub and PyPI. Paid download adds Excel, scans, and tables that run across pages. Also on Apify, pay per page.",
        "intro": "Copying tables out of a PDF by hand is slow, and pasting them into Excel often wrecks the columns. pdf-table-pull does it in one step.",
        "gallery": "/assets/img/tools/pdf-table-pull-gallery.png",
        "gallery_alt": "A real run of pdf-table-pull: a sample PDF goes in, and an Excel file comes out with real numbers. The value (40) became -40, and a table that ran across two pages was joined.",
        "gallery_caption": "A real run on the sample PDF that ships with the paid tool. The value “(40)” became −40, and a table that ran across two pages was joined.",
        "offers": [
            ("Free: pdf-table-pull-lite", "Pulls tables out of text PDFs and saves each one as CSV. Runs on your computer. MIT license. Also works as an MCP server for AI apps.", "Free", "https://github.com/tidybytetools/pdf-table-pull-lite", "GitHub"),
            ("Pay once: pdf-table-pull", "Adds Excel and JSON output, joins tables that carry on to the next page, reads scanned pages with optional OCR, and opens password-protected PDFs.", "$12", "https://tidybyte.gumroad.com/l/hkxqxh", "Get on Gumroad"),
            ("Pay per use: PDF Table Extractor", "The same job on Apify. $0.003 per page with a table, $0.01 per scanned OCR page. Pages with no tables are free.", "$0.003 / page", "https://apify.com/tidybytetools/pdf-table-pull", "Try on Apify"),
        ],
        "limits": "Text PDFs (where you can select the words with your mouse) give the best results. OCR on scans is slower and can misread blurry pages. Handwriting and photos of crumpled receipts will not work well.",
        "for": "People with bank statements, invoices, supplier price lists, reports, or government data.",
    },
    "doc2md": {
        "title": "doc2md",
        "headline": "doc2md",
        "seo_title": "doc2md: PDF, Word, and HTML to clean Markdown",
        "seo_desc": "Turn PDFs, Word files, and web pages into clean Markdown with real tables, plus chunks for AI search. Free lite tool on GitHub and PyPI. Paid download and Apify versions available.",
        "intro": "AI tools read Markdown best. Most converters give you a wall of text, and tables turn into word soup. doc2md keeps headings, lists, and tables intact.",
        "gallery": "/assets/img/tools/doc2md-gallery.png",
        "gallery_alt": "A real run of doc2md turning a sample file into clean Markdown with a table kept as a table.",
        "gallery_caption": "A real run on a sample file that ships with the paid tool. Tables stay as Markdown tables.",
        "offers": [
            ("Free: doc2md-lite", "Turns one text PDF or a saved web page (.html) into Markdown, and keeps tables. MIT license. Also works as an MCP server.", "Free", "https://github.com/tidybytetools/doc2md-lite", "GitHub"),
            ("Pay once: doc2md", "Adds Word (.docx) files, whole folders, page picking, password-locked PDFs, and RAG chunks with heading paths and page numbers.", "$12", "https://tidybyte.gumroad.com/l/frlkv", "Get on Gumroad"),
            ("Pay per use: Doc to Markdown", "The same job on Apify, including OCR for scanned PDFs. $0.003 per file (first 20 PDF pages included).", "$0.003 / file", "https://apify.com/tidybytetools/doc-to-markdown", "Try on Apify"),
        ],
        "limits": "The free lite tool reads text PDFs and saved HTML, not Word files and not scans. Two-column PDFs, like science papers, may mix the columns. Old .doc files and images are not read.",
        "for": "People feeding docs to ChatGPT, Claude, or their own AI app, building a search index, or moving old Word docs into a wiki.",
    },
    "link-check": {
        "title": "link-check",
        "headline": "link-check",
        "seo_title": "link-check: find broken links and redirects",
        "seo_desc": "Check a list of links and see which ones work, break, or redirect. Free lite tool on GitHub and PyPI. Pay-per-use Apify actor can also scan sitemaps and pages.",
        "intro": "A simple way to check a list of links. You see which ones work, which are broken, and where redirects end up.",
        "gallery": "/assets/img/tools/link-check-gallery.png",
        "gallery_alt": "A sample run of link-check showing status codes and redirect results for a list of URLs.",
        "gallery_caption": "A sample run that ships with the tool, showing status codes and where redirects end up.",
        "offers": [
            ("Free: link-check-lite", "Checks a list of links on your computer. MIT license. Also works as an MCP server.", "Free", "https://github.com/tidybytetools/link-check-lite", "GitHub"),
            ("Pay per use: Broken Link Checker", "Checks thousands of links on Apify. Paste a list, give a sitemap, or scan pages for their links. Follows robots.txt. $0.001 per link.", "$0.001 / link", "https://apify.com/tidybytetools/broken-link-checker", "Try on Apify"),
        ],
        "limits": "The free tool checks the links you give it. It does not crawl a whole site or read a sitemap. The Apify tool can do those jobs.",
        "for": "People who maintain docs, a website, or a list of resources and want to catch 404s early.",
    },
    "markdown-chunker": {
        "title": "Markdown chunker",
        "headline": "md-chunk-lite",
        "seo_title": "md-chunk-lite: split Markdown into RAG chunks",
        "seo_desc": "Split Markdown into chunks by heading, with heading paths and line numbers. Free on GitHub and PyPI. Also on Apify at $0.0001 per chunk.",
        "intro": "Splits Markdown into chunks by heading. Every chunk knows its heading path and the line numbers it came from. The same file always gives the same chunks, because this is plain code, not an AI model.",
        "offers": [
            ("Free: md-chunk-lite", "Runs on your computer. MIT license. Also works as an MCP server.", "Free", "https://github.com/tidybytetools/md-chunk-lite", "GitHub"),
            ("Pay per use: Markdown RAG Chunker", "The same job on Apify. Keeps code blocks and tables whole when they fit. Optional overlap. $0.0001 per chunk.", "$0.0001 / chunk", "https://apify.com/tidybytetools/markdown-rag-chunker", "Try on Apify"),
        ],
        "limits": "These tools chunk Markdown you already have. To turn PDFs or Word files into chunks, use doc2md.",
        "for": "People building AI search (RAG), embeddings, or a docs bot.",
    },
    "json-shaper": {
        "title": "json-shaper",
        "headline": "json-shaper",
        "seo_title": "json-shaper: messy text, CSV, and logs to clean JSON",
        "seo_desc": "Turn notes, CSV, and Markdown tables into clean JSON. Free lite tool on GitHub and PyPI. The paid version also parses app logs and US addresses.",
        "intro": "Free converters handle neat CSV. json-shaper is for the messy stuff they choke on: notes, pasted tables, and — in the paid version — logs and addresses. Numbers stay numbers, and true/false become booleans.",
        "gallery": "/assets/img/tools/json-shaper-gallery.png",
        "gallery_alt": "A real run of json-shaper turning a sample log file and a Markdown table into clean JSON.",
        "gallery_caption": "A real run on sample files that ship with the paid tool.",
        "offers": [
            ("Free: json-shaper-lite", "Turns key: value notes, CSV/TSV, and Markdown tables into JSON. MIT license. Also works as an MCP server. Free download also on Gumroad.", "Free", "https://github.com/tidybytetools/json-shaper-lite", "GitHub"),
            ("Pay once: json-shaper", "Adds app log parsing and one-line US address splitting. One Python file, no extra installs.", "$5+", "https://tidybyte.gumroad.com/l/cznmeo", "Get on Gumroad"),
        ],
        "limits": "The address parser in the paid tool handles US one-line addresses only. If you only need plain CSV to JSON, the free lite tool is enough.",
        "for": "People turning messy notes or exports into JSON for scripts and AI tools.",
    },
    "sheet-scrub": {
        "title": "sheet-scrub",
        "headline": "sheet-scrub",
        "seo_title": "sheet-scrub: clean messy Excel and CSV files",
        "seo_desc": "Clean messy Excel and CSV files in one command. Fixes duplicates, dates, phones, and emails, and writes a report of every change. $9, pay once, runs on your computer.",
        "intro": "Got a contact list or export full of double spaces, duplicate rows, five date styles, and phone numbers typed every possible way? sheet-scrub fixes it in one command and tells you exactly what it changed. Your original file is never touched.",
        "gallery": "/assets/img/tools/sheet-scrub-gallery.png",
        "gallery_alt": "A before and after of sheet-scrub cleaning a messy contact list: names cased, phones and dates made consistent, a duplicate row removed, and a bad email flagged.",
        "gallery_caption": "A real run on the sample file that ships with the tool. One duplicate was removed, phones and dates were made consistent, and a bad email was flagged.",
        "offers": [
            ("Pay once: sheet-scrub", "Works with Excel, CSV, and JSON, and can convert between them. Runs offline on your computer.", "$9", "https://tidybyte.gumroad.com/l/cknndc", "Get on Gumroad"),
            ("Need this in the cloud?", "The Apify CSV & Excel Data Cleaner does a similar job, charged per clean row.", "$0.0005 / row", "https://apify.com/tidybytetools/csv-excel-data-cleaner", "Try on Apify"),
        ],
        "limits": "Phone formatting is built for US and Canada 10-digit numbers. Other numbers are left as they are and listed in the report. Dates like 03/04/2026 are read month-first by default, with a switch for day-first.",
        "for": "People with messy spreadsheets who want a clean file and a short report.",
    },
    "lead-sheet-fixer": {
        "title": "lead-sheet-fixer",
        "headline": "lead-sheet-fixer",
        "seo_title": "lead-sheet-fixer: clean a lead list in one command",
        "seo_desc": "Clean the lead list you already have. Phones fixed, bad emails flagged, names split, duplicates merged. $9, pay once, runs on your computer.",
        "intro": "Got a lead list from a form, an event, or an old CRM export? Phones typed five ways, names in ALL CAPS, the same person three times? lead-sheet-fixer cleans it and gives you a short report. Your original file is never touched.",
        "gallery": "/assets/img/tools/lead-sheet-fixer-gallery.png",
        "gallery_alt": "A real run of lead-sheet-fixer cleaning a messy lead list: names split, phones made consistent, and duplicates merged.",
        "gallery_caption": "A real run on the sample lead list that ships with the tool.",
        "offers": [
            ("Pay once: lead-sheet-fixer", "Works with Excel, CSV, and JSON. Finds email, phone, name, and company columns on its own. Runs offline.", "$9", "https://tidybyte.gumroad.com/l/iaiacv", "Get on Gumroad"),
        ],
        "limits": "It checks that emails and phones look right. It does not check that an inbox exists or that a phone still works. It does not find new leads or scrape websites. It cleans the list you already have.",
        "for": "People cleaning a lead list they already have, not finding new leads.",
    },
    "gif-forge": {
        "title": "gif-forge",
        "headline": "gif-forge",
        "seo_title": "gif-forge: batch videos to small, sharp GIFs",
        "seo_desc": "Turn a folder of videos into small, sharp GIFs, and remove solid backgrounds from images. $7, pay once, runs offline on your computer.",
        "intro": "Drop a folder of clips in and get a folder of small, sharp, looping GIFs out. gif-forge uses ffmpeg’s two-pass palette method, so you skip the grainy, bloated files most online converters make. No uploads, no size caps, no watermark.",
        "gallery": "/assets/img/tools/gif-forge-gallery.png",
        "gallery_alt": "A sample of gif-forge turning a short clip into a GIF and removing a solid background from a sprite.",
        "gallery_caption": "A sample that ships with the tool: a short clip to a GIF, and a sprite with its solid background removed.",
        "offers": [
            ("Pay once: gif-forge", "Batch video-to-GIF plus a batch background remover for product shots, sprites, logos, and screenshots on a plain solid background.", "$7", "https://tidybyte.gumroad.com/l/vjbsqs", "Get on Gumroad"),
        ],
        "limits": "It is a command-line tool, not a point-and-click app. The background remover is for solid backgrounds. It will not cut a person out of a busy photo. You need Python 3.8+, ffmpeg, and Pillow.",
        "for": "People making GIFs for Discord, store listings, README demos, or social posts.",
    },
    "server-pulse": {
        "title": "server-pulse",
        "headline": "server-pulse",
        "seo_title": "server-pulse: Discord uptime and donation alerts",
        "seo_desc": "Get Discord alerts when a website or game server goes down, plus Stripe and PayPal donation alerts. $19, pay once, runs on your own machine.",
        "intro": "server-pulse watches your website and game ports. It posts a down alert to Discord when something breaks, and an up alert when it is back. It only alerts after a few failed checks in a row, so a short network blip will not spam your channel. It can also announce Stripe and PayPal donations.",
        "gallery": "/assets/img/tools/server-pulse-gallery.png",
        "gallery_alt": "Sample Discord alerts from server-pulse: a down alert, an up alert, and a donation alert.",
        "gallery_caption": "The kind of Discord messages server-pulse posts: down, back up, and a donation.",
        "offers": [
            ("Pay once: server-pulse", "Checks websites, Minecraft, Rust, or any TCP port. Pure Python, no pip installs. Runs on a VPS, a Raspberry Pi, or a Windows PC.", "$19", "https://tidybyte.gumroad.com/l/cjatbj", "Get on Gumroad"),
        ],
        "limits": "It has to run on a machine that is always on. A cheap VPS works best. Donation alerts need your server reachable from the internet so Stripe or PayPal can send to it. The guide explains how.",
        "for": "People who run a website or a game server and want alerts in Discord, without a monthly uptime bill.",
    },
    "data-cleanup-bundle": {
        "title": "Data Cleanup Bundle",
        "headline": "Data Cleanup Bundle",
        "seo_title": "Data Cleanup Bundle: three Python tools for messy data",
        "seo_desc": "Get pdf-table-pull, sheet-scrub, and json-shaper together for $19. Save $7 versus buying them one by one. All three run on your computer.",
        "intro": "Three small command-line tools for the boring part of working with data: getting it out of PDFs, cleaning up spreadsheets, and turning messy text into JSON. They all run on your own computer, so your files are never uploaded.",
        "gallery": "/assets/img/tools/data-cleanup-bundle-cover.png",
        "gallery_alt": "The Data Cleanup Bundle: pdf-table-pull, sheet-scrub, and json-shaper together.",
        "gallery_caption": "Three tools, one download. Bought one by one they cost at least $26. The bundle is $19.",
        "offers": [
            ("Pay once: the bundle", "Includes the full paid versions of pdf-table-pull ($12), sheet-scrub ($9), and json-shaper ($5 minimum). All 1.x updates to all three are free.", "$19", "https://tidybyte.gumroad.com/l/qnlxiy", "Get on Gumroad"),
        ],
        "limits": "These are command-line tools. If you have never opened a terminal, the READMEs walk you through it. pdf-table-pull works best on PDFs with clear table lines or columns.",
        "for": "People who want the three data tools together and a lower price.",
    },
    "csv-excel-data-cleaner": {
        "title": "CSV & Excel Data Cleaner",
        "headline": "CSV & Excel Data Cleaner",
        "seo_title": "CSV & Excel Data Cleaner on Apify",
        "seo_desc": "Clean CSV, Excel, or JSON tables on Apify. Fix headers, dates, emails, and phones, and remove duplicate and empty rows. $0.0005 per clean row.",
        "intro": "A pay-per-use cleaner for messy tables. It fixes column names, trims spaces, makes dates, emails, and phones match, and removes duplicate and empty rows. You get a clean CSV and a short report of what changed.",
        "offers": [
            ("Pay per use on Apify", "$0.0005 per clean row. Removed rows are free.", "$0.0005 / row", "https://apify.com/tidybytetools/csv-excel-data-cleaner", "Try on Apify"),
            ("Want this on your computer?", "sheet-scrub is the pay-once download that cleans Excel and CSV offline.", "$9", "https://tidybyte.gumroad.com/l/cknndc", "Get on Gumroad"),
        ],
        "limits": "Results come from the rules in the code. We do not promise more than that. Failed files and removed rows are free.",
        "for": "People who want a messy table cleaned in the cloud, without installing anything.",
    },
    "phone-number-validator": {
        "title": "Phone Number Validator & Formatter",
        "headline": "Phone Number Validator",
        "seo_title": "Phone Number Validator & Formatter on Apify",
        "seo_desc": "Validate and format phone numbers as E.164, international, and national. Get country, line type, area, and time zone. Offline rules, $0.001 per number.",
        "intro": "Checks if phone numbers are valid and writes them three ways: E.164, international, and national. It also shows the country, line type (like mobile or fixed line), area, and time zones. It uses Google’s open phone rules and never calls or texts anyone.",
        "offers": [
            ("Pay per use on Apify", "$0.001 per number. Repeat numbers are free. No start fee beyond Apify’s tiny actor-start charge.", "$0.001 / number", "https://apify.com/tidybytetools/phone-number-validator-formatter", "Try on Apify"),
        ],
        "limits": "It checks that a number looks valid under the published rules. It does not check that the phone is in service, and it never calls or texts anyone.",
        "for": "People cleaning a list of phone numbers in bulk.",
    },
    "json-to-csv": {
        "title": "JSON to CSV Converter",
        "headline": "JSON to CSV Converter",
        "seo_title": "JSON to CSV Converter: flatten nested JSON on Apify",
        "seo_desc": "Turn nested JSON or JSON Lines into a flat CSV table for Excel and Google Sheets. $0.0001 per row on Apify.",
        "intro": "Flattens nested objects (for example user.name and user.address.city) into a flat table. It reads JSON, JSON Lines, and Apify dataset links. You can pick how lists are handled. Columns stay in the order they first show up.",
        "offers": [
            ("Pay per use on Apify", "$0.0001 per row. Saves a CSV file and also puts rows in the dataset.", "$0.0001 / row", "https://apify.com/tidybytetools/json-to-csv-flattener", "Try on Apify"),
        ],
        "limits": "Results come from the rules in the code. Very deep or unusual JSON may need you to pick the list option that fits your file.",
        "for": "People who have nested JSON and need a spreadsheet.",
    },
    "csv-encoding-fixer": {
        "title": "CSV Encoding Fixer & Splitter",
        "headline": "CSV Encoding Fixer",
        "seo_title": "CSV Encoding Fixer & Splitter on Apify",
        "seo_desc": "Fix broken characters in CSV files (Ã© instead of é) and split big files while keeping the header. $0.01 per file on Apify.",
        "intro": "Fixes garbled letters like Ã©, â€™, and Ã¼. It can read UTF-8, UTF-16, and old Windows files, then save clean UTF-8 that opens right in Excel. It can also split big files into parts, and every part keeps the header.",
        "offers": [
            ("Pay per use on Apify", "$0.01 per file. Shows examples of what it fixed.", "$0.01 / file", "https://apify.com/tidybytetools/csv-encoding-fixer-splitter", "Try on Apify"),
        ],
        "limits": "It fixes common encoding mix-ups. It cannot recover text that was already lost or overwritten.",
        "for": "People whose CSVs look garbled in Excel, or who need to split a file that is too big.",
    },
}

FAQ = [
    (
        "Do I need to know how to code?",
        "For the downloads, you run one command in a terminal. Each README shows the exact words to type. The Apify tools run in your browser, so you do not need to install anything for those.",
    ),
    (
        "Is this a monthly subscription?",
        "No. Gumroad tools are pay once, and you get free updates to that tool’s 1.x versions. Apify tools charge only when you run them — by the page, file, row, link, or number.",
    ),
    (
        "Does my data leave my computer?",
        "The GitHub, PyPI, and Gumroad tools run on your own computer. Your files stay with you. The Apify tools run on Apify’s servers, so only use those when you are okay with that.",
    ),
    (
        "Can I try a tool before I pay?",
        "Yes. The lite tools are free on GitHub and PyPI. json-shaper-lite and pdf-table-pull-lite also have a free download on Gumroad.",
    ),
    (
        "What if a tool does not work on my file?",
        "Gumroad purchases follow Gumroad’s 30-day refund policy. Message us through Gumroad and we will help or refund you. For free tools, open a GitHub issue.",
    ),
    (
        "Who is Tidy Byte Tools?",
        "We are a small shop that makes focused tools for messy files. Each tool does one job. We do not use fake reviews or fake user counts. We describe what the code actually does.",
    ),
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def head(title: str, desc: str, path: str, extra: str = "") -> str:
    url = BASE + path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{esc(url)}">
  <meta name="theme-color" content="#F4F7F5">
  <meta name="robots" content="index,follow">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Tidy Byte Tools">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{esc(url)}">
  <meta property="og:image" content="{BASE}/assets/img/og.png">
  <meta property="og:image:width" content="1280">
  <meta property="og:image:height" content="640">
  <meta property="og:image:alt" content="Tidy Byte Tools — small tools that clean up messy data">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{BASE}/assets/img/og.png">
  <link rel="icon" href="/assets/img/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" href="/assets/img/favicon-32.png" sizes="32x32">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="stylesheet" href="/assets/css/styles.css">
  {extra}
</head>
"""


def org_jsonld() -> str:
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": BASE + "/#org",
                "name": "Tidy Byte Tools",
                "url": BASE,
                "logo": BASE + "/assets/img/logo-512.png",
                "description": "Small tools that clean up messy data. Each one does one job and does it well.",
                "sameAs": [
                    "https://github.com/tidybytetools",
                    "https://apify.com/tidybytetools",
                    "https://tidybyte.gumroad.com",
                ],
            },
            {
                "@type": "WebSite",
                "@id": BASE + "/#site",
                "url": BASE,
                "name": "Tidy Byte Tools",
                "publisher": {"@id": BASE + "/#org"},
            },
        ],
    }
    return '<script type="application/ld+json">' + json.dumps(data, indent=2) + "</script>"


def header(current: str = "") -> str:
    def item(href, label, ident):
        cur = ' aria-current="page"' if current == ident else ""
        return f'<a href="{href}"{cur}>{label}</a>'

    return f"""<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="logo" href="/" aria-label="Tidy Byte Tools home">
        <img src="/assets/img/lockup.svg" alt="Tidy Byte Tools" width="240" height="36">
      </a>
      <input type="checkbox" id="nav-toggle" aria-controls="site-nav">
      <label class="nav-toggle" for="nav-toggle">Menu</label>
      <nav class="nav-panel" id="site-nav" aria-label="Site">
        {item("/#free-tools", "Free tools", "free")}
        {item("/#pay-per-use", "Pay per use", "apify")}
        {item("/#downloads", "Downloads", "paid")}
        {item("/#faq", "FAQ", "faq")}
        <a href="https://github.com/tidybytetools">GitHub</a>
      </nav>
    </div>
  </header>
"""


def footer() -> str:
    return f"""  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <a class="logo" href="/"><img src="/assets/img/lockup.svg" alt="Tidy Byte Tools" width="200" height="30"></a>
        <p>Small tools that clean up messy data. Each one does one job and does it well.</p>
      </div>
      <div>
        <h2>Where to find us</h2>
        <ul>
          <li><a href="https://github.com/tidybytetools">GitHub</a></li>
          <li><a href="https://apify.com/tidybytetools">Apify store</a></li>
          <li><a href="https://tidybyte.gumroad.com">Gumroad shop</a></li>
          <li><a href="https://pypi.org/user/tidybytetools/">PyPI</a></li>
        </ul>
      </div>
      <div>
        <h2>This site</h2>
        <ul>
          <li><a href="/#free-tools">Free tools</a></li>
          <li><a href="/#pay-per-use">Pay per use</a></li>
          <li><a href="/#downloads">Downloads</a></li>
          <li><a href="/#faq">FAQ</a></li>
          <li><a href="/llms.txt">llms.txt</a></li>
        </ul>
      </div>
    </div>
    <div class="wrap legal">
      <p>© {YEAR} Tidy Byte Tools. No trackers on this site. Geist font © Geist Project Authors, SIL Open Font License 1.1.</p>
      <p>Questions about a paid tool? Message us through Gumroad. Found a bug in a free tool? <a href="https://github.com/tidybytetools">Open a GitHub issue</a>.</p>
    </div>
  </footer>
</body>
</html>
"""


def card(name, blurb, who, price, page, buttons, tag, tag_class):
    btns = "\n        ".join(
        f'<a class="btn btn-small {"btn-primary" if i == 0 else "btn-secondary"}" href="{esc(href)}">{esc(label)}</a>'
        for i, (label, href) in enumerate(buttons)
    )
    return f"""    <article class="card">
      <div class="meta-row"><span class="tag {tag_class}">{esc(tag)}</span></div>
      <h3><a href="{esc(page)}">{esc(name)}</a></h3>
      <p class="blurb">{esc(blurb)}</p>
      <p class="who">{esc(who)}</p>
      <p class="price">{esc(price)}</p>
      <div class="actions">
        {btns}
      </div>
    </article>
"""


def homepage() -> str:
    title = "Tidy Byte Tools — small tools that clean up messy data"
    desc = "Small tools that clean up messy data. Pull tables from PDFs, clean spreadsheets, turn docs into Markdown, and check links. Free on GitHub, pay-per-use on Apify, or pay once on Gumroad."
    free_cards = []
    for t in FREE:
        buttons = [("GitHub", t["github"]), ("PyPI", t["pypi"]), ("Details", t["page"])]
        if t.get("gumroad"):
            buttons.insert(2, ("Free download", t["gumroad"]))
        free_cards.append(card(t["name"], t["blurb"], t["who"], t["price"] + (". CLI and MCP server." if t.get("mcp") else ""), t["page"], buttons, "Free", "tag-free"))
    apify_cards = []
    for t in APIFY:
        buttons = [("Try on Apify", t["url"]), ("Details", t["page"])]
        apify_cards.append(card(t["name"], t["blurb"], t["who"], t["price_short"], t["page"], buttons, "Pay per use", "tag-ppe"))
    paid_cards = []
    for t in GUMROAD:
        buttons = [("Get on Gumroad", t["url"]), ("Details", t["page"])]
        paid_cards.append(card(t["name"], t["blurb"], t["who"], t["price_short"], t["page"], buttons, t["price_short"], "tag-paid"))

    faq_html = []
    for i, (q, a) in enumerate(FAQ):
        faq_html.append(
            f"""    <details class="faq-item"{' open' if i == 0 else ''}>
      <summary>{esc(q)}</summary>
      <p class="faq-body">{esc(a)}</p>
    </details>"""
        )

    return (
        head(title, desc, "/", org_jsonld())
        + header("home")
        + f"""  <main id="main">
    <section class="hero">
      <div class="wrap">
        <p class="kicker">Tidy Byte Tools</p>
        <h1>Small tools that clean up messy data.</h1>
        <p class="lede">Each tool does one job and does it well. Pull tables out of PDFs. Clean spreadsheets. Turn documents into Markdown. Check for broken links. Run them on your own computer, or pay only for what you use.</p>
        <div class="actions">
          <a class="btn btn-primary" href="#free-tools">See the tools</a>
          <a class="btn btn-secondary" href="https://apify.com/tidybytetools">Try one on Apify</a>
        </div>

        <aside class="demo" aria-label="Example of sheet-scrub cleaning a contact list">
          <div class="demo-head">
            <div>
              <h2>A real run, not a mockup</h2>
              <p>sheet-scrub on the sample file that ships with the tool.</p>
            </div>
            <a href="/tools/sheet-scrub/">See sheet-scrub</a>
          </div>
          <div class="demo-grid">
            <div class="demo-pane">
              <p class="demo-label">Before · contacts-messy.csv</p>
              <table class="data">
                <thead><tr><th>Full Name</th><th>Email</th><th>Phone #</th><th>Signup Date</th></tr></thead>
                <tbody>
                  <tr><td>ada LOVELACE</td><td>Ada.Lovelace@Example.com</td><td>512.555.0100</td><td>03/04/2026</td></tr>
                  <tr><td>Grace  Hopper</td><td>grace@example.com</td><td>1-512-555-0199</td><td>March 5th, 2026</td></tr>
                  <tr class="bad"><td>ada LOVELACE</td><td>ada.lovelace@example.com</td><td>(512) 555-0100</td><td>4 Mar 2026</td></tr>
                  <tr><td>Alan Turing</td><td>alan@example</td><td>512 555 0142</td><td>2026-03-07</td></tr>
                </tbody>
              </table>
            </div>
            <div class="demo-pane">
              <p class="demo-label">After · contacts-clean.csv</p>
              <table class="data">
                <thead><tr><th>full_name</th><th>email</th><th>phone</th><th>signup_date</th></tr></thead>
                <tbody>
                  <tr><td>Ada Lovelace</td><td>ada.lovelace@example.com</td><td>(512) 555-0100</td><td>2026-03-04</td></tr>
                  <tr><td>Grace Hopper</td><td>grace@example.com</td><td>(512) 555-0199</td><td>2026-03-05</td></tr>
                  <tr><td>Alan Turing</td><td>alan@example</td><td>(512) 555-0142</td><td>2026-03-07</td></tr>
                </tbody>
              </table>
            </div>
          </div>
          <p class="demo-note">Report: 1 duplicate removed · 4 phones formatted · dates made the same · a bad email flagged for a human look. Your original file is never touched.</p>
        </aside>
      </div>
    </section>

    <div class="wrap">
      <div class="paths">
        <a class="path" href="#free-tools">
          <span class="tag tag-free">Free</span>
          <h2>Open source on GitHub</h2>
          <p>Lite tools you can install with pip. They also work as MCP servers for AI apps. MIT license, run on your computer.</p>
        </a>
        <a class="path" href="#pay-per-use">
          <span class="tag tag-ppe">Pay per use</span>
          <h2>Run on Apify</h2>
          <p>Eight tools you can run in the browser. You pay only for the pages, files, rows, or links you process.</p>
        </a>
        <a class="path" href="#downloads">
          <span class="tag tag-paid">Pay once</span>
          <h2>Downloads on Gumroad</h2>
          <p>The full tools, plus a bundle. Pay once, run offline, and get free 1.x updates.</p>
        </a>
      </div>
    </div>

    <section class="section" id="free-tools">
      <div class="wrap">
        <div class="section-head">
          <h2>Free tools</h2>
          <p>Install with pip, or clone from GitHub. Each one also works as an MCP server, so AI apps can use them. They run on your computer, so your files stay with you.</p>
        </div>
        <div class="grid">
{''.join(free_cards)}        </div>
      </div>
    </section>

    <section class="section" id="pay-per-use">
      <div class="wrap">
        <div class="section-head">
          <h2>Pay per use on Apify</h2>
          <p>No install. Run a tool in your browser and pay only for what it processes. Failed items and skipped rows are free. See each tool page for the exact prices.</p>
        </div>
        <div class="grid">
{''.join(apify_cards)}        </div>
      </div>
    </section>

    <section class="section" id="downloads">
      <div class="wrap">
        <div class="section-head">
          <h2>Pay once on Gumroad</h2>
          <p>Download the files and run them on your own computer. Not a subscription. Refunds follow Gumroad’s 30-day policy.</p>
        </div>
        <div class="grid">
{''.join(paid_cards)}        </div>
      </div>
    </section>

    <section class="section" id="faq">
      <div class="wrap">
        <div class="section-head">
          <h2>FAQ</h2>
        </div>
        <div class="faq">
{chr(10).join(faq_html)}
        </div>
      </div>
    </section>
  </main>
"""
        + footer()
    )


def tool_page(slug: str, page: dict) -> str:
    path = f"/tools/{slug}/"
    ld = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": page["title"],
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Windows, macOS, Linux",
        "url": BASE + path,
        "description": page["seo_desc"],
        "publisher": {"@type": "Organization", "name": "Tidy Byte Tools", "url": BASE},
    }
    extra = '<script type="application/ld+json">' + json.dumps(ld) + "</script>"
    figure = ""
    if page.get("gallery"):
        figure = f"""
        <figure class="tool-figure">
          <img src="{esc(page['gallery'])}" alt="{esc(page.get('gallery_alt') or page['title'])}" width="1280" height="720">
          <figcaption>{esc(page.get('gallery_caption') or '')}</figcaption>
        </figure>
"""
    offers = []
    for title, body, price, href, label in page["offers"]:
        offers.append(f"""        <div class="offer">
          <div class="meta-row"><span class="tag">{esc(price)}</span></div>
          <h3>{esc(title)}</h3>
          <p>{esc(body)}</p>
          <a class="btn btn-primary btn-small" href="{esc(href)}">{esc(label)}</a>
        </div>""")
    return (
        head(page["seo_title"] + " · Tidy Byte Tools", page["seo_desc"], path, extra)
        + header()
        + f"""  <main id="main">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a> / <span>{esc(page['title'])}</span></p>
      <header class="tool-hero">
        <p class="kicker">Tidy Byte Tools</p>
        <h1>{esc(page['headline'])}</h1>
        <p class="lede">{esc(page['intro'])}</p>
        <p class="who">{esc(page['for'])}</p>
      </header>
      {figure}
      <div class="prose">
        <h2>How to get it</h2>
      </div>
      <div class="offer-list">
{chr(10).join(offers)}
      </div>
      <div class="prose">
        <h2>Honest limits</h2>
        <p>{esc(page['limits'])}</p>
        <p><a href="/">See all Tidy Byte Tools</a></p>
      </div>
    </div>
  </main>
"""
        + footer()
    )


def not_found() -> str:
    return (
        head("Page not found · Tidy Byte Tools", "That page is not on this site.", "/404.html")
        + header()
        + """  <main id="main" class="err">
    <div class="wrap">
      <h1>This page is not here.</h1>
      <p class="lede">The link may be old, or the address may have a typo.</p>
      <div class="actions">
        <a class="btn btn-primary" href="/">Go to the home page</a>
        <a class="btn btn-secondary" href="/#free-tools">See the tools</a>
      </div>
    </div>
  </main>
"""
        + footer()
    )


def sitemap() -> str:
    urls = ["/"]
    for slug in TOOL_PAGES:
        urls.append(f"/tools/{slug}/")
    urls += ["/llms.txt", "/llms-full.txt"]
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pri = "1.0" if u == "/" else "0.8"
        parts.append("  <url>")
        parts.append(f"    <loc>{BASE}{u}</loc>")
        parts.append("    <lastmod>2026-11-09</lastmod>")
        parts.append(f"    <priority>{pri}</priority>")
        parts.append("  </url>")
    parts.append("</urlset>\n")
    return "\n".join(parts)


def robots() -> str:
    return f"""User-agent: *
Allow: /

Sitemap: {BASE}/sitemap.xml
"""


def llms_txt() -> str:
    lines = [
        "# Tidy Byte Tools",
        "",
        "> Small tools that clean up messy data. Each one does one job and does it well. Free lite tools run on your computer (CLI + MCP). Paid downloads are on Gumroad. Pay-per-use actors are on Apify.",
        "",
        f"Home: {BASE}",
        "GitHub: https://github.com/tidybytetools",
        "Apify: https://apify.com/tidybytetools",
        "Gumroad: https://tidybyte.gumroad.com",
        "PyPI: https://pypi.org/user/tidybytetools/",
        "",
        "## Free tools (GitHub, PyPI, MCP)",
        "",
    ]
    for t in FREE:
        lines.append(f"- [{t['name']}]({BASE}{t['page']}): {t['blurb']} Install: `{t['install']}`. GitHub: {t['github']}. PyPI: {t['pypi']}.")
    lines += ["", "## Pay per use (Apify)", ""]
    for t in APIFY:
        lines.append(f"- [{t['name']}]({BASE}{t['page']}): {t['blurb']} Price: {t['price_short']}. Run: {t['url']}.")
    lines += ["", "## Pay once (Gumroad)", ""]
    for t in GUMROAD:
        lines.append(f"- [{t['name']}]({BASE}{t['page']}): {t['blurb']} Price: {t['price']}. Buy: {t['url']}.")
    lines += [
        "",
        "## Notes for agents",
        "",
        "- Do not invent reviews, user counts, or testimonials. We do not publish those here.",
        "- Offline tools (GitHub, PyPI, Gumroad) run on the user's computer. Apify tools run on Apify's servers.",
        "- Refunds for Gumroad purchases follow Gumroad's 30-day policy.",
        f"- Full catalog: {BASE}/llms-full.txt",
        "",
    ]
    return "\n".join(lines)


def llms_full() -> str:
    parts = [llms_txt(), "", "## Tool details", ""]
    for slug, page in TOOL_PAGES.items():
        parts.append(f"### {page['title']}")
        parts.append(f"URL: {BASE}/tools/{slug}/")
        parts.append(page["intro"])
        parts.append(f"Who it is for: {page['for']}")
        parts.append(f"Honest limits: {page['limits']}")
        for title, body, price, href, _ in page["offers"]:
            parts.append(f"- {title} ({price}): {body} Link: {href}")
        parts.append("")
    return "\n".join(parts)


def readme() -> str:
    return """# tidybytetools.github.io

Public site for [Tidy Byte Tools](https://tidybytetools.github.io).

Static HTML and CSS, no trackers. Built from the brand kit and live product listings. To rebuild after catalog changes, run `python3 _build.py` from this folder (the generator lives in the working copy used to publish).

Geist is included under the SIL Open Font License 1.1 (`assets/fonts/OFL.txt`).
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", path.relative_to(ROOT), "bytes", path.stat().st_size)


def main() -> None:
    write(ROOT / "index.html", homepage())
    for slug, page in TOOL_PAGES.items():
        write(ROOT / "tools" / slug / "index.html", tool_page(slug, page))
    write(ROOT / "404.html", not_found())
    write(ROOT / "sitemap.xml", sitemap())
    write(ROOT / "robots.txt", robots())
    write(ROOT / "llms.txt", llms_txt())
    write(ROOT / "llms-full.txt", llms_full())
    write(ROOT / "README.md", readme())
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()
