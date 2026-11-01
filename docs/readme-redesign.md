# README design and rollback

The neo-brutalist draft lives on `design/neo-brutalist-readme`.
The original profile is preserved on `backup/readme-before-neo-brutalist-2026-11-01`
at commit `40a82ce52d20dd3bbea35508be14148a8d046890`.

Only the default branch's README appears on the GitHub profile. Reviewing this
branch does not publish the redesign to the profile.

## Graphics

Run `python scripts/build_readme.py` to rebuild `assets/loud/` and `README.md`.
The generator uses only the Python standard library. It preserves the original
project details from the baseline commit, which must be available in local Git
history (use a normal clone rather than a shallow clone).

The SVGs use system font fallbacks and contain no external resources, scripts,
or embedded HTML. Each featured card is a separate repository link. The stack
and project cards have mobile variants selected through `<picture>` elements.
Project descriptions and links are also available as native expandable text.
The existing contribution-snake workflow and original graphic assets are kept.

## Restore the original profile after merging

From an up-to-date, clean checkout, these commands restore the original README
without rewriting history. The original assets are still in the repository.
Run this only when you want the original profile published again:

```sh
git fetch origin
git switch main
git pull --ff-only origin main
git restore --source=origin/backup/readme-before-neo-brutalist-2026-11-01 -- README.md
git add README.md
git commit -m "Restore original profile README"
git push origin main
```

Before merging, rollback requires no file changes: leave the redesign branch
unmerged and the live profile remains on the original design.
