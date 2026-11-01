# Petrol & Copper palette experiment

Branch: `design/boarding-pass-petrol-copper`.
Starting checkpoint: `checkpoint-boarding-pass-approved-reflip`, commit
`680829cb2d5f8814c42b5e339d4175446497d92a`.

This alternative preserves the approved content, layouts, independent project
name re-flips, reduced-motion fallbacks and relaxed 84-second Flight Log.
Neither the approved charcoal design, Midnight Terminal branch nor `main` changes.

Palette:

- Deep petrol background and ticket ink: `#102A2B`
- Parchment ticket and foreground: `#F3EBDD`
- Copper signage, ticket stripe and highlights: `#D98A5B`
- Burnt copper plane, home-base code and radar: `#B85F3F`
- Muted text: `#B5C4BC`; ticket secondary text: `#516661`
- Flap faces: `#193936` / `#142F2E`; dark borders: `#3F605B`

The Flight Log pairs muted sage/teal contribution tiles with copper activity
glows. Dark mode uses a copper plane on petrol; light mode uses burnt copper
on parchment. Its workflow publishes four separate light/dark and animated/static
variants to `output-petrol-copper`, preserving the other palettes' output branches.
Scheduled daily refresh begins only after the chosen workflow reaches `main`.

Rebuild using `python scripts/build_boarding_readme.py` after installing
`scripts/requirements-boarding.txt`. The Flight Log uses
`scripts/build_flight_log.py` and Python's standard library. The original
boarding-pass notes describe the baseline implementation; this file records
the palette-specific differences.
