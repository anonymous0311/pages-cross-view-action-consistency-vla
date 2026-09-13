# Action-Flow Consistency Across Views

Research project page for **Action-Flow Consistency Across Views: Scene-Camera Robustness for Flow-Based VLA Policies**.

Public website: https://anonymous0311.github.io/pages-cross-view-action-consistency-vla/

## Content and media

- The text, tables, and seven figures follow `PAPER/ICRA_20260913/main_v6.tex` (September 13, 2026). `static/paper.pdf` is compiled from that source, including its bibliography (8 pages).
- `static/css/project.css` and `static/js/project.js` provide the responsive layout and accessible camera tabs / playback controls. No JavaScript packages, CDN, tracking, or build dependencies are needed.
- `static/videos/Teaser.mp4` is the supplied original. `static/media/teaser.mp4` is its unchanged video stream remuxed with faststart for progressive playback.
- All 33 supplied real-robot clips are represented: 12 comparison clips, 9 recorded-view successes, 12 displaced-view failures. `static/media/manifest.json` maps each browser copy back to its source filename. Originals stay in the local `static/videos/page*` directories; only compressed playback copies are published.
- Camera folder `C1+` uses the paper's label **C2+ (−56°)**, as established by the setup diagram and final results frame in the teaser. The other placements are C0+ (+63°), C0–C1 (+24°), and C1–C2 (−22°). File paths and source filenames are preserved in the manifest.
- Method labels follow the enclosing `page5_comparison` method folders, including where individual filenames use a different recipe token. The examples are illustrative clips and are not claimed to be the same trial. Quantitative claims come from the paper.
- Six existing simulation videos remain available under the simulation results.

## Updating / publishing

This is a static GitHub Pages site. The repository already has the automatic `pages build and deployment` workflow; pushing the site's `main` branch triggers deployment. No separate hosting service is required.

Preview with `python -m http.server 8000`, then open http://localhost:8000/. Run `python scripts/validate_site.py` before publishing. The validation checks local references, video manifests / formats, and the expected paper content. Regenerate compressed robot videos with `python scripts/prepare_media.py` when the original local files are available (requires FFmpeg).

Figures are supplied paper assets, exported to PNG for inline reading, with the original PDF linked for full-resolution access. Original source videos are retained locally. Older video deletions were already present before the redesign.

## Attribution

The repository originated from the [Nerfies website template](https://github.com/nerfies/nerfies.github.io). The previous website credited the template under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The September 2026 page layout and interactions have been rewritten.
