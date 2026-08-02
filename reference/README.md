# URM Reference-Sample Library

Pinned, source-verified reference repositories and specifications for the
open-standard browser 3D educational game project (WebGL 2.0 + WebAssembly
runtime, [glTF 2.0 / ISO-IEC 12113:2022](https://www.iso.org/standard/83990.html)
interchange, Godot 4.7 desktop authoring lane).

Every `repo_url` and `ref` (tag or commit SHA) in [`MANIFEST.json`](./MANIFEST.json)
was checked live against the GitHub API (`gh api repos/OWNER/NAME` /
`.../tags` / `.../git/refs/tags/<tag>`) or fetched directly. No ref in this
library was invented. Use [`fetch_reference.sh`](./fetch_reference.sh) to
shallow-clone the git-hosted entries — **do not run it blind**, several
repos are large; read the header comment and use `--small` if disk is
constrained.

## Manifest

| ID | Name | Category | Licence | Ref | Why |
|---|---|---|---|---|---|
| REF-01 | [glTF](https://github.com/KhronosGroup/glTF) | glTF specification | Other (Khronos spec licence) | `77b44be` | Normative schema/text defining every glTF 2.0 object your exporter and loader must agree on. |
| REF-02 | [glTF-Sample-Assets](https://github.com/KhronosGroup/glTF-Sample-Assets) | glTF sample assets | Mixed per-asset (CC0/CC-BY/CC-BY-SA) | `2bac6f8` | Feature-test corpus (morph targets, skinning, KTX2, sparse accessors) for loader conformance testing. |
| REF-03 | [glTF-Sample-Viewer](https://github.com/KhronosGroup/glTF-Sample-Viewer) | glTF sample viewer | Apache-2.0 | `v1.0.10` | Reference WebGL2 PBR shader implementation to sanity-check your renderer's material output. |
| REF-04 | [glTF-Validator](https://github.com/KhronosGroup/glTF-Validator) | glTF validation tooling | Apache-2.0 | `2.0.0-dev.3.10` | CI-friendly conformance checker to reject malformed `.glb` before it reaches the runtime. |
| REF-05 | [KTX-Software](https://github.com/KhronosGroup/KTX-Software) | KTX2 texture tooling | Apache-2.0 (+ bundled components) | `v4.4.0` | `toktx`/`ktx2check` reference tools for Basis Universal/UASTC texture compression. |
| REF-06 | [glTF-Blender-IO](https://github.com/KhronosGroup/glTF-Blender-IO) | Blender export pipeline | Apache-2.0 | `v4.2.3` | Source of Blender's glTF exporter — shows exactly which DCC features map to glTF and which don't. |
| REF-07 | [three.js](https://github.com/mrdoob/three.js) | Browser 3D runtime | MIT | `r185` | Second independent glTF loader implementation plus WebGL2 renderer-state patterns. |
| REF-08 | [Babylon.js](https://github.com/BabylonJS/Babylon.js) | Browser 3D runtime | Apache-2.0 | `9.19.0` | Built-in scene optimizer and glTF loader — contrast case for scene-budget and camera-rig patterns. |
| REF-09 | [PlayCanvas engine](https://github.com/playcanvas/engine) | Browser 3D runtime | MIT | `v2.21.3` | Lean, minimal scene-graph implementation (`graph-node.js`) to benchmark against. |
| REF-10 | [godot-demo-projects: 3d/platformer](https://github.com/godotengine/godot-demo-projects) | Godot official demo | MIT | `4652e17` | Official third-person platformer with `CharacterBody3D` movement + follow camera. |
| REF-11 | [godot-demo-projects: rigidbody/kinematic character](https://github.com/godotengine/godot-demo-projects) | Godot official demo | MIT | `4652e17` | Contrasts physics-driven vs. kinematic character controllers in the same engine version. |
| REF-12 | [Godot engine (4.7.1-stable)](https://github.com/godotengine/godot) | Godot authoring lane | MIT | `4.7.1-stable` | Pinned engine source for reproducible export builds and GLES3/Vulkan→WebGL2 behaviour checks. |
| REF-13 | [Godot: Exporting for the Web](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html) | Web export / hosting | CC-BY 3.0 | `stable docs` | Official COOP/COEP header requirements for threaded WebAssembly builds. |
| REF-14 | [MDN: Cross-Origin-Embedder-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy) | Web export / hosting | CC0 1.0 | `current` | Platform-level explanation of why COOP/COEP gate `SharedArrayBuffer` and multithreading. |
| REF-15 | [WCAG 2.2 (W3C Recommendation)](https://www.w3.org/TR/WCAG22/) | Accessibility | W3C Document Licence | `12 Dec 2024 REC` | Current accessibility baseline, ISO-ratified as ISO/IEC 40500:2025. |
| REF-16 | [Godot: Internationalizing games](https://docs.godotengine.org/en/stable/tutorials/i18n/internationalizing_games.html) | Localisation | CC-BY 3.0 | `stable docs` | Concrete i18n workflow: locale vs. language, translation import, pluralisation, pseudolocalisation. |
| REF-17 | [Poly Haven](https://polyhaven.com/license) | Open 3D assets | CC0 1.0 (all assets) | n/a | Zero-restriction PBR textures/models, several already exported as glTF/.glb. |
| REF-18 | [Kenney game assets](https://kenney.nl/assets) | Open 3D assets | CC0 1.0 (verify per-pack) | n/a | Large catalogue of stylised low-poly props/UI kits for prototyping. |
| REF-19 | [ISO/IEC 12113:2022](https://www.iso.org/standard/83990.html) | glTF specification | ISO copyright (catalogue page free) | n/a | Formal ISO identity of glTF 2.0 for procurement/compliance references. |

## What to actually read first

For an enterprise architect coming in cold, read these five in order before
touching anything else:

1. **[glTF](https://github.com/KhronosGroup/glTF) (REF-01)** — Read the
   schema and normative text first. Every downstream decision (exporter
   behaviour, runtime loader, texture packing) is a consequence of this
   document; skipping it means re-deriving semantics from engine source
   code later, which is slower and error-prone.
2. **[Godot: Exporting for the Web](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html) (REF-13)** —
   Read this before writing any hosting configuration. The COOP/COEP header
   requirement is a hard platform constraint, not an optional optimisation,
   and it determines what your CDN/hosting layer must support on day one.
3. **[glTF-Sample-Viewer](https://github.com/KhronosGroup/glTF-Sample-Viewer) (REF-03)** —
   Once the spec is understood, this is the fastest way to see a
   spec-compliant WebGL2 PBR renderer in working code, useful as a
   correctness oracle for your own runtime's shader output.
4. **[godot-demo-projects: 3d/platformer](https://github.com/godotengine/godot-demo-projects) (REF-10)** —
   The authoring-side reference for camera-relative movement and camera rig
   design; study this before designing your own character controller so the
   desktop-authored behaviour and the browser runtime behaviour do not
   diverge.
5. **[glTF-Blender-IO](https://github.com/KhronosGroup/glTF-Blender-IO) (REF-06)** —
   Read this if any art comes from Blender rather than being authored
   directly in Godot; it documents exactly which materials, armatures, and
   shader setups survive the round-trip to glTF and which are silently
   dropped, which otherwise surfaces as a confusing runtime bug much later.

## Licence hazards

- **Non-permissive / non-SPDX licences.** [glTF](https://github.com/KhronosGroup/glTF) (REF-01) and
  [KTX-Software](https://github.com/KhronosGroup/KTX-Software) (REF-05) both report as GitHub licence
  key `other` / `NOASSERTION` rather than a standard SPDX licence — read
  each repo's own `LICENSE.md` before redistributing spec text or bundled
  third-party components; KTX-Software in particular bundles several
  third-party libraries each under their own terms.
- **Copyleft-adjacent licence in the runtime set.** [Babylon.js](https://github.com/BabylonJS/Babylon.js) (REF-08)
  is Apache-2.0, which carries a patent-grant clause and NOTICE-file
  propagation requirement that [three.js](https://github.com/mrdoob/three.js) (REF-07, MIT) and
  [PlayCanvas engine](https://github.com/playcanvas/engine) (REF-09, MIT) do not — if the two-lane
  engine strategy (URM 11.2) ever mixes runtime code from more than one of
  these, track NOTICE-file obligations separately per engine.
- **Asset licences differ from code licences — this is the biggest trap.**
  [glTF-Sample-Assets](https://github.com/KhronosGroup/glTF-Sample-Assets) (REF-02) has **no single
  repository-wide licence**: each sample model carries its own `license.txt`
  (a mix of CC0, CC-BY, and CC-BY-SA). CC-BY-SA in particular is a
  share-alike licence — if any of those specific models are shipped inside
  the actual game (rather than used only for internal loader testing),
  attribution and share-alike obligations attach per-model. Treat REF-02 as
  test fixtures only unless you have individually checked the licence of
  each model you intend to ship.
- **Kenney packs are "verify per-pack."** [Kenney game assets](https://kenney.nl/assets) (REF-18) are
  overwhelmingly CC0, but Kenney occasionally bundles a font with its own
  separate licence inside a pack — check the specific pack's licence file,
  don't assume the site-wide CC0 statement covers every byte in every ZIP.
- **W3C and ISO documents are look-but-don't-relicense.** [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
  (REF-15) is free to read and cite under the W3C Document Licence but is
  not a permissive open-source licence for redistribution/modification of
  the spec text itself; the [ISO/IEC 12113:2022 catalogue record](https://www.iso.org/standard/83990.html)
  (REF-19) is similarly free to view as a catalogue page, but the full
  ISO-typeset PDF is normally paywalled — use the free
  [Khronos glTF GitHub text](https://github.com/KhronosGroup/glTF) (REF-01) as the working copy
  of the identical normative content instead of purchasing the ISO PDF.
- **Godot documentation pages** ([REF-13](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html),
  [REF-16](https://docs.godotengine.org/en/stable/tutorials/i18n/internationalizing_games.html)) are CC-BY 3.0 —
  permissive but attribution-bearing if excerpts are reproduced in internal
  documentation.
