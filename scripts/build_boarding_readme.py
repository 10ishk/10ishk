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
MOTION_CSS = '''<style>
.plane{transform:translateX(13px);animation:flight 8s ease-in-out infinite}
.contrail{animation:trail 8s ease-in-out infinite;opacity:0}
@keyframes trail{0%,8%{opacity:0}18%,43%{opacity:.65}56%,100%{opacity:0}}
.radar-sweep{animation:radar 10s linear infinite}
@keyframes radar{to{transform:rotate(360deg)}}
.radar-ping{transform-box:fill-box;transform-origin:center;animation:ping 5.2s ease-out infinite;opacity:.35}
@keyframes ping{0%{transform:scale(1);opacity:.45}75%,100%{transform:scale(3.5);opacity:0}}
@keyframes flight{0%{transform:translateX(0);opacity:0}8%{opacity:1}48%,80%{transform:translateX(26px);opacity:1}94%{transform:translateX(26px);opacity:0}100%{transform:translateX(0);opacity:0}}
.status-ring{transform-box:fill-box;transform-origin:center;animation:signal 3.6s ease-out infinite}
@keyframes signal{0%,100%{transform:scale(1);opacity:.2}60%{transform:scale(2.1);opacity:0}85%{opacity:0}}
.board-letter{transform-box:fill-box;transform-origin:center;animation:boardFlip 14s ease-in-out infinite}
@keyframes boardFlip{0%{transform:scaleY(.18);opacity:.65}2.5%{transform:scaleY(1);opacity:1}4%{transform:scaleY(.9)}6%,100%{transform:scaleY(1);opacity:1}}
.project-reveal{animation:reveal .85s ease-out both}
@keyframes reveal{from{transform:translateY(4px);opacity:.72}to{transform:translateY(0);opacity:1}}
@media(prefers-reduced-motion:reduce){.plane,.status-ring,.board-letter,.project-reveal,.contrail,.radar-sweep,.radar-ping{animation:none!important;transform:none!important;opacity:1!important}.plane{transform:translateX(13px)!important}.status-ring,.radar-ping{opacity:.2!important}.contrail{opacity:0!important}}
</style>'''


def plane_route(x, y):
    return (f'<path d="M{x-7} {y}H{x+36}" stroke="#bdb7a9" stroke-width="1.5"/>'
            f'<g transform="translate({x} {y})"><g class="plane">'
            '<g class="contrail" stroke="#e5372b" stroke-width="1.2" stroke-linecap="round">'
            '<path d="M-25-3H-16M-29 0H-17M-25 3H-16"/></g>'
            '<g transform="rotate(90)"><path transform="translate(-12 -12)" '
            'd="M21 16V14L13 9V3.5A1.5 1.5 0 0 0 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5Z" '
            'fill="#e5372b" stroke="#e5372b" stroke-width=".5" stroke-linejoin="round"/></g>'
            '</g></g>')


def home_radar(x, y):
    return (f'<g transform="translate({x} {y})" aria-hidden="true">'
            '<circle r="14" fill="none" stroke="#bdb7a9" stroke-width=".8"/>'
            '<circle r="7" fill="none" stroke="#bdb7a9" stroke-width=".6"/>'
            '<g class="radar-sweep"><path d="M0 0V-13" stroke="#e5372b" stroke-width="1.2"/>'
            '<path d="M0 0L-5-12A13 13 0 0 1 0-13Z" fill="#e5372b" opacity=".13"/></g>'
            '<circle class="radar-ping" r="3.5" fill="none" stroke="#e5372b" stroke-width=".65"/>'
            '<circle r="2" fill="#e5372b"/></g>')


def animated_heading(x, y, value, size):
    face = FONTS['display']
    glyphs, cmap = face.getGlyphSet(), face.getBestCmap()
    result = ''
    for i, char in enumerate(value):
        result += f'<g class="board-letter" style="animation-delay:{i*.065:.3f}s">'+label(x,y,char,size,GOLD,'display')+'</g>'
        x += glyphs[cmap[ord(char)]].width * size / face['head'].unitsPerEm
    return result


def system_status(x, y, size=10):
    return (f'<circle class="status-ring" cx="{x}" cy="{y-3}" r="4" fill="#f6d77a"/>'
            f'<circle cx="{x}" cy="{y-3}" r="2.5" fill="#f6d77a"/>'
            + label(x+12,y,'SYSTEMS ONLINE',size,GOLD,'bold'))


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
        f'<title>{escape(title)}</title>{MOTION_CSS if "class=" in body else ""}'
        f'{box(0,0,w,h,background)}{body}</svg>\n', encoding="utf-8")


PROJECTS = [
    ("movi-agent", "Natural-language transport workflows with guarded action execution.", "REACT / TYPESCRIPT / FASTAPI", "AI SYSTEMS"),
    ("two-stage-ppe", "Two-stage inference, crop batching, tracking and training tools.", "PYTHON / ULTRALYTICS / OPENCV", "VISION SYSTEMS"),
    ("FlickVox", "Local speech synthesis with hotkeys, saved phrases and playback.", "C# / WPF / PIPER", "LOCAL DESKTOP"),
    ("voice-lead-agent", "State-aware voice workflows with grounded facts and typed summaries.", "PYTHON / VAPI / DEEPGRAM", "VOICE AI"),
    ("ak680-studio", "Native keyboard profile tools with HID detection and device controls.", "TAURI / RUST / REACT / HID", "HARDWARE"),
    ("quick-commerce-launch-control-tower", "Launch readiness, inventory and risk controls. Synthetic data.", "EXCEL / POWER QUERY / PYTHON", "OPERATIONS"),
    ("b2b-customer-expansion-radar", "Account intelligence, scoring and CRM handoffs. Synthetic data.", "EXCEL / PYTHON / CRM HANDOFF", "CUSTOMER OPS"),
    ("yardvision-sop-monitoring", "Camera feeds into SOP events, zone alerts and evidence snapshots.", "PYTHON / OPENCV / YOLOv8", "VISION"),
    ("it-support-operations-lab", "Windows diagnostics, incident evidence and backup verification.", "POWERSHELL / WINDOWS / SHA-256", "IT SUPPORT"),
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
body += plane_route(174,208)
body += label(242, 225, 'SHIPPED', 48, INK, 'display')
body += label(56, 264, 'APPLIED AI ENGINEER', 30, INK, 'display')
body += label(56, 291, 'INTELLIGENT SYSTEMS BUILDER', 18, '#5f5a52', 'display', spacing=1)
body += label(691, 73, 'BUILDER ID', 11, '#5f5a52', 'bold', spacing=1)
body += label(689, 124, '10ISHK', 52, INK, 'display')
body += barcode(691,148,42,130)
body += label(691, 212, f'{len(PROJECTS):02} PROJECTS ABOARD', 9, INK, 'bold')
body += '<path d="M691 227H824" stroke="#bdb7a9"/>'
body += label(691, 246, 'HOME BASE', 10, '#5f5a52', 'bold', spacing=1)
body += label(690, 282, 'DXB', 38, RED, 'display')
body += home_radar(792,270)
body += label(691, 302, 'DUBAI, UAE', 11, INK, 'bold')
save('hero.svg',880,340,'Tanishk Bhardwaj — Applied AI Engineer / Intelligent Systems Builder. Home base DXB — Dubai, UAE. Idea to shipped. 16 projects aboard.',body)

body = box(12,16,376,494,CREAM,16)
body += '<defs><clipPath id="ticket"><rect x="12" y="16" width="376" height="494" rx="16"/></clipPath></defs>'
body += '<g clip-path="url(#ticket)">' + box(12,16,376,10,RED) + '</g>'
body += label(32,60,'BOARDING PASS / PROFILE',11,'#5f5a52','bold',spacing=1)
body += label(29,126,'TANISHK',68,INK,'display')
body += label(29,193,'BHARDWAJ',68,INK,'display')
body += label(32,228,'FROM',10,'#5f5a52','bold',spacing=2)
body += label(186,228,'TO',10,'#5f5a52','bold',spacing=2)
body += label(32,268,'IDEA',42,INK,'display')
body += plane_route(124,253)
body += label(186,268,'SHIPPED',42,INK,'display')
body += label(32,299,'APPLIED AI ENGINEER',26,INK,'display')
body += label(32,321,'INTELLIGENT SYSTEMS BUILDER',19,'#5f5a52','display',spacing=.3)
body += '<path d="M24 335H376" stroke="#bdb7a9" stroke-width="2" stroke-dasharray="6 5"/>'
body += '<circle cx="12" cy="335" r="11" fill="#0f0e0d"/><circle cx="388" cy="335" r="11" fill="#0f0e0d"/>'
body += label(32,365,'BUILDER ID',10,'#5f5a52','bold',spacing=1)
body += label(32,409,'10ISHK',42,INK,'display')
body += barcode(206,355,49,145)
body += label(206,430,'16 PROJECTS ABOARD',10,INK,'bold')
body += '<path d="M32 443H368" stroke="#bdb7a9"/>'
body += label(32,463,'HOME BASE',10,'#5f5a52','bold',spacing=1)
body += label(31,495,'DXB',34,RED,'display')
body += home_radar(338,480)
body += label(113,490,'DUBAI, UAE',15,INK,'bold')
save('hero-mobile.svg',400,526,'Tanishk Bhardwaj — Applied AI Engineer / Intelligent Systems Builder. Home base DXB — Dubai, UAE. Idea to shipped. Builder 10ishk.',body)

for name,title in [('website','tanishk.net'),('linkedin','LinkedIn'),('github','GitHub')]:
    body=box(3,3,274,48,INK,7,GOLD)
    body+=label(24,34,title+' →',18,GOLD,'bold',max_width=236)
    save(f'{name}.svg',280,56,title,body)
    body=box(3,3,122,40,INK,5,GOLD)
    body+=label(10,29,title+' →',14,GOLD,'bold',max_width=108)
    save(f'{name}-mobile.svg',128,48,title,body)

# A terminal-style mission panel carries the introduction without a plain-text break.
body=box(28,12,824,140,INK,8,'#6b6255')
body+=box(28,12,4,140,RED)
body+=label(50,40,'MISSION BRIEF',12,GOLD,'bold',spacing=2)
body+=system_status(672,40,10)
body+=label(50,73,'I build intelligent systems that turn models, data',16,CREAM,max_width=776)
body+=label(50,100,'and software into practical tools.',16,CREAM)
body+=label(50,133,'VOICE / VISION / DESKTOP APPS / DECISION WORKFLOWS',11,GOLD,'bold',spacing=.5)
save('mission.svg',880,168,'I build intelligent systems that turn models, data and software into practical tools — voice, vision, desktop apps and decision workflows.',body)
body=box(14,12,372,176,INK,8,'#6b6255')
body+=box(14,12,4,176,RED)
body+=label(32,39,'MISSION BRIEF',11,GOLD,'bold',spacing=1)
body+=system_status(236,39,8)
for i,line in enumerate(['I build intelligent systems that','turn models, data and software','into practical tools.']):
    body+=label(32,73+i*24,line,15,CREAM,max_width=336)
body+=label(32,154,'VOICE / VISION / DESKTOP APPS',10,GOLD,'bold')
body+=label(32,173,'DECISION WORKFLOWS',10,GOLD,'bold')
save('mission-mobile.svg',400,200,'I build intelligent systems that turn models, data and software into practical tools — voice, vision, desktop apps and decision workflows.',body)

groups = [
    ('AI & MODELS',['Python / PyTorch','Ultralytics YOLO','OpenCV','Whisper / Piper']),
    ('APPLICATIONS & APIs',['TypeScript / React','Next.js / FastAPI','Express','C# / WPF / .NET']),
    ('DATA & DECISIONS',['SQL / SQLite','Excel / Power Query','OR-Tools','Streamlit']),
    ('SYSTEMS & HARDWARE',['Rust / Tauri','Electron','HID integration','PowerShell']),
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
    body=animated_heading(16 if mobile else 28,52,'DEPARTURES',44)
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
    if i <= 3:
        body=f'<g class="project-reveal" style="animation-delay:{(i-1)*.18:.2f}s">{body}</g>'
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
    if i <= 3:
        body=f'<g class="project-reveal" style="animation-delay:{(i-1)*.18:.2f}s">{body}</g>'
    save(f'{name}-mobile.svg',400,h+5,f'{i:02}. {name}: {description} Stack: {stack}.',body)

for name,title,subtitle in [
    ('earlier','ARRIVED EARLIER','EARLY EXPERIMENTS / SAME CURIOSITY'),
    ('log','FLIGHT LOG','A YEAR OF BUILDING / CONTRIBUTION AIRSPACE'),
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
    # A new image URL avoids GitHub serving a cached static version of an animated asset.
    version = '?v=flight2' if stem == 'hero' else ('?v=motion1' if stem in {'mission','departures',*[name for name,*_ in PROJECTS[:3]]} else '')
    return (f'<picture>\n  <source media="(max-width: 600px)" srcset="assets/boarding/{stem}-mobile.svg{version}">\n'
            f'  <img src="assets/boarding/{stem}.svg{version}" width="100%" alt="{escape(alt,quote=True)}">\n</picture>')


readme=picture('hero','Tanishk Bhardwaj — Applied AI Engineer / Intelligent Systems Builder. Home base: DXB — Dubai, UAE. Boarding pass from idea to shipped. Builder 10ishk.')+'\n\n'
readme+='<p align="center">\n'
for slug,url,title in [('website','https://tanishk.net','Visit tanishk.net'),('linkedin','https://www.linkedin.com/in/tanishk004','Connect on LinkedIn'),('github','https://github.com/10ishk','Explore my GitHub')]:
    readme+=(f'  <a href="{url}"><picture>'
             f'<source media="(max-width: 600px)" srcset="assets/boarding/{slug}-mobile.svg">'
             f'<img src="assets/boarding/{slug}.svg" width="32%" alt="{title}"></picture></a>\n')
readme+='</p>\n\n'
readme+=picture('mission','Mission brief: I build intelligent systems that turn models, data and software into practical tools — voice, vision, desktop apps and decision workflows.')+'\n\n'
readme+=picture('stack','Carry-on stack — AI and models, applications and APIs, data and decisions, systems and hardware.')+'\n\n'
readme+=picture('departures','Departures — 16 projects, selected work first.')+'\n\n'
for i,(name,description,stack,_) in enumerate(PROJECTS,1):
    readme+=f'<a href="https://github.com/10ishk/{name}">\n'+picture(name,f'{i:02}. {name} — {description} Stack: {stack}.')+'\n</a>\n'
readme+='\n'+picture('earlier','Arrived earlier — early experiments, same curiosity.')+'\n\n'
for name,description in EARLIER:
    readme+=f'<a href="https://github.com/10ishk/{name}">\n'+picture(name,f'Earlier work: {name} — {description}')+'\n</a>\n'
readme+='\n'
readme+=picture('log','Flight log — a year of building, flown across the contribution calendar.')+'\n\n'
readme+='''<picture>
  <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/10ishk/10ishk/output-boarding/flight-log-dark-still.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/10ishk/10ishk/output-boarding/flight-log-light-still.svg">
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/10ishk/10ishk/output-boarding/flight-log-dark.svg">
  <img width="100%" alt="GitHub contribution flight log — a plane flies over real activity tiles with a fading trail; contributions stay visible" src="https://raw.githubusercontent.com/10ishk/10ishk/output-boarding/flight-log-light.svg">
</picture>

'''
(ROOT/'README.md').write_text(readme.rstrip()+'\n',encoding='utf-8')
print(f'Built boarding-pass README: {len(PROJECTS)} project rows, {len(EARLIER)} earlier-work rows, {len(list(OUT.glob("*.svg")))} SVGs.')
