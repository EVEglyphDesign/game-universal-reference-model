#!/usr/bin/env python3
"""Render EgD-URM-001 from tools/model.py into JSON, CSV and the blueprint Markdown.

One source of truth, many renderings. Fields are deliberately repeated across
outputs so that each numbered section can be mapped into an external reference
model without re-deriving anything.
"""
import csv, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import DOMAINS, WIREFRAMES, PREFIX, rows  # noqa: E402

ROOT = "/home/user/workspace/urm"
TOGAF = {"B": "Business", "D": "Data", "A": "Application", "T": "Technology", "": ""}

# ---------------------------------------------------------------- JSON
R = rows()
meta = {
    "document_id": "EgD-URM-001",
    "key_id": "EgD-KEY-2026-07",
    "title": "Game Universal Reference Model",
    "version": "1.0",
    "status": "blueprint — for review and approval",
    "numbering": "L1 = domain (n), L2 = capability (n.n). Section numbers are stable "
                 "identifiers and are never reused or renumbered once approved.",
    "crosswalk_rule": "One section may map to many external model nodes. Repeating a "
                      "field into several target models is expected, not a defect.",
    "domains": len(DOMAINS),
    "capabilities": sum(1 for r in R if r["level"] == 2),
}
with open(f"{ROOT}/model/EgD-URM-001.json", "w") as f:
    json.dump({"meta": meta, "sections": R, "wireframes":
               [{"id": w[0], "title": w[1], "implements": w[2]} for w in WIREFRAMES]},
              f, indent=2)

# ---------------------------------------------------------------- CSV crosswalk
# Blank columns on the right are the mapping surface. Fill one row per target model.
with open(f"{ROOT}/model/EgD-URM-001-crosswalk.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["urm_id", "level", "section", "title", "statement", "togaf_domain",
                "standard", "internal_source", "status",
                "map_epic_section", "map_togaf_artifact", "map_apqc_pcf",
                "map_iso", "map_local_1", "map_local_2", "notes"])
    for r in R:
        w.writerow([r["id"], r["level"], r["num"], r["title"], r["statement"],
                    TOGAF.get(r["togaf"], r["togaf"]), r["standard"],
                    r["source"], r["status"], "", "", "", "", "", "", ""])

# ---------------------------------------------------------------- Markdown
L = []
A = L.append
A("# Game Universal Reference Model")
A("")
A("## What this is, and what it is not")
A("")
A("This is the blueprint layer only — the L0 document. It says what the game is made of "
  "and numbers every part so the parts can be argued about separately. It does not say "
  "how any part is built. That is the technical design, and it comes after you approve "
  "these numbers.")
A("")
A("The rule is the one you used at Epic: the blueprint carries the numbers, the technical "
  "design refers to them, and every layer below inherits them unchanged. Nothing downstream "
  "invents its own numbering.")
A("")
A(f"There are **{meta['domains']} domains** and **{meta['capabilities']} capabilities**. "
  "Every capability is one sentence. If a capability needs a paragraph, it is two "
  "capabilities and I have got it wrong.")
A("")
A("### How to read the numbers")
A("")
A("| Level | Form | Meaning | Example |")
A("| --- | --- | --- | --- |")
A("| L1 | `n` | Domain. A part of the system that can be owned by one person. | `7` Interaction and Control |")
A("| L2 | `n.n` | Capability. One testable statement. | `7.2` Camera-relative movement |")
A("| L3 | `n.n.n` | Component. Added in the technical design, not here. | `7.2.1` Input vector rotation |")
A("")
A("Numbers are stable identifiers. Once you approve them they are never reused and never "
  "renumbered — if a capability dies it is marked withdrawn and its number stays retired. "
  "That is what makes them safe to reference from a contract, a test plan or another "
  "architecture.")
A("")
A("### The crosswalk rule")
A("")
A("Each section carries a row in a crosswalk sheet with empty columns for your Epic "
  "numbering, TOGAF artefacts, APQC process classifications, ISO references and two "
  "free local columns. One section may map to many nodes in a target model, and one "
  "target node may receive many sections. Repeating a field into several models is "
  "expected and is not duplication — it is the mapping.")
A("")
A("Where two external models disagree about shape, this model holds the simpler shape "
  "and maps upward. That is the lowest-common-denominator rule, section 13.5, and it is "
  "the reason the model is deliberately shallow at L1.")
A("")

A("## The decision you need to make first")
A("")
A("Research turned up one constraint that changes the architecture, so it goes at the "
  "front rather than buried in section 11.")
A("")
A("The desktop engine lane and the browser lane do not render the same way. Godot 4 can "
  "only target WebGL 2.0 on the web, using its Compatibility renderer; the Forward+ and "
  "Mobile renderers are not available in a browser because WebGPU support is not "
  "implemented, per the "
  "[Godot web export documentation](https://docs.godotengine.org/en/latest/tutorials/export/exporting_for_web.html). "
  "The starter project I built you yesterday uses Forward+. That is fine for a desktop "
  "build and wrong for a URL.")
A("")
A("There are three honest options.")
A("")
A("| Option | What you get | What it costs |")
A("| --- | --- | --- |")
A("| A. Godot, web export | One engine, one codebase, desktop and browser. Editor, scene tools, animation, physics all included. | Compatibility renderer only, so simpler lighting. Roughly 25-40 MB of runtime downloaded before the game starts. |")
A("| B. Browser-native runtime | Small download, instant start, renders in any tab, sits naturally inside the parish portal. | No editor. Scenes must be authored elsewhere and imported. More code written by hand. |")
A("| C. Two lanes, glTF as the seam | Author in a full desktop engine, deliver in the browser, with glTF 2.0 as the contract between them. Neither lane owns the content. | Two runtimes to maintain. The seam has to be disciplined. |")
A("")
A("**The model recommends C**, and section 11.2 records it as a decision rather than a "
  "fact so you can overturn it. The reason is that C is the only option where the asset "
  "layer survives the engine. If a runtime is abandoned, or the browser gets WebGPU and "
  "the calculus changes, glTF scenes and Blender sources carry forward untouched. Options "
  "A and B both make the engine the owner of your content, and you have spent this whole "
  "year making sure nothing owns your content.")
A("")
A("I have already proved the seam works. The verified Godot world from the starter project "
  "exported to a 125 KB binary glTF file — 29 nodes, 8 meshes, 5 materials — and it now "
  "loads and runs in a browser. That is the live surface linked from the blueprint page.")
A("")

A("## The standards this rests on")
A("")
A("| Layer | Standard | Status |")
A("| --- | --- | --- |")
A("| 3D asset and scene interchange | glTF 2.0, binary `.glb` | Published as [ISO/IEC 12113:2022](https://www.khronos.org/news/press/khronos-gltf-2.0-released-as-an-iso-iec-international-standard) by [Khronos](https://www.khronos.org/gltf/) |")
A("| Browser rendering | WebGL 2.0 | Web standard, universally available |")
A("| Browser execution | WebAssembly | Web standard |")
A("| Texture container | KTX 2.0 with Basis Universal | Khronos, optional extension |")
A("| Accessibility | WCAG 2.2 | W3C recommendation |")
A("| Document control | ISO 8601 timestamps, SHA-256 hashes | In force in this document |")
A("")
A("A note on currency, because it affects a choice you may be asked about later. "
  "[Phoronix reported](https://www.phoronix.com/news/Khronos-glTF-2.1-Released) that "
  "Khronos released glTF 2.1 on 11 June 2026, adding multi-file scene composition, "
  "embedded thumbnails and a 64-bit container. I could not confirm that on the Khronos "
  "landing page, which still describes 2.0 as current, so I have not built the model on "
  "2.1. Section 10.1 anchors on glTF 2.0 because it is the ISO-published version and the "
  "one every tool already reads. If 2.1 is confirmed, it is backward compatible and the "
  "section text changes, not the architecture.")
A("")

A("## The model")
A("")
A("Status values: **Canon** is decided and in force. **Proposed** needs your approval. "
  "**Decision** is a fork I have recommended but not closed. **Open** is unresolved and "
  "waiting on information.")
A("")
for num, title, blurb, items in DOMAINS:
    A(f"### {num}. {title}")
    A("")
    A(blurb)
    A("")
    A("| ID | Capability | Statement | Layer | Status |")
    A("| --- | --- | --- | --- | --- |")
    for n, t, s, tg, std, src, st in items:
        layer = TOGAF.get(tg, tg)
        if std:
            layer = f"{layer} · {std}"
        A(f"| {n} | {t} | {s} | {layer} | {st} |")
    A("")

A("## Wireframes")
A("")
A("Eight screens. Each one names the capability numbers it implements, so a screen can be "
  "reviewed against the model rather than against taste. They are line drawings on purpose "
  "— arguing about colour before the flow is agreed wastes everybody's time.")
A("")
A("| Screen | Title | Implements |")
A("| --- | --- | --- |")
for wid, wt, imp in WIREFRAMES:
    A(f"| {wid} | {wt} | {imp} |")
A("")
A("The screens are published on the blueprint page at full size.")
A("")

A("## What I need from you")
A("")
A("Five things, in this order. Everything downstream waits on the first three.")
A("")
A("1. **Close the engine decision.** Section 11.2, options A, B or C above.")
A("2. **Approve or renumber the L1 domains.** Fifteen is a judgement call. If your Epic "
  "convention wants a different top level, now is the cheap moment to change it — after "
  "the technical design it is not.")
A("3. **Rule on the Proposed rows.** There are proposals across the model that need a yes, "
  "a no, or a rewrite.")
A("4. **Name the first chapter to build.** Chapter 2, What We Kept, already exists as a "
  "trilingual puzzle. Chapter 3, Four Lost Days, has the calendar mechanic. Either could "
  "be the first 3D chapter, and the choice changes what gets built first.")
A("5. **Confirm the product title.** Section 1.4 is open. PAIX names the parishioner "
  "surface, and the earlier note that a game title carries mark exposure the studio name "
  "does not still stands.")
A("")

A("## What happens after approval")
A("")
A("The technical design inherits these numbers and adds the L3 layer. Each L2 capability "
  "gets components, interfaces, data structures and acceptance tests, all numbered beneath "
  "its parent. Nothing in the technical design may exist without a parent number here — if "
  "something needs to be built that has no number, the blueprint was wrong and comes back "
  "for amendment rather than being quietly extended.")
A("")
A("That constraint is the whole value of doing it this way. It is also the part that will "
  "irritate whoever writes the technical design, which is how you know it is working.")
A("")

A("## Sources")
A("")
A("Standards: [Khronos glTF](https://www.khronos.org/gltf/), the "
  "[glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html), and "
  "[glTF 2.0 as ISO/IEC 12113:2022](https://www.khronos.org/news/press/khronos-gltf-2.0-released-as-an-iso-iec-international-standard). "
  "Engine constraints: [Exporting for the Web](https://docs.godotengine.org/en/latest/tutorials/export/exporting_for_web.html), "
  "Godot documentation. glTF 2.1 report: "
  "[Phoronix, 11 June 2026](https://www.phoronix.com/news/Khronos-glTF-2.1-Released), "
  "unconfirmed against Khronos at time of issue.")
A("")
A("Internal canon: capability statements are drawn from the EVEglyphDesign knowledge record "
  "for the PAIX educational game, EVE Hyperloop, EVE Glyph Education, the Acadian Heritage "
  "Record, the Enoch Convergence research boundary, Starship Academy, the "
  "[Executive Boot Contract](https://github.com/EVEglyphDesign/eve-glyph-boot-contract), "
  "and the measured behaviour of "
  "[EgD-GDS-001](https://eveglyphdesign.github.io/godot-action-adventure-starter/), the "
  "verified Godot starter. The `internal_source` column of the crosswalk sheet records the "
  "origin of every row.")

open(f"{ROOT}/model/EgD-URM-001.md", "w").write("\n".join(L) + "\n")

print(f"domains {meta['domains']}  capabilities {meta['capabilities']}  "
      f"rows {len(R)}  md_lines {len(L)}")
