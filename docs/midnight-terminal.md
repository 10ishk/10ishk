# Midnight Terminal palette experiment

Branch: `design/boarding-pass-midnight-terminal`.
Starting checkpoint: `checkpoint-boarding-pass-approved-reflip`, commit
`680829cb2d5f8814c42b5e339d4175446497d92a`.

The approved charcoal boarding-pass design remains on
`design/boarding-pass-readme`. This branch changes the colours while preserving
project order, wording, layout, tile re-flips and the relaxed 84-second Flight Log.
The live profile on `main` is unchanged.

Palette:

- Navy background and ticket ink: `#101B2D`
- Ivory ticket and foreground: `#F4F0E6`
- Amber signage, ticket stripe and highlights: `#F2B544`
- Red plane, home-base code and radar: `#E5372B`
- Muted text: `#B6C0CF`; ticket secondary text: `#526174`
- Flap faces: `#1D2B40` / `#162337`; dark borders: `#43536B`

The Flight Log uses cool slate contribution tiles, amber activity highlights and
a gold plane on navy in dark mode. Light mode uses slate tiles and a red plane
on ivory. Its workflow publishes to `output-midnight-terminal`, leaving the
approved version's `output-boarding` files unchanged. Daily refresh begins only
after the selected workflow is merged into the default branch.

Rebuild the profile with `python scripts/build_boarding_readme.py` after installing
`scripts/requirements-boarding.txt`. Flight Log generation uses
`scripts/build_flight_log.py` and only the Python standard library. The original
boarding-pass implementation notes remain in `docs/boarding-pass-design.md`;
this file records the palette-specific differences.
