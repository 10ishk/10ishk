"""Add opaque themed panels so snake contrast is independent of the page theme."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


def style(source, background, border, title):
    root = ET.fromstring(source)
    x, y, width, height = root.attrib["viewBox"].split()
    # Platane/snk v3 uses --cb for the outline of contribution cells.
    source, count = re.subn(r"--cb:[^;}]+", f"--cb:{border}", source, count=1)
    if count != 1:
        raise ValueError("Expected the generator's cell-outline variable")
    panel = (f'<title>{title}</title><rect x="{x}" y="{y}" width="{width}" '
             f'height="{height}" rx="8" fill="{background}"/>')
    return re.sub(r"(<svg\b[^>]*>)", lambda m: m[1] + panel, source, count=1)


if __name__ == "__main__":
    folder = Path(sys.argv[1])
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else folder
    output.mkdir(parents=True, exist_ok=True)
    for filename, background, border, title in [
        ("snake.svg", "#f7f4ec", "#a89d88", "Flight log — red snake and warm contribution tiles"),
        ("snake-dark.svg", "#0f0e0d", "#8c8270", "Flight log — gold snake and warm contribution tiles"),
    ]:
        file = folder / filename
        (output / filename).write_text(style(file.read_text(encoding="utf-8"), background, border, title), encoding="utf-8")
        print(f"Styled {filename}")
