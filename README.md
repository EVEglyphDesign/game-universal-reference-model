# Game Universal Reference Model — EgD-URM-001

The L0 blueprint for an EVEglyphDesign 3D educational game delivered at a URL on open
standards, numbered so every section maps outward to other reference models and
enterprise architectures.

- Public page — <https://eveglyphdesign.github.io/game-universal-reference-model/>
- Live 3D proof — <https://eveglyphdesign.github.io/game-universal-reference-model/play/>
- Controlled PDF — [`docs/blueprint/EVEglyphDesign_Game_Universal_Reference_Model.pdf`](docs/blueprint/EVEglyphDesign_Game_Universal_Reference_Model.pdf)

**Status:** blueprint v1.0 — for review and approval. 15 domains, 88 capabilities.

## Assessments

- [`EgD-URM-002` — GenAI Library Fit Assessment](docs/blueprint/EVEglyphDesign_GenAI_Library_Fit_Assessment.pdf)
  — ten generative-AI Python libraries tested against four admission gates derived from this
  model's own capability numbers. Two accepted with boundaries, one refused as a canon breach,
  seven declined. Includes five hygiene findings against this repository, two of them live
  defects on the child-facing surface.
  Source: [`model/EgD-URM-002-library-assessment.md`](model/EgD-URM-002-library-assessment.md)

## Numbering

| Level | Form | Meaning |
|---|---|---|
| L1 | `n` | Domain — a part of the system one person can own |
| L2 | `n.n` | Capability — one testable sentence |
| L3 | `n.n.n` | Component — belongs to the technical design, not here |

Numbers are stable identifiers. Once approved they are never reused and never renumbered;
a withdrawn capability keeps its retired number. Nothing in the technical design may exist
without a parent number in this model.

## Crosswalk

`model/EgD-URM-001-crosswalk.csv` carries one row per section with empty columns for Epic
section numbers, TOGAF artefacts, APQC PCF, ISO references and two free local columns. One
section may map to many external nodes and one external node may receive many sections —
repeating a field into several target models is the mapping, not duplication.

## Layout

```
tools/model.py         single source of truth — domains, capabilities, wireframe index
tools/gen_model.py     renders model/ JSON + crosswalk CSV + blueprint Markdown
tools/build_blueprint_pdf.py   renders the controlled PDF (two-pass, page-count stamped)
tools/gen_index.py     renders docs/index.html from the model
tools/gen_wireframes.py  emits the eight SVG screens with overflow/overlap assertions
tools/verify_play.py   headless check of the browser runtime
model/                 rendered model — JSON, crosswalk CSV, Markdown
reference/             19 pinned reference repositories, every ref verified live
wireframes/            W1-W8 source SVG
docs/                  the published surface (GitHub Pages)
docs/play/             browser runtime + world.glb exported from the Godot starter
```

Regenerate everything:

```
python3 tools/gen_wireframes.py
python3 tools/gen_model.py
N=$(python3 tools/build_blueprint_pdf.py | awk '{print $2}') && python3 tools/build_blueprint_pdf.py $N
python3 tools/gen_index.py
```

## Standards

glTF 2.0 / [ISO/IEC 12113:2022](https://www.khronos.org/news/press/khronos-gltf-2.0-released-as-an-iso-iec-international-standard)
for interchange, [WebGL 2.0](https://registry.khronos.org/webgl/specs/latest/2.0/) for
rendering, WebAssembly for execution, KTX 2.0 for textures, WCAG 2.2 for accessibility.
Godot 4 can only target WebGL 2.0 on the web via its Compatibility renderer, per
[Exporting for the Web](https://docs.godotengine.org/en/latest/tutorials/export/exporting_for_web.html) —
this constraint is the reason section 11.2 exists.

## Related

- [EgD-GDS-001 — Godot Action Adventure Starter](https://github.com/EVEglyphDesign/godot-action-adventure-starter)
- [Executive Boot Contract](https://github.com/EVEglyphDesign/eve-glyph-boot-contract)

---

© 2026 EVEglyphDesign. All rights reserved. Controlled copy. Key ID `EgD-KEY-2026-07`.

*Pour le bien-être du peuple.*
