from __future__ import annotations

import argparse
import json

from src.die_line_agent import generate_die_line


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a packaging die-line specification.")
    parser.add_argument("--product", required=True, help="Product or packaging name")
    parser.add_argument("--width", type=float, required=True, help="Width in mm")
    parser.add_argument("--height", type=float, required=True, help="Height in mm")
    parser.add_argument("--depth", type=float, required=True, help="Depth in mm")
    parser.add_argument("--style", default="box", help="Packaging style such as box, sleeve, tuck")
    parser.add_argument("--material", default="paperboard", help="Packaging material type")
    args = parser.parse_args()

    spec = generate_die_line(
        product_name=args.product,
        width_mm=args.width,
        height_mm=args.height,
        depth_mm=args.depth,
        style=args.style,
        material=args.material,
    )

    print(json.dumps(spec, indent=2))


if __name__ == "__main__":
    main()
