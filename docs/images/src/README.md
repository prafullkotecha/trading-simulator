# Diagram sources

The scripts and pages here draw the diagrams in `docs/images`. Change a source, run it, and commit the source with its PNG.

| Output | Source | Run |
| --- | --- | --- |
| `lessons/lesson-I-1.png` to `lesson-I-6.png` | `lesson_diagrams_investing.py` | `python3 docs/images/src/lesson_diagrams_investing.py` |
| `lessons/coverage-map.png` | `coverage_map.py`, which reads the Coverage by lesson table in `docs/lesson-plan.md` | `python3 docs/images/src/coverage_map.py` |
| `design-colors.png`, `design-app-map.png`, `design-wireframes.png`, `implementation-phases.png`, `implementation-ownership.png`, `implementation-pr-flow.png` | the `.html` file of the same name, with `base.css` | `node docs/images/src/render.js` (all), or add names to render some |

The Python scripts need matplotlib. `render.js` needs Playwright with Chromium and the Inter font installed, and writes each PNG at twice its page size.

Not covered: the 38 level diagrams (`lessons/lesson-1-1.png` to `lesson-4-6.png`) and `implementation-dependencies.png` were drawn before these sources were kept. Nothing in the Nov 28 review changed what they show, so they were left as they were.
