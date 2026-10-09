from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import json


@dataclass
class ProductDimensions:
    width_mm: float
    height_mm: float
    depth_mm: float
    bleed_mm: float = 3.0
    safe_area_mm: float = 5.0


class DieLineAgent:
    """Creates a basic die-line specification for packaging layouts."""

    def __init__(self, product_name: str, width_mm: float, height_mm: float, depth_mm: float,
                 style: str = "box", material: str = "paperboard"):
        self.product_name = product_name
        self.dimensions = ProductDimensions(width_mm, height_mm, depth_mm)
        self.style = style.lower()
        self.material = material

    def build_panel_map(self) -> Dict[str, str]:
        width = self.dimensions.width_mm
        height = self.dimensions.height_mm
        depth = self.dimensions.depth_mm

        if self.style in {"box", "carton", "folding-carton"}:
            panels = {
                "front": f"{width} x {height} mm",
                "back": f"{width} x {height} mm",
                "side_left": f"{depth} x {height} mm",
                "side_right": f"{depth} x {height} mm",
                "top": f"{width} x {depth} mm",
                "bottom": f"{width} x {depth} mm",
            }
        elif self.style in {"sleeve", "wrap"}:
            panels = {
                "front": f"{width} x {height} mm",
                "back": f"{width} x {height} mm",
                "sleeve_body": f"{width} x {height} mm",
                "seal_area": f"{width} x {depth} mm",
            }
        elif self.style in {"tuck", "tuck-end"}:
            panels = {
                "front": f"{width} x {height} mm",
                "back": f"{width} x {height} mm",
                "tuck_end": f"{width} x {depth} mm",
                "side_panel": f"{depth} x {height} mm",
            }
        else:
            panels = {
                "front": f"{width} x {height} mm",
                "back": f"{width} x {height} mm",
                "side": f"{depth} x {height} mm",
                "top": f"{width} x {depth} mm",
            }

        return panels

    def build_cut_lines(self) -> List[str]:
        width = self.dimensions.width_mm
        height = self.dimensions.height_mm
        depth = self.dimensions.depth_mm

        if self.style in {"box", "carton", "folding-carton"}:
            return [
                f"Front/back panels: {width} x {height} mm",
                f"Side panels: {depth} x {height} mm",
                f"Top/bottom panels: {width} x {depth} mm",
            ]
        elif self.style in {"sleeve", "wrap"}:
            return [
                f"Sleeve body: {width} x {height} mm",
                f"Seal tab: {width} x {depth} mm",
            ]
        else:
            return [
                f"Primary panel: {width} x {height} mm",
                f"Secondary panel: {depth} x {height} mm",
            ]

    def build_fold_lines(self) -> List[str]:
        width = self.dimensions.width_mm
        height = self.dimensions.height_mm
        depth = self.dimensions.depth_mm

        lines = [
            f"Vertical fold at {width} mm intervals",
            f"Horizontal fold at {height} mm intervals",
        ]

        if self.style in {"box", "carton", "folding-carton"}:
            lines.append(f"Depth fold allowance: {depth} mm")

        return lines

    def build_notes(self) -> List[str]:
        return [
            f"Material: {self.material}",
            f"Bleed: {self.dimensions.bleed_mm} mm on all edges",
            f"Safe area: keep critical content inside {self.dimensions.safe_area_mm} mm from the trim edge",
            "Add glue tabs and locking features for assembly",
        ]

    def generate_spec(self) -> Dict[str, object]:
        return {
            "product_name": self.product_name,
            "style": self.style,
            "material": self.material,
            "dimensions": {
                "width_mm": self.dimensions.width_mm,
                "height_mm": self.dimensions.height_mm,
                "depth_mm": self.dimensions.depth_mm,
                "bleed_mm": self.dimensions.bleed_mm,
                "safe_area_mm": self.dimensions.safe_area_mm,
            },
            "panels": self.build_panel_map(),
            "cut_lines": self.build_cut_lines(),
            "fold_lines": self.build_fold_lines(),
            "notes": self.build_notes(),
        }


def generate_die_line(product_name: str, width_mm: float, height_mm: float, depth_mm: float,
                     style: str = "box", material: str = "paperboard") -> Dict[str, object]:
    agent = DieLineAgent(product_name, width_mm, height_mm, depth_mm, style=style, material=material)
    return agent.generate_spec()


if __name__ == "__main__":
    sample = generate_die_line(
        product_name="Sample Product Box",
        width_mm=80,
        height_mm=120,
        depth_mm=40,
        style="box",
        material="paperboard",
    )
    print(json.dumps(sample, indent=2))
