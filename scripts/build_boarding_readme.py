"""Build the boarding-pass profile. Install requirements-boarding.txt first.

Lettering is outlined from the bundled OFL fonts, so GitHub needs no web fonts.
"""
from pathlib import Path
from html import escape
import textwrap
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "boarding"
FONT_DIR = OUT / "fonts"
INK, CREAM, GOLD, RED, MUTED = "#0f0e0d", "#f7f4ec", "#f6d77a", "#e5372b", "#b6ad9e"
FONTS = {name: TTFont(FONT_DIR / file) for name, file in {
    "display": "BarlowCondensed-Bold.ttf", "mono": "SpaceMono-Regular.ttf",
    "bold": "SpaceMono-Bold.ttf"}.items()}
BOUNDS = []


def label(x, y, value, size=16, color=CREAM, font="mono", max_width=None, spacing=0):
    face = FONTS[font]
    glyphs, cmap = face.getGlyphSet(), face.getBestCmap()
    scale = size / face['head'].unitsPerEm
    advance = sum(glyphs[cmap.get(ord(c), '.notdef')].width * scale + spacing for c in value)
    sx = scale * min(1, max_width / advance) if max_width and advance else scale
    pen = SVGPathPen(glyphs, ntos=lambda value: f'{value:.2f}'.rstrip('0').rstrip('.') if value else '0')
    bounds = BoundsPen(glyphs)
    cursor = x
    for char in value:
        glyph = glyphs[cmap.get(ord(char), '.notdef')]
        transform = (sx, 0, 0, -scale, cursor, y)
        glyph.draw(TransformPen(pen, transform))
        glyph.draw(TransformPen(bounds, transform))
        cursor += glyph.width * sx + spacing
    if bounds.bounds:
        BOUNDS.append((value, bounds.bounds))
    return f'<path fill="{color}" d="{pen.getCommands()}"/>'


def box(x, y, w, h, fill=INK, radius=0, stroke=None, dash=None):
    attrs = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ''
    if dash:
        attrs += f' stroke-dasharray="{dash}"'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"{attrs}/>'


def save(name, w, h, title, body, background=INK):
    for value, (left, top, right, bottom) in BOUNDS:
        if left < 0 or top < 0 or right > w or bottom > h:
            raise ValueError(f'{name}: text outside artboard: {value} {(left, top, right, bottom)}')
    BOUNDS.clear()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title, quote=True)}">'
        f'<title>{escape(title)}</title>{box(0,0,w,h,background)}{body}</svg>\n', encoding="utf-8")


PROJECTS = [
    ("two-stage-ppe", "Person-first PPE detection, video tracking and training tools.", "PYTHON / ULTRALYTICS / OPENCV", "VISION"),
    ("FlickVox", "Local Windows speech: hotkey, saved phrases and Piper playback.", "C# / WPF / PIPER", "DESKTOP"),
    ("movi-agent", "Transport operations copilot with guarded, human-approved actions.", "REACT / TYPESCRIPT / FASTAPI", "AI + OPS"),
    ("quick-commerce-launch-control-tower", "Launch readiness, inventory and risk controls. Synthetic data.", "EXCEL / POWER QUERY / PYTHON", "OPERATIONS"),
    ("b2b-customer-expansion-radar", "Account intelligence, scoring and CRM handoffs. Synthetic data.", "EXCEL / PYTHON / CRM HANDOFF", "CUSTOMER OPS"),
    ("yardvision-sop-monitoring", "Camera feeds into SOP events, zone alerts and evidence snapshots.", "PYTHON / OPENCV / YOLOv8", "VISION"),
    ("it-support-operations-lab", "Windows diagnostics, incident evidence and backup verification.", "POWERSHELL / WINDOWS / SHA-256", "IT SUPPORT"),
    ("voice-lead-agent", "Permission-first multilingual voice qualification and summaries.", "PYTHON / VAPI / DEEPGRAM", "VOICE AI"),
    ("ak680-studio", "Native keyboard profile tools, HID detection and lighting controls.", "TAURI / RUST / REACT / HID", "HARDWARE"),
    ("ak680-overlay-studio", "Electron overlay controller for the AJAZZ keyboard web driver.", "ELECTRON / REACT / TYPESCRIPT", "HARDWARE"),
    ("cargo-visibility-control-tower", "Shipment visibility, SLA breaches and revenue-at-risk analysis.", "PYTHON / SQLITE / POWER BI", "LOGISTICS"),
    ("port-yard-dispatch-optimizer", "Dispatch planning with capacity, time windows and OR-Tools.", "PYTHON / OR-TOOLS / FASTAPI", "OPTIMIZATION"),
    ("tanishk-portfolio", "Motion-led portfolio with project pages, notes and canvas work.", "NEXT.JS / REACT / MOTION", "WEB"),
    ("lstm-text-generator", "Reproducible word-level text generation and temperature sampling.", "PYTHON / PYTORCH / LSTM", "ML"),
    ("CallSense-App", "Call transcription, summaries, emotion and action extraction.", "PYTHON / WHISPER / NLP", "VOICE + NLP"),
    ("AdverseWeatherAVDetection", "Vehicle detection in rain, fog and snow on a BDD100K subset.", "PYTHON / YOLOv5 / PYTORCH", "VISION"),
]


def barcode(x, y, height, width):
    # Decorative stripe pattern, not a scannable travel credential.
    bars = [3,1,2,1,4,2,1,3,2,1,4,1,2,3,1,2,4,1,3,2,1,4,2,1]
    unit = width / (sum(bars) + len(bars) * 1.5)
    result = ''
    for bar in bars:
        result += box(x, y, bar * unit, height, INK)
        x += (bar + 1.5) * unit
    return result


# Cream ticket, dark terminal surround, red airline stripe and tear-off stub.
body = box(28, 24, 824, 292, CREAM, 18)
body += '<defs><clipPath id="ticket"><rect x="28" y="24" width="824" height="292" rx="18"/></clipPath></defs>'
body += '<g clip-path="url(#ticket)">' + box(28,24,824,12,RED) + '</g>'
body += '<path d="M664 36V304" stroke="#bdb7a9" stroke-width="2" stroke-dasharray="6 5"/>'
body += '<circle cx="664" cy="24" r="13" fill="#0f0e0d"/><circle cx="664" cy="316" r="13" fill="#0f0e0d"/>'
body += label(56, 70, 'BOARDING PASS / BUILDER PROFILE', 12, '#5f5a52', 'bold', spacing=2)
body += label(54, 145, 'TANISHK BHARDWAJ', 76, INK, 'display', max_width=578)
body += label(56, 180, 'FROM', 11, '#5f5a52', 'bold', spacing=2)
body += label(242, 180, 'TO', 11, '#5f5a52', 'bold', spacing=2)
body += label(56, 225, 'IDEA', 48, INK, 'display')
body += '<path d="M167 208H209M198 197L209 208L198 219" fill="none" stroke="#e5372b" stroke-width="3"/>'
body += label(242, 225, 'SHIPPED', 48, INK, 'display')
body += label(56, 264, 'AI × LOGISTICS × VISION', 18, INK, 'bold')
body += label(56, 291, 'LOCAL APPS / PRACTICAL SYSTEMS / 10ISHK', 10, '#5f5a52', 'mono', spacing=.5)
body += label(691, 73, 'BUILDER ID', 11, '#5f5a52', 'bold', spacing=1)
body += label(689, 124, '10ISHK', 52, INK, 'display')
body += barcode(691,153,64,130)
body += label(691, 250, f'{len(PROJECTS):02} PROJECTS', 12, INK, 'bold')
body += label(691, 274, 'ABOARD', 11, '#5f5a52', 'bold', spacing=2)
save('hero.svg',880,340,'Tanishk Bhardwaj — boarding pass from idea to shipped. AI, logistics and vision. 16 projects aboard.',body)

body = box(12,16,376,438,CREAM,16)
body += '<defs><clipPath id="ticket"><rect x="12" y="16" width="376" height="438" rx="16"/></clipPath></defs>'
body += '<g clip-path="url(#ticket)">' + box(12,16,376,10,RED) + '</g>'
body += label(32,60,'BOARDING PASS / PROFILE',11,'#5f5a52','bold',spacing=1)
body += label(29,126,'TANISHK',68,INK,'display')
body += label(29,193,'BHARDWAJ',68,INK,'display')
body += label(32,228,'FROM',10,'#5f5a52','bold',spacing=2)
body += label(186,228,'TO',10,'#5f5a52','bold',spacing=2)
body += label(32,268,'IDEA',42,INK,'display')
body += '<path d="M118 253H157M147 244L157 253L147 262" fill="none" stroke="#e5372b" stroke-width="3"/>'
body += label(186,268,'SHIPPED',42,INK,'display')
body += label(32,307,'AI × LOGISTICS × VISION',14,INK,'bold')
body += '<path d="M24 335H376" stroke="#bdb7a9" stroke-width="2" stroke-dasharray="6 5"/>'
body += '<circle cx="12" cy="335" r="11" fill="#0f0e0d"/><circle cx="388" cy="335" r="11" fill="#0f0e0d"/>'
body += label(32,365,'BUILDER ID',10,'#5f5a52','bold',spacing=1)
body += label(32,409,'10ISHK',42,INK,'display')
body += barcode(206,355,49,145)
body += label(206,430,'16 PROJECTS ABOARD',10,INK,'bold')
save('hero-mobile.svg',400,470,'Tanishk Bhardwaj — idea to shipped. AI, logistics and vision. Builder 10ishk.',body)

for name,title in [('website','tanishk.net'),('linkedin','LinkedIn'),('github','GitHub')]:
    body=box(3,3,274,48,INK,7,GOLD)
    body+=label(24,34,title+' →',18,GOLD,'bold',max_width=236)
    save(f'{name}.svg',280,56,title,body)
    body=box(3,3,122,40,INK,5,GOLD)
    body+=label(10,29,title+' →',14,GOLD,'bold',max_width=108)
    save(f'{name}-mobile.svg',128,48,title,body)

groups = [
    ('LANGUAGES',['Python','TypeScript','Rust','C#','PowerShell']),
    ('APPS + APIS',['React / Next.js','FastAPI / Express','Tauri','WPF / .NET']),
    ('VISION + ML',['PyTorch','OpenCV','Ultralytics YOLO','Whisper / Piper']),
    ('DATA + OPS',['SQL / SQLite','Excel / Power Query','OR-Tools','Streamlit']),
]
for mobile in [False,True]:
    w,h=(400,488) if mobile else (880,296)
    body=label(20 if mobile else 28,34,'CARRY-ON / STACK',12,MUTED,'bold',spacing=2)
    for i,(title,items) in enumerate(groups):
        x,y=(14+(i%2)*190,58+(i//2)*208) if mobile else (28+i*209,62)
        cw=182 if mobile else 197
        body+=box(x,y,cw,194,INK,9,'#6b6255','5 4')
        body+=label(x+14,y+28,title,11,GOLD,'bold',max_width=cw-28,spacing=.7)
        for j,item in enumerate(items):
            body+=label(x+14,y+58+j*27,item,23,CREAM,'display',max_width=cw-28)
    save('stack-mobile.svg' if mobile else 'stack.svg',w,h,'Carry-on stack: Python, TypeScript, Rust, C#, PowerShell, React, FastAPI, Tauri, WPF, PyTorch, OpenCV, YOLO, speech, SQL, Excel, Power Query and OR-Tools.',body)


def flap(x,y,value,size=16,cell=16,height=26,color=GOLD):
    body=''
    for character in value:
        body+=box(x,y,cell-2,height,'#24211d',2)
        body+=box(x,y+height/2,cell-2,height/2,'#1b1916')
        body+=label(x+2,y+height-6,character,size,color,'bold')
        body+=f'<path d="M{x} {y+height/2}H{x+cell-2}" stroke="#0f0e0d" stroke-width=".7"/>'
        x+=cell
    return body


for mobile in [False,True]:
    w=400 if mobile else 880
    body=label(16 if mobile else 28,52,'DEPARTURES',44,GOLD,'display')
    body+=label(16 if mobile else 520,77 if mobile else 46,'16 PROJECTS / SELECTED FIRST',10,MUTED,'bold',spacing=.5)
    body+=f'<path d="M{16 if mobile else 28} {92 if mobile else 69}H{w-(16 if mobile else 28)}" stroke="#f6d77a" stroke-width="2"/>'
    save('departures-mobile.svg' if mobile else 'departures.svg',w,106 if mobile else 82,'Departures — 16 projects, selected work first.',body)

for i,(name,description,stack,category) in enumerate(PROJECTS,1):
    body=flap(28,19,f'{i:02}',16)
    body+=flap(88,19,name.upper(),16,cell=17)
    body+=label(88,76,description,14,CREAM,max_width=712)
    body+=label(88,103,stack,11,MUTED,'bold')
    body+=label(807,42,'↗',22,GOLD,'bold')
    body+='<path d="M28 124H852" stroke="#39342c"/>'
    save(f'{name}.svg',880,132,f'{i:02}. {name}: {description} Stack: {stack}.',body)
    lines=textwrap.wrap(name.upper(),width=23,break_long_words=False,break_on_hyphens=True)
    descriptions=textwrap.wrap(description,width=39)
    start=26+len(lines)*27
    h=start+len(descriptions)*20+52
    body=label(16,20,f'{i:02} / {category}',10,MUTED,'bold')
    for j,line in enumerate(lines):
        body+=flap(16,33+j*27,line,14,cell=15,height=24)
    for j,line in enumerate(descriptions):
        body+=label(16,start+29+j*20,line,14,CREAM,max_width=366)
    body+=label(16,h-15,stack,10,GOLD,'bold',max_width=366)
    body+=f'<path d="M16 {h-2}H384" stroke="#39342c"/>'
    save(f'{name}-mobile.svg',400,h+5,f'{i:02}. {name}: {description} Stack: {stack}.',body)

for name,title,subtitle in [
    ('earlier','ARRIVED EARLIER','EARLY EXPERIMENTS / SAME CURIOSITY'),
    ('log','FLIGHT LOG','A YEAR OF BUILDING / CONTRIBUTION SNAKE'),
]:
    body=label(28,52,title,44,GOLD,'display')
    body+=label(28,81,subtitle,11,MUTED,'bold',spacing=.5)
    body+='<path d="M28 99H852" stroke="#6b6255" stroke-dasharray="6 5"/>'
    save(f'{name}.svg',880,112,title+' — '+subtitle,body)
    body=label(16,48,title,38,GOLD,'display')
    body+=label(16,75,subtitle,9,MUTED,'bold',max_width=368)
    body+='<path d="M16 91H384" stroke="#6b6255" stroke-dasharray="6 5"/>'
    save(f'{name}-mobile.svg',400,104,title+' — '+subtitle,body)

EARLIER = [
    ('ai_models', 'Classic machine-learning notebooks.'),
    ('Face_recog', 'Early face-recognition experiments.'),
    ('Housing_analysis', 'Housing data exploration and regression.'),
]
for name,description in EARLIER:
    body=flap(28,17,'--',16,color=MUTED)
    body+=flap(88,17,name.upper(),16,cell=17,color=MUTED)
    body+=label(430,37,description,12,CREAM,max_width=360)
    body+=label(807,39,'↗',22,GOLD,'bold')
    body+='<path d="M28 61H852" stroke="#39342c"/>'
    save(f'{name}.svg',880,68,f'Earlier work: {name} — {description}',body)
    body=flap(16,12,name.upper(),14,cell=15,height=24,color=MUTED)
    body+=label(16,61,description,13,CREAM,max_width=345)
    body+='<path d="M16 77H384" stroke="#39342c"/>'
    save(f'{name}-mobile.svg',400,84,f'Earlier work: {name} — {description}',body)


def picture(stem,alt):
    return (f'<picture>\n  <source media="(max-width: 600px)" srcset="assets/boarding/{stem}-mobile.svg">\n'
            f'  <img src="assets/boarding/{stem}.svg" width="100%" alt="{escape(alt,quote=True)}">\n</picture>')


readme=picture('hero','Tanishk Bhardwaj — boarding pass from idea to shipped. AI × Logistics × Vision. Builder 10ishk.')+'\n\n'
readme+='<p align="center">\n'
for slug,url,title in [('website','https://tanishk.net','Visit tanishk.net'),('linkedin','https://www.linkedin.com/in/tanishk004','Connect on LinkedIn'),('github','https://github.com/10ishk','Explore my GitHub')]:
    readme+=(f'  <a href="{url}"><picture>'
             f'<source media="(max-width: 600px)" srcset="assets/boarding/{slug}-mobile.svg">'
             f'<img src="assets/boarding/{slug}.svg" width="32%" alt="{title}"></picture></a>\n')
readme+='</p>\n\n'
readme+='I turn ideas into useful tools: computer vision for logistics and safety, local desktop apps, and practical operations systems.\n\n'
readme+=picture('stack','Carry-on stack — languages, apps and APIs, vision and ML, data and operations.')+'\n\n'
readme+=picture('departures','Departures — 16 projects, selected work first.')+'\n\n'
for i,(name,description,stack,_) in enumerate(PROJECTS,1):
    readme+=f'<a href="https://github.com/10ishk/{name}">\n'+picture(name,f'{i:02}. {name} — {description} Stack: {stack}.')+'\n</a>\n'
readme+='\n'+picture('earlier','Arrived earlier — early experiments, same curiosity.')+'\n\n'
for name,description in EARLIER:
    readme+=f'<a href="https://github.com/10ishk/{name}">\n'+picture(name,f'Earlier work: {name} — {description}')+'\n</a>\n'
readme+='\n'
readme+=picture('log','Flight log — a year of building, shown as a contribution snake.')+'\n\n'
readme+='''<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/10ishk/10ishk/output-boarding/snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/10ishk/10ishk/output-boarding/snake.svg">
  <img width="100%" alt="GitHub contribution snake animation — warm terminal tiles with a red snake in light mode and gold in dark mode" src="https://raw.githubusercontent.com/10ishk/10ishk/output-boarding/snake.svg">
</picture>

<p align="center"><sub><a href="https://tanishk.net">tanishk.net</a> · <a href="https://www.linkedin.com/in/tanishk004">LinkedIn</a> · <a href="https://github.com/10ishk">GitHub</a></sub></p>
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
print(f'Built boarding-pass README: {len(PROJECTS)} project rows, {len(EARLIER)} earlier-work rows, {len(list(OUT.glob("*.svg")))} SVGs.')
