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
    for filename, background, border, title in [
        ("snake.svg", "#f6f8fc", "#a9b7cd", "Contribution snake — ink snake and blue tiles"),
        ("snake-dark.svg", "#111827", "#61718e", "Contribution snake — yellow snake and blue tiles"),
    ]:
        file = folder / filename
        file.write_text(style(file.read_text(encoding="utf-8"), background, border, title), encoding="utf-8")
        print(f"Styled {filename}")
