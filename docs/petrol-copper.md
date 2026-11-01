# Petrol & Copper final candidate

Branch: `design/boarding-pass-petrol-copper`.
Starting checkpoint: `checkpoint-boarding-pass-approved-reflip`, commit
`680829cb2d5f8814c42b5e339d4175446497d92a`.

This alternative preserves the approved content, layouts, independent project
name re-flips, reduced-motion fallbacks and relaxed 84-second Flight Log.
Neither the approved charcoal design, Midnight Terminal branch nor `main` changes.

Final polish routes the portfolio card to the public `tanishk.net` website because
its source repository is private. The Face_recog and Housing_analysis rows are
labelled as private archives and are not linked to inaccessible repositories.
Their desktop rows use a small closed-padlock icon. No repository visibility was
changed. Public project source links were checked through GitHub's API.

Primary body text, copper signage, muted panel text and secondary ticket text
have contrast ratios of approximately 12.8:1, 5.6:1, 8.4:1 and 5.2:1 respectively.
The larger burnt-copper DXB label has approximately 3.7:1 contrast on parchment.
Desktop and mobile layouts, all 32 project-name animation variants, static
reduced-motion states and the Flight Log's completion/pause behaviour are verified.

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
