"""Single source of product data for the Tidy Byte Tools website.

Edit this file to add or change a tool. build.py turns it into every page,
tools.json, llms.txt, the MCP catalog, and the OpenAPI file.
"""
from __future__ import annotations

from pathlib import Path

PRODUCTS_DIR = Path("/workspace/products")

CATEGORIES = [
    ("pdf", "PDF & docs"),
    ("data", "CSV & data"),
    ("web", "Links & web"),
    ("ai", "AI / RAG"),
    ("media", "Images & video"),
    ("n8n", "n8n workflows"),
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


def E(before, after, before_label="Messy input", after_label="Clean output", lang="text", source=""):
    return {
        "before": before.strip("\n"),
        "after": after.strip("\n"),
        "before_label": before_label,
        "after_label": after_label,
        "lang": lang,
        "source": source,
    }


# Live Apify start fee, from the public pay-per-event settings.
ACTOR_START_USD = 0.00005


TOOLS = [
    {
        "slug": "pdf-table-pull",
        "name": "PDF Table Pull",
        "category": "pdf",
        "icon": "table",
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
        "actor": "pdf-table-pull",
        "event": {"id": "table-page", "price_usd": 0.003, "unit": "pages with a table", "title": "Page with a table"},
        "input": "A PDF file or a link to a PDF.",
        "output": "Tables as Excel, CSV, or JSON. Numbers like (40) become -40.",
        "example": E(
            "Region  Q1     Q2\nNorth   1200   1350\nSouth    980   (40)",
            "Region,Q1,Q2\nNorth,1200,1350\nSouth,980,-40",
            "Table in a PDF",
            "CSV out",
            "csv",
            "From the quarterly-report sample in pdf-table-pull/samples.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.003 per page with a table",
              "https://apify.com/tidybytetools/pdf-table-pull",
              card_price="$0.003/page",
              note="Pages with no tables are free. Scanned pages read with OCR are $0.01 each.",
              cta="Try it on Apify"),
            V("Gumroad", "For your computer", "$12",
              "https://tidybyte.gumroad.com/l/hkxqxh",
              note="Excel, CSV and JSON output, scanned PDFs, and tables that run across pages.",
              cta="Buy on Gumroad"),
            V("GitHub & PyPI", "Free lite", "Free",
              urls=[
                  ("GitHub", "https://github.com/tidybytetools/pdf-table-pull-lite"),
                  ("PyPI", "https://pypi.org/project/pdf-table-pull-lite/"),
                  ("Gumroad", "https://tidybyte.gumroad.com/l/qrbzvo"),
              ],
              note="Text PDFs to CSV. CLI and MCP server. No Excel, no OCR, no joining tables across pages."),
        ],
        "repos": ["pdf-table-pull-lite"],
    },
    {
        "slug": "doc2md",
        "name": "Doc to Markdown",
        "category": "pdf",
        "icon": "doc",
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
        "actor": "doc-to-markdown",
        "event": {"id": "document-converted", "price_usd": 0.003, "unit": "files", "title": "File converted"},
        "input": "A PDF, Word file, HTML file, or a page link.",
        "output": "Clean Markdown. Tables stay as Markdown tables. Paid runs can also write RAG chunks.",
        "example": E(
            """<nav>Home | Shop</nav>
<main><h1>How returns work</h1>
<p>You can send back most items within <strong>30 days</strong>.</p>
<table><tr><th>Paid with</th><th>Refund time</th></tr>
<tr><td>Card</td><td>3-5 days</td></tr></table>
</main><footer>Copyright Example Shop</footer>""",
            """# How returns work

You can send back most items within **30 days**.

| Paid with | Refund time |
| --- | --- |
| Card | 3-5 days |""",
            "HTML page (nav and footer included)",
            "Markdown out (nav and footer dropped)",
            "html",
            "From doc2md/samples/returns-help.html and samples/output/returns-help.md.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.003 per file",
              "https://apify.com/tidybytetools/doc-to-markdown",
              note="First 20 PDF pages are included. Extra PDF pages are $0.0003 each. Scanned pages with OCR are $0.005. Failed files are free.",
              cta="Try it on Apify"),
            V("Gumroad", "For your computer", "$12",
              "https://tidybyte.gumroad.com/l/frlkv",
              note="PDF, Word and HTML, plus RAG chunks with heading paths and page numbers. Runs offline.",
              cta="Buy on Gumroad"),
            V("GitHub & PyPI", "Free lite", "Free",
              urls=[
                  ("GitHub", "https://github.com/tidybytetools/doc2md-lite"),
                  ("PyPI", "https://pypi.org/project/doc2md-lite/"),
                  ("Gumroad", "https://tidybyte.gumroad.com/l/doc2md-lite"),
              ],
              note="Text PDF or HTML, one file at a time. No Word files, no folders, no RAG chunks, no OCR. Free download, $3 suggested."),
        ],
        "repos": ["doc2md-lite"],
    },
    {
        "slug": "sheet-scrub",
        "name": "CSV & spreadsheet cleanup",
        "category": "data",
        "icon": "sheet",
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
        "actor": "csv-excel-data-cleaner",
        "event": {"id": "row-cleaned", "price_usd": 0.0005, "unit": "clean rows", "title": "Clean row saved"},
        "input": "A CSV, Excel, or JSON table.",
        "output": "A clean CSV and a short report of what changed. Removed rows are free.",
        "example": E(
            """ Full Name ,Email,Phone #,Signup Date,State
ada LOVELACE,Ada.Lovelace@Example.com ,512.555.0100,03/04/2026,tx
Grace  Hopper,grace@example.com,1-512-555-0199,"March 5th, 2026",TX
ada LOVELACE,ada.lovelace@example.com,(512) 555-0100,4 Mar 2026,tx
,,,,""",
            """full_name,email,phone,signup_date,state
Ada Lovelace,ada.lovelace@example.com,(512) 555-0100,2026-03-04,TX
Grace Hopper,grace@example.com,(512) 555-0199,2026-03-05,TX""",
            "Messy CSV",
            "Clean CSV (duplicate and empty rows gone)",
            "csv",
            "From sheet-scrub/samples/contacts-messy.csv and contacts-clean.csv.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.0005 per clean row",
              "https://apify.com/tidybytetools/csv-excel-data-cleaner",
              card_price="$0.0005/row",
              note="Removed rows are free. Gives you a clean CSV and a short report of what changed.",
              cta="Try it on Apify"),
            V("Gumroad", "For your computer", "$9",
              "https://tidybyte.gumroad.com/l/cknndc",
              note="sheet-scrub: one command for messy Excel and CSV files. Runs on your computer.",
              cta="Buy on Gumroad"),
        ],
        "repos": [],
    },
    {
        "slug": "json-shaper",
        "name": "JSON Shaper",
        "category": "data",
        "icon": "json",
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
        "input": "Notes, a CSV or TSV file, or a Markdown table. Paid also reads app logs.",
        "output": "Typed JSON. Numbers, booleans, and nulls stay as real types.",
        "example": E(
            """| Product | Price | In stock |
|---|---|---|
| Widget | 9.50 | true |
| Gadget | 24 | false |""",
            """[
  {"product": "Widget", "price": 9.5, "in_stock": true},
  {"product": "Gadget", "price": 24, "in_stock": false}
]""",
            "Markdown table",
            "Typed JSON",
            "markdown",
            "From json-shaper/samples/table.md and table.json.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "From $5",
              "https://tidybyte.gumroad.com/l/cznmeo",
              note="Pay what you want, $5 minimum. Adds app logs and a US address splitter.",
              cta="Buy on Gumroad"),
            V("GitHub & PyPI", "Free lite", "Free",
              urls=[
                  ("GitHub", "https://github.com/tidybytetools/json-shaper-lite"),
                  ("PyPI", "https://pypi.org/project/json-shaper-lite/"),
                  ("Gumroad", "https://tidybyte.gumroad.com/l/txytmi"),
              ],
              note="Notes, CSV/TSV and Markdown tables. CLI and MCP server. No log parsing, no address splitter."),
        ],
        "repos": ["json-shaper-lite"],
    },
    {
        "slug": "lead-sheet-fixer",
        "name": "Lead Sheet Fixer",
        "category": "data",
        "icon": "leads",
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
        "input": "A CSV or Excel lead list.",
        "output": "A clean sheet with split names, formatted phones, email status, and merged duplicates.",
        "example": E(
            """Full Name,Company,Email,Phone
  Dr. maria GARCIA ,Sunrise Bakery LLC,Maria@SunriseBakery.com,512.555.0142
Maria Garcia,Sunrise Bakery,,5125550142
lee chen,Northwind Supply Inc.,lee.chen@gmial.com,212 555 0187""",
            """full_name,first_name,last_name,company,email,phone,email_status,lead_issues
Dr. Maria Garcia,Maria,Garcia,Sunrise Bakery LLC,maria@sunrisebakery.com,(512) 555-0142,ok,
Lee Chen,Lee,Chen,Northwind Supply Inc.,lee.chen@gmial.com,(212) 555-0187,invalid,email domain looks like a typo of gmail.com""",
            "Messy lead list",
            "Clean list (duplicate merged, typo flagged)",
            "csv",
            "From lead-sheet-fixer/samples/leads.csv and leads-clean.csv.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "$9",
              "https://tidybyte.gumroad.com/l/iaiacv",
              cta="Buy on Gumroad"),
        ],
        "repos": [],
    },
    {
        "slug": "phone-validator",
        "name": "Phone Number Validator",
        "category": "data",
        "icon": "phone",
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
        "thumb": None,
        "cover": None,
        "gen_art": {
            "title": "phone-validator",
            "sub": "Bulk phones to E.164, offline",
            "badge": "PAY PER USE",
            "vis": "phone",
        },
        "actor": "phone-number-validator-formatter",
        "event": {"id": "phone-checked", "price_usd": 0.001, "unit": "numbers", "title": "Phone number checked"},
        "input": "A list of phone numbers, plus a default country for numbers with no country code.",
        "output": "Valid or not, plus E.164, international, and national forms, country, and line type.",
        "example": E(
            """+1 650-253-0000
(415) 555-2671
020 7946 0958
12345""",
            """+1 650-253-0000  →  +16502530000   valid, US
(415) 555-2671   →  +14155552671   valid, US
020 7946 0958    →  +442079460958  valid, GB
12345            →  (not valid)""",
            "Mixed phone numbers",
            "Checked and formatted (from the Actor test)",
            "text",
            "From the default sample and tests in phone-validator-apify.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.001 per number",
              "https://apify.com/tidybytetools/phone-number-validator-formatter",
              card_price="$0.001/number",
              cta="Try it on Apify"),
        ],
        "repos": [],
    },
    {
        "slug": "data-cleanup-bundle",
        "name": "Data Cleanup Bundle",
        "category": "data",
        "icon": "bundle",
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
        "input": "The same inputs as the three tools: PDFs, Excel or CSV files, and messy notes or tables.",
        "output": "The same clean Excel, CSV, JSON, or Markdown each tool would give you on its own.",
        "example": E(
            """ Full Name ,Phone #,Signup Date
ada LOVELACE,512.555.0100,03/04/2026
ada LOVELACE,(512) 555-0100,4 Mar 2026""",
            """full_name,phone,signup_date
Ada Lovelace,(512) 555-0100,2026-03-04""",
            "A messy sheet (one of the three tools)",
            "Clean CSV from sheet-scrub",
            "csv",
            "Sheet-scrub sample, included because the bundle ships that tool.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "$19",
              "https://tidybyte.gumroad.com/l/qnlxiy",
              note="Saves $7 versus buying the three tools separately at their listed prices ($12 + $9 + $5).",
              cta="Buy on Gumroad"),
        ],
        "repos": [],
    },
    {
        "slug": "link-check",
        "name": "Broken Link Checker",
        "category": "web",
        "icon": "link",
        "tagline": "Check a list of links for status codes, redirects, and broken pages.",
        "summary": (
            "Paste a list, give a sitemap, or scan pages for their links. "
            "Get a clear report of what works, what is broken, and where redirects end up."
        ),
        "does": [
            "Shows the status code, redirect chain, and final URL for each link.",
            "The paid download and the Apify version can also read a sitemap, check speed, and flag look-alike domains.",
            "The Apify version can scan pages for links and follows robots.txt.",
            "The free lite tool checks a text file of links on your computer, includes an MCP server, and is also on the GitHub Marketplace as an Action.",
        ],
        "thumb": PRODUCTS_DIR / "link-check" / "thumb.png",
        "cover": PRODUCTS_DIR / "link-check" / "cover.png",
        "actor": "broken-link-checker",
        "event": {"id": "link-checked", "price_usd": 0.001, "unit": "links", "title": "Link checked"},
        "input": "A list of links, a sitemap, or pages to scan for links.",
        "output": "Status code, redirect chain, final URL, and a short report of broken links.",
        "example": E(
            """https://example.com/
https://github.com/tidybytetools/this-page-does-not-exist
https://httpbin.org/redirect/3""",
            """https://example.com/                                       200  ok
https://github.com/tidybytetools/this-page-does-not-exist  404  broken
https://httpbin.org/redirect/3                             200  3 hops → https://httpbin.org/get""",
            "A list of links",
            "Report (from the sample run)",
            "text",
            "From link-check/samples/links.txt and report.md.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.001 per link",
              "https://apify.com/tidybytetools/broken-link-checker",
              card_price="$0.001/link",
              note="Scanning a page for links is $0.002 per page. Duplicates and links skipped by robots.txt are free.",
              cta="Try it on Apify"),
            V("Gumroad", "For your computer", "$7",
              "https://tidybyte.gumroad.com/l/link-check",
              note="Sitemaps, speed checks, look-alike domain warnings, and CSV reports. Runs offline.",
              cta="Buy on Gumroad"),
            V("GitHub & PyPI", "Free lite", "Free",
              urls=[
                  ("GitHub", "https://github.com/tidybytetools/link-check-lite"),
                  ("PyPI", "https://pypi.org/project/link-check-lite/"),
                  ("GitHub Action", "https://github.com/marketplace/actions/link-check-lite"),
              ],
              note="Checks a text file of links. CLI, MCP server, and a GitHub Action. No sitemap input, no speed flags, no CSV report in the lite version."),
        ],
        "repos": ["link-check-lite"],
    },
    {
        "slug": "server-pulse",
        "name": "Server Pulse",
        "category": "web",
        "icon": "pulse",
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
        "input": "A small config file with the sites or ports to watch, and a Discord webhook.",
        "output": "A Discord message when a site goes down or comes back. A local check prints UP or DOWN.",
        "example": E(
            """{
  "targets": [
    {"name": "Website", "url": "https://example.com/"},
    {"name": "Closed port (demo)", "host": "127.0.0.1", "port": 1}
  ]
}""",
            """UP   Website: HTTP 200 (49 ms)
DOWN Closed port (demo): [Errno 111] Connection refused (0 ms)""",
            "Sample config (shortened)",
            "Output of a local check",
            "json",
            "From server-pulse/samples/sample-config.json and check-output.txt.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "$19",
              "https://tidybyte.gumroad.com/l/cjatbj",
              cta="Buy on Gumroad"),
        ],
        "repos": [],
    },
    {
        "slug": "markdown-chunker",
        "name": "Markdown Chunker for RAG",
        "category": "ai",
        "icon": "chunk",
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
        "actor": "markdown-rag-chunker",
        "event": {"id": "chunk-created", "price_usd": 0.0001, "unit": "chunks", "title": "Chunk created"},
        "input": "Markdown or plain text, plus a max chunk size.",
        "output": "JSON lines with text, heading path, line numbers, and an id for each chunk.",
        "example": E(
            """# Garden Guide

## Tools

You need a shovel, a rake and gloves.

## Planting

### Tomatoes

Plant tomatoes after the last frost. Give them sun.""",
            """{
  "id": "guide.md#3",
  "heading_path": ["Garden Guide", "Planting", "Tomatoes"],
  "start_line": 9,
  "text": "Plant tomatoes after the last frost. Give them sun."
}""",
            "Markdown with headings",
            "One chunk (heading path kept)",
            "markdown",
            "From md-chunk-lite/tests/fixtures/guide.md and the chunk tests.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.0001 per chunk",
              "https://apify.com/tidybytetools/markdown-rag-chunker",
              card_price="$0.0001/chunk",
              cta="Try it on Apify"),
            V("GitHub & PyPI", "Free lite", "Free",
              urls=[
                  ("GitHub", "https://github.com/tidybytetools/md-chunk-lite"),
                  ("PyPI", "https://pypi.org/project/md-chunk-lite/"),
              ],
              note="Markdown and plain text. CLI and MCP server. It does not read PDF or Word files."),
        ],
        "repos": ["md-chunk-lite"],
    },
    {
        "slug": "gif-forge",
        "name": "GIF Forge",
        "category": "media",
        "icon": "gif",
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
        "input": "A folder of video clips, or an image with a solid background.",
        "output": "A folder of looping GIFs, or a PNG with the solid background removed.",
        "example": E(
            "samples/clip.mp4          (3-second test video)\nsamples/sprite-white-bg.png (sprite on a white background)",
            "samples/out/clip.gif            (small looping GIF)\nsamples/out/sprite-white-bg.png (transparent PNG)",
            "Sample folder in",
            "Sample folder out",
            "text",
            "From gif-forge/README.md sample files.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "$7",
              "https://tidybyte.gumroad.com/l/vjbsqs",
              cta="Buy on Gumroad"),
        ],
        "repos": [],
    },
    {
        "slug": "n8n-data-cleanup-pack",
        "name": "n8n Data Cleanup Pack",
        "category": "n8n",
        "icon": "workflow",
        "tagline": "9 n8n workflows for messy CSVs, leads, invoices, sheets, and uptime alerts.",
        "summary": (
            "Import a file, pick your logins, and run. These workflows clean messy data "
            "in n8n, using only the nodes that come with n8n."
        ),
        "does": [
            "Nine ready-to-import workflows, including CSV cleanup, lead cleanup, invoice email to Sheets, and uptime alerts.",
            "Only nodes that come with n8n. No community nodes and no paid APIs.",
            "Each workflow has plain setup steps inside it.",
        ],
        "thumb": PRODUCTS_DIR / "n8n-data-cleanup-pack" / "thumb.png",
        "cover": PRODUCTS_DIR / "n8n-data-cleanup-pack" / "cover.png",
        "input": "A messy CSV, a lead list, invoice text, or a sitemap, imported into n8n.",
        "output": "A clean CSV or a JSONL file, made by the workflow.",
        "example": E(
            """Full Name , E-mail ,Phone,Notes
Maria Garcia,Maria@Sunrise.com ,512.555.0142,N/A
  jon smith,jon@acme.com,415 555 0110,null
Maria Garcia,maria@sunrise.com,5125550142,called twice
,,,,""",
            """full_name,email,phone,notes
Maria Garcia,maria@sunrise.com,512.555.0142,
jon smith,jon@acme.com,415 555 0110,""",
            "Messy CSV in n8n",
            "Clean CSV from a real n8n 2.46.4 run",
            "csv",
            "From n8n-data-cleanup-pack/samples/input.csv and clean-output-from-n8n.csv.",
        ),
        "versions": [
            V("Gumroad", "For n8n", "$19",
              "https://tidybyte.gumroad.com/l/n8n-data-cleanup-pack",
              cta="Buy on Gumroad",
              note="Tested on self-hosted n8n 2.46.4. Workflows that read files from disk need self-hosted n8n."),
            V("Gumroad", "Free sample", "Free",
              "https://tidybyte.gumroad.com/l/n8n-cleanup-sampler",
              cta="Get free on Gumroad",
              note="Two workflows from the pack: CSV cleanup and uptime alerts."),
        ],
        "repos": [],
    },
    {
        "slug": "n8n-cleanup-sampler",
        "name": "n8n Cleanup Sampler",
        "category": "n8n",
        "icon": "workflow",
        "tagline": "2 free n8n workflows from the Data Cleanup Pack: CSV cleanup and uptime alerts.",
        "summary": (
            "Try two workflows for free before you buy the full pack. Import a file, "
            "follow the setup note inside, and run. No logins are stored in the files."
        ),
        "does": [
            "Includes CSV cleanup and dedupe, plus website uptime alerts to Discord or Slack.",
            "Uses only nodes that come with n8n. No community nodes and no paid APIs.",
            "Leads to the full n8n Data Cleanup Pack ($19) with 9 workflows.",
        ],
        "thumb": PRODUCTS_DIR / "n8n-cleanup-sampler" / "thumb.png",
        "cover": PRODUCTS_DIR / "n8n-cleanup-sampler" / "cover.png",
        "input": "A messy CSV, or a list of sites to watch.",
        "output": "A clean CSV, or a Discord or Slack message when a site goes down.",
        "example": E(
            """Full Name , E-mail ,Phone,Notes
Maria Garcia,Maria@Sunrise.com ,512.555.0142,N/A
Maria Garcia,maria@sunrise.com,5125550142,called twice
,,,,""",
            """full_name,email,phone,notes
Maria Garcia,maria@sunrise.com,512.555.0142,""",
            "Messy CSV",
            "After the free CSV cleanup workflow",
            "csv",
            "From the pack samples, which this free sampler also uses.",
        ),
        "versions": [
            V("Gumroad", "Free sample", "Free",
              "https://tidybyte.gumroad.com/l/n8n-cleanup-sampler",
              cta="Get free on Gumroad",
              note="Two workflows from the $19 n8n Data Cleanup Pack. The CSV cleanup workflow needs self-hosted n8n."),
        ],
        "repos": [],
    },
    {
        "slug": "csv-char-fix",
        "name": "csv-char-fix",
        "category": "data",
        "icon": "letters",
        "tagline": "Fix weird characters like Ã© and â€™ in CSV and text files.",
        "summary": (
            "Did an export turn José into JosÃ© or it's into itâ€™s? This small script "
            "puts the text back the way it should be and saves the file so Excel shows accents right."
        ),
        "does": [
            "Fixes garbled letters that were broken once, twice, or three times.",
            "Leaves normal accented text alone.",
            "Reads UTF-8, UTF-16, and Windows-1252 files, and never changes your original.",
        ],
        "thumb": PRODUCTS_DIR / "csv-char-fix" / "thumb.png",
        "cover": PRODUCTS_DIR / "csv-char-fix" / "cover.png",
        "input": "A CSV or text file with broken letters such as JosÃ©.",
        "output": "The same file with letters fixed, saved as Excel-friendly UTF-8.",
        "example": E(
            """name,city,note
JosÃ© NÃºÃ±ez,SÃ£o Paulo,"Itâ€™s done â€” thanks!"
ZoÃ« BrontÃ«,ZÃ¼rich,Price: â‚¬25""",
            """name,city,note
José Núñez,São Paulo,"It’s done — thanks!"
Zoë Brontë,Zürich,Price: €25""",
            "Broken characters",
            "Fixed file",
            "csv",
            "From csv-char-fix/samples/contacts-broken.csv and contacts-fixed.csv.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "$1",
              "https://tidybyte.gumroad.com/l/csv-char-fix",
              cta="Buy on Gumroad",
              note="One Python script. Needs Python 3.8+. CSV and text files only, not .xlsx."),
        ],
        "repos": [],
    },
    {
        "slug": "csv-split",
        "name": "csv-split",
        "category": "data",
        "icon": "split",
        "tagline": "Split a big CSV into smaller files. Every new file keeps the header.",
        "summary": (
            "Use it when a CSV is too big for Excel, too big to upload, or when you want "
            "one file per group, like one file per state."
        ),
        "does": [
            "Splits by row count, number of parts, file size, or a column value.",
            "Keeps the header on every new file.",
            "Reads the file bit by bit, so it can handle files bigger than your computer's memory.",
        ],
        "thumb": PRODUCTS_DIR / "csv-split" / "thumb.png",
        "cover": PRODUCTS_DIR / "csv-split" / "cover.png",
        "input": "One CSV file, plus how you want it split (by rows, size, parts, or a column).",
        "output": "Smaller CSV files that each start with the same header row.",
        "example": E(
            """Order ID,Date,Customer,State,Total
A00001,2026-02-02,Ben Ode,NY,35.43
A00002,2026-03-03,Dev Patel,FL,50.72
A00003,2026-04-04,Ana Ruiz,CA,123.47
… 1,197 more rows (1,200 rows total)""",
            """orders-CA.csv  (header + only CA rows)
orders-FL.csv  (header + only FL rows)
orders-NY.csv  (header + only NY rows)""",
            "One big orders.csv",
            "Split by the State column",
            "csv",
            "From csv-split/samples/orders.csv (1,200 rows) and the README example.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "$1",
              "https://tidybyte.gumroad.com/l/csv-split",
              cta="Buy on Gumroad",
              note="One Python script. Needs Python 3.8+. CSV and text files only, not .xlsx."),
        ],
        "repos": [],
    },
    {
        "slug": "regex-pack",
        "name": "Regex Pack for Messy Data",
        "category": "data",
        "icon": "regex",
        "tagline": "49 ready-to-use regex patterns for emails, phones, dates, money, and more.",
        "summary": (
            "Copy a pattern into your tool, or use the small helper script to check or fix "
            "a CSV column. Every pattern comes with examples that are tested in Python and JavaScript."
        ),
        "does": [
            "49 patterns for contact info, web links, dates, money, text cleanup, and IDs.",
            "Includes a printable cheat sheet, Markdown, JSON, and a helper script.",
            "Every example is tested in Python and JavaScript.",
        ],
        "thumb": PRODUCTS_DIR / "regex-pack" / "thumb.png",
        "cover": PRODUCTS_DIR / "regex-pack" / "cover.png",
        "input": "A value or a CSV column you want to check or tidy.",
        "output": "A match, a cleaned value, or a yes/no, depending on the pattern.",
        "example": E(
            """Before                  After
JosÃ©                   (see csv-char-fix; this pack is regex)
(40)                    -40
$1,234.56               1234.56
Smith, Jane             Jane Smith
03/04/2026              2026-03-04""",
            """Pattern examples from the pack:
  (40)        →  -40
  $1,234.56   →  1234.56
  Smith, Jane →  Jane Smith
  03/04/2026  →  2026-03-04""",
            "Common messy values",
            "What the pack's patterns are for",
            "text",
            "Pattern groups listed in regex-pack/README.md (money, names, dates).",
        ),
        "versions": [
            V("Gumroad", "For your computer", "$2",
              "https://tidybyte.gumroad.com/l/regex-pack",
              cta="Buy on Gumroad",
              note="Patterns are tested in Python and JavaScript. A regex checks shape, not whether a value is real."),
        ],
        "repos": [],
    },
    {
        "slug": "claude-data-skills",
        "name": "CSV Skills for Claude Code",
        "category": "ai",
        "icon": "skills",
        "tagline": "4 Claude Code skills that profile, diff, fix, and split CSV files on your computer.",
        "summary": (
            "Claude runs a small, tested script and reads the short result, instead of "
            "loading a big CSV into the chat line by line. Your data stays on your computer."
        ),
        "does": [
            "csv-profile: a quick look at every column, blanks, duplicates, and broken rows.",
            "csv-diff: compares two CSV files by a key column and shows what changed.",
            "fix-chars and split-csv: fix garbled characters, or split a big file while keeping the header.",
        ],
        "thumb": PRODUCTS_DIR / "claude-data-skills" / "thumb.png",
        "cover": PRODUCTS_DIR / "claude-data-skills" / "cover.png",
        "input": "A CSV or text file on your computer, opened in Claude Code.",
        "output": "A short profile, a diff, a fixed file, or smaller split files. The original can stay unchanged.",
        "example": E(
            """name,city,note
JosÃ© NÃºÃ±ez,SÃ£o Paulo,"Itâ€™s done â€” thanks!"
ZoÃ« BrontÃ«,ZÃ¼rich,Price: â‚¬25""",
            """name,city,note
José Núñez,São Paulo,"It’s done — thanks!"
Zoë Brontë,Zürich,Price: €25""",
            "A broken CSV Claude is asked to fix",
            "After the fix-chars skill runs",
            "csv",
            "The fix-chars skill ships the csv-char-fix sample.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "$3",
              "https://tidybyte.gumroad.com/l/claude-data-skills",
              cta="Buy on Gumroad",
              note="Made for Claude Code. Scripts also run on their own with Python 3.8+. CSV and text only, not .xlsx."),
        ],
        "repos": [],
    },
    {
        "slug": "base64-lite",
        "name": "Base64 Encode & Decode",
        "category": "data",
        "icon": "base64",
        "tagline": "Encode or decode Base64 for text and local files, on your computer.",
        "summary": (
            "Turn text or a local file into Base64, or turn Base64 back into text or bytes. "
            "You can also use the URL-safe alphabet and data-URI output. It runs offline."
        ),
        "does": [
            "Encodes and decodes Base64 for text and local files.",
            "Supports the URL-safe alphabet and data-URI output.",
            "Includes a free MCP server for AI apps. No API key is needed.",
            "The free tool does not fetch file links from the internet. The Apify version does.",
        ],
        "thumb": None,
        "cover": None,
        "gen_art": {"title": "base64-lite", "sub": "Encode and decode Base64, offline", "badge": "FREE LITE"},
        "actor": "base64-encode-decode",
        "event": {"id": "item-converted", "price_usd": 0.001, "unit": "unique texts", "title": "Item converted"},
        "input": "Text or a local file, plus encode, decode, or auto.",
        "output": "Base64 text, a data URI, or the decoded text or bytes.",
        "apify_url": "https://apify.com/tidybytetools/base64-encode-decode",
        "apify_pending": "The Apify listing goes public this week.",
        "example": E(
            "hello world",
            "aGVsbG8gd29ybGQ=",
            "Plain text",
            "Base64",
            "text",
            "From base64-lite/README.md.",
        ),
        "versions": [
            V("GitHub", "Free lite", "Free",
              urls=[("GitHub", "https://github.com/tidybytetools/base64-lite")],
              note="CLI and MCP server. Install for now with: pip install git+https://github.com/tidybytetools/base64-lite. We will switch this to a PyPI install when the package is on PyPI."),
            V("Apify", "Pay per use", "$0.001 per unique item",
              "https://apify.com/tidybytetools/base64-encode-decode",
              card_price="$0.001/item",
              note="Failed items are free. The public store page goes live this week.",
              cta="Try it on Apify"),
        ],
        "repos": ["base64-lite"],
    },
    {
        "slug": "json-repair-lite",
        "name": "JSON Repair",
        "category": "data",
        "icon": "json",
        "tagline": "Repair broken or incomplete JSON, including output from language models.",
        "summary": (
            "Paste JSON that is missing quotes or has a trailing comma, and get valid JSON back. "
            "Already-valid JSON is left alone. It runs offline. No API key is needed."
        ),
        "does": [
            "Repairs broken or incomplete JSON, including common model output.",
            "Can also repair JSON Lines, one document per line.",
            "Includes a free MCP server for AI apps. No API key is needed.",
            "This is a repair step, not a language model. Some text cannot be repaired.",
        ],
        "thumb": None,
        "cover": None,
        "gen_art": {"title": "json-repair-lite", "sub": "Repair broken JSON, offline", "badge": "FREE LITE"},
        "actor": "json-repair",
        "event": {"id": "document-repaired", "price_usd": 0.001, "unit": "documents", "title": "Document saved"},
        "input": "Broken or incomplete JSON, or a local JSON or JSON Lines file.",
        "output": "Valid JSON. Already-valid input is left alone and marked as wasValid.",
        "apify_url": "https://apify.com/tidybytetools/json-repair",
        "apify_pending": "The Apify listing goes public this week.",
        "example": E(
            "{name: 'Ada', ok: true, trailing: 'comma',}",
            '{"name": "Ada", "ok": true, "trailing": "comma"}',
            "Not valid JSON",
            "Repaired JSON",
            "json",
            "From json-repair-lite/README.md.",
        ),
        "versions": [
            V("GitHub", "Free lite", "Free",
              urls=[("GitHub", "https://github.com/tidybytetools/json-repair-lite")],
              note="CLI and MCP server. Install for now with: pip install git+https://github.com/tidybytetools/json-repair-lite. We will switch this to a PyPI install when the package is on PyPI."),
            V("Apify", "Pay per use", "$0.001 per document",
              "https://apify.com/tidybytetools/json-repair",
              card_price="$0.001/document",
              note="Empty or unreadable input is free. The public store page goes live this week.",
              cta="Try it on Apify"),
        ],
        "repos": ["json-repair-lite"],
    },
    {
        "slug": "hash-lite",
        "name": "Hash & Checksum",
        "category": "data",
        "icon": "hash",
        "tagline": "Hash text or local files with SHA-256, SHA-1, MD5, and optional SHA-512.",
        "summary": (
            "Get hex and Base64 hashes for text or a local file. "
            "SHA-256, SHA-1, and MD5 are on by default. Prefer SHA-256 or SHA-512 for new security work."
        ),
        "does": [
            "Hashes text or local files with SHA-256, SHA-1, MD5, and optional SHA-512.",
            "Returns both hex and Base64 forms.",
            "Includes a free MCP server for AI apps. No API key is needed.",
            "MD5 and SHA-1 are included for checks, but they are not safe for new security work.",
        ],
        "thumb": None,
        "cover": None,
        "gen_art": {"title": "hash-lite", "sub": "SHA-256, SHA-1, MD5, SHA-512", "badge": "FREE LITE"},
        "actor": "hash-checksum",
        "event": {"id": "input-hashed", "price_usd": 0.001, "unit": "unique texts", "title": "Input hashed"},
        "input": "Text or a local file, plus the hash algorithms to use.",
        "output": "Hex and Base64 hashes for each selected algorithm.",
        "apify_url": "https://apify.com/tidybytetools/hash-checksum",
        "apify_pending": "The Apify listing goes public this week.",
        "example": E(
            "hello world",
            "sha256: b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9\nsha1:   2aae6c35c94fcfb415dbe95f408b9ce91ee846ed\nmd5:    5eb63bbbe01eeed093cb22bb8f5acdc3",
            "Text in",
            "Default hashes out (SHA-256, SHA-1, MD5)",
            "text",
            "From hash-lite/README.md.",
        ),
        "versions": [
            V("GitHub", "Free lite", "Free",
              urls=[("GitHub", "https://github.com/tidybytetools/hash-lite")],
              note="CLI and MCP server. Install for now with: pip install git+https://github.com/tidybytetools/hash-lite. We will switch this to a PyPI install when the package is on PyPI."),
            V("Apify", "Pay per use", "$0.001 per unique input",
              "https://apify.com/tidybytetools/hash-checksum",
              card_price="$0.001/input",
              note="All selected hashes are included. Repeats in the same run are free. The public store page goes live this week.",
              cta="Try it on Apify"),
        ],
        "repos": ["hash-lite"],
    },
]


OPTIONAL_APIFY = [
    {
        "slug": "html-table-extractor",
        "name": "HTML Table Extractor",
        "category": "web",
        "icon": "table",
        "tagline": "Pull tables from web pages into CSV and JSON.",
        "summary": (
            "Reads HTML tables from a page or pasted HTML. Keeps merged cells, "
            "handles more than one table on a page, and saves CSV. Honest about "
            "tables that only appear after JavaScript runs."
        ),
        "does": [
            "Finds HTML tables on a page or in pasted HTML.",
            "Handles merged cells and more than one table.",
            "Saves CSV and JSON rows. Failed pages are free.",
        ],
        "thumb": None,
        "cover": None,
        "gen_art": {"title": "html-table-extractor", "sub": "Web tables to CSV & JSON", "badge": "PAY PER USE"},
        "actor": "html-table-extractor",
        "event": {"id": "table-row", "price_usd": 0.0005, "unit": "data rows", "title": "Table row saved"},
        "input": "Page links, or pasted HTML that contains tables.",
        "output": "One CSV per table, and one dataset row per data row. Header rows are free.",
        "example": E(
            """<table>
  <caption>Scores</caption>
  <tr><th>Name</th><th colspan="2">Scores</th></tr>
  <tr><td>Ann</td><td>12</td><td>4</td></tr>
  <tr><td>Bob</td><td rowspan="2">8</td><td>1</td></tr>
  <tr><td>Cara</td><td>2</td></tr>
</table>""",
            """Name,Scores,Scores
Ann,12,4
Bob,8,1
Cara,8,2""",
            "HTML with merged cells",
            "Flat rows (rowspan fills Cara's score)",
            "html",
            "From html-table-extractor-apify/tests/test_actor.py.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.0005 per data row",
              "https://apify.com/tidybytetools/html-table-extractor",
              cta="Try it on Apify"),
        ],
        "repos": [],
        "apify_url": "https://apify.com/tidybytetools/html-table-extractor",
        "console_url": "https://console.apify.com/actors/tidybytetools~html-table-extractor",
    },
    {
        "slug": "llm-token-counter",
        "name": "LLM Token Counter",
        "category": "ai",
        "icon": "tokens",
        "tagline": "Count tokens and estimate cost for GPT, Claude, and Gemini.",
        "summary": (
            "Counts tokens offline for OpenAI models and estimates Claude and Gemini. "
            "Uses public list prices. No API key. Paste text or add file links."
        ),
        "does": [
            "Exact OpenAI token counts with tiktoken.",
            "Claude and Gemini counts marked as estimates.",
            "Shows dated public list prices for cost estimates.",
        ],
        "thumb": None,
        "cover": None,
        "gen_art": {"title": "llm-token-counter", "sub": "Tokens & cost, offline", "badge": "PAY PER USE"},
        "actor": "llm-token-counter",
        "event": {"id": "text-counted", "price_usd": 0.0005, "unit": "unique texts", "title": "Text counted"},
        "input": "Pasted text, a list of texts, or file links, plus the models to count.",
        "output": "Token counts per model (exact or estimate) and a cost estimate from public list prices.",
        "example": E(
            """texts:
  Hello tokens
  Hello tokens     (repeat, not charged again)
  A second text
models: gpt-4o, claude-sonnet-5.5""",
            """"Hello tokens"   gpt-4o: exact token count + input cost
                 claude-sonnet-5.5: estimate, marked as estimate
"A second text"  same models, billed once
Repeats and blank lines are free.""",
            "Texts and models",
            "What you get back (from the Actor test)",
            "text",
            "From token-counter-apify/tests/test_actor.py.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.0005 per unique text",
              "https://apify.com/tidybytetools/llm-token-counter",
              cta="Try it on Apify"),
        ],
        "repos": [],
        "apify_url": "https://apify.com/tidybytetools/llm-token-counter",
        "console_url": "https://console.apify.com/actors/tidybytetools~llm-token-counter",
    },
    {
        "slug": "json-to-csv",
        "name": "JSON to CSV Converter",
        "category": "data",
        "icon": "json",
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
        "gen_art": {"title": "json-to-csv", "sub": "Flatten nested JSON for Excel", "badge": "PAY PER USE"},
        "actor": "json-to-csv-flattener",
        "event": {"id": "row-converted", "price_usd": 0.0001, "unit": "rows", "title": "Row converted"},
        "input": "JSON, JSON Lines, or a dataset link. You pick how lists are flattened.",
        "output": "A flat CSV table, with columns like user.name and user.tags.",
        "example": E(
            """[
  {"id": 1, "user": {"name": "Ann", "tags": ["a", "b"]}},
  {"id": 2, "user": {"name": "Bo"}, "ok": true}
]""",
            """id,user.name,user.tags,ok
1,Ann,a; b,
2,Bo,,true""",
            "Nested JSON",
            "Flat CSV",
            "json",
            "From json-to-csv-apify/tests/test_actor.py.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.0001 per row",
              "https://apify.com/tidybytetools/json-to-csv-flattener",
              cta="Try it on Apify"),
        ],
        "repos": [],
        "apify_url": "https://apify.com/tidybytetools/json-to-csv-flattener",
        "console_url": "https://console.apify.com/actors/tidybytetools~json-to-csv-flattener",
    },
    {
        "slug": "csv-encoding-fixer",
        "name": "CSV Encoding Fixer",
        "category": "data",
        "icon": "letters",
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
        "gen_art": {"title": "csv-encoding-fixer", "sub": "Fix mojibake, split big CSVs", "badge": "PAY PER USE"},
        "actor": "csv-encoding-fixer-splitter",
        "event": {"id": "file-fixed", "price_usd": 0.01, "unit": "files", "title": "File fixed"},
        "input": "A CSV file or pasted CSV text. Optional: split into parts after the fix.",
        "output": "A clean UTF-8 CSV that opens right in Excel. Split parts each keep the header.",
        "example": E(
            "name,city\nJosÃ©,MÃ¼nchen\nAnn,Paris",
            "name,city\nJosé,München\nAnn,Paris",
            "Broken CSV",
            "Fixed UTF-8 CSV",
            "csv",
            "From csv-fixer-apify/tests/test_actor.py.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.01 per file",
              "https://apify.com/tidybytetools/csv-encoding-fixer-splitter",
              cta="Try it on Apify"),
        ],
        "repos": [],
        "apify_url": "https://apify.com/tidybytetools/csv-encoding-fixer-splitter",
        "console_url": "https://console.apify.com/actors/tidybytetools~csv-encoding-fixer-splitter",
    },
    {
        "slug": "json-schema-validator",
        "name": "JSON Schema Validator",
        "category": "data",
        "icon": "check",
        "tagline": "Check JSON documents against a schema and see what failed.",
        "summary": (
            "Paste a schema and your JSON. Each document gets a clear pass or fail, "
            "the field that broke, and a plain message. It works offline. No API key is needed."
        ),
        "does": [
            "Checks one or many JSON documents against a schema you paste or load from a link.",
            "Accepts one JSON value, a JSON array, or JSON Lines.",
            "Supports Draft 7, 2019-09, and 2020-12, or reads the draft from $schema.",
            "If the schema itself is not valid, documents are not charged.",
        ],
        "thumb": None,
        "cover": None,
        "gen_art": {"title": "json-schema-validator", "sub": "Bulk JSON Schema checks", "badge": "PAY PER USE"},
        "actor": "json-schema-validator",
        "event": {"id": "document-validated", "price_usd": 0.001, "unit": "documents", "title": "Document validated"},
        "input": "A JSON Schema, plus JSON documents (one value, an array, or JSON Lines).",
        "output": "A pass or fail for each document, the field path, and a plain error message.",
        "example": E(
            """schema: name is a string, age is an integer 0 or more
{"name":"Ann","age":32}
{"name":"Bob","age":-2}
{"age":10}""",
            """Ann   valid
Bob   fail  age: must be 0 or more
(no name) fail  name: this field is required""",
            "Schema plus three documents",
            "Pass or fail with a plain message",
            "json",
            "From json-schema-validator-apify/tests/test_actor.py.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.001 per document",
              "https://apify.com/tidybytetools/json-schema-validator",
              card_price="$0.001/document",
              cta="Try it on Apify"),
        ],
        "repos": [],
        "apify_url": "https://apify.com/tidybytetools/json-schema-validator",
        "console_url": "https://console.apify.com/actors/tidybytetools~json-schema-validator",
    },
    {
        "slug": "link-preview",
        "name": "Link Preview",
        "category": "web",
        "icon": "preview",
        "tagline": "Pull the title, description, and image from a web page.",
        "summary": (
            "Give it a link and get a ready preview: title, description, image, and other "
            "common tags. It reads Open Graph, Twitter Card, and JSON-LD when they are on the page."
        ),
        "does": [
            "Fetches each page and reads the title, description, image, and other common meta tags.",
            "Reads Open Graph, Twitter Card, canonical link, favicon, author, and keywords.",
            "Can also return JSON-LD blocks, often used for articles, products, and events.",
            "Failed pages and exact repeat links in the same run are free.",
        ],
        "thumb": None,
        "cover": None,
        "gen_art": {"title": "link-preview", "sub": "Open Graph, Twitter, JSON-LD", "badge": "PAY PER USE"},
        "actor": "link-preview",
        "event": {"id": "page-previewed", "price_usd": 0.002, "unit": "pages", "title": "Page previewed"},
        "input": "One or more page links.",
        "output": "A preview object with title, description, image, canonical URL, and optional JSON-LD.",
        "example": E(
            """<meta property="og:title" content="OG Title">
<meta property="og:description" content="OG description.">
<meta property="og:image" content="/cover.png">
<link rel="canonical" href="https://example.com/article">
<h1>Heading One</h1>""",
            """title:       OG Title
description: OG description.
image:       https://example.com/cover.png
canonical:   https://example.com/article
heading:     Heading One""",
            "Page meta tags",
            "Ready preview object",
            "html",
            "From link-preview-apify/tests/test_actor.py.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.002 per page",
              "https://apify.com/tidybytetools/link-preview",
              card_price="$0.002/page",
              note="Failed pages and exact repeat links in the same run are free.",
              cta="Try it on Apify"),
        ],
        "repos": [],
        "apify_url": "https://apify.com/tidybytetools/link-preview",
        "console_url": "https://console.apify.com/actors/tidybytetools~link-preview",
    },
    {
        "slug": "language-detector",
        "name": "Language Detector",
        "category": "ai",
        "icon": "lang",
        "tagline": "Detect the language of a text, offline, with a confidence score.",
        "summary": (
            "Paste text and get the language name, ISO codes, and how sure the tool is. "
            "Short or mixed texts are marked as less reliable. No API key is needed."
        ),
        "does": [
            "Detects the language of each text you paste, list, or load from a file.",
            "Returns the language name, ISO 639-1 and ISO 639-3 codes, and a confidence score.",
            "Lists a few close alternatives when the result is not a clear winner.",
            "Marks short or mixed texts as less reliable. Blank lines and repeats are free.",
        ],
        "thumb": None,
        "cover": None,
        "gen_art": {"title": "language-detector", "sub": "ISO codes & confidence, offline", "badge": "PAY PER USE"},
        "actor": "language-detector",
        "event": {"id": "text-detected", "price_usd": 0.0008, "unit": "unique texts", "title": "Text language detected"},
        "input": "Pasted text, a list of texts, or file links.",
        "output": "Language name, ISO 639-1 and 639-3 codes, a confidence score, and close alternatives.",
        "example": E(
            """Hello, how are you today? I hope you are well and the weather is nice.
Bonjour, comment allez-vous aujourd'hui ? J'espere que vous allez bien.""",
            """Hello, how are you today?…     en   English    confidence > 0.5
Bonjour, comment allez-vous…   fr   French     confidence > 0.5""",
            "Two texts",
            "Language and ISO code (from the Actor test)",
            "text",
            "From language-detector-apify/tests/test_actor.py.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.0008 per unique text",
              "https://apify.com/tidybytetools/language-detector",
              card_price="$0.0008/text",
              note="Blank lines and repeats are free.",
              cta="Try it on Apify"),
        ],
        "repos": [],
        "apify_url": "https://apify.com/tidybytetools/language-detector",
        "console_url": "https://console.apify.com/actors/tidybytetools~language-detector",
    },
    {
        "slug": "date-timezone",
        "name": "Date & Timezone Normalizer",
        "category": "data",
        "icon": "date",
        "tagline": "Turn messy dates into a timezone you choose, as ISO 8601.",
        "summary": (
            "It reads dates like \"March 5, 2024 3:30pm\" and dates that could be read two ways. "
            "You get ISO 8601, UTC, and a Unix timestamp. Strings it cannot parse are free."
        ),
        "does": [
            "Parses messy dates, times, and relative phrases like \"tomorrow at 2pm\".",
            "Converts each result to a timezone you choose.",
            "Returns ISO 8601, UTC, a Unix timestamp, and an optional custom format.",
            "Marks numeric dates that could be read two ways (for example 03/04/05) as ambiguous.",
        ],
        "thumb": None,
        "cover": None,
        "gen_art": {"title": "date-timezone-normalizer", "sub": "Parse, convert, ISO 8601", "badge": "PAY PER USE"},
        "actor": "date-timezone-normalizer",
        "event": {"id": "date-normalized", "price_usd": 0.001, "unit": "dates", "title": "Date normalized"},
        "input": "A list of date strings, a source timezone, and a target timezone.",
        "output": "ISO 8601, UTC, a Unix timestamp, and a flag if the date could be read two ways.",
        "example": E(
            """March 5, 2024 3:30pm
2024-03-05T15:30:00Z
05/03/2024
not a date at all
source: America/Chicago   target: UTC""",
            """March 5, 2024 3:30pm   →  2024-03-05T21:30:00+00:00
2024-03-05T15:30:00Z   →  2024-03-05T15:30:00+00:00
05/03/2024             →  2024-05-03 (flagged as ambiguous; also 2024-03-05)
not a date at all      →  not parsed, not charged""",
            "Messy dates",
            "Normalized to UTC (from the Actor test)",
            "text",
            "From date-timezone-apify/tests/test_actor.py.",
        ),
        "versions": [
            V("Apify", "Pay per use", "$0.001 per date",
              "https://apify.com/tidybytetools/date-timezone-normalizer",
              card_price="$0.001/date",
              note="Blank lines, repeats, and strings we cannot parse are free.",
              cta="Try it on Apify"),
        ],
        "repos": [],
        "apify_url": "https://apify.com/tidybytetools/date-timezone-normalizer",
        "console_url": "https://console.apify.com/actors/tidybytetools~date-timezone-normalizer",
    },
]


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
    "date-timezone-normalizer": "date-timezone",
}


HOME_FAQS = [
    ("What is Tidy Byte Tools?", "A small shop of tools that clean up messy data. We sell downloads you run on your computer, and pay-per-use tools on Apify. Free lite tools are on GitHub and PyPI."),
    ("Will you see my files?", "The download tools run on your computer, so those files stay with you. The Apify tools run in your own Apify account. This website does not take uploads."),
    ("What is the difference between free and paid?", "The free lite tools cover the common case, like a text PDF or a simple list of links. Paid versions add things like Excel output, scanned pages, Word files, or folder support. Each tool page lists the difference."),
    ("What does pay per use mean?", "On Apify you pay for what the tool does, such as each page with a table or each link checked. Failed or skipped items are free. Each run also has a $0.00005 start fee. The exact price is on the tool page and on Apify."),
    ("Do the free tools work with AI apps?", "Yes. The free lite tools include a small MCP server you run on your computer. The Apify tools can also be called from Apify MCP. No API key is needed for the local tools."),
    ("How do I get help?", "Open an issue on the GitHub page for that tool. For a Gumroad or Apify purchase, you can also use the support option on that site."),
]
