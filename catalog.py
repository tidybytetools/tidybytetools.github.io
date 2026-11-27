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
            V("Gumroad", "For n8n", "From $1",
              "https://tidybyte.gumroad.com/l/n8n-data-cleanup-pack",
              cta="Buy on Gumroad",
              note="Pay what you want, suggested $5. Tested on self-hosted n8n 2.46.4. Workflows that read files from disk need self-hosted n8n."),
            V("Gumroad", "Free sample", "Free",
              "https://tidybyte.gumroad.com/l/n8n-cleanup-sampler",
              cta="Get free on Gumroad",
              note="Two workflows from the pack: CSV cleanup and uptime alerts."),
            V("Gumroad", "Also: prompts and reliability", "From $1",
              "https://tidybyte.gumroad.com/l/n8n-prompt-reliability-pack",
              cta="See on Gumroad",
              note="12 AI prompts and 4 workflows for error alerts, retries, duplicate webhooks, and lead checks."),
            V("Gumroad", "Also: n8n Builder Kit", "$9",
              "https://tidybyte.gumroad.com/l/n8n-builder-kit-claude-code",
              cta="See on Gumroad",
              note="3 skills, a 27-rule linter, and a lookup of all 572 n8n nodes, so AI agents write workflows that import and run."),
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
            "Leads to the full n8n Data Cleanup Pack (from $1) with 9 workflows.",
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
              note="Two workflows from the n8n Data Cleanup Pack (from $1). The CSV cleanup workflow needs self-hosted n8n."),
            V("Gumroad", "Full data cleanup pack", "From $1",
              "https://tidybyte.gumroad.com/l/n8n-data-cleanup-pack",
              cta="Buy on Gumroad",
              note="9 workflows, pay what you want, suggested $5."),
            V("Gumroad", "Also: prompts and reliability", "From $1",
              "https://tidybyte.gumroad.com/l/n8n-prompt-reliability-pack",
              cta="See on Gumroad",
              note="12 AI prompts and 4 workflows for error alerts, retries, duplicate webhooks, and lead checks."),
            V("Gumroad", "Also: n8n Builder Kit", "$9",
              "https://tidybyte.gumroad.com/l/n8n-builder-kit-claude-code",
              cta="See on Gumroad",
              note="3 skills, a 27-rule linter, and a lookup of all 572 n8n nodes, so AI agents write workflows that import and run."),
        ],
        "repos": [],
    },
    {
        "slug": "n8n-prompt-reliability-pack",
        "name": "n8n Prompt + Reliability Pack",
        "category": "n8n",
        "icon": "workflow",
        "tagline": "12 AI prompts plus 4 n8n workflows for alerts, retries, duplicate webhooks, and lead checks.",
        "summary": (
            "Most n8n workflows work on day one and break on day thirty. This pack helps you "
            "build faster with AI, and build so a failure is not silent."
        ),
        "does": [
            "12 copy-paste prompts for Claude, ChatGPT, or Gemini, with rules that keep secrets out and add an error path.",
            "Four ready-to-import workflows: error alerts, ignore duplicate webhooks, retry an API with a fallback, and validate leads.",
            "Built-in nodes only. No secrets in the files. Each workflow has sticky notes and sample data.",
        ],
        "thumb": PRODUCTS_DIR / "n8n-prompt-reliability-pack" / "thumb.png",
        "cover": PRODUCTS_DIR / "n8n-prompt-reliability-pack" / "cover.png",
        "input": "A webhook, a failed n8n run, or an API URL, plus the sample data in each workflow.",
        "output": "An alert message, a processed-or-ignored reply, a fallback result, or a lead report with HTTP 200, 422, or 502.",
        "example": E(
            """POST /webhook/validate-leads
[
  {"name":"  Ana Ruiz ","email":"ANA@Example.com "},
  {"name":"Bo","email":"bo-at-example.com","phone":"12"},
  {"name":"","email":"cy@example.com"}
]""",
            """HTTP 422
checked: 3
accepted: 1
rejected: 2
results:
  Ana Ruiz   accepted  ana@example.com
  Bo         rejected  email does not look right; phone needs 7 to 15 digits
  (empty)    rejected  name is missing or too short""",
            "Three leads posted to the webhook",
            "Report from a real n8n 2.46.4 run",
            "text",
            "From a test run of 04-validate-and-route-incoming-leads.json in n8n 2.46.4.",
        ),
        "versions": [
            V("Gumroad", "For n8n", "From $1",
              "https://tidybyte.gumroad.com/l/n8n-prompt-reliability-pack",
              cta="Buy on Gumroad",
              note="Pay what you want, suggested $5. Tested on self-hosted n8n 2.46.4. Not tested on n8n Cloud or with a real Discord or Slack account."),
            V("Gumroad", "Free data-cleanup sample", "Free",
              "https://tidybyte.gumroad.com/l/n8n-cleanup-sampler",
              cta="Get free on Gumroad",
              note="Two free cleanup workflows, separate from this pack."),
            V("Gumroad", "Also: n8n Builder Kit", "$9",
              "https://tidybyte.gumroad.com/l/n8n-builder-kit-claude-code",
              cta="See on Gumroad",
              note="3 skills, a 27-rule linter, and a lookup of all 572 n8n nodes, so AI agents write workflows that import and run."),
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
            V("Gumroad", "Also: 8 dev cheat sheets", "$3",
              "https://tidybyte.gumroad.com/l/dev-cheat-sheets",
              cta="See on Gumroad",
              note="One-page PDFs for git, curl and jq, SQL, cron, Docker, grep/sed/awk, ssh, and Python CSV."),
        ],
        "repos": [],
    },
    {
        "slug": "dev-cheat-sheets",
        "name": "Dev Cheat Sheets",
        "category": "data",
        "icon": "doc",
        "tagline": "8 one-page PDFs for git, curl and jq, SQL, cron, Docker, grep/sed/awk, ssh, and Python CSV.",
        "summary": (
            "You know the command. You just cannot remember the flag. These one-page sheets "
            "put the answers where you can see them. Print them, or keep the PDF open."
        ),
        "does": [
            "Eight letter-size PDFs, one page each, plus one combined PDF and Markdown copies you can search.",
            "A test script that runs the safe examples (git, jq, grep, sed, awk, SQL, and the Python snippets).",
            "Commands that delete things are marked DANGER or careful.",
        ],
        "thumb": PRODUCTS_DIR / "dev-cheat-sheets" / "thumb.png",
        "cover": PRODUCTS_DIR / "dev-cheat-sheets" / "cover.png",
        "input": "A question like how to undo a commit, call an API, or write a cron line.",
        "output": "The command and a short note, on a one-page PDF or in the Markdown copy.",
        "example": E(
            """# I need to call an API and pull one field
curl ?  jq ?""",
            """curl -fsS https://api.example.com/items | jq -r '.items[].name'

# Other curl + jq lines on the same page:
curl -s -o /dev/null -w "%{http_code}\n" URL
jq -r '.items[] | [.id, .name] | @csv' file.json
jq empty file.json && echo ok""",
            "A common lookup",
            "Lines from the curl + jq sheet",
            "text",
            "From sheets/curl-jq-cheat-sheet.md. The safe examples were run by test_examples.sh.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "$3",
              "https://tidybyte.gumroad.com/l/dev-cheat-sheets",
              cta="Buy on Gumroad",
              note="Not tested here: ssh, scp, rsync, Docker, crontab, and curl against a live server. Those limits are listed in the README."),
            V("Gumroad", "Also: All Tidy Byte Agent Packs", "$19",
              "https://tidybyte.gumroad.com/l/all-agent-packs",
              cta="See the bundle",
              note="All 6 agent packs in one bundle for $19. Bought alone at each pack's minimum, they come to $24 (the struck-through price Gumroad shows)."),
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
            V("Gumroad", "Bigger pack: 8 data skills", "From $1",
              "https://tidybyte.gumroad.com/l/agent-data-skills",
              cta="See on Gumroad",
              note="These 4 CSV skills plus json-repair, json-flatten, pii-redact, and md-chunk, for Claude Code, Cursor, and Codex. Suggested $7."),
            V("Gumroad", "Also: AGENTS.md starter pack", "From $1",
              "https://tidybyte.gumroad.com/l/agents-md-starter-pack",
              cta="See on Gumroad",
              note="12 instruction files that tell Codex, Cursor, and Claude Code how your project works."),
            V("Gumroad", "Also: Ship-Ready Skills Pack", "From $1",
              "https://tidybyte.gumroad.com/l/ship-ready-skills-pack",
              cta="See on Gumroad",
              note="10 tested skills for code review, tests, secret scans, and changelogs. Suggested $7."),
        ],
        "repos": [],
    },
    {
        "slug": "agent-data-skills",
        "name": "Agent Data Skills Pack",
        "category": "ai",
        "icon": "skills",
        "tagline": "8 tested skills that let Claude Code, Cursor, and Codex clean CSV, repair JSON, hide personal info, and chunk Markdown.",
        "summary": (
            "Each skill is a SKILL.md file plus a small tested Python script that runs on your computer. "
            "The agent runs the script and reads a short result, instead of loading a whole file into the chat."
        ),
        "does": [
            "csv-profile, csv-diff, fix-chars, and split-csv for messy CSV files.",
            "json-repair and json-flatten for broken or nested JSON from AI chats and exports.",
            "pii-redact hides emails, phones, card numbers, and US SSNs. md-chunk splits Markdown for search or RAG.",
        ],
        "thumb": PRODUCTS_DIR / "agent-data-skills" / "thumb.png",
        "cover": PRODUCTS_DIR / "agent-data-skills" / "cover.png",
        "input": "A CSV, JSON, text, or Markdown file on your computer.",
        "output": "A profile, a diff, a fixed file, a CSV, a redacted copy, or JSONL chunks. The original can stay unchanged.",
        "example": E(
            """Please call Jane at +1 (415) 555-0134 or email jane.doe@example.com.
Card 4242 4242 4242 4242 (test Visa that passes Luhn). SSN 219-09-9999.""",
            """Please call Jane at [PHONE] or email [EMAIL].
Card [CARD] (test Visa that passes Luhn). SSN [SSN].""",
            "samples/pii-sample.txt (made-up test data)",
            "After the pii-redact skill runs",
            "text",
            "A real run of redact_pii.py from the pack on its sample file.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "From $1",
              "https://tidybyte.gumroad.com/l/agent-data-skills",
              cta="Buy on Gumroad",
              note="Pay what you want, suggested $7. Needs Python 3.9+. CSV and text only, not .xlsx. pii-redact is regex only, not a compliance tool."),
            V("Gumroad", "Free skill sample", "Free",
              "https://tidybyte.gumroad.com/l/json-repair-skill-free",
              cta="Get free sample",
              note="The json-repair skill on its own. 1 of the 8 skills in this pack."),
            V("Gumroad", "Also: Ship-Ready Skills Pack", "From $1",
              "https://tidybyte.gumroad.com/l/ship-ready-skills-pack",
              cta="See on Gumroad",
              note="10 tested skills for code review, tests, secret scans, and changelogs. Suggested $7."),
            V("Gumroad", "Also: All Tidy Byte Agent Packs", "$19",
              "https://tidybyte.gumroad.com/l/all-agent-packs",
              cta="See the bundle",
              note="All 6 agent packs in one bundle for $19. Bought alone at each pack's minimum, they come to $24 (the struck-through price Gumroad shows)."),
        ],
        "repos": [],
    },
    {
        "slug": "agents-md-starter-pack",
        "name": "AGENTS.md Starter Pack",
        "category": "ai",
        "icon": "skills",
        "tagline": "12 instruction files that tell Codex, Cursor, and Claude Code how your project works.",
        "summary": (
            "An AGENTS.md file is a plain note that lists your commands, your rules, and how "
            "the agent should prove its work. Copy one template, change a few lines, and you are done."
        ),
        "does": [
            "12 templates: Python CLI, data scripts, Node API, React, Cloudflare Worker, docs site, n8n repo, skill repo, Django, research notes, monorepo, and bug-fix mode.",
            "7 short rule blocks you can mix in, such as secrets and safety, small diffs, and test first.",
            "An install script that copies a template into your project and never overwrites a file you already have.",
        ],
        "thumb": PRODUCTS_DIR / "agents-md-starter-pack" / "thumb.png",
        "cover": PRODUCTS_DIR / "agents-md-starter-pack" / "cover.png",
        "input": "Your project folder, and the template that matches it.",
        "output": "An AGENTS.md file, and a CLAUDE.md that imports it so Claude Code reads it too.",
        "example": E(
            """# AGENTS.md: Python command-line tool

## Commands (run these, do not guess)
- Run tests: `pytest -q`
- Lint: `ruff check .`

## Rules
- Ask before adding a new dependency.
- Never print a secret.

## Before you say you are done
1. Run pytest -q and ruff check .
2. Paste the last lines of each.""",
            """./install.sh 01 ~/code/mytool secrets-and-safety test-first
Wrote ~/code/mytool/AGENTS.md
Wrote ~/code/mytool/CLAUDE.md (imports AGENTS.md)""",
            "Part of the Python CLI template",
            "What the install script prints",
            "text",
            "From templates/01-python-cli.md and a real install.sh run.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "From $1",
              "https://tidybyte.gumroad.com/l/agents-md-starter-pack",
              cta="Buy on Gumroad",
              note="Pay what you want, suggested $5. These are text files. An agent can still ignore a rule. Change the commands to match your project."),
            V("Gumroad", "Also: Ship-Ready Skills Pack", "From $1",
              "https://tidybyte.gumroad.com/l/ship-ready-skills-pack",
              cta="See on Gumroad",
              note="10 tested skills for code review, tests, secret scans, and changelogs. Suggested $7."),
            V("Gumroad", "Free skill sample", "Free",
              "https://tidybyte.gumroad.com/l/json-repair-skill-free",
              cta="Get free sample",
              note="A free JSON repair skill, also on GitHub at github.com/tidybytetools/json-repair-skill. Separate from this pack."),
            V("Gumroad", "Also: Dev OS in Claude Code", "$9",
              "https://tidybyte.gumroad.com/l/dev-os-claude-code",
              cta="See on Gumroad",
              note="15 skills, 5 subagents, and 4 safety hooks, plus an installer. A daily workflow kit for Claude Code."),
            V("Gumroad", "Free: Agent Cost Saver", "Free",
              "https://tidybyte.gumroad.com/l/agent-cost-saver",
              cta="Get free guide",
              note="A short guide and 4 scripts for cutting Claude Code, Cursor, and Codex token costs."),
            V("Gumroad", "Also: All Tidy Byte Agent Packs", "$19",
              "https://tidybyte.gumroad.com/l/all-agent-packs",
              cta="See the bundle",
              note="All 6 agent packs in one bundle for $19. Bought alone at each pack's minimum, they come to $24 (the struck-through price Gumroad shows)."),
        ],
        "repos": [],
    },
    {
        "slug": "ship-ready-skills-pack",
        "name": "Ship-Ready Skills Pack",
        "category": "ai",
        "icon": "skills",
        "tagline": "10 tested agent skills that make Claude Code, Cursor, and Codex prove the work before they say done.",
        "summary": (
            "AI coding agents are fast, and they also say they are done when the tests never ran. "
            "This pack gives the agent 10 skills, 8 with a small Python script, so it works from real output."
        ),
        "does": [
            "verify-before-done finds and runs your real lint, type, test, and build commands, then reports PASS or FAIL.",
            "code-review, write-tests, changelog, release notes, PR text, secret scan, dependency check, bug repro, and API docs.",
            "install.sh copies the skills into Claude Code and Cursor and never overwrites a skill you already have, unless you pass --force.",
        ],
        "thumb": PRODUCTS_DIR / "ship-ready-skills-pack" / "thumb.png",
        "cover": PRODUCTS_DIR / "ship-ready-skills-pack" / "cover.png",
        "input": "Your project folder, plus the skill the agent should follow.",
        "output": "A PASS or FAIL from your real checks, a ranked review, a test list, a changelog, or a secret scan with the values masked.",
        "example": E(
            """# in your project folder
sh install.sh --project
python3 .claude/skills/verify-before-done/scripts/find_checks.py .""",
            """installed ./.claude/skills/verify-before-done
installed ./.claude/skills/code-review
# ...8 more skills...
Checks for /home/you/myapp:
  test    python3 -m pytest -q                     (from pyproject.toml)
CI runs these (match them if you can):
  - python -m unittest discover -s tests -v   (.github/workflows/tests.yml)""",
            "Install, then find the real checks",
            "What the script printed on a real Python repo",
            "text",
            "install.sh is from the pack. find_checks.py was run on json-repair-lite.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "From $1",
              "https://tidybyte.gumroad.com/l/ship-ready-skills-pack",
              cta="Buy on Gumroad",
              note="Pay what you want, suggested $7. Scripts use the Python standard library only. An agent can still ignore a skill."),
            V("Gumroad", "Free sample skill", "Free",
              "https://tidybyte.gumroad.com/l/verify-before-done-free",
              cta="Get free sample",
              note="The verify-before-done skill, plus a short definition-of-done block. 1 of the 10 skills in this pack."),
            V("Gumroad", "Also: Dev OS in Claude Code", "$9",
              "https://tidybyte.gumroad.com/l/dev-os-claude-code",
              cta="See on Gumroad",
              note="15 skills, 5 subagents, and 4 safety hooks, plus an installer. A daily workflow kit for Claude Code."),
            V("Gumroad", "Free: Agent Cost Saver", "Free",
              "https://tidybyte.gumroad.com/l/agent-cost-saver",
              cta="Get free guide",
              note="A short guide and 4 scripts for cutting Claude Code, Cursor, and Codex token costs. No made-up savings numbers."),
            V("Gumroad", "Also: All Tidy Byte Agent Packs", "$19",
              "https://tidybyte.gumroad.com/l/all-agent-packs",
              cta="See the bundle",
              note="All 6 agent packs in one bundle for $19. Bought alone at each pack's minimum, they come to $24 (the struck-through price Gumroad shows)."),
            V("Gumroad", "Also: Anti-Slop Kit", "$9",
              "https://tidybyte.gumroad.com/l/anti-slop-kit",
              cta="See on Gumroad",
              note="A tested checker, 4 skills, hooks, and CI that keep AI-written docs, commits, and PR text plain."),
        ],
        "repos": [],
    },
    {
        "slug": "verify-before-done-free",
        "name": "Verify Before Done",
        "category": "ai",
        "icon": "skills",
        "tagline": "A free agent skill that makes Claude Code, Cursor, and Codex run your real tests before they say done.",
        "summary": (
            "Your AI coding agent says it is done. Did it run the tests? This free skill finds your "
            "real lint, type, test, and build commands, runs them, and shows PASS or FAIL."
        ),
        "does": [
            "Finds your project's real check commands from package.json, pyproject.toml, Makefile, Cargo.toml, go.mod, and CI files.",
            "Runs them in order and reports PASS or FAIL with the last lines of output. It must not delete or skip a test to get a green result.",
            "Includes a short definition-of-done block you can add to AGENTS.md or CLAUDE.md.",
        ],
        "thumb": PRODUCTS_DIR / "verify-before-done-free" / "thumb.png",
        "cover": PRODUCTS_DIR / "verify-before-done-free" / "cover.png",
        "input": "Your project folder.",
        "output": "A list of the checks it found, then PASS or FAIL for each one, plus three lines: Checks run, What changed, Not checked.",
        "example": E(
            "python3 scripts/find_checks.py /home/you/myapp",
            """Checks for /home/you/myapp:
  test    python3 -m pytest -q                     (from pyproject.toml)
CI runs these (match them if you can):
  - python -m unittest discover -s tests -v   (.github/workflows/tests.yml)""",
            "Ask the skill to find the checks",
            "What find_checks.py printed on a real Python repo",
            "text",
            "Run on json-repair-lite with the script from this free skill.",
        ),
        "versions": [
            V("Gumroad", "Free sample", "Free",
              "https://tidybyte.gumroad.com/l/verify-before-done-free",
              cta="Get free on Gumroad",
              note="Free to use in any project. Pay what you want, $0+."),
            V("Gumroad", "Full 10-skill pack", "From $1",
              "https://tidybyte.gumroad.com/l/ship-ready-skills-pack",
              cta="See on Gumroad",
              note="Adds code review, tests, secret scan, changelog, release notes, PR text, dependency checks, bug repro, and API docs. Suggested $7."),
            V("Gumroad", "Free: Agent Cost Saver", "Free",
              "https://tidybyte.gumroad.com/l/agent-cost-saver",
              cta="Get free guide",
              note="A short guide and 4 scripts for cutting Claude Code, Cursor, and Codex token costs."),
            V("Gumroad", "Free: Anti-Slop Rules", "Free",
              "https://tidybyte.gumroad.com/l/anti-slop-rules-free",
              cta="Get free rules",
              note="12 plain-writing rules and a de-slop skill for Claude Code, Cursor, and Codex."),
        ],
        "repos": [],
    },
    {
        "slug": "agent-cost-saver",
        "name": "Agent Cost Saver",
        "category": "ai",
        "icon": "skills",
        "tagline": "A free guide and 4 scripts to cut Claude Code, Cursor, and Codex token costs.",
        "summary": (
            "Your AI coding agent costs more than it should. Most of the waste comes from a few habits "
            "and a few big files. This free pack shows you which ones, then lets you measure before and after."
        ),
        "does": [
            "A short guide for each tool: 14 Claude Code habits, 8 Cursor habits, and 9 Codex habits, with the exact command or setting and a link to the official docs (checked Nov 25, 2026).",
            "cost_audit.py scans a project for what is sent with every request. session_report.py totals tokens per Claude Code session from your own local logs.",
            "make_ignore.py suggests a .cursorignore and Claude Code Read-deny rules. filter_test_output.py is a hook that keeps test output short and keeps the real exit code.",
        ],
        "thumb": PRODUCTS_DIR / "agent-cost-saver" / "thumb.png",
        "cover": PRODUCTS_DIR / "agent-cost-saver" / "cover.png",
        "input": "Your project folder, plus, for the session report, your local Claude Code logs.",
        "output": "A ranked fix list, a per-session token total, a suggested ignore file, or a hook that shortens test output.",
        "example": E(
            "python3 scripts/cost_audit.py demo-project",
            """Sent with every request if your tools read all of these (rough guess): up to about 9,186 tokens
  CLAUDE.md: 225 lines, about 4,444 tokens
  Cursor always-apply rules: about 3,810 tokens
[HIGH] CLAUDE.md and AGENTS.md repeat the same text
   Fix: Keep the rules in AGENTS.md and make CLAUDE.md one line: @AGENTS.md
1 high, 4 medium, 2 info. Token numbers are rough (characters / 4).""",
            "Run the audit on the sample project",
            "What cost_audit.py printed",
            "text",
            "From samples/cost-audit-demo-output.txt in the pack (the included demo project).",
        ),
        "versions": [
            V("GitHub", "Source (MIT)", "Free",
              "https://github.com/tidybytetools/agent-cost-saver",
              cta="View on GitHub",
              note="Clone or download. Same files as the Gumroad pack. Release v1.0.0. MIT license."),
            V("Gumroad", "Free guide", "Free",
              "https://tidybyte.gumroad.com/l/agent-cost-saver",
              cta="Get free on Gumroad",
              note="Free to use and change (MIT). Pay what you want, $0+. It does not promise a percent saved. Measure before and after instead. Also on GitHub at github.com/tidybytetools/agent-cost-saver."),
            V("Gumroad", "Also: Ship-Ready Skills Pack", "From $1",
              "https://tidybyte.gumroad.com/l/ship-ready-skills-pack",
              cta="See on Gumroad",
              note="10 tested skills for code review, tests, secret scans, and changelogs. Suggested $7."),
            V("Gumroad", "Also: AGENTS.md starter pack", "From $1",
              "https://tidybyte.gumroad.com/l/agents-md-starter-pack",
              cta="See on Gumroad",
              note="12 instruction files that tell Codex, Cursor, and Claude Code how your project works."),
            V("Gumroad", "Also: Dev OS in Claude Code", "$9",
              "https://tidybyte.gumroad.com/l/dev-os-claude-code",
              cta="See on Gumroad",
              note="15 skills, 5 subagents, and 4 safety hooks, plus an installer. A daily workflow kit for Claude Code."),
            V("Gumroad", "Free: Anti-Slop Rules", "Free",
              "https://tidybyte.gumroad.com/l/anti-slop-rules-free",
              cta="Get free rules",
              note="12 plain-writing rules and a de-slop skill for Claude Code, Cursor, and Codex."),
        ],
        "repos": ["agent-cost-saver"],
    },
    {
        "slug": "dev-os-claude-code",
        "name": "Dev OS in Claude Code",
        "category": "ai",
        "icon": "skills",
        "tagline": "15 skills, 5 subagents, and 4 safety hooks that turn a Claude Code day into a repeatable loop.",
        "summary": (
            "Claude Code is powerful, but every day starts the same way: re-explain the project, hope it checks "
            "its work, hope it does not run something nasty. This kit installs into a project in about 5 minutes."
        ),
        "does": [
            "15 slash-command skills for the daily loop: start, plan, build, review, commit, hand off, plus fix, test, explain, refactor, and release.",
            "5 subagents (a cheap file finder, a reviewer, a test runner, a security pass, and a docs writer) and 4 hooks that block dangerous shell commands, protect .env and keys, format the file just written, and show your branch at session start.",
            "A safe installer (dry run by default, merges your settings, never overwrites your files, can be undone) and a doctor script that checks the install.",
        ],
        "thumb": PRODUCTS_DIR / "dev-os-claude-code" / "thumb.png",
        "cover": PRODUCTS_DIR / "dev-os-claude-code" / "cover.png",
        "input": "Your project folder.",
        "output": "A .claude/ folder with skills, subagents, hooks, and merged settings, plus a short status from the doctor.",
        "example": E(
            """python3 install.py /path/to/your/project --apply --with-claude-md
python3 doctor.py /path/to/your/project""",
            """PASS  15 skills have valid frontmatter
PASS  5 subagents have valid frontmatter
PASS  settings.json calls all four hooks
0 fail, 0 warn. Looks good. Open Claude Code here and type /dev-start.""",
            "Install, then check",
            "What doctor.py printed after a real install",
            "text",
            "install.py --apply --with-claude-md and doctor.py were run on a temporary git repo.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "$9",
              "https://tidybyte.gumroad.com/l/dev-os-claude-code",
              cta="Buy on Gumroad",
              note="Fixed $9. You may use it in your own projects, including client work. Please do not resell it. The hooks match command patterns; they are not a sandbox. Keep Claude Code's permission prompts on."),
            V("Gumroad", "Free: Agent Cost Saver", "Free",
              "https://tidybyte.gumroad.com/l/agent-cost-saver",
              cta="Get free guide",
              note="A short guide and 4 scripts for cutting Claude Code, Cursor, and Codex token costs."),
            V("Gumroad", "Also: Ship-Ready Skills Pack", "From $1",
              "https://tidybyte.gumroad.com/l/ship-ready-skills-pack",
              cta="See on Gumroad",
              note="10 tested skills for code review, tests, secret scans, and changelogs. Suggested $7."),
            V("Gumroad", "Also: All Tidy Byte Agent Packs", "$19",
              "https://tidybyte.gumroad.com/l/all-agent-packs",
              cta="See the bundle",
              note="All 6 agent packs in one bundle for $19. Bought alone at each pack's minimum, they come to $24 (the struck-through price Gumroad shows)."),
            V("Gumroad", "Also: Anti-Slop Kit", "$9",
              "https://tidybyte.gumroad.com/l/anti-slop-kit",
              cta="See on Gumroad",
              note="A tested checker, 4 skills, hooks, and CI that keep AI-written docs, commits, and PR text plain."),
        ],
        "repos": [],
    },
    {
        "slug": "anti-slop-kit",
        "name": "Anti-Slop Kit",
        "category": "ai",
        "icon": "skills",
        "tagline": "A tested checker, 4 skills, hooks, and CI that keep AI-written READMEs, docs, commits, and PR text plain.",
        "summary": (
            "AI coding agents often write the same way: \"Certainly!\", \"blazing fast\", \"seamless\", "
            "\"It's not X, it's Y\", em dashes, and emoji bullets. This kit finds those patterns with a script "
            "and gives Claude Code, Cursor, and Codex the rules to write plainly."
        ),
        "does": [
            "slop_check.py checks Markdown and text. No AI. Python 3.8+, standard library only. About 150 phrases plus 10 pattern checks, each with a line number and a plain fix. It skips code, URLs, and front matter.",
            "4 skills: slop-check, de-slop, plain-readme, and plain-commits-and-prs. A Claude Code hook, a git commit-msg hook, and a GitHub Action.",
            "12 writing rules, a Cursor rule, a settings file, before and after examples, and 35 tests you can run yourself.",
        ],
        "thumb": PRODUCTS_DIR / "anti-slop-kit" / "thumb.png",
        "cover": PRODUCTS_DIR / "anti-slop-kit" / "cover.png",
        "input": "A README, docs folder, pull request text, or commit message.",
        "output": "A list of findings with line, severity, and a plain fix, or a rewrite that keeps your facts and code the same.",
        "example": E(
            """$ python3 scripts/slop_check.py examples/README-before.md
README-before.md:3:102  HIGH  "game-changer"
README-before.md:7:5    HIGH  "Blazing fast"
README-before.md:13:1   HIGH  "Let's dive in"
22 findings, 101 words, score 51.49 (heavy)""",
            """$ python3 scripts/slop_check.py examples/README-after.md
0 findings, 73 words, score 0.0 (clean)""",
            "A real run on the kit's sample AI-style README",
            "The same run on the rewritten README in the kit",
            "text",
            "slop_check.py was run on examples/README-before.md and examples/README-after.md from the kit.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "$9",
              "https://tidybyte.gumroad.com/l/anti-slop-kit",
              cta="Buy on Gumroad",
              note="Fixed $9. It is not an AI detector. It checks words and patterns, in English only. Free prompt-only anti-slop skills exist on GitHub; this kit adds the tested checker, hooks, and CI."),
            V("Gumroad", "Free: Anti-Slop Rules", "Free",
              "https://tidybyte.gumroad.com/l/anti-slop-rules-free",
              cta="Get free rules",
              note="12 writing rules, a Cursor rule, an AGENTS.md block, and a de-slop skill. Instructions only. Nothing checks the result."),
            V("Gumroad", "Also: All Tidy Byte Agent Packs", "$19",
              "https://tidybyte.gumroad.com/l/all-agent-packs",
              cta="See the bundle",
              note="This kit plus Ship-Ready, Dev OS, Agent Data Skills, the AGENTS.md Starter Pack, and Dev Cheat Sheets. $19. Bought alone at each pack's minimum, they come to $24."),
        ],
        "repos": [],
    },
    {
        "slug": "anti-slop-rules-free",
        "name": "Anti-Slop Rules",
        "category": "ai",
        "icon": "skills",
        "tagline": "Free: 12 plain-writing rules and a de-slop skill for Claude Code, Cursor, and Codex.",
        "summary": (
            "Your AI coding agent writes READMEs, commit messages, and PR text. These free rules "
            "make it write them plainly, without \"Certainly!\", \"blazing fast\", or emoji bullets."
        ),
        "does": [
            "12 writing rules you can paste into CLAUDE.md, AGENTS.md, or any agent instructions.",
            "The same rules as a Cursor rule file, plus a short AGENTS.md block for Codex and other tools.",
            "A de-slop-lite skill that rewrites text in plain words and keeps your facts, commands, and code the same.",
        ],
        "thumb": PRODUCTS_DIR / "anti-slop-rules-free" / "thumb.png",
        "cover": PRODUCTS_DIR / "anti-slop-rules-free" / "cover.png",
        "input": "A README, docs page, pull request, or commit message you want written in plain words.",
        "output": "A rewritten draft, plus a short list of what changed.",
        "example": E(
            """Welcome to QuickCSV! In today's fast-paced world, working with data shouldn't be hard. QuickCSV is a game-changer that will revolutionize the way you handle CSV files.""",
            """QuickCSV cleans messy CSV files from the command line: it fixes broken quotes, trims spaces and removes duplicate rows.""",
            "A typical AI-written intro",
            "The same facts, rewritten with the free rules",
            "text",
            "From examples in the paid Anti-Slop Kit, which uses the same 12 rules.",
        ),
        "versions": [
            V("GitHub", "Source (MIT)", "Free",
              "https://github.com/tidybytetools/anti-slop-rules",
              cta="View on GitHub",
              note="Clone or download, or add the Claude Code plugin marketplace. Same rules as the Gumroad pack. Release v1.0.0. MIT license."),
            V("Gumroad", "Free rules", "Free",
              "https://tidybyte.gumroad.com/l/anti-slop-rules-free",
              cta="Get free on Gumroad",
              note="Free to use and change (MIT). Pay what you want, $0+. This version is instructions only. Nothing checks the result. Also on GitHub at github.com/tidybytetools/anti-slop-rules."),
            V("Gumroad", "Full Anti-Slop Kit", "$9",
              "https://tidybyte.gumroad.com/l/anti-slop-kit",
              cta="See on Gumroad",
              note="Adds the tested checker, a Claude Code hook, a git hook, a GitHub Action, and 4 skills. Fixed $9."),
        ],
        "repos": ["anti-slop-rules"],
    },
    {
        "slug": "all-agent-packs",
        "name": "All Tidy Byte Agent Packs",
        "category": "ai",
        "icon": "skills",
        "tagline": "6 packs for Claude Code, Cursor, and Codex in one bundle: skills, hooks, AGENTS.md, and the Anti-Slop Kit.",
        "summary": (
            "Every Tidy Byte pack for AI coding agents, in one purchase. Each pack has its own README and tests. "
            "The bundle is $19. Bought alone at each pack's minimum price, they come to $24, which is the struck-through price Gumroad shows."
        ),
        "does": [
            "Ship-Ready Skills Pack (10 skills) and Dev OS in Claude Code (15 skills, 5 subagents, 4 safety hooks).",
            "Anti-Slop Kit (checker, 4 skills, hooks, and CI) and Agent Data Skills Pack (8 skills for CSV, JSON, PII, and Markdown).",
            "AGENTS.md Starter Pack (12 instruction files) and Dev Cheat Sheets (8 one-page PDFs).",
        ],
        "thumb": PRODUCTS_DIR / "all-agent-packs" / "thumb.png",
        "cover": PRODUCTS_DIR / "all-agent-packs" / "cover.png",
        "input": "Your project folder, plus the pack you want to install first.",
        "output": "Each pack's own files, with their README, installer, and tests.",
        "example": E(
            """Bought alone at each pack's minimum:
  Ship-Ready Skills Pack     from $1
  Dev OS in Claude Code      $9
  Anti-Slop Kit              $9
  Agent Data Skills Pack     from $1
  AGENTS.md Starter Pack     from $1
  Dev Cheat Sheets           $3
  Total                      $24""",
            "This bundle: $19",
            "The six packs and their minimum prices",
            "The bundle price",
            "text",
            "Minimums match the live Gumroad listings on Nov 25, 2026. Gumroad shows $24 struck through.",
        ),
        "versions": [
            V("Gumroad", "The bundle", "$19",
              "https://tidybyte.gumroad.com/l/all-agent-packs",
              cta="Buy on Gumroad",
              note="Fixed $19. Some packs are pay-what-you-want from $1 on their own, so buying one or two alone can cost less. You may use them in your own and client projects. Please do not resell them."),
            V("Gumroad", "Free: Anti-Slop Rules", "Free",
              "https://tidybyte.gumroad.com/l/anti-slop-rules-free",
              cta="Get free rules",
              note="The free writing-rules pack. Not in the bundle. The paid Anti-Slop Kit is."),
            V("Gumroad", "Free: Agent Cost Saver", "Free",
              "https://tidybyte.gumroad.com/l/agent-cost-saver",
              cta="Get free guide",
              note="A short guide and 4 scripts for cutting Claude Code, Cursor, and Codex token costs. Not in the bundle."),
        ],
        "repos": [],
    },

    {
        "slug": "n8n-lint-free",
        "name": "n8n Lint",
        "category": "n8n",
        "icon": "workflow",
        "tagline": "A free 27-rule linter and node lookup for n8n workflow JSON.",
        "summary": (
            "Check n8n workflow JSON before you import it. Catch invented node names, wrong "
            "typeVersion numbers, broken connections, and keys left in the file."
        ),
        "does": [
            "n8n_lint.py runs 27 rules (13 errors, 14 warnings) on structure, names, node types and versions, connections, expressions, and secrets. It suggests the closest real name for a typo. --json and --strict for CI.",
            "n8n_nodes.py searches all 572 built-in nodes of n8n 2.49.6, with type strings, versions, credentials, and parameter names.",
            "A skill so Claude Code, Cursor, or Codex can run both for you, plus a test file that checks every rule (41 checks).",
        ],
        "thumb": PRODUCTS_DIR / "n8n-lint-free" / "thumb.png",
        "cover": PRODUCTS_DIR / "n8n-lint-free" / "cover.png",
        "input": "An n8n workflow JSON file, or a folder of them.",
        "output": "A list of errors and warnings, each with a code, the node name, and a plain fix, or a close name for a typo.",
        "example": E(
            """$ python3 n8n_lint.py flow.json
flow.json: 2 error(s), 1 warning(s)
  E006 error [Manual Trigger]: unknown node type 'n8n-nodes-base.googleSheetz'. Did you mean: n8n-nodes-base.googleSheets, n8n-nodes-base.googleChat, n8n-nodes-base.googleSheetsTrigger?
  E007 error [Call LLM]: typeVersion 9 is not known for n8n-nodes-base.httpRequest. Known: [1, 2, 3, 4, 4.1, 4.2, 4.3, 4.4, 4.5]""",
            """$ python3 n8n_lint.py examples/error-alert-repeat-blocker.json
examples/error-alert-repeat-blocker.json: 0 error(s), 0 warning(s)""",
            "A typo and a wrong typeVersion",
            "A real example workflow from the pack",
            "text",
            "Run Nov 25, 2026 against n8n 2.49.6. The typo file was made from a pack example; the clean file is examples/error-alert-repeat-blocker.json.",
        ),
        "versions": [
            V("Gumroad", "Free linter", "Free",
              "https://tidybyte.gumroad.com/l/n8n-lint-free",
              cta="Get free on Gumroad",
              note="MIT license. Python 3.9+, standard library only. Nothing leaves your computer. It checks structure, not whether your API key is right, and it does not run the workflow. Tested on n8n 2.49.6."),
            V("Gumroad", "Full n8n Builder Kit", "$9",
              "https://tidybyte.gumroad.com/l/n8n-builder-kit-claude-code",
              cta="Buy on Gumroad",
              note="Adds a builder skill, a review skill, a debug skill, 7 reference pages, 3 slash commands, 12 prompts, and 3 working example workflows."),
        ],
        "repos": [],
    },
    {
        "slug": "n8n-builder-kit-claude-code",
        "name": "n8n Builder Kit for Claude Code",
        "category": "n8n",
        "icon": "workflow",
        "tagline": "3 skills, a 27-rule linter, and a node lookup so AI agents write n8n workflows that import and run.",
        "summary": (
            "AI agents get n8n wrong in the same few ways: they invent node names, use old typeVersion "
            "numbers, link connections by id, and forget the '=' in an expression. This kit catches those "
            "before you import the file."
        ),
        "does": [
            "3 skills: n8n-workflow-builder (plan, look up real nodes, write the JSON, lint it), n8n-workflow-review, and n8n-debug-run (reads a failed run and names the fix).",
            "n8n_lint.py (27 rules) and n8n_nodes.py (all 572 built-in nodes of n8n 2.49.6). n8n_builder.py writes workflows in Python with 22 helpers, each run in a real n8n.",
            "7 reference pages, 12 prompts, 3 slash commands, and 3 example workflows that run in demo mode with no accounts. 64 offline checks, plus a --real mode that runs the examples in n8n.",
        ],
        "thumb": PRODUCTS_DIR / "n8n-builder-kit-claude-code" / "thumb.png",
        "cover": PRODUCTS_DIR / "n8n-builder-kit-claude-code" / "cover.png",
        "input": "A plain-language description of the workflow you want, or an existing n8n JSON file, or a failed n8n run log.",
        "output": "Workflow JSON that linted clean, a ranked review, or a table that names the failing node and a likely fix.",
        "example": E(
            """$ python3 n8n_lint.py flow.json
flow.json: 2 error(s), 1 warning(s)
  E006 error [Manual Trigger]: unknown node type 'n8n-nodes-base.googleSheetz'. Did you mean: n8n-nodes-base.googleSheets, n8n-nodes-base.googleChat, n8n-nodes-base.googleSheetsTrigger?
  E007 error [Call LLM]: typeVersion 9 is not known for n8n-nodes-base.httpRequest. Known: [1, 2, 3, 4, 4.1, 4.2, 4.3, 4.4, 4.5]""",
            """$ python3 n8n_lint.py examples/error-alert-repeat-blocker.json
examples/error-alert-repeat-blocker.json: 0 error(s), 0 warning(s)""",
            "A typo and a wrong typeVersion",
            "A real example workflow from the kit",
            "text",
            "Run Nov 25, 2026 against n8n 2.49.6. The typo file was made from a kit example; the clean file is examples/error-alert-repeat-blocker.json.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "$9",
              "https://tidybyte.gumroad.com/l/n8n-builder-kit-claude-code",
              cta="Buy on Gumroad",
              note="Fixed $9. Standard library Python only. Nothing leaves your computer. Tested on n8n 2.49.6, with a fake model server. Other n8n versions may differ. It does not host or run your workflows."),
            V("Gumroad", "Free: n8n Lint", "Free",
              "https://tidybyte.gumroad.com/l/n8n-lint-free",
              cta="Get free on Gumroad",
              note="The 27-rule linter and the 572-node lookup, plus a skill and 41 tests. MIT license."),
            V("Gumroad", "Also: n8n Data Cleanup Pack", "From $1",
              "https://tidybyte.gumroad.com/l/n8n-data-cleanup-pack",
              cta="See on Gumroad",
              note="9 ready-to-import cleanup workflows, using only nodes that come with n8n."),
        ],
        "repos": [],
    },
    {
        "slug": "production-readiness-lite-free",
        "name": "Production Readiness Lite",
        "category": "ai",
        "icon": "check",
        "tagline": "A free 15-check release scanner and a go or no-go sheet.",
        "summary": (
            "A small scanner that finds the problems that most often cause release-day outages: "
            "a committed .env, missing tests or CI, no health check, no timeouts, a container running as root."
        ),
        "does": [
            "readiness_lite.py runs 15 checks on Node, Python, Java, and Go repos. It prints GO, GO WITH RISKS, or NO-GO, the file and line behind each failure, and the fix. It reads files only and never prints a secret value.",
            "It also lists 4 questions for a person: who owns the secrets, was a rollback practiced, was a restore tested, and do alerts reach someone.",
            "Includes a checklist and a go or no-go sheet. Python 3.9+, standard library only. Tests on good and bad sample repos are included.",
        ],
        "thumb": PRODUCTS_DIR / "production-readiness-lite-free" / "thumb.png",
        "cover": PRODUCTS_DIR / "production-readiness-lite-free" / "cover.png",
        "input": "A repository folder on your computer.",
        "output": "A verdict (GO, GO WITH RISKS, or NO-GO), each failed check with a file, line, and fix, plus 4 questions for a person.",
        "example": E(
            """$ python3 readiness_lite.py .
READINESS SCAN (lite)  .
VERDICT: NO-GO    (some pass, some fail)
  FAIL S02  blocker   No real .env file is committed
  FAIL R02  important SIGTERM is handled (graceful shutdown)
  FAIL C02  important Container does not run as root""",
            "Fix the blockers, then fill in the go or no-go sheet, including the 4 questions the scan cannot answer.",
            "A scan on a repo with known problems",
            "What you do next",
            "text",
            "The scanner was tested Nov 25, 2026 on good and bad sample repos. This sample is shortened from a real run.",
        ),
        "versions": [
            V("Gumroad", "Free scanner", "Free",
              "https://tidybyte.gumroad.com/l/production-readiness-lite-free",
              cta="Get free on Gumroad",
              note="MIT license. The scan finds patterns, so open each finding before you act. It is not a security audit, and it cannot see backups, alerts, or load."),
            V("Gumroad", "Full Production Readiness Kit", "$9",
              "https://tidybyte.gumroad.com/l/production-readiness-kit",
              cta="Buy on Gumroad",
              note="All 45 scanned checks and 22 questions, a skill and 4 slash commands, 6 templates, 3 starter services, and stack pages for Node, Python, Java, and Go."),
        ],
        "repos": [],
    },
    {
        "slug": "production-readiness-kit",
        "name": "Production Readiness Kit",
        "category": "ai",
        "icon": "check",
        "tagline": "A read-only scanner, 22 questions, a review skill, 6 templates, and 3 starter services for a go or no-go call.",
        "summary": (
            "Most outages on release day come from the same short list: a committed .env, no health check, "
            "no timeouts, a container running as root, a migration nobody could roll back, no one on call. "
            "This kit finds the ones that files can show, and makes you answer the ones they cannot."
        ),
        "does": [
            "readiness_scan.py runs 45 checks in 8 areas and prints GO, GO WITH RISKS, or NO-GO, with the file and line and the fix. It reads files only, never runs your code, never uses the network, and never prints a secret value.",
            "22 questions only a person can answer sit in the same report (45 + 22 = 67). A skill and 4 slash commands run the scan, check each finding in the code, and fill in the sheets.",
            "6 templates (go or no-go, rollback plan, runbook, release day checklist, postmortem, risk acceptance), 3 starter services (Node, Python, Go) that scan GO, and stack pages for Node, Python, Java and Spring Boot, and Go.",
        ],
        "thumb": PRODUCTS_DIR / "production-readiness-kit" / "thumb.png",
        "cover": PRODUCTS_DIR / "production-readiness-kit" / "cover.png",
        "input": "A repository folder on your computer.",
        "output": "A verdict, a table of findings, and, if you want them, filled-in go or no-go, rollback, runbook, or postmortem sheets.",
        "example": E(
            """$ python3 readiness_scan.py .
READINESS SCAN  service-starter-with-problems
stacks: node   service: yes   database: no   git: yes
VERDICT: NO-GO    (33 pass, 7 fail, 5 not applicable)
  FAIL R01  important A health endpoint exists
  FAIL R02  important SIGTERM is handled (graceful shutdown)
  FAIL C02  important Container does not run as root
  FAIL C03  important Base image tags are pinned
  FAIL X01  blocker   TLS certificate checks are not turned off""",
            "Fix X01 first (a blocker). Then fix the important items, or accept each one in writing. Then answer the 22 manual questions.",
            "A real scan of the kit's sample starter after four problems were added",
            "What the verdict means",
            "text",
            "From examples/sample-scan-output.txt in the kit, made by copying starters/node and removing health routes and SIGTERM handling, using FROM node:latest with no USER, and adding rejectUnauthorized: false. Tested Nov 25, 2026.",
        ),
        "versions": [
            V("Gumroad", "For your computer", "$9",
              "https://tidybyte.gumroad.com/l/production-readiness-kit",
              cta="Buy on Gumroad",
              note="Fixed $9. The scan uses patterns, so it can miss a problem or flag a harmless line. There is no Java starter. The starter Dockerfiles were not built in our tests. A good verdict is not a security audit."),
            V("Gumroad", "Free: Production Readiness Lite", "Free",
              "https://tidybyte.gumroad.com/l/production-readiness-lite-free",
              cta="Get free on Gumroad",
              note="15 of the checks, 4 questions, the lite checklist, and the go or no-go sheet. MIT license."),
        ],
        "repos": [],
    },

    {
        "slug": 'n8n-ai-workflows-free',
        "name": 'n8n AI Workflows (free)',
        "category": "ai",
        "icon": "check",
        "tagline": 'Three n8n AI workflows you can import and run now, with no accounts and demo mode on.',
        "summary": 'Three n8n workflows with no API keys needed: a social post writer, a text-to-JSON extractor with retry, and an error alert with a repeat blocker. A free sample of the 8-workflow pack.',
        "does": ['Three workflows you import and run right away. Each model step has a demo mode so you see the full flow first.', 'Includes a 27-rule linter, setup notes, and tests. MIT license.', 'Webhook nodes ship without authentication. Add Header Auth before you activate them.'],
        "thumb": PRODUCTS_DIR / "gumroad-next2" / "covers" / "n8n-ai-workflows-free-thumb.png",
        "cover": PRODUCTS_DIR / "gumroad-next2" / "covers" / "n8n-ai-workflows-free-cover.png",
        "input": 'An n8n instance (2.x) and a JSON file to import.',
        "output": 'Importable workflow JSON files, with demo replies you can swap for a real model.',
        "example": E(
            'Import workflows/01-social-post-writer.json into n8n, click Test workflow, and open the last node.',
            'Demo mode is on, so no key is needed. Turn it off and add your model details when you want live replies.',
            'The first step after import',
            "What you do next",
            "text",
            'Run Nov 25, 2026 in n8n 2.49.6 with demo mode and a local fake model server. Not tested against live model services.',
        ),
        "versions": [
            V("Gumroad", 'Free sample', 'Free',
              "https://tidybyte.gumroad.com/l/n8n-ai-workflows-free",
              cta='Get free on Gumroad',
              note='MIT license. Demo replies are fixed sample text and show the flow, not model quality.'),
            V("Gumroad", 'Full n8n AI Workflow Pack', '$9',
              "https://tidybyte.gumroad.com/l/n8n-ai-workflow-pack",
              cta='Buy on Gumroad',
              note='All 8 workflows, tested in n8n 2.49.6.'),
        ],
        "repos": [],
    },
    {
        "slug": 'n8n-ai-workflow-pack',
        "name": 'n8n AI Workflow Pack',
        "category": "ai",
        "icon": "check",
        "tagline": 'Eight n8n AI workflows you can import and run with no accounts, each run in a real n8n.',
        "summary": 'Eight workflows: social posts, lead scorer, ticket triage, blog repurposer, meeting notes, text-to-JSON, page change monitor, and error alerts. Demo mode is on by default.',
        "does": ['8 workflows, each run in n8n 2.49.6 in demo mode and through the live HTTP path against a local fake model server.', 'A Config node in every workflow, a 27-rule linter, setup notes, and tests.', 'Works with any OpenAI-compatible model when you switch demo mode off.'],
        "thumb": PRODUCTS_DIR / "gumroad-next2" / "covers" / "n8n-ai-workflow-pack-thumb.png",
        "cover": PRODUCTS_DIR / "gumroad-next2" / "covers" / "n8n-ai-workflow-pack-cover.png",
        "input": 'An n8n instance (2.x) and a JSON file to import.',
        "output": 'Eight importable workflow files, plus a linter, notes, and tests.',
        "example": E(
            'Import workflows/01-social-post-writer.json into n8n, click Test workflow, and open the last node.',
            'Demo mode is on, so no key is needed. Turn it off and add your model details when you want live replies.',
            'The first step after import',
            "What you do next",
            "text",
            'Run Nov 25, 2026 in n8n 2.49.6 with demo mode and a local fake model server. Not tested against live model services.',
        ),
        "versions": [
            V("Gumroad", 'For n8n', '$9',
              "https://tidybyte.gumroad.com/l/n8n-ai-workflow-pack",
              cta='Buy on Gumroad',
              note='Fixed $9. Not tested against live OpenAI or OpenRouter. Tested on n8n 2.49.6 only. Webhook nodes ship without authentication.'),
            V("Gumroad", 'Free: n8n AI Workflows', 'Free',
              "https://tidybyte.gumroad.com/l/n8n-ai-workflows-free",
              cta='Get free on Gumroad',
              note='3 of the 8 workflows. MIT license.'),
        ],
        "repos": [],
    },
    {
        "slug": 'claude-code-commands-free',
        "name": 'Claude Code Commands (free)',
        "category": "ai",
        "icon": "check",
        "tagline": 'Eight safe slash commands for Claude Code, one CLAUDE.md template, and a folder map.',
        "summary": 'Eight plain Markdown slash commands that read a read-only snapshot of your repo first. None pre-approves edits or commits. A free sample of the cookbook.',
        "does": ['8 commands: explain-repo, fix-failing-test, review-diff, commit-msg, pr-description, handoff, scope-check, undo-plan.', 'Install with sh install.sh. It never overwrites a same-named file unless you add --force.', 'Includes tests and a Cursor converter. MIT license.'],
        "thumb": PRODUCTS_DIR / "gumroad-next2" / "covers" / "claude-code-commands-free-thumb.png",
        "cover": PRODUCTS_DIR / "gumroad-next2" / "covers" / "claude-code-commands-free-cover.png",
        "input": 'A repo and Claude Code (or Cursor).',
        "output": 'Slash commands, a CLAUDE.md template, and a .claude folder map.',
        "example": E(
            'Install: sh install.sh\nThen start a new Claude Code session and type /',
            'Each command reads a read-only snapshot of your repo first. Claude Code still asks before it edits, commits, or pushes.',
            'How to install and use',
            "What you do next",
            "text",
            'Checked for format, safety, and the exact commands they run. Not run inside a live Claude Code session.',
        ),
        "versions": [
            V("Gumroad", 'Free commands', 'Free',
              "https://tidybyte.gumroad.com/l/claude-code-commands-free",
              cta='Get free on Gumroad',
              note='MIT license. On Windows use Git Bash or WSL.'),
            V("Gumroad", 'Full Cookbook', '$9',
              "https://tidybyte.gumroad.com/l/claude-code-commands-cookbook",
              cta='Buy on Gumroad',
              note='30 commands, 5 templates, and 3 guides.'),
        ],
        "repos": [],
    },
    {
        "slug": 'claude-code-commands-cookbook',
        "name": 'Claude Code Commands Cookbook',
        "category": "ai",
        "icon": "check",
        "tagline": 'Thirty safe slash commands for Claude Code, 5 CLAUDE.md templates, and short guides.',
        "summary": 'Thirty commands that each do one job, five CLAUDE.md templates, and three short guides. None pre-approves edits or commits.',
        "does": ['30 commands in 6 groups: understand, fix, change safely, test and review, ship, and session.', '5 CLAUDE.md templates, a guide to writing one that works, 12 time and money saving habits, and the folder map.', 'A Cursor converter, an installer, and tests.'],
        "thumb": PRODUCTS_DIR / "gumroad-next2" / "covers" / "claude-code-commands-cookbook-thumb.png",
        "cover": PRODUCTS_DIR / "gumroad-next2" / "covers" / "claude-code-commands-cookbook-cover.png",
        "input": 'A repo and Claude Code (or Cursor).',
        "output": 'Slash commands, templates, guides, and an installer.',
        "example": E(
            'Install: sh install.sh\nThen start a new Claude Code session and type /',
            'Each command reads a read-only snapshot of your repo first. Claude Code still asks before it edits, commits, or pushes.',
            'How to install and use',
            "What you do next",
            "text",
            'Checked for format, safety, and the exact commands they run. Not run inside a live Claude Code session.',
        ),
        "versions": [
            V("Gumroad", 'For your computer', '$9',
              "https://tidybyte.gumroad.com/l/claude-code-commands-cookbook",
              cta='Buy on Gumroad',
              note='Fixed $9. Not run inside a live Claude Code session. How well Claude follows each command depends on your model and repo.'),
            V("Gumroad", 'Free: Claude Code Commands', 'Free',
              "https://tidybyte.gumroad.com/l/claude-code-commands-free",
              cta='Get free on Gumroad',
              note='8 commands, 1 template, and the folder map. MIT license.'),
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
              note="Failed items are free.",
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
