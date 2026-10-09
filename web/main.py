"""Export die-line specs to PDF and SVG formats."""

from typing import Dict, Any
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class DieLinePDFExporter:
    """Export die-line specification to PDF."""

    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec

    def export(self) -> BytesIO:
        """Generate PDF from die-line spec."""
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 20)
        c.drawString(40, height - 50, f"Die-Line Specification: {self.spec['product_name']}")

        c.setFont("Helvetica", 10)
        y_pos = height - 100
        info_lines = [
            f"Style: {self.spec['style'].title()}",
            f"Material: {self.spec['material']}",
            f"Dimensions: {self.spec['dimensions']['width_mm']}W × {self.spec['dimensions']['height_mm']}H × {self.spec['dimensions']['depth_mm']}D mm",
            f"Bleed: {self.spec['dimensions']['bleed_mm']} mm | Safe Area: {self.spec['dimensions']['safe_area_mm']} mm",
        ]

        for line in info_lines:
            c.drawString(40, y_pos, line)
            y_pos -= 20

        y_pos -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y_pos, "Panels:")
        y_pos -= 15
        c.setFont("Helvetica", 10)
        for panel_name, panel_size in self.spec['panels'].items():
            c.drawString(50, y_pos, f"{panel_name}: {panel_size}")
            y_pos -= 12

        y_pos -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y_pos, "Cut Lines:")
        y_pos -= 15
        c.setFont("Helvetica", 9)
        for cut_line in self.spec['cut_lines']:
            c.drawString(50, y_pos, cut_line)
            y_pos -= 12

        y_pos -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y_pos, "Fold Lines:")
        y_pos -= 15
        c.setFont("Helvetica", 9)
        for fold_line in self.spec['fold_lines']:
            c.drawString(50, y_pos, fold_line)
            y_pos -= 12

        c.save()
        buffer.seek(0)
        return buffer


class DieLineSVGExporter:
    """Export die-line specification to SVG."""

    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec
        self.scale = 2

    def export(self) -> str:
        """Generate SVG from die-line spec."""
        dims = self.spec['dimensions']
        w = dims['width_mm'] * self.scale
        h = dims['height_mm'] * self.scale

        svg_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w + 100}" height="{h + 100}" viewBox="0 0 {w + 100} {h + 100}">',
            '  <defs>',
            '    <style>',
            '      .cut-line { stroke: red; stroke-width: 2; fill: none; }',
            '      .fold-line { stroke: blue; stroke-width: 1; stroke-dasharray: 5,5; fill: none; }',
            '      .text { font-size: 12px; font-family: Arial; }',
            '    </style>',
            '  </defs>',
            f'  <rect class="cut-line" x="50" y="50" width="{w}" height="{h}" />',
        ]

        if self.spec['style'] in ['box', 'carton', 'folding-carton']:
            fold_x = 50 + w / 2
            fold_y = 50 + h / 2
            svg_lines.append(f'  <line class="fold-line" x1="{fold_x}" y1="50" x2="{fold_x}" y2="{50 + h}" />')
            svg_lines.append(f'  <line class="fold-line" x1="50" y1="{fold_y}" x2="{50 + w}" y2="{fold_y}" />')

        svg_lines.append(f'  <text class="text" x="50" y="30">{self.spec["product_name"]} - {self.spec["style"].title()}</text>')
        svg_lines.append(f'  <text class="text" x="50" y="{h + 80}">{dims["width_mm"]}×{dims["height_mm"]}×{dims["depth_mm"]} mm</text>')
        svg_lines.append('</svg>')
        return '\n'.join(svg_lines)
