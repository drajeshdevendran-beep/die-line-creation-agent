"""AI-powered die-line generation from natural language prompts."""

from dataclasses import dataclass
from typing import Dict, Optional
import re


@dataclass
class ParsedBrief:
    """Parsed packaging brief from user prompt."""
    product_name: str
    width_mm: float
    height_mm: float
    depth_mm: float
    style: str
    material: str
    special_notes: list[str]


class AIPackagingAgent:
    """Extracts packaging parameters from natural language briefs."""

    def __init__(self):
        self.dimension_patterns = {
            'width': r'(?:width|w)[\s:]*([0-9.]+)\s*(?:mm|millimeter)',
            'height': r'(?:height|h)[\s:]*([0-9.]+)\s*(?:mm|millimeter)',
            'depth': r'(?:depth|d)[\s:]*([0-9.]+)\s*(?:mm|millimeter)',
        }
        self.style_keywords = {
            'box': ['box', 'carton', 'folding', 'rigid'],
            'sleeve': ['sleeve', 'wrap', 'wrapper'],
            'tuck': ['tuck', 'auto-lock', 'auto lock'],
            'pouch': ['pouch', 'stand-up', 'standup'],
        }
        self.material_keywords = {
            'paperboard': ['paperboard', 'cardboard', 'corrugated'],
            'kraft': ['kraft', 'kraft paper'],
            'folding_carton': ['folding carton', 'white board'],
            'corrugated': ['corrugated', 'fluted'],
        }

    def extract_dimensions(self, text: str) -> Dict[str, Optional[float]]:
        """Extract width, height, depth from natural language."""
        dims = {}
        for key, pattern in self.dimension_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            dims[key] = float(match.group(1)) if match else None
        return dims

    def extract_style(self, text: str) -> str:
        """Detect packaging style from keywords."""
        text_lower = text.lower()
        for style, keywords in self.style_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return style
        return 'box'

    def extract_material(self, text: str) -> str:
        """Extract material type from keywords."""
        text_lower = text.lower()
        for material, keywords in self.material_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return material.replace('_', ' ')
        return 'paperboard'

    def extract_product_name(self, text: str) -> str:
        """Extract or infer product name from brief."""
        match = re.search(r'(?:for|product:?\s+)([^,.]*?)(?:\.|,|width|height|depth|$)', text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if len(name) > 3 and len(name) < 100:
                return name
        return 'Custom Product'

    def extract_special_notes(self, text: str) -> list[str]:
        """Extract any special requirements or notes."""
        notes = []
        keywords = [
            ('eco', 'Use eco-friendly materials'),
            ('recycl', 'Include recycling guidance'),
            ('print', 'Complex printing required'),
            ('gloss', 'Glossy finish requested'),
            ('matte', 'Matte finish requested'),
            ('emboss', 'Embossing required'),
            ('window', 'Product window/die-cut required'),
            ('handle', 'Include handles'),
        ]
        for keyword, note in keywords:
            if keyword.lower() in text.lower():
                notes.append(note)
        return notes

    def parse_brief(self, prompt: str) -> ParsedBrief:
        """Parse a natural language packaging brief into structured parameters."""
        dims = self.extract_dimensions(prompt)
        width = dims.get('width') or 80.0
        height = dims.get('height') or 120.0
        depth = dims.get('depth') or 40.0

        return ParsedBrief(
            product_name=self.extract_product_name(prompt),
            width_mm=width,
            height_mm=height,
            depth_mm=depth,
            style=self.extract_style(prompt),
            material=self.extract_material(prompt),
            special_notes=self.extract_special_notes(prompt),
        )


def parse_packaging_brief(prompt: str) -> ParsedBrief:
    """Convenience function to parse a packaging brief."""
    agent = AIPackagingAgent()
    return agent.parse_brief(prompt)
