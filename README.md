# Tidy Byte Tools website

This is the public homepage for [Tidy Byte Tools](https://tidybytetools.github.io).

Small tools that clean up messy data. The site lists every live product, with real links and real prices, and is hosted for free on GitHub Pages.

## Rebuild

```
python3 build.py
```

You need Pillow, fontTools, brotli, and (for generated product art) Google Chrome, which `build.py` uses through `/workspace/design/render.py` when a tool has no existing cover.

Fonts are a subset of [Geist](https://github.com/vercel/geist-font), SIL Open Font License 1.1. The license is in `assets/fonts/OFL.txt`.

The site itself is MIT licensed. See `LICENSE`.
