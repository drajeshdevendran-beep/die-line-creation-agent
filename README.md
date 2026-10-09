# Die Line Creation Agent

A lightweight Python agent that creates packaging die-line specs from product dimensions and packaging requirements.

## Features

- Generates die-line specifications from a product name and dimensions
- Produces cut, fold, bleed, and safe-area guidance
- Supports carton style presets like tuck end, sleeve, and box
- Exports a structured JSON spec for downstream tooling or design workflows
- Includes a CLI for quick generation
- Includes web app, AI prompt parsing, and PDF/SVG export support

## Quick start

```bash
pip install -r requirements.txt
python -m uvicorn web.main:app --reload
```

Open `http://localhost:8000` to use the web app.

## CLI example

```bash
python app.py --product "Face Cream Box" --width 80 --height 120 --depth 40 --style "box" --material "paperboard"
```

## AI prompt example

```text
I need a luxury kraft box for face cream. It should be 80mm wide, 120mm tall, and 40mm deep. Use eco-friendly materials and include a product window.
```

## License

This project is a starter implementation for packaging die-line generation.
