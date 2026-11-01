# Boarding-pass concept

This alternative is on `design/boarding-pass-readme`, based on the preserved
neo-brutalist draft at `02199ff57587eea1d5c0c2fb37d2969c279a18b6`.
Neither this branch nor the neo-brutalist branch changes the live profile until
merged into `main`.

The supplied airport reference is adapted into a cream boarding pass with a red
stripe, a perforated builder-ID stub, four carry-on stack groups, and a split-flap
departures board. The ticket keeps the name and focus separate from the barcode
stub. Sixteen individual project rows remain clickable, followed by three compact
"Arrived earlier" rows for older work. The five newer projects are included. The board
leads with movi-agent, two-stage-ppe and FlickVox, followed by voice and hardware
work before operations tools. Business workbook descriptions identify synthetic data.

The ticket positions Tanishk as an Applied AI Engineer / Intelligent Systems
Builder. The ticket's home-base field uses DXB in airline red and spells out Dubai, UAE,
with a dedicated location strip beneath the tear-off section on mobile.
A themed Mission Brief replaces the plain-text introduction and spans
voice, vision, desktop apps and decision workflows. Carry-on groups are AI &
Models, Applications & APIs, Data & Decisions, and Systems & Hardware. Contact
links appear once near the top; the page ends with the flight-log animation.

## Motion

A red plane makes a short trip along IDEA → SHIPPED every eight seconds, with
a pause between trips. The DEPARTURES lettering briefly flips into place every
fourteen seconds; the project names do not continuously flip. The first three
project rows have a single subtle staggered reveal. A decorative SYSTEMS ONLINE
light pulses slowly in the Mission Brief; it is a design detail, not a live
uptime monitor.

Animations use CSS inside self-contained SVG images. All text is visible without
animation support. `prefers-reduced-motion: reduce` disables the plane, heading,
reveals and pulse, and the generated contribution snake also stops animating.
The README also selects a bundled static contribution snapshot for reduced-motion
viewers, so this fallback works even while a remote animation is cached.

All graphics have outlined lettering using the bundled Barlow Condensed and
Space Mono OFL fonts. They need no external fonts, JavaScript, or remote image
rendering services. Font licenses are included under `assets/boarding/fonts/`.
The barcode is decorative. Mobile SVG variants rearrange the ticket, stack and
departures rows instead of shrinking the desktop board into unreadable text.

## Rebuild

```sh
python -m pip install -r scripts/requirements-boarding.txt
python scripts/build_boarding_readme.py
```

The generator contains the project summaries, stacks and repository names.
Project links open their own READMEs for full details; no duplicate expandable
project list interrupts the departures-board theme.
`scripts/build_readme.py` remains the neo-brutalist generator and will replace
the README with that earlier design if run; use the boarding generator here.

## Flight log

The snake workflow publishes to `output-boarding`, separate from both the original
`output` and the neo-brutalist `output-loud` branches. Warm contribution tiles,
explicit panel backgrounds and a red light-mode / gold dark-mode snake match
the ticket palette. Relevant branch pushes generate the preview. Daily updates
run from the default branch after merging.

## Restore either earlier design

Before merging, leave this branch unmerged; the live profile is unchanged.
The neo-brutalist draft remains on `design/neo-brutalist-readme`. The original
profile is preserved on `backup/readme-before-neo-brutalist-2026-11-01`.
After merging, restore `README.md`, `.github/workflows/snake.yml` and
`scripts/style_snake.py` from the desired earlier branch and commit the restore.
All earlier assets remain in the repository, so existing image paths still work.
