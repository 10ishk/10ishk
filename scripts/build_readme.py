"""Build self-contained profile graphics using Python's standard library.

Run from any directory: python scripts/build_readme.py
No JavaScript, external fonts, or remote image services are needed by the README.
"""

from pathlib import Path
from html import escape
import re
import subprocess
import textwrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "loud"
COLORS = ["#ffd23f", "#ff6b9d", "#4d7cff", "#3ddc97"]
INK = "#111111"


def text(x, y, value, size=24, fill=INK, mono=False, **attrs):
    font = "Consolas,monospace" if mono else "Arial,Helvetica,sans-serif"
    extra = " ".join(f'{k}="{escape(str(v), quote=True)}"' for k, v in attrs.items())
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'font-weight="700" fill="{fill}" {extra}>{escape(value)}</text>')


def rect(x, y, w, h, fill, stroke=3):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'fill="{fill}" stroke="{INK}" stroke-width="{stroke}"/>')


def svg(name, w, h, label, body):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label, quote=True)}">'
        f'<title>{escape(label)}</title>{body}</svg>\n', encoding="utf-8")


hero = rect(10, 10, 806, 324, INK, 0) + rect(3, 3, 806, 324, COLORS[0], 6)
hero += text(28, 114, "TANISHK", 112, textLength=665, lengthAdjust="spacingAndGlyphs")
hero += text(28, 222, "BHARDWAJ", 112, textLength=750, lengthAdjust="spacingAndGlyphs")
hero += '<g transform="rotate(-3 190 275)">' + rect(28, 250, 345, 46, INK, 0)
hero += text(42, 280, "AI × LOGISTICS × VISION", 21, COLORS[0], mono=True) + '</g>'
hero += '<g transform="translate(427 249) rotate(5 52 30)">'
hero += rect(5, 5, 100, 63, INK, 0) + rect(0, 0, 100, 63, COLORS[3])
hero += '<path d="M20 9V54M40 9V54M60 9V54M80 9V54" stroke="#111" stroke-width="3"/></g>'
hero += '<g transform="translate(551 249) rotate(-6 46 30)">'
hero += rect(5, 5, 92, 63, INK, 0) + rect(0, 0, 92, 63, COLORS[1])
hero += '<path d="M10 31Q46 -3 82 31Q46 65 10 31Z" fill="white" stroke="#111" stroke-width="3"/><circle cx="46" cy="31" r="11" fill="#111"/></g>'
hero += '<g transform="translate(669 252) rotate(-3 52 28)">'
hero += rect(5, 5, 103, 57, INK, 0) + rect(0, 0, 103, 57, COLORS[2])
hero += '<path d="M17 22V35M31 12V45M45 19V38M59 7V50M73 16V41M87 24V33" stroke="#111" stroke-width="5" stroke-linecap="round"/></g>'
svg("hero.svg", 824, 344, "Tanishk Bhardwaj — AI × Logistics × Vision", hero)

for name, label, color, width in [
    ("website", "tanishk.net ↗", COLORS[1], 228),
    ("linkedin", "LinkedIn ↗", COLORS[2], 200),
    ("github", "GitHub ↗", COLORS[3], 180),
]:
    body = rect(7, 7, width - 10, 46, INK, 0) + rect(2, 2, width - 10, 46, color)
    body += text(17, 33, label, 22, mono=True)
    svg(f"{name}.svg", width, 56, label, body)

skills = ["Python", "TypeScript", "Rust", "React", "FastAPI", "Express", "Tauri",
          "PyTorch", "OpenCV", "YOLOv8", "SQLite", "OR-Tools", "Streamlit",
          "C# / WPF", "PowerShell", "Excel", "Power Query"]
body = ""
x, y = 3, 3
for i, label in enumerate(skills):
    width = len(label) * 14 + 30
    if x + width > 810:
        x, y = 3, y + 64
    body += rect(x + 4, y + 4, width, 44, INK, 0)
    body += rect(x, y, width, 44, COLORS[i % 4])
    body += text(x + 14, y + 30, label, 23, mono=True)
    x += width + 18
svg("stack.svg", 824, y + 55, "What I build with: " + ", ".join(skills), body)
body = ""
x, y = 3, 3
for i, label in enumerate(skills):
    width = len(label) * 12 + 24
    if x + width > 390:
        x, y = 3, y + 54
    body += rect(x + 4, y + 4, width, 40, INK, 0)
    body += rect(x, y, width, 40, COLORS[i % 4])
    body += text(x + 11, y + 27, label, 20, mono=True)
    x += width + 14
svg("stack-mobile.svg", 400, y + 50, "What I build with: " + ", ".join(skills), body)

featured = [
    ("two-stage-ppe", "Two-stage safety vision framework", "Person-first PPE detection, video tracking and training tools.", "PYTHON / ULTRALYTICS / OPENCV", COLORS[0]),
    ("FlickVox", "Local text-to-speech for Windows", "Hotkey speech, saved phrases and offline Piper playback.", "C# / .NET / WPF / PIPER", COLORS[1]),
    ("movi-agent", "Transport operations copilot", "Natural-language trips. Guarded actions. Human confirmation.", "REACT / TYPESCRIPT / FASTAPI", COLORS[0]),
    ("quick-commerce-launch-control-tower", "Multi-site launch operations", "Readiness gates, inventory and launch decisions. Synthetic data.", "EXCEL / POWER QUERY / PYTHON", COLORS[2]),
    ("b2b-customer-expansion-radar", "Customer intelligence operations", "Account signals, scoring and CRM handoffs. Synthetic data.", "EXCEL / PYTHON / HUBSPOT HANDOFF", COLORS[3]),
    ("yardvision-sop-monitoring", "Computer vision for logistics", "Camera feeds into SOP events, alerts and evidence snapshots.", "PYTHON / OPENCV / YOLOv8", COLORS[1]),
    ("it-support-operations-lab", "Windows diagnostics and recovery", "System health, network checks and verified backup restores.", "POWERSHELL / WINDOWS / SHA-256", COLORS[2]),
    ("voice-lead-agent", "Multilingual voice qualification", "Grounded conversations, explainable outcomes, typed summaries.", "PYTHON / VAPI / DEEPGRAM", COLORS[2]),
    ("ak680-studio", "Native keyboard configurator", "HID detection, local profiles and Rapid Trigger controls.", "TAURI / RUST / REACT / HID", COLORS[3]),
]
for index, (name, title, description, stack, color) in enumerate(featured, 1):
    body = rect(10, 10, 804, 172, INK, 0) + rect(3, 3, 804, 172, color, 4)
    body += text(25, 35, f"0{index} / {title.upper()}", 18, mono=True)
    title_attrs = {"textLength": 700, "lengthAdjust": "spacingAndGlyphs"} if len(name) > 29 else {}
    body += text(25, 80, name, 36 if len(name) < 29 else 30, **title_attrs)
    body += '<path d="M759 74L781 52M760 52H781V73" fill="none" stroke="#111" stroke-width="4"/>'
    body += text(25, 119, description, 23)
    body += text(25, 153, stack, 19, mono=True)
    svg(f"{name}.svg", 824, 190, f"{name}: {description} Stack: {stack}", body)
    name_lines = textwrap.wrap(name, width=23, break_long_words=False, break_on_hyphens=True)
    desc_lines = textwrap.wrap(description, width=33)
    height = 102 + len(name_lines) * 30 + len(desc_lines) * 25
    body = rect(9, 9, 382, height - 12, INK, 0) + rect(3, 3, 382, height - 12, color, 4)
    body += text(20, 32, f"0{index} / SELECTED PROJECT", 14, mono=True)
    body += '<path d="M349 34L366 17M350 17H366V33" fill="none" stroke="#111" stroke-width="3"/>'
    for j, line in enumerate(name_lines):
        body += text(20, 71 + j * 30, line, 26)
    desc_y = 81 + len(name_lines) * 30
    for j, line in enumerate(desc_lines):
        body += text(20, desc_y + j * 25, line, 19)
    body += text(20, height - 23, stack, 14, mono=True)
    svg(f"{name}-mobile.svg", 400, height + 3, f"{name}: {description} Stack: {stack}", body)

svg("divider.svg", 824, 16, "", '<path d="M0 8H824" stroke="#111" stroke-width="4"/>'
    + ''.join(f'<rect x="{i * 206}" y="4" width="206" height="8" fill="{c}"/>' for i, c in enumerate(COLORS)))

# Keep the existing project descriptions and repository links as real text.
original = subprocess.check_output(
    ["git", "show", "40a82ce52d20dd3bbea35508be14148a8d046890:README.md"],
    cwd=ROOT, encoding="utf-8")
details = re.search(r"(<details open>.*?</details>)\s*\n\s*<img src=\"assets/divider.svg", original, re.S).group(1)
details = details.replace("<details open>", "<details>")
new_projects = [
    ("two-stage-ppe", "python · ultralytics · opencv", "Two-stage person-to-PPE detection with crop batching, global coordinate remapping, video inference, optional ByteTrack tracking, and dataset preparation and training tools. Bring compatible model checkpoints; none are bundled.", "Python, Ultralytics YOLO, OpenCV, ByteTrack"),
    ("FlickVox", "c# · wpf · piper", "Windows text-to-speech companion with a global quick-pill hotkey, saved phrases, playback controls and voice downloads. Speech runs locally after setup; a Windows x64 preview is available in GitHub Releases.", "C#, .NET 10, WPF, Piper, NAudio"),
    ("quick-commerce-launch-control-tower", "excel · power-query · python", "Excel-first multi-site launch planning with readiness gates, inventory reconciliation, risk and issue tracking, and executive reporting. Uses synthetic UAE operations data. Includes Power BI model and report build specifications; no PBIX is included.", "Excel, Power Query / M, Python, Power BI build specifications"),
    ("b2b-customer-expansion-radar", "excel · python · crm", "Customer intelligence workbook with documented business signals, transparent opportunity scoring, stakeholder gaps, account briefs and staged HubSpot handoffs. All account and business data is synthetic; the handoff package is prepared offline.", "Excel, Python, structured CSV / JSON, HubSpot handoff assets"),
    ("it-support-operations-lab", "powershell · windows · diagnostics", "Windows support toolkit for system health, networking, event logs, service investigation and SHA-256 backup/restore verification. Includes controlled execution evidence, guided incidents and local HTML reports.", "PowerShell, Windows CIM / networking cmdlets, SHA-256, HTML / JSON / CSV"),
]
new_details = ""
for name, tags, description, stack in new_projects:
    new_details += (f'<details>\n<summary><strong>{name}</strong> · <code>{tags}</code></summary>\n\n'
                    f'{description}\n\n**Stack:** {stack}<br>\n'
                    f'**Repo:** [10ishk/{name}](https://github.com/10ishk/{name})\n\n</details>\n\n')
details = new_details + details
readme = '''<p align="center">
  <img src="assets/loud/hero.svg" width="100%" alt="Tanishk Bhardwaj — AI × Logistics × Vision. A yellow headline with shipping-container, vision and sound-wave stickers.">
</p>

<p align="center">
  <a href="https://tanishk.net"><img src="assets/loud/website.svg" width="27%" alt="Visit tanishk.net"></a>
  <a href="https://www.linkedin.com/in/tanishk004"><img src="assets/loud/linkedin.svg" width="24%" alt="Connect on LinkedIn"></a>
  <a href="https://github.com/10ishk"><img src="assets/loud/github.svg" width="22%" alt="Explore my GitHub"></a>
</p>

I build AI and computer-vision tools, local desktop apps, and practical systems for logistics, operations and customer intelligence.

## What I build with

<picture>
  <source media="(max-width: 600px)" srcset="assets/loud/stack-mobile.svg">
  <img src="assets/loud/stack.svg" width="100%" alt="Python, TypeScript, Rust, React, FastAPI, Express, Tauri, PyTorch, OpenCV, YOLOv8, SQLite, OR-Tools, Streamlit, C# / WPF, PowerShell, Excel and Power Query">
</picture>

## Things I shipped

'''
for name, _, description, stack, _ in featured:
    readme += (f'<p>\n<a href="https://github.com/10ishk/{name}">\n<picture>\n'
               f'  <source media="(max-width: 600px)" srcset="assets/loud/{name}-mobile.svg">\n'
               f'  <img src="assets/loud/{name}.svg" width="100%" '
               f'alt="{name} — {escape(description, quote=True)} Built with {stack}.">\n'
               '</picture>\n</a>\n</p>\n\n')
readme += '''## All projects

Open a project for its description, stack and repository link.

''' + details + '''

<br>
<img src="assets/loud/divider.svg" width="100%" alt="">

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/10ishk/10ishk/output-loud/snake-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/10ishk/10ishk/output-loud/snake.svg">
    <img width="100%" alt="GitHub contribution snake animation — blue contribution tiles, dark snake in light mode and yellow snake in dark mode" src="https://raw.githubusercontent.com/10ishk/10ishk/output-loud/snake.svg">
  </picture>
</p>

<p align="center"><sub><a href="https://tanishk.net">tanishk.net</a> · <a href="https://www.linkedin.com/in/tanishk004">LinkedIn</a> · <a href="https://github.com/10ishk">GitHub</a></sub></p>
'''
(ROOT / "README.md").write_text(readme, encoding="utf-8")
print(f"Built {len(list(OUT.glob('*.svg')))} SVG assets and README.md")
