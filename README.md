# Die Line Creation Agent

A lightweight Python agent that creates packaging die-line specs from product dimensions and packaging requirements.

## Features

- Generates die-line specifications from a product name and dimensions
- Produces cut, fold, bleed, and safe-area guidance
- Supports carton style presets like tuck end, sleeve, and box
- Exports a structured JSON spec for downstream tooling or design workflows
- Includes a CLI for quick generation

## Project structure

- `src/die_line_agent.py` — core generation logic
- `app.py` — command-line entry point
- `README.md` — project usage guide

## Quick start

```bash
python app.py --product "Face Cream Box" --width 80 --height 120 --depth 40 --style "box" --material "paperboard"
```

Example output:

```json
{
  "product_name": "Face Cream Box",
  "dimensions": {
    "width_mm": 80,
    "height_mm": 120,
    "depth_mm": 40,
    "bleed_mm": 3,
    "safe_area_mm": 5
  },
  "style": "box",
  "panels": {
    "front": "80 x 120 mm",
    "back": "80 x 120 mm",
    "side_left": "40 x 120 mm",
    "side_right": "40 x 120 mm",
    "top": "80 x 40 mm",
    "bottom": "80 x 40 mm"
  },
  "cut_lines": [
    "Front/back panels: 80 x 120 mm",
    "Side panels: 40 x 120 mm",
    "Top/bottom panels: 80 x 40 mm"
  ],
  "fold_lines": [
    "Vertical fold at 80 mm intervals",
    "Horizontal fold at 120 mm intervals"
  ],
  "notes": [
    "Use 3 mm bleed on all edges.",
    "Keep critical graphics inside the 5 mm safe zone."
  ]
}
```

## Extending the agent

You can extend this starter into a real production workflow by adding:

- PDF or SVG die-line export
- CAD-friendly output markup
- AI assisted prompts from packaging briefs
- Template library by product category
- Optional database or API integration

## License

This repository is provided as a starter implementation for packaging die-line generation.
