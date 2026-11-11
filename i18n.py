"""Language helpers and translations for the Tidy Byte Tools site."""
from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "i18n"

LANGS = [
    {"code": "en", "hreflang": "en", "prefix": "", "name": "English", "short": "EN"},
    {"code": "es", "hreflang": "es", "prefix": "es", "name": "Espa\u00f1ol", "short": "ES"},
    {"code": "pt-BR", "hreflang": "pt-BR", "prefix": "pt", "name": "Portugu\u00eas", "short": "PT"},
    {"code": "de", "hreflang": "de", "prefix": "de", "name": "Deutsch", "short": "DE"},
    {"code": "fr", "hreflang": "fr", "prefix": "fr", "name": "Fran\u00e7ais", "short": "FR"},
    {"code": "ja", "hreflang": "ja", "prefix": "ja", "name": "\u65e5\u672c\u8a9e", "short": "JA"},
    {"code": "zh-CN", "hreflang": "zh-CN", "prefix": "zh", "name": "\u4e2d\u6587", "short": "\u4e2d\u6587"},
]
LANG_BY_CODE = {L["code"]: L for L in LANGS}

UNIT_KEY = {
    "pages with a table": "pages_with_table",
    "files": "files",
    "clean rows": "clean_rows",
    "numbers": "numbers",
    "links": "links",
    "chunks": "chunks",
    "data rows": "data_rows",
    "unique texts": "unique_texts",
    "rows": "rows",
    "documents": "documents",
    "pages": "pages",
    "dates": "dates",
}

TOOL_I18N = json.loads((DATA / "tools.json").read_text())
UI = json.loads((DATA / "ui.json").read_text()) if (DATA / "ui.json").exists() else {}


def format_count(n: int, lang: str) -> str:
    s = f"{n:,}"
    if lang in ("es", "de", "pt-BR"):
        return s.replace(",", ".")
    if lang == "fr":
        return s.replace(",", "\u00a0")
    return s


def ui(lang: str, key: str, default=None):
    pack = UI.get(lang) or UI.get("en") or {}
    if key in pack:
        return pack[key]
    en = UI.get("en") or {}
    if key in en:
        return en[key]
    if default is not None:
        return default
    raise KeyError(key)


def tool_translations_obj(slug: str) -> dict:
    item = TOOL_I18N.get(slug) or {}
    out = {}
    for code in ("es", "pt-BR", "de", "fr", "ja", "zh-CN"):
        if code in item:
            out[code] = {
                "description": item[code]["description"],
                "keywords": list(item[code].get("keywords") or []),
            }
    return out


def tool_description(tool: dict, lang: str) -> str:
    if lang != "en":
        tr = (TOOL_I18N.get(tool["slug"]) or {}).get(lang)
        if tr and tr.get("description"):
            return tr["description"]
    return tool["tagline"]
