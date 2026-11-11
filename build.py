#!/usr/bin/env python3
"""Build the Tidy Byte Tools static website into this folder."""
from __future__ import annotations

import html
import re
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

from PIL import Image

from guide_build import load_guides, md_to_html, rewrite_guide_links
from catalog import (
    TOOLS, OPTIONAL_APIFY, CATEGORIES, GALLERIES, ALIASES, HOME_FAQS,
    PRODUCTS_DIR as CATALOG_PRODUCTS, ACTOR_START_USD,
)
import i18n as I18N

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
ASSETS = ROOT / "assets"
OUT = ROOT
BRAND = Path("/workspace/design/brand")
PRODUCTS_DIR = Path("/workspace/products")
GUIDES_DIR = PRODUCTS_DIR / "guides"
import os
PATH_PREFIX = os.environ.get("PATH_PREFIX", "").rstrip("/")  # e.g. "/tidybytetools" for snowrsps.com
BASE = os.environ.get("SITE_BASE", "https://tidybytetools.github.io").rstrip("/")
YEAR = "2026"

# Live Cloudflare Worker API (separate from this site's Apify OpenAPI).
API_WORKER = "https://tidybytetools.tidybytetools.workers.dev"


def P(path: str) -> str:
    """Site-absolute path with optional hosting subpath prefix."""
    if not path.startswith("/"):
        path = "/" + path
    if PATH_PREFIX and not path.startswith(PATH_PREFIX + "/") and path != PATH_PREFIX:
        return PATH_PREFIX + path
    return path


def configure() -> None:
    """Set BASE, PATH_PREFIX, and OUT from the environment."""
    global PATH_PREFIX, BASE, OUT, ASSETS
    PATH_PREFIX = os.environ.get("PATH_PREFIX", "").rstrip("/")
    BASE = os.environ.get("SITE_BASE", "https://tidybytetools.github.io").rstrip("/")
    dest = os.environ.get("DEST")
    OUT = Path(dest).resolve() if dest else ROOT
    ASSETS = OUT / "assets"
    OUT.mkdir(parents=True, exist_ok=True)


def lang_href(lang_code: str, path: str = "/") -> str:
    info = I18N.LANG_BY_CODE[lang_code]
    prefix = info["prefix"]
    if not path.startswith("/"):
        path = "/" + path
    if path == "/":
        return P(f"/{prefix}/") if prefix else P("/")
    return P(f"/{prefix}{path}") if prefix else P(path)


def about_price_line(tool: dict, lang: str = "en") -> str | None:
    ev = tool.get("event")
    if not ev or not ev.get("price_usd"):
        return None
    usd = float(ev["price_usd"])
    if usd <= 0:
        return None
    n = int(round(1 / usd))
    unit_key = I18N.UNIT_KEY.get(ev.get("unit") or "", "")
    units = I18N.ui(lang, "units")
    unit = units.get(unit_key) if isinstance(units, dict) else ev.get("unit")
    unit = unit or ev.get("unit") or "uses"
    tmpl = I18N.ui(lang, "about_price")
    return tmpl.format(n=I18N.format_count(n, lang), unit=unit)


def minify_css(src: str) -> str:
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"\s+", " ", src)
    src = re.sub(r"\s*([{}:;,])\s*", r"\1", src)
    return src.strip()


def minify_js(src: str) -> str:
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    lines = []
    for line in src.splitlines():
        cut = line.find("//")
        if cut >= 0:
            # keep URLs like https://
            if cut > 0 and line[cut-1] == ":":
                pass
            else:
                line = line[:cut]
        lines.append(line)
    src = "\n".join(lines)
    src = re.sub(r"[ \t]+", " ", src)
    src = re.sub(r"\n+", "\n", src)
    return src.strip()


ICONS = {
    "table": "M4 4h16v16H4zM4 9h16M9 4v16",
    "doc": "M7 3h7l6 6v12H7zM14 3v6h6",
    "sheet": "M4 5h16v14H4zM4 9h16M9 5v14M13 5v14",
    "json": "M8 5c-2 0-3 1.5-3 3.5S6 12 8 12M16 5c2 0 3 1.5 3 3.5S18 12 16 12M8 12c-2 0-3 1.5-3 3.5S6 19 8 19M16 12c2 0 3 1.5 3 3.5S18 19 16 19",
    "leads": "M16 7a3 3 0 11-6 0 3 3 0 016 0zM5 19a6 6 0 0112 0",
    "phone": "M7 3h4l1 5-2 1a12 12 0 006 6l1-2 5 1v4c0 1-1 2-2 2C10 20 4 14 4 5c0-1 1-2 3-2z",
    "bundle": "M4 8l8-4 8 4-8 4-8-4zM4 12l8 4 8-4M4 16l8 4 8-4",
    "link": "M10 13a5 5 0 007.07 0l1.41-1.41a5 5 0 00-7.07-7.07L10 5.93M14 11a5 5 0 00-7.07 0L5.5 12.41a5 5 0 007.07 7.07L14 18.07",
    "pulse": "M3 12h4l2-6 4 12 2-6h6",
    "chunk": "M5 5h14v4H5zM5 11h14v3H5zM5 16h9v3H5z",
    "gif": "M5 6h14v12H5zM9 10v4M9 12h2M13 10v4h2",
    "workflow": "M6 6h5v5H6zM13 13h5v5h-5zM8.5 11v2H13",
    "letters": "M5 17l4-10 4 10M7 13h4M15 7v10",
    "split": "M12 4v16M5 9l-2 3 2 3M19 9l2 3-2 3",
    "regex": "M6 16V8l4 4-4 4M12 8h6M12 12h6M12 16h6",
    "skills": "M12 3l2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5z",
    "tokens": "M8 12h8M12 8v8M5 5h14v14H5z",
    "check": "M5 13l5 5L20 7",
    "preview": "M3 12s3.5-6 9-6 9 6 9 6-3.5 6-9 6-9-6-9-6zM12 9a3 3 0 100 6 3 3 0 000-6z",
    "lang": "M4 6h10M9 6c0 8-4 12-4 12M9 6c0 8 4 12 4 12M6 14h6M14 8h6l-6 12h6",
    "date": "M6 4v2M18 4v2M4 8h16M5 6h14v14H5z",
    "base64": "M5 8c2-3 5-3 7 0s5 3 7 0M5 16c2 3 5 3 7 0s5-3 7 0",
    "hash": "M9 5l-2 14M17 5l-2 14M5 9h16M4 15h16",
}


def icon_svg(name: str, size: int = 24) -> str:
    d = ICONS.get(name) or ICONS["doc"]
    # Some icons use a path with multiple subpaths; use polyline/path mix via a single path if possible.
    # For line icons, stroke a path.
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'<path d="{e(d)}"/></svg>'
    )


def highlight(text: str, lang: str) -> str:
    """Light syntax coloring for short before/after samples."""
    raw = text
    esc = e(text)
    if lang in {"json", "js"}:
        def repl_str(m):
            return f'<span class="token-str">{e(m.group(0))}</span>'
        tmp = re.sub(r'"(\\.|[^"\\])*"', lambda m: f"\x00S{m.group(0)}\x00", raw)
        tmp = re.sub(r"\b-?\d+(?:\.\d+)?\b", lambda m: f"\x00N{m.group(0)}\x00", tmp)
        tmp = e(tmp)
        tmp = re.sub(r"\x00S(.*?)\x00", lambda m: f'<span class="token-str">{m.group(1)}</span>', tmp)
        tmp = re.sub(r"\x00N(.*?)\x00", lambda m: f'<span class="token-num">{m.group(1)}</span>', tmp)
        return tmp
    if lang in {"csv", "html", "markdown", "text"}:
        return esc
    return esc


def hreflang_tags(en_path: str, current_lang: str) -> str:
    """Alternate language tags. Only homepages are translated so far."""
    tags = []
    # en_path is "/" for homes; other pages only get self + x-default English.
    if en_path == "/":
        for lang in I18N.LANGS:
            href = BASE + (f"/{lang['prefix']}/" if lang["prefix"] else "/")
            tags.append(f'<link rel="alternate" hreflang="{e(lang["hreflang"])}" href="{e(href)}">')
        tags.append(f'<link rel="alternate" hreflang="x-default" href="{e(BASE + "/")}">')
    return "\n  ".join(tags)


def lang_switcher(current_lang: str, en_path: str = "/") -> str:
    items = []
    for lang in I18N.LANGS:
        # Untranslated pages fall back to that language's home.
        if en_path == "/" or lang["code"] == "en":
            href = lang_href(lang["code"], en_path if lang["code"] == "en" or en_path == "/" else "/")
            if lang["code"] != "en" and en_path != "/":
                href = lang_href(lang["code"], "/")
        else:
            href = lang_href(lang["code"], "/")
        cur = ' aria-current="true"' if lang["code"] == current_lang else ""
        items.append(
            f'<li><a href="{e(href)}" lang="{e(lang["hreflang"])}" hreflang="{e(lang["hreflang"])}"'
            f' title="{e(lang["name"])}"{cur}>{e(lang["short"])}</a></li>'
        )
    label = I18N.ui(current_lang, "lang_label")
    return f'<nav class="lang-switch" aria-label="{e(label)}"><ul class="lang-switch">{"".join(items)}</ul></nav>'



def e(text: str) -> str:
    return html.escape(text, quote=True)


_HTTP_OK_CACHE: dict[str, bool] = {}


def http_ok(url: str, timeout: int = 20) -> bool:
    if url in _HTTP_OK_CACHE:
        return _HTTP_OK_CACHE[url]
    ok = False
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "TidyByteToolsSiteBot/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as res:
            ok = 200 <= res.status < 400
    except Exception:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "TidyByteToolsSiteBot/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as res:
                ok = 200 <= res.status < 400
        except Exception:
            ok = False
    _HTTP_OK_CACHE[url] = ok
    return ok


def _sanitize_apify_versions(tool: dict) -> dict:
    """Drop store links that are not public yet, and keep an honest note."""
    tool = dict(tool)
    versions = []
    store = tool.get("apify_url")
    pending = tool.get("apify_pending")
    for ver in tool.get("versions") or []:
        ver = dict(ver)
        url = ver.get("url")
        if ver.get("place") == "Apify" and url and url.startswith("https://apify.com/") and not http_ok(url):
            print(f"hiding unpublished Apify store link for {tool.get('slug')}")
            ver["url"] = None
            ver["cta"] = None
            note = ver.get("note") or ""
            extra = pending or "The public store page is not up yet."
            if extra not in note:
                ver["note"] = (note + " " + extra).strip()
        versions.append(ver)
    tool["versions"] = versions
    return tool


def live_tools() -> list[dict]:
    tools = [_sanitize_apify_versions(dict(t)) for t in TOOLS]
    for item in OPTIONAL_APIFY:
        item = dict(item)
        store = item["apify_url"]
        console = item.get("console_url")
        if http_ok(store):
            print(f"including optional {item['slug']} (store page live)")
            tools.append(item)
            continue
        # isPublic and Store search already list these actors, but the
        # apify.com/username/name HTML page still 404s. Link the working Console URL.
        if not console:
            print(f"skipping optional {item['slug']} (no store page, no console URL)")
            continue
        print(f"including optional {item['slug']} via Console (store HTML still 404)")
        versions = []
        for ver in item["versions"]:
            ver = dict(ver)
            if ver.get("url") == store:
                ver["url"] = console
                ver["cta"] = "Open in Apify Console"
                extra = (
                    "The public store page is not up yet, so this link opens the working Apify Console page."
                )
                ver["note"] = (ver.get("note") + " " if ver.get("note") else "") + extra
            versions.append(ver)
        item["versions"] = versions
        item["apify_url"] = console
        tools.append(item)
    return tools


def subset_fonts() -> None:
    from fontTools.subset import Subsetter, Options
    from fontTools.ttLib import TTFont

    outdir = ASSETS / "fonts"
    outdir.mkdir(parents=True, exist_ok=True)
    src_fonts = ROOT / "assets" / "fonts"
    if OUT.resolve() != ROOT.resolve() and (src_fonts / "geist-latin.woff2").exists():
        for name in ("OFL.txt", "geist-latin.woff2", "geist-mono-latin.woff2"):
            src = src_fonts / name
            if not src.exists() and name == "OFL.txt":
                src = BRAND / "fonts" / "OFL.txt"
            if src.exists():
                shutil.copyfile(src, outdir / name)
        print("copied fonts from existing site build")
        return
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
        root_art = ROOT / "assets" / "img" / "generated"
        if not tool.get("thumb") or not Path(tool.get("thumb") or "").exists():
            existing = root_art / f"{tool['slug']}-thumb.png"
            if existing.exists():
                tool["thumb"] = existing
        if not tool.get("cover") or not Path(tool.get("cover") or "").exists():
            existing = root_art / f"{tool['slug']}-cover.png"
            if existing.exists():
                tool["cover"] = existing
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
        by_slug[slug]["gallery_src"] = P("/assets/img/galleries/%s.webp" % slug)
        by_slug[slug]["gallery_png"] = P("/assets/img/galleries/%s.png" % slug)
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
        ) % (e(BASE + dest), e(P(dest)), e(P(dest)), e(BASE + dest))
        write_page("tools/%s/index.html" % alias, html_text)


def copy_brand_assets(tools: list[dict]) -> None:
    img = ASSETS / "img"
    img.mkdir(parents=True, exist_ok=True)
    # Icons
    shutil.copyfile(BRAND / "favicon.ico", OUT / "favicon.ico")
    shutil.copyfile(BRAND / "png" / "favicon-32.png", img / "favicon-32.png")
    shutil.copyfile(BRAND / "png" / "favicon-16.png", img / "favicon-16.png")
    shutil.copyfile(BRAND / "png" / "apple-touch-icon-180.png", OUT / "apple-touch-icon.png")
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
        tool["thumb_src"] = P(f"/assets/img/thumbs/{tool['slug']}.webp")
        tool["thumb_png"] = P(f"/assets/img/thumbs/{tool['slug']}.png")
        tool["cover_src"] = P(f"/assets/img/covers/{tool['slug']}.webp")
        tool["cover_png"] = P(f"/assets/img/covers/{tool['slug']}.png")


def write_css() -> None:
    css_src = (SRC / "site.css").read_text()
    font_url = P("/assets/fonts/geist-latin.woff2")
    mono_url = P("/assets/fonts/geist-mono-latin.woff2")
    font_css = f"""
@font-face {{
  font-family: "Geist";
  src: url("{font_url}") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}}
@font-face {{
  font-family: "Geist Mono";
  src: url("{mono_url}") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}}
"""
    dest = ASSETS / "css"
    dest.mkdir(parents=True, exist_ok=True)
    combined = font_css.strip() + "\n\n" + css_src
    (dest / "site.css").write_text(minify_css(combined) + "\n")
    js_src = SRC / "site.js"
    if js_src.exists():
        js_dest = ASSETS / "js"
        js_dest.mkdir(parents=True, exist_ok=True)
        (js_dest / "site.js").write_text(minify_js(js_src.read_text()) + "\n")


def version_links(ver: dict) -> str:
    items = []
    if ver.get("url"):
        label = ver.get("cta") or "Open"
        if ver.get("place") == "Apify":
            label = ver.get("cta") or I18N.ui("en", "try_apify")
        items.append((label, ver["url"], "primary" if ver.get("place") == "Apify" or (ver.get("price") or "").lower() == "free" and ver.get("cta") else "secondary"))
    for label, url in ver.get("urls") or []:
        kind = "primary" if label == "GitHub" and (ver.get("price") or "").lower() == "free" and not ver.get("url") else "secondary"
        if label == "GitHub" and (ver.get("price") or "").lower() == "free":
            items.append((I18N.ui("en", "free_download"), url, "primary" if not any(k=="primary" for _,_,k in items) else "secondary"))
        else:
            items.append((label, url, kind))
    if not items:
        return ""
    parts = []
    for label, url, kind in items:
        cls = "btn btn-primary btn-sm" if kind == "primary" else "btn btn-secondary btn-sm"
        parts.append(f'<a class="{cls}" href="{e(url)}">{e(label)}</a>')
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


def card(tool: dict, lang: str = "en") -> str:
    price = about_price_line(tool, lang)
    price_html = f'<p class="price-line">{e(price)}</p>' if price else ""
    tagline = I18N.tool_description(tool, lang)
    cat = (I18N.ui(lang, "cats") or {}).get(tool["category"], dict(CATEGORIES)[tool["category"]])
    search = " ".join([
        tool["name"], tool["slug"], tool["tagline"], tool["summary"], tagline,
        " ".join(sum((tr.get("keywords") or [] for tr in I18N.tool_translations_obj(tool["slug"]).values()), [])),
    ]).lower()
    return f"""
<article class="card" id="tool-{e(tool["slug"])}" data-tool-card data-category="{e(tool["category"])}" data-search="{e(search)}">
  <div class="card-top">
    <div class="card-icon" aria-hidden="true">{icon_svg(tool.get("icon") or "doc")}</div>
    <div>
      <p class="cat-label">{e(cat)}</p>
      <h3><a href="{P("/tools/")}{e(tool["slug"])}/">{e(tool["name"])}</a></h3>
      <p class="tagline">{e(tagline)}</p>
      {price_html}
    </div>
  </div>
  {versions_list(tool, compact=True)}
</article>
"""


def logo_html(lang: str = "en") -> str:
    return f'''
    <a class="logo" href="{lang_href(lang, "/")}">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="{P("/assets/img/lockup-horizontal-dark.svg")}">
        <img src="{P("/assets/img/lockup-horizontal-light.svg")}" alt="Tidy Byte Tools" height="32" width="118">
      </picture>
    </a>
    '''


def nav_html(page: str, lang: str = "en") -> str:
    u = lambda k: I18N.ui(lang, k)
    home = lang_href(lang, "/")
    links = [
        (P("/tools/"), u("nav_tools"), "tools"),
        (P("/guides/"), u("nav_guides"), "guides"),
        (home + "#how", u("nav_how"), "how"),
        (home + "#faq", u("nav_faq"), "faq"),
        (P("/connect/"), u("nav_connect"), "connect"),
        (P("/api/"), u("nav_api"), "api"),
        ("https://github.com/tidybytetools", u("nav_github"), "github"),
    ]
    items = []
    for href, label, key in links:
        cur = ' aria-current="page"' if page == key else ""
        items.append(f'<li><a href="{e(href)}"{cur}>{e(label)}</a></li>')
    return "<nav aria-label=\"Primary\"><ul>" + "".join(items) + "</ul></nav>"


def featured_on_html(lang: str = "en") -> str:
    items = []  # badges go here when a directory lists us
    logos = "".join(items)
    return f"""
  <section class="featured-on" aria-label="{e(I18N.ui(lang, "footer_featured"))}">
    <div class="wrap">
      <h2>{e(I18N.ui(lang, "footer_featured"))}</h2>
      <p>{e(I18N.ui(lang, "footer_featured_note"))}</p>
      <ul class="featured-logos">{logos}</ul>
    </div>
  </section>
"""


def footer_html(tools: list[dict], lang: str = "en") -> str:
    tool_links = "\n".join(
        f'<li><a href="{P("/tools/")}{e(t["slug"])}/">{e(t["name"])}</a></li>' for t in tools
    )
    u = lambda k: I18N.ui(lang, k)
    return f"""
<footer class="site-footer">
  {featured_on_html(lang)}
  <div class="wrap footer-grid">
    <div class="footer-brand">
      {logo_html(lang)}
      <p>{e(u("footer_tagline"))}</p>
    </div>
    <div>
      <h2>{e(u("footer_tools"))}</h2>
      <ul>{tool_links}</ul>
    </div>
    <div>
      <h2>{e(u("footer_shops"))}</h2>
      <ul>
        <li><a href="https://apify.com/tidybytetools">Apify</a></li>
        <li><a href="https://tidybyte.gumroad.com">Gumroad</a></li>
        <li><a href="https://github.com/tidybytetools">GitHub</a></li>
      </ul>
    </div>
    <div>
      <h2>{e(u("footer_site"))}</h2>
      <ul>
        <li><a href="{P("/guides/")}">{e(u("nav_guides"))}</a></li>
        <li><a href="{P("/connect/")}">{e(u("nav_connect"))}</a></li>
        <li><a href="{P("/api/")}">{e(u("nav_api"))}</a></li>
        <li><a href="{P("/privacy/")}">{e(u("nav_privacy"))}</a></li>
        <li><a href="{P("/terms/")}">{e(u("nav_terms"))}</a></li>
        <li><a href="{P("/llms.txt")}">llms.txt</a></li>
        <li><a href="{P("/tools.json")}">tools.json</a></li>
        <li><a href="{P("/.well-known/mcp.json")}">mcp.json</a></li>
        <li><a href="{P("/openapi.json")}">openapi.json</a></li>
        <li><a href="{P("/sitemap.xml")}">Sitemap</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap legal">
    <p>{e(u("footer_legal").format(year=YEAR))}</p>
  </div>
</footer>
"""


def org_ld() -> dict:
    return {
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


def head_html(
    title: str,
    description: str,
    path: str,
    page_type: str = "website",
    extra: str = "",
    lang: str = "en",
    en_path: str | None = None,
    og_path: str | None = None,
) -> str:
    info = I18N.LANG_BY_CODE[lang]
    # English pages always canonicalize to themselves. Translated homes canonicalize to themselves too.
    if lang == "en":
        canon = BASE + path
    else:
        canon = BASE + path
    og_img = BASE + (og_path or "/assets/img/og.png")
    hreflang = hreflang_tags(en_path if en_path is not None else ("/" if path in {"/", f"/{info['prefix']}/"} else path), lang)
    font = P("/assets/fonts/geist-latin.woff2")
    return f"""<!DOCTYPE html>
<html lang="{e(info["hreflang"])}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{e(canon)}">
  {hreflang}
  <link rel="icon" href="{P("/favicon.ico")}" sizes="any">
  <link rel="icon" type="image/svg+xml" href="{P("/assets/img/favicon.svg")}">
  <link rel="icon" type="image/png" sizes="32x32" href="{P("/assets/img/favicon-32.png")}">
  <link rel="apple-touch-icon" href="{P("/apple-touch-icon.png")}">
  <link rel="preload" href="{font}" as="font" type="font/woff2" crossorigin>
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
  <meta property="og:locale" content="{e(info["hreflang"].replace("-", "_"))}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(description)}">
  <meta name="twitter:image" content="{e(og_img)}">
  <link rel="stylesheet" href="{P("/assets/css/site.css")}">
  {extra}
</head>
"""



def ld_script(data) -> str:
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=True) + "</script>"


def offer_from_version(ver: dict) -> dict | None:
    """Build a schema.org Offer, including a numeric price when we can read one."""
    url = ver.get("url")
    if not url:
        urls = ver.get("urls") or []
        url = urls[0][1] if urls else None
    if not url:
        return None
    offer = {
        "@type": "Offer",
        "url": url,
        "availability": "https://schema.org/InStock",
        "priceCurrency": "USD",
        "description": f"{ver['label']} on {ver['place']}: {ver['price']}",
    }
    price = str(ver.get("price") or "").strip()
    if price.lower() == "free":
        offer["price"] = "0"
    else:
        m = re.search(r"\$([0-9]+(?:\.[0-9]+)?)", price)
        if m:
            offer["price"] = m.group(1)
    return offer


def faq_page_ld(faqs: list[tuple[str, str]], page_url: str | None = None) -> dict:
    data = {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }
    if page_url:
        data["url"] = page_url
    return data


def faq_html(faqs: list[tuple[str, str]]) -> str:
    if not faqs:
        return ""
    items = "".join(
        f'<div class="faq-item"><h3>{e(q)}</h3><p>{e(a)}</p></div>'
        for q, a in faqs
    )
    return f'<div class="faq" style="margin-top:36px"><h2>FAQ</h2>{items}</div>'


def tool_faqs(tool: dict) -> list[tuple[str, str]]:
    faqs = [
        ("What does this tool do?", tool["tagline"] + " " + tool["summary"]),
    ]
    cost_bits = []
    for ver in tool["versions"]:
        cost_bits.append(f"{ver['label']} on {ver['place']} costs {ver['price']}.")
        if ver.get("note"):
            cost_bits.append(ver["note"])
    faqs.append(("What does it cost?", " ".join(cost_bits)))
    faqs.append((
        "Will you see my files?",
        "The download tools run on your computer, so those files stay with you. "
        "The Apify tools run in your own Apify account. This website does not take uploads.",
    ))
    mentions_mcp = any("MCP" in x for x in tool.get("does", [])) or any(
        "MCP" in (ver.get("note") or "") for ver in tool["versions"]
    )
    if mentions_mcp:
        faqs.append((
            "Does the free tool work with AI apps?",
            "Yes. The free lite version includes a small MCP server. You can use it from "
            "Cursor, Claude Desktop, and other apps that support MCP. No API key is needed.",
        ))
    return faqs


def tool_github_and_mcp(tool: dict) -> tuple[str | None, str | None]:
    """Best GitHub and MCP links we can honestly list for a tool."""
    github = None
    mcp = None
    for ver in tool["versions"]:
        for label, url in ver.get("urls") or []:
            if label == "GitHub":
                github = url
                if "MCP" in (ver.get("note") or ""):
                    mcp = url
        if ver.get("place", "").startswith("GitHub") and ver.get("url"):
            github = github or ver["url"]
    if not github:
        repos = tool.get("repos") or []
        if repos:
            github = f"https://github.com/tidybytetools/{repos[0]}"
    mentions_mcp = any("MCP" in x for x in tool.get("does", [])) or any(
        "MCP" in (ver.get("note") or "") for ver in tool["versions"]
    )
    if mentions_mcp and github and not mcp:
        mcp = github
    return github, mcp


def tools_catalog(tools: list[dict]) -> dict:
    entries = []
    for tool in tools:
        prices = []
        apify = None
        for ver in tool["versions"]:
            url = ver.get("url")
            if not url and ver.get("urls"):
                url = ver["urls"][0][1]
            prices.append({
                "place": ver["place"],
                "label": ver["label"],
                "price": ver["price"],
                "url": url,
            })
            if ver["place"] == "Apify" and ver.get("url"):
                apify = ver["url"]
        github, mcp = tool_github_and_mcp(tool)
        actor = tool.get("actor")
        apify_mcp = f"https://mcp.apify.com/?tools=tidybytetools/{actor}" if actor and apify else None
        entries.append({
            "name": tool["name"],
            "slug": tool["slug"],
            "url": f"{BASE}/tools/{tool['slug']}/",
            "what_it_does": tool["tagline"],
            "summary": tool["summary"],
            "category": tool["category"],
            "price": prices,
            "apify": apify,
            "apify_mcp": apify_mcp,
            "mcp": mcp or apify_mcp,
            "github": github,
            "input": tool.get("input"),
            "output": tool.get("output"),
            "translations": I18N.tool_translations_obj(tool["slug"]),
        })
    return {
        "name": "Tidy Byte Tools",
        "url": BASE + "/",
        "description": "Small tools that clean up messy data. Each one does one job and does it well.",
        "updated": f"{YEAR}-11-10",
        "api": {
            "name": "Tidy Byte Tools API",
            "url": API_WORKER + "/",
            "mcp": API_WORKER + "/mcp",
            "openapi": API_WORKER + "/openapi.json",
            "pricing": API_WORKER + "/pricing",
            "pricing_json": API_WORKER + "/pricing.json",
            "site_page": BASE + "/api/",
            "registry": "io.github.tidybytetools/api",
            "note": "Free public JSON API and remote MCP. 50 anonymous calls per IP per UTC day, or 200 with a free key from POST /keys. Paid billing is not live. The Worker OpenAPI is separate from this site's /openapi.json, which describes Apify actors.",
        },
        "tools": entries,
    }


def page_shell(title, description, path, body, nav_page, tools, extra_head="", lang="en", en_path=None, og_path=None):
    if en_path is None:
        en_path = path if lang == "en" else "/"
    js = ""
    if (SRC / "site.js").exists() and nav_page in {"home", "tools"}:
        js = f'<script src="{P("/assets/js/site.js")}" defer></script>'
    return "\n".join([
        head_html(title, description, path, extra=extra_head + js, lang=lang, en_path=en_path, og_path=og_path),
        "<body>",
        f'<a class="skip" href="#main">{e(I18N.ui(lang, "skip"))}</a>',
        '<header class="site-header"><div class="header-inner">',
        logo_html(lang),
        '<div class="header-tools">',
        nav_html(nav_page, lang),
        lang_switcher(lang, en_path if en_path != path or lang=="en" else "/"),
        "</div></div></header>",
        f'<main id="main">{body}</main>',
        footer_html(tools, lang),
        "</body></html>\n",
    ])



def write_page(rel: str, html_text: str) -> None:
    dest = OUT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html_text)
    print("wrote", dest.relative_to(OUT))


def example_html(tool: dict) -> str:
    ex = tool.get("example")
    if not ex or not ex.get("before") or not ex.get("after"):
        return ""
    lang = ex.get("lang") or "text"
    before = highlight(ex["before"], lang)
    after = highlight(ex["after"], lang)
    source = f'<p class="ba-source">{e(ex["source"])}</p>' if ex.get("source") else ""
    return f'''
        <h2>Before and after</h2>
        <div class="ba">
          <div class="ba-pane before">
            <p class="ba-label">{e(ex.get("before_label") or "Before")}</p>
            <pre><code>{before}</code></pre>
          </div>
          <div class="ba-pane after">
            <p class="ba-label">{e(ex.get("after_label") or "After")}</p>
            <pre><code>{after}</code></pre>
          </div>
        </div>
        {source}
    '''


def toolbar_html(tools: list[dict], lang: str) -> str:
    u = lambda k: I18N.ui(lang, k)
    cats = I18N.ui(lang, "cats") or {}
    chips = [
        f'<button type="button" class="chip is-active" data-filter="all" aria-pressed="true">{e(u("filter_all"))}</button>'
    ]
    for key, label in CATEGORIES:
        if not any(t["category"] == key for t in tools):
            continue
        shown = cats.get(key, label)
        chips.append(
            f'<button type="button" class="chip" data-filter="{e(key)}" aria-pressed="false">{e(shown)}</button>'
        )
    magnifier = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.75" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/>'
        '<path d="M20 20l-3.5-3.5"/></svg>'
    )
    return f'''
        <div class="toolbar">
          <div class="search">
            <span class="search-icon">{magnifier}</span>
            <label class="sr-only" for="tool-search">{e(u("search_label"))}</label>
            <input id="tool-search" type="search" placeholder="{e(u("search_placeholder"))}" autocomplete="off">
          </div>
          <div class="cat-nav" role="group" aria-label="{e(u("filter_all"))}">{"".join(chips)}</div>
        </div>
        <p id="filter-empty" class="filter-empty" hidden>{e(u("filter_empty"))}</p>
    '''


def home_page(tools: list[dict], lang: str = "en") -> None:
    u = lambda k: I18N.ui(lang, k)
    cats = u("cats") or {}
    groups = []
    for key, label in CATEGORIES:
        items = [t for t in tools if t["category"] == key]
        if not items:
            continue
        shown = cats.get(key, label)
        cards = "\n".join(card(t, lang) for t in items)
        groups.append(f'''
        <section id="{e(key)}" aria-labelledby="h-{e(key)}">
          <div class="wrap">
            <div class="section-head">
              <h2 id="h-{e(key)}">{e(shown)}</h2>
            </div>
            <div class="grid">{cards}</div>
          </div>
        </section>
        ''')
    faqs = u("faqs")
    faq_items = "".join(f'<div class="faq-item"><h3>{e(q)}</h3><p>{e(a)}</p></div>' for q, a in faqs)
    path = "/" if lang == "en" else f"/{I18N.LANG_BY_CODE[lang]['prefix']}/"
    canon = BASE + path
    body = f'''
    <section class="hero">
      <div class="wrap hero-inner">
        <p class="eyebrow">{e(u("eyebrow"))}</p>
        <h1>{e(u("hero_title"))}</h1>
        <p class="lede">{e(u("hero_lede"))}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="#tools">{e(u("cta_try"))}</a>
          <a class="btn btn-secondary" href="https://github.com/tidybytetools">{e(u("cta_github"))}</a>
        </div>
      </div>
    </section>
    <div id="tools">
      <section>
        <div class="wrap">
          {toolbar_html(tools, lang)}
        </div>
      </section>
      {"".join(groups)}
    </div>
    <section id="how">
      <div class="wrap">
        <h2>{e(u("how_title"))}</h2>
        <p class="section-intro">{e(u("how_intro"))}</p>
        <div class="steps">
          <div class="step">
            <p class="step-num">01</p>
            <h3>{e(u("how_1_title"))}</h3>
            <p>{e(u("how_1_body"))}</p>
          </div>
          <div class="step">
            <p class="step-num">02</p>
            <h3>{e(u("how_2_title"))}</h3>
            <p>{e(u("how_2_body"))}</p>
          </div>
          <div class="step">
            <p class="step-num">03</p>
            <h3>{e(u("how_3_title"))}</h3>
            <p>{e(u("how_3_body"))}</p>
          </div>
        </div>
        <p class="section-intro" style="margin-top:28px">{e(u("how_mcp"))}</p>
      </div>
    </section>
    <section id="faq">
      <div class="wrap">
        <h2>{e(u("faq_title"))}</h2>
        <div class="faq">{faq_items}</div>
      </div>
    </section>
    '''
    extra = ld_script({
        "@context": "https://schema.org",
        "@graph": [
            {**org_ld(), "inLanguage": I18N.LANG_BY_CODE[lang]["hreflang"]},
            {
                "@type": "WebSite",
                "name": "Tidy Byte Tools",
                "url": canon,
                "description": u("home_desc"),
                "inLanguage": I18N.LANG_BY_CODE[lang]["hreflang"],
                "publisher": {"@type": "Organization", "name": "Tidy Byte Tools", "url": BASE},
            },
            faq_page_ld(list(tuple(x) for x in faqs), canon),
        ],
    })
    html_text = page_shell(
        u("home_title"),
        u("home_desc"),
        path,
        body,
        "home",
        tools,
        extra_head=extra,
        lang=lang,
        en_path="/",
        og_path="/assets/img/og.png",
    )
    rel = "index.html" if lang == "en" else f"{I18N.LANG_BY_CODE[lang]['prefix']}/index.html"
    write_page(rel, html_text)


def tools_index(tools: list[dict]) -> None:
    cards = "\n".join(card(t) for t in tools)
    body = f'''
    <section class="page-hero">
      <div class="wrap">
        <p class="crumb"><a href="{P('/')}">Home</a> / Tools</p>
        <h1>All tools</h1>
        <p class="lede">Downloads for your computer, free lite tools, and pay-per-use tools on Apify.</p>
        {toolbar_html(tools, "en")}
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
        offer = offer_from_version(ver)
        if offer:
            offers.append(offer)
    page_url = f"{BASE}/tools/{tool['slug']}/"
    faqs = tool_faqs(tool)
    cover_src = tool.get("cover_src")
    cover_png = tool.get("cover_png")
    origin = BASE
    if PATH_PREFIX and origin.endswith(PATH_PREFIX):
        origin = origin[: -len(PATH_PREFIX)]
    png_path = cover_png or "/assets/img/og.png"
    image_url = origin + png_path if png_path.startswith("/") else origin + "/" + png_path
    ld_app = {
        "@type": "SoftwareApplication",
        "name": tool["name"],
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Windows, macOS, Linux",
        "description": tool["tagline"],
        "url": page_url,
        "image": image_url,
        "author": {"@type": "Organization", "name": "Tidy Byte Tools", "url": BASE},
        "inLanguage": "en",
    }
    if offers:
        ld_app["offers"] = offers if len(offers) > 1 else offers[0]
    graph: list[dict] = [ld_app]
    apify_ver = next((v for v in tool["versions"] if v.get("place") == "Apify" and v.get("url")), None)
    if apify_ver:
        api_offer = offer_from_version(apify_ver)
        api = {
            "@type": "WebAPI",
            "name": tool["name"] + " API",
            "description": tool["tagline"],
            "url": apify_ver["url"],
            "documentation": apify_ver["url"],
            "provider": {"@type": "Organization", "name": "Tidy Byte Tools", "url": BASE},
        }
        if api_offer:
            api["offers"] = api_offer
        graph.append(api)
    if faqs:
        graph.append(faq_page_ld(faqs, page_url))
    ld = {"@context": "https://schema.org", "@graph": graph}
    gallery_html = ""
    if tool.get("gallery_src"):
        gallery_html = (
            '<div class="cover"><picture>'
            f'<source type="image/webp" srcset="{e(tool["gallery_src"])}">'
            f'<img src="{e(tool["gallery_png"])}" alt="{e(tool["gallery_alt"])}" width="1280" height="720">'
            '</picture></div>'
        )
    cover_html = ""
    if cover_src and cover_png:
        cover_html = f'''
        <div class="cover">
          <picture>
            <source type="image/webp" srcset="{e(cover_src)}">
            <img src="{e(cover_png)}" alt="{e(tool["name"] + " — " + tool["tagline"])}" width="1280" height="720">
          </picture>
        </div>
        '''
    price = about_price_line(tool)
    price_html = f'<p class="price-line">{e(price)}</p>' if price else ""
    # Prominent top CTAs: first free download + public Apify link
    top_ctas = []
    for ver in tool["versions"]:
        top_ctas.append(version_links(ver))
    top_cta_html = "".join(top_ctas)
    cat = dict(CATEGORIES)[tool["category"]]
    body = f'''
    <article class="page-hero">
      <div class="wrap">
        <p class="crumb"><a href="{P('/')}">Home</a> / <a href="{P('/tools/')}">Tools</a> / {e(tool["name"])}</p>
        <p class="cat-label">{e(cat)}</p>
        <h1>{e(tool["name"])}</h1>
        <p class="lede">{e(tool["tagline"])}</p>
        {price_html}
        {top_cta_html}
        {cover_html}
        {gallery_html}
        <div class="prose">
          <p>{e(tool["summary"])}</p>
          <h2>What it does</h2>
          <ul>{bullets}</ul>
        </div>
        {example_html(tool)}
        <div class="prose">
          <h2>Get it</h2>
        </div>
        {"".join(version_blocks)}
        {faq_html(faqs)}
      </div>
    </article>
    '''
    og_path = tool.get("og_path") or "/assets/img/og.png"
    html_text = page_shell(
        f"{tool['name']} — Tidy Byte Tools",
        tool["tagline"],
        f"/tools/{tool['slug']}/",
        body,
        "tools",
        tools,
        extra_head=ld_script(ld),
        og_path=og_path,
    )
    write_page(f"tools/{tool['slug']}/index.html", html_text)


def privacy_page(tools: list[dict]) -> None:
    body = f'''
    <section class="page-hero">
      <div class="wrap prose">
        <p class="crumb"><a href="{P('/')}">Home</a> / Privacy</p>
        <h1>Privacy</h1>
        <p>This is a static website. It has no accounts, no contact forms, and no tracking cookies. We do not run analytics on this site, and we do not set tracking cookies.</p>
        <p>The free lite tools run on your own computer. They read the files you give them and write the result back to you. Those tools do not send your files to us.</p>
        <p>Paid download tools sold on Gumroad also run on your own computer. They do not send your files to us.</p>
        <p>The tools on Apify run in your own Apify account. They process the input you give them so they can return a result. We do not use that input for advertising, training, or any other purpose. Apify is a separate company and has its own rules for how it handles data. Read the <a href="https://docs.apify.com/legal/privacy-policy">Apify privacy policy</a>.</p>
        <p>Links on this site go to other places, such as GitHub, Gumroad, Apify, and PyPI. Those sites have their own privacy policies. If you buy a tool or start a run there, your data is handled by that site.</p>
        <p>This site is run by Tidy Byte Tools. We do not list a personal email address here. For help or a privacy question, open an issue at <a href="https://github.com/tidybytetools">github.com/tidybytetools</a>, on the page for the tool you are using.</p>
        <p>Last updated: November 10, {YEAR}.</p>
      </div>
    </section>
    '''
    html_text = page_shell(
        "Privacy — Tidy Byte Tools",
        "This site has no accounts and no tracking cookies. Lite tools run on your computer. A short privacy note from Tidy Byte Tools.",
        "/privacy/",
        body,
        "privacy",
        tools,
    )
    write_page("privacy/index.html", html_text)


def terms_page(tools: list[dict]) -> None:
    body = f'''
    <section class="page-hero">
      <div class="wrap prose">
        <p class="crumb"><a href="{P('/')}">Home</a> / Terms</p>
        <h1>Terms</h1>
        <p>This website is a catalog of tools from Tidy Byte Tools. The pages describe the tools in plain language. They are not a contract for a paid run or a paid download.</p>
        <p>The free lite tools are released under the license in each GitHub repository. Read that license before you use the tool.</p>
        <p>Paid downloads sold on Gumroad are covered by the terms of that sale and by the license that comes with the download.</p>
        <p>Tools you run on Apify are also covered by Apify’s terms, including the <a href="https://docs.apify.com/legal/general-terms-and-conditions">Apify General Terms and Conditions</a> and the <a href="https://docs.apify.com/legal/actor-terms-and-conditions">Apify Actor Terms and Conditions</a>. Prices shown here are the public pay-per-event prices we know about. The price you pay is the price Apify shows you when you start a run. Each run also has a $0.00005 start fee charged by Apify.</p>
        <p>The tools are offered as-is. We work to make them accurate, but we do not promise that a result will be perfect or fit a particular purpose. You are responsible for checking the output before you rely on it.</p>
        <p>This site does not use tracking cookies and does not take uploads. See the <a href="{P('/privacy/')}">privacy page</a> for how data is handled.</p>
        <p>These terms are for this website. If a word here disagrees with the license of a specific tool or with the terms of Gumroad or Apify for a purchase, the terms of that purchase or license come first.</p>
        <p>For questions, open an issue at <a href="https://github.com/tidybytetools">github.com/tidybytetools</a>.</p>
        <p>Last updated: November 10, {YEAR}.</p>
      </div>
    </section>
    '''
    html_text = page_shell(
        "Terms — Tidy Byte Tools",
        "Plain terms for the Tidy Byte Tools website, free lite tools, paid downloads, and Apify runs.",
        "/terms/",
        body,
        "terms",
        tools,
    )
    write_page("terms/index.html", html_text)


def not_found_page(tools: list[dict]) -> None:
    body = f'''
    <section class="empty">
      <div class="wrap">
        <h1>Page not found</h1>
        <p class="lede">That address is not on this site. Try the tool list, or go back home.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{P('/')}">Home</a>
          <a class="btn btn-secondary" href="{P('/tools/')}">All tools</a>
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


def _apify_store_url(tool: dict) -> str | None:
    for ver in tool["versions"]:
        if ver.get("place") == "Apify" and ver.get("url"):
            return ver["url"]
    return None


def _event_price_line(tool: dict) -> str:
    ev = tool.get("event")
    if not ev:
        return "No pay-per-use price. This tool is a download or a free lite tool."
    usd = ev.get("price_usd")
    unit = ev.get("unit") or "use"
    title = ev.get("title") or ev.get("id") or "event"
    line = f"${usd} per {unit} ({title})."
    about = about_price_line(tool)
    if about:
        line += " " + about
    line += f" Each Apify run also has a ${ACTOR_START_USD} start fee."
    return line


def connect_page(tools: list[dict]) -> None:
    rows = []
    for tool in tools:
        actor = tool.get("actor")
        store = _apify_store_url(tool)
        if actor and store:
            actor_cell = f'<a href="{e(store)}">tidybytetools/{e(actor)}</a>'
            mcp_cell = f'<a href="https://mcp.apify.com/?tools=tidybytetools/{e(actor)}"><code>https://mcp.apify.com/?tools=tidybytetools/{e(actor)}</code></a>'
        elif actor:
            actor_cell = f'tidybytetools/{e(actor)} <span class="note">(public store page is not up yet)</span>'
            mcp_cell = "Available when the public store page is up."
        else:
            actor_cell = "No Apify actor."
            mcp_cell = "—"
        github, local_mcp = tool_github_and_mcp(tool)
        if local_mcp:
            mcp_cell += f'<br>Local lite MCP: <a href="{e(local_mcp)}">{e(local_mcp)}</a>'
        price = _event_price_line(tool) if actor else "Free or paid download. See the tool page."
        rows.append(
            "<tr>"
            f'<td><a href="{P("/tools/")}{e(tool["slug"])}/">{e(tool["name"])}</a></td>'
            f"<td>{actor_cell}</td>"
            f"<td>{mcp_cell}</td>"
            f"<td>{e(price)}</td>"
            f"<td>{e(tool.get('input') or 'See the tool page.')}</td>"
            f"<td>{e(tool.get('output') or 'See the tool page.')}</td>"
            "</tr>"
        )
    body = f'''
    <section class="page-hero">
      <div class="wrap prose">
        <p class="crumb"><a href="{P('/')}">Home</a> / For AI agents</p>
        <h1>How to connect</h1>
        <p>You can call the public Apify tools through <a href="https://mcp.apify.com/">Apify MCP</a>, or through the Apify HTTP API. The free lite tools include a small MCP server that you run on your computer. No API key is needed for those local tools.</p>
        <p>There is also a live public API for small text jobs (repair JSON, hash text, convert units, and more). That API has its own landing page, remote MCP, and OpenAPI file, which are different from the Apify lists on this page. See <a href="{P('/api/')}">the API page</a>.</p>
        <h2>Apify MCP</h2>
        <p>Add the MCP endpoint for a tool in Cursor, Claude Desktop, or another app that supports MCP. Each public tool has its own endpoint of the form <code>https://mcp.apify.com/?tools=tidybytetools/&lt;actor&gt;</code>.</p>
        <h2>Apify HTTP API</h2>
        <p>You can also start a run with <code>POST https://api.apify.com/v2/acts/tidybytetools~&lt;actor&gt;/run-sync-get-dataset-items</code>. The OpenAPI file for that shape is at <a href="{P('/openapi.json')}">{BASE}/openapi.json</a>. You will need an Apify token for the HTTP API.</p>
        <h2>Local lite MCP</h2>
        <p>For a free lite tool, install it from GitHub and run its MCP server on your computer. Some tools are not on PyPI yet. For those, install with <code>pip install git+https://github.com/tidybytetools/&lt;repo&gt;</code> until a PyPI package is up. Then point your app at the local MCP command shown in that tool’s README.</p>
        <p>Machine-readable lists of the same tools are at <a href="{P('/.well-known/mcp.json')}">/.well-known/mcp.json</a>, <a href="{P('/tools.json')}">/tools.json</a>, and <a href="{P('/llms.txt')}">/llms.txt</a>.</p>
        <p>Each Apify run has a ${ACTOR_START_USD} start fee in addition to the event price below. Failed or skipped items are free, as described on each tool page.</p>
      </div>
    </section>
    <section>
      <div class="wrap">
        <h2>Tools you can call</h2>
        <div class="agent-table-wrap">
          <table class="agent-table">
            <thead>
              <tr>
                <th>Tool</th>
                <th>Apify actor</th>
                <th>MCP endpoint</th>
                <th>Price per event</th>
                <th>Input</th>
                <th>Output</th>
              </tr>
            </thead>
            <tbody>
              {"".join(rows)}
            </tbody>
          </table>
        </div>
      </div>
    </section>
    '''
    html_text = page_shell(
        "How to connect — Tidy Byte Tools",
        "Connect Tidy Byte Tools to an AI app with Apify MCP, the Apify HTTP API, or a local lite MCP server.",
        "/connect/",
        body,
        "connect",
        tools,
    )
    write_page("connect/index.html", html_text)



def api_page(tools: list[dict]) -> None:
    """Human page for the live Cloudflare Worker API."""
    landing = API_WORKER + "/"
    mcp = API_WORKER + "/mcp"
    openapi = API_WORKER + "/openapi.json"
    pricing = API_WORKER + "/pricing"
    pricing_json = API_WORKER + "/pricing.json"
    registry = "https://registry.modelcontextprotocol.io/v0/servers/io.github.tidybytetools%2Fapi/versions/1.0.0"
    body = f"""
    <section class="page-hero">
      <div class="wrap prose">
        <p class="crumb"><a href="{P('/')}">Home</a> / API</p>
        <h1>Tidy Byte Tools API</h1>
        <p>This is a public JSON API for small text jobs: repair JSON, hash or encode text, format data, make IDs, convert dates and units, and similar tools. It runs on a Cloudflare Worker. You can also call the same tools through a remote MCP server.</p>
        <p>You can try it without a key (50 calls per IP each UTC day). Or post to <code>/keys</code> to get a free key and raise the cap to 200 calls per key each UTC day. Paid billing is not live. You cannot pay for this API yet.</p>
        <h2>Where to call it</h2>
        <ul>
          <li>Landing page: <a href="{e(landing)}">{e(landing)}</a></li>
          <li>Remote MCP: <a href="{e(mcp)}"><code>{e(mcp)}</code></a></li>
          <li>OpenAPI for this API: <a href="{e(openapi)}"><code>{e(openapi)}</code></a></li>
          <li>Prices: <a href="{e(pricing)}">{e(pricing)}</a> and <a href="{e(pricing_json)}">{e(pricing_json)}</a></li>
        </ul>
        <p>The OpenAPI file above describes the Worker API. It is not the same file as <a href="{P('/openapi.json')}">{BASE}/openapi.json</a>, which describes how to call public Apify actors.</p>
        <h2>For AI agents</h2>
        <p>Point an MCP client at <code>{e(mcp)}</code> (Streamable HTTP). An API key is optional. A bad key is rejected with HTTP 401; it does not fall back to the anonymous cap.</p>
        <p>Official MCP Registry name: <code>io.github.tidybytetools/api</code>. Record: <a href="{e(registry)}">{e(registry)}</a>.</p>
        <p>This site also lists the API in <a href="{P('/tools.json')}">/tools.json</a>, <a href="{P('/llms.txt')}">/llms.txt</a>, and <a href="{P('/.well-known/mcp.json')}">/.well-known/mcp.json</a>.</p>
      </div>
    </section>
    """
    html_text = page_shell(
        "API — Tidy Byte Tools",
        "Public JSON API and remote MCP for small text jobs. Landing page, MCP endpoint, and OpenAPI are on the Cloudflare Worker.",
        "/api/",
        body,
        "api",
        tools,
    )
    write_page("api/index.html", html_text)


def generate_og_images(tools: list[dict]) -> None:
    """Make a 1200×630 Open Graph image for each tool from its cover."""
    dest = ASSETS / "img" / "og"
    dest.mkdir(parents=True, exist_ok=True)
    default = ASSETS / "img" / "og.png"
    for tool in tools:
        out = dest / f"{tool['slug']}.png"
        src = Path(tool["cover"]) if tool.get("cover") else None
        if src and src.exists():
            im = Image.open(src).convert("RGB")
            w, h = im.size
            target_ratio = 1200 / 630
            src_ratio = w / h
            if src_ratio > target_ratio:
                new_w = int(h * target_ratio)
                left = (w - new_w) // 2
                im = im.crop((left, 0, left + new_w, h))
            else:
                new_h = int(w / target_ratio)
                top = (h - new_h) // 2
                im = im.crop((0, top, w, top + new_h))
            im = im.resize((1200, 630), Image.Resampling.LANCZOS)
            im.save(out, "PNG", optimize=True)
        elif default.exists() and not out.exists():
            shutil.copyfile(default, out)
        if out.exists():
            tool["og_path"] = f"/assets/img/og/{tool['slug']}.png"
        print("og", tool["slug"])


def write_mcp(tools: list[dict]) -> None:
    entries = []
    for tool in tools:
        actor = tool.get("actor")
        store = _apify_store_url(tool)
        ev = tool.get("event")
        github, local_mcp = tool_github_and_mcp(tool)
        item = {
            "name": tool["name"],
            "slug": tool["slug"],
            "description": tool["tagline"],
            "url": f"{BASE}/tools/{tool['slug']}/",
            "github": github,
            "input": tool.get("input"),
            "output": tool.get("output"),
            "translations": I18N.tool_translations_obj(tool["slug"]),
        }
        if actor:
            item["actor"] = f"tidybytetools/{actor}"
            if store:
                item["apify"] = store
                item["mcp"] = f"https://mcp.apify.com/?tools=tidybytetools/{actor}"
            else:
                item["apify_status"] = "The public store page is not up yet."
        if ev:
            item["price"] = {
                "event": ev.get("id"),
                "title": ev.get("title"),
                "usd": ev.get("price_usd"),
                "unit": ev.get("unit"),
                "start_fee_usd": ACTOR_START_USD,
            }
        if local_mcp:
            item["local_mcp"] = local_mcp
        entries.append(item)
    data = {
        "name": "Tidy Byte Tools",
        "description": "Small tools that clean up messy data. Call the public Worker API over HTTP or remote MCP, call public Apify actors through Apify MCP, or run a free lite MCP server on your computer.",
        "website": BASE + "/",
        "connect": BASE + "/connect/",
        "api": BASE + "/api/",
        "openapi": BASE + "/openapi.json",
        "openapi_note": "This file describes public Apify actors. The Worker API has its own OpenAPI at " + API_WORKER + "/openapi.json.",
        "catalog": BASE + "/tools.json",
        "mcp_apify_pattern": "https://mcp.apify.com/?tools=tidybytetools/<actor>",
        "remote_mcp": {
            "name": "Tidy Byte Tools API",
            "url": API_WORKER + "/mcp",
            "transport": "streamable-http",
            "landing": API_WORKER + "/",
            "openapi": API_WORKER + "/openapi.json",
            "registry": "io.github.tidybytetools/api",
            "note": "API key optional. Anonymous use is allowed. A bad key is rejected with HTTP 401.",
        },
        "tools": entries,
    }
    dest = OUT / ".well-known"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "mcp.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print("wrote .well-known/mcp.json")


def write_openapi(tools: list[dict]) -> None:
    paths = {}
    schemas = {}
    for tool in tools:
        actor = tool.get("actor")
        store = _apify_store_url(tool)
        if not actor or not store:
            continue
        actor_id = f"tidybytetools~{actor}"
        path = f"/acts/{actor_id}/run-sync-get-dataset-items"
        ev = tool.get("event") or {}
        desc = (
            f"{tool['name']}: {tool['tagline']} "
            f"Input: {tool.get('input') or 'See the tool page.'} "
            f"Output: {tool.get('output') or 'See the tool page.'}"
        )
        if ev:
            desc += f" Price: ${ev.get('price_usd')} per {ev.get('unit')} ({ev.get('title')}). Start fee ${ACTOR_START_USD}."
        paths[path] = {
            "post": {
                "operationId": f"run_{tool['slug'].replace('-', '_')}",
                "summary": tool["name"],
                "description": desc,
                "tags": [tool["name"]],
                "security": [{"ApifyToken": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"type": "object", "additionalProperties": True},
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Dataset items from a finished run.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"type": "object", "additionalProperties": True},
                                }
                            }
                        },
                    }
                },
            }
        }
    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": "Tidy Byte Tools Apify API",
            "description": (
                "Call public Tidy Byte Tools actors with the Apify run-sync API. "
                "POST the actor input as JSON. You need an Apify API token. "
                "See also https://mcp.apify.com/ and this site's /connect/ page. "
                "Actors whose public store page is not up yet are omitted here."
            ),
            "version": f"{YEAR}-11-10",
        },
        "servers": [{"url": "https://api.apify.com/v2", "description": "Apify API"}],
        "paths": paths,
        "components": {
            "securitySchemes": {
                "ApifyToken": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "description": "Use 'Bearer <APIFY_TOKEN>'.",
                }
            }
        },
    }
    (OUT / "openapi.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    print("wrote openapi.json", "paths", len(paths))


def write_meta(tools: list[dict], guides: list[dict] | None = None) -> None:
    guides = guides or []
    robots = [
        "User-agent: *",
        "Allow: /",
        "",
        "User-agent: GPTBot",
        "Allow: /",
        "",
        "User-agent: ChatGPT-User",
        "Allow: /",
        "",
        "User-agent: ClaudeBot",
        "Allow: /",
        "",
        "User-agent: anthropic-ai",
        "Allow: /",
        "",
        "User-agent: Google-Extended",
        "Allow: /",
        "",
        "User-agent: Applebot-Extended",
        "Allow: /",
        "",
        "User-agent: PerplexityBot",
        "Allow: /",
        "",
        "User-agent: CCBot",
        "Allow: /",
        "",
        "User-agent: Bytespider",
        "Allow: /",
        "",
        f"Sitemap: {BASE}/sitemap.xml",
        "",
    ]
    (OUT / "robots.txt").write_text("\n".join(robots))

    urls = [
        "/",
        "/tools/",
        "/tools.json",
        "/guides/",
        "/privacy/",
        "/terms/",
        "/connect/",
        "/api/",
        "/llms.txt",
        "/llms-full.txt",
        "/openapi.json",
        "/.well-known/mcp.json",
    ]
    for lang in I18N.LANGS:
        if lang["prefix"]:
            urls.append(f"/{lang['prefix']}/")
    urls += [f"/tools/{t['slug']}/" for t in tools]
    urls += [f"/guides/{g['slug']}/" for g in guides]

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    home_paths = {"/"} | {f"/{lang['prefix']}/" for lang in I18N.LANGS if lang["prefix"]}
    for path in urls:
        loc = e(BASE + path)
        extras = []
        if path in home_paths:
            for lang in I18N.LANGS:
                href = BASE + (f"/{lang['prefix']}/" if lang["prefix"] else "/")
                extras.append(
                    f'    <xhtml:link rel="alternate" hreflang="{e(lang["hreflang"])}" href="{e(href)}"/>'
                )
            extras.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{e(BASE + "/")}"/>')
        if extras:
            parts.append(f"  <url>\n    <loc>{loc}</loc>\n" + "\n".join(extras) + "\n  </url>")
        else:
            parts.append(f"  <url><loc>{loc}</loc></url>")
    parts.append("</urlset>\n")
    (OUT / "sitemap.xml").write_text("\n".join(parts))

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
        f"- [Spanish home]({BASE}/es/)",
        f"- [Portuguese home]({BASE}/pt/)",
        f"- [German home]({BASE}/de/)",
        f"- [French home]({BASE}/fr/)",
        f"- [Japanese home]({BASE}/ja/)",
        f"- [Chinese home]({BASE}/zh/)",
        f"- [All tools]({BASE}/tools/)",
        f"- [Guides]({BASE}/guides/)",
        f"- [How to connect]({BASE}/connect/): Apify actor URLs, MCP endpoints, prices, and input/output",
        f"- [API]({BASE}/api/): public JSON API and remote MCP (landing, /mcp, and Worker OpenAPI)",
        f"- [Privacy]({BASE}/privacy/)",
        f"- [Terms]({BASE}/terms/)",
        f"- [Machine-readable catalog]({BASE}/tools.json): name, what it does, price, Apify, MCP, GitHub, and translations",
        f"- [MCP catalog]({BASE}/.well-known/mcp.json)",
        f"- [OpenAPI]({BASE}/openapi.json): call public actors with the Apify run-sync API",
        f"- [Long catalog]({BASE}/llms-full.txt)",
        "",
        "## Public API (Cloudflare Worker)",
        f"- [Landing page]({API_WORKER}/): human docs, examples, and a free key form (POST /keys)",
        f"- [Remote MCP]({API_WORKER}/mcp): Streamable HTTP. Official registry name io.github.tidybytetools/api",
        f"- [OpenAPI for this API]({API_WORKER}/openapi.json): the Worker endpoints. This is not the same file as {BASE}/openapi.json, which describes Apify actors.",
        f"- [Prices]({API_WORKER}/pricing) and [{API_WORKER}/pricing.json]({API_WORKER}/pricing.json): free daily caps are $0. Paid billing is not live.",
        f"- [Site API page]({BASE}/api/)",
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
        tr = I18N.tool_translations_obj(t["slug"])
        if tr:
            lines.append("  - Multilingual keywords:")
            for code, pack in tr.items():
                kws = ", ".join(pack.get("keywords") or [])
                lines.append(f"    - {code}: {pack.get('description', '')} | {kws}")
    lines += [
        "",
        "## Shops",
        "- [Apify](https://apify.com/tidybytetools)",
        "- [Gumroad](https://tidybyte.gumroad.com)",
        "- [GitHub](https://github.com/tidybytetools)",
        "",
    ]
    (OUT / "llms.txt").write_text("\n".join(lines + ["", f"Full catalog: {BASE}/llms-full.txt", ""]))
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
    full.append("Do not advertise a private Apify Console URL as a public store page.")
    full.append("")
    (OUT / "llms-full.txt").write_text("\n".join(full))
    catalog = tools_catalog(tools)
    (OUT / "tools.json").write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
    print("wrote tools.json")
    write_mcp(tools)
    write_openapi(tools)
    (OUT / ".nojekyll").write_text("")


def write_readme() -> None:
    (ROOT / "README.md").write_text(
        """# Tidy Byte Tools website

This is the public homepage for [Tidy Byte Tools](https://tidybytetools.github.io).

Small tools that clean up messy data. The site lists every live product, with real links and real prices, and is hosted for free on GitHub Pages. A machine-readable catalog is at [tools.json](https://tidybytetools.github.io/tools.json). Agents can also read [llms.txt](https://tidybytetools.github.io/llms.txt), [/.well-known/mcp.json](https://tidybytetools.github.io/.well-known/mcp.json), and [openapi.json](https://tidybytetools.github.io/openapi.json).

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


def guides_index(tools: list[dict], guides: list[dict]) -> None:
    cards = []
    for g in guides:
        cards.append(
            f'<article class="card"><h3><a href="{P(f"/guides/{g["slug"]}/")}">{e(g["title"])}</a></h3>'
            f'<p class="tagline">{e(g["description"])}</p></article>'
        )
    body = f'''
    <section class="wrap page-hero">
      <p class="crumb"><a href="{P("/")}">Home</a> / Guides</p>
      <h1>How-to guides</h1>
      <p class="lede">Short, honest guides for common file jobs. Free options first, then our tools when they help.</p>
    </section>
    <section class="wrap" style="padding-bottom:48px">
      <div class="card-grid">{"".join(cards)}</div>
    </section>
    '''
    html_text = page_shell(
        "How-to guides · Tidy Byte Tools",
        "Short how-to guides for PDF tables, Markdown for AI, broken links, LLM tokens, and JSON to CSV.",
        "/guides/",
        body,
        "guides",
        tools,
    )
    write_page("guides/index.html", html_text)


def guide_page(guide: dict, tools: list[dict], guides: list[dict]) -> None:
    article = rewrite_guide_links(md_to_html(guide["body_md"], P), guides, P)
    import re as _re
    article = _re.sub(r"^<h1>.*?</h1>\s*", "", article, count=1)
    others = "".join(
        f'<li><a href="{P(f"/guides/{g["slug"]}/")}">{e(g["title"])}</a></li>'
        for g in guides
        if g["slug"] != guide["slug"]
    )
    body = f'''
    <section class="wrap page-hero">
      <p class="crumb"><a href="{P("/")}">Home</a> / <a href="{P("/guides/")}">Guides</a> / {e(guide["title"])}</p>
      <h1>{e(guide["title"])}</h1>
      <p class="lede">{e(guide["description"])}</p>
    </section>
    <section class="wrap" style="padding-bottom:48px">
      <article class="prose guide-body">{article}</article>
      <aside style="margin-top:36px">
        <h2>More guides</h2>
        <ul>{others}</ul>
      </aside>
    </section>
    '''
    html_text = page_shell(
        f'{guide["title"]} · Tidy Byte Tools',
        guide["description"],
        f'/guides/{guide["slug"]}/',
        body,
        "guides",
        tools,
    )
    write_page(f'guides/{guide["slug"]}/index.html', html_text)


def pack_snowrsps() -> None:
    """Rebuild the snowrsps.com copy and zip it with shutil.make_archive."""
    parent = Path("/workspace/products/site-snowrsps")
    dest = parent / "tidybytetools"
    dest.mkdir(parents=True, exist_ok=True)
    ht = dest / ".htaccess"
    ht_text = ht.read_text() if ht.exists() else "DirectoryIndex index.html index.php\nOptions -Indexes\n"
    for child in list(dest.iterdir()):
        if child.name == ".htaccess":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    env = os.environ.copy()
    env["SITE_BASE"] = "https://snowrsps.com/tidybytetools"
    env["PATH_PREFIX"] = "/tidybytetools"
    env["DEST"] = str(dest)
    print("packing snowrsps copy into", dest)
    subprocess.check_call([sys.executable, str(ROOT / "build.py"), "--no-pack"], env=env, cwd=str(ROOT))
    ht.write_text(ht_text)
    zip_path = parent / "tidybytetools.zip"
    if zip_path.exists():
        zip_path.unlink()
    shutil.make_archive(str(parent / "tidybytetools"), "zip", root_dir=str(parent), base_dir="tidybytetools")
    file_count = sum(1 for p in dest.rglob("*") if p.is_file())
    print(f"wrote {zip_path} ({file_count} files in tidybytetools/)")


def build_site() -> list[dict]:
    print("Building Tidy Byte Tools website…", "BASE=", BASE, "OUT=", OUT)
    tools = live_tools()
    guides = load_guides(GUIDES_DIR)
    subset_fonts()
    generate_missing_art(tools)
    copy_brand_assets(tools)
    copy_galleries(tools)
    generate_og_images(tools)
    write_css()
    home_page(tools)
    for lang in I18N.LANGS:
        if lang["code"] != "en":
            home_page(tools, lang=lang["code"])
    tools_index(tools)
    for tool in tools:
        tool_page(tool, tools)
    write_aliases(tools)
    privacy_page(tools)
    terms_page(tools)
    connect_page(tools)
    api_page(tools)
    not_found_page(tools)
    guides_index(tools, guides)
    for g in guides:
        guide_page(g, tools, guides)
    write_meta(tools, guides)
    if OUT.resolve() == ROOT.resolve():
        write_readme()
        write_gitignore()
    print(f"done: {len(tools)} tools, {len(guides)} guides, out={OUT}")
    return tools


def main() -> None:
    args = set(sys.argv[1:])
    configure()
    build_site()
    if "--no-pack" not in args and OUT.resolve() == ROOT.resolve():
        pack_snowrsps()


if __name__ == "__main__":
    main()
