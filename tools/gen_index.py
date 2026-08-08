#!/usr/bin/env python3
"""Render the public blueprint page from the model. Canon palette and typography."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import DOMAINS  # noqa

TOGAF = {"B": "Business", "D": "Data", "A": "Application", "T": "Technology", "": ""}


def layer(tg, std):
    v = TOGAF.get(tg, tg)
    return f"{v} &middot; {std}" if std else v

ROOT = "/home/user/workspace/urm"
D = json.load(open(f"{ROOT}/model/EgD-URM-001.json"))
REF = json.load(open(f"{ROOT}/reference/MANIFEST.json"))
WF_FILES = {"W1": "w1-entry", "W2": "w2-safety", "W3": "w3-chapters", "W4": "w4-hud",
            "W5": "w5-standup", "W6": "w6-twinquest", "W7": "w7-village",
            "W8": "w8-guardian"}
PDF = "blueprint/EVEglyphDesign_Game_Universal_Reference_Model.pdf"
ASSESS = "blueprint/EVEglyphDesign_GenAI_Library_Fit_Assessment.pdf"

dom_html = []
for num, title, blurb, items in DOMAINS:
    rows = "".join(
        f'<tr><td class="id">{n}</td><td class="cap">{t}</td><td>{s}</td>'
        f'<td class="mu">{layer(tg, std)}</td><td><span class="st st-{st.lower()}">{st}</span></td></tr>'
        for n, t, s, tg, std, src, st in items)
    dom_html.append(
        f'<section class="dom" id="s{num}"><h3><span class="n">{num}</span>{title}</h3>'
        f'<p class="blurb">{blurb}</p>'
        f'<div class="tw"><table><thead><tr><th>ID</th><th>Capability</th><th>Statement</th>'
        f'<th>Layer</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div></section>')

wf_html = "".join(
    f'<figure><a href="wireframes/{WF_FILES[w["id"]]}.svg">'
    f'<img src="wireframes/{WF_FILES[w["id"]]}.svg" alt="{w["title"]} wireframe" loading="lazy"></a>'
    f'<figcaption><b>{w["id"]}</b> {w["title"]}<span class="mu"> · implements {w["implements"]}</span>'
    f'</figcaption></figure>' for w in D["wireframes"])

ref_html = "".join(
    f'<tr><td class="id">{e["id"]}</td>'
    f'<td class="cap"><a href="{e["repo_url"]}">{e["name"]}</a></td>'
    f'<td class="mu">{e["category"]}</td><td><code>{e["ref"]}</code></td>'
    f'<td class="mu">{e["licence"].split("(")[0].strip()}</td></tr>' for e in REF)

nav = " · ".join(f'<a href="#s{n}">{n}</a>' for n, _, _, _ in DOMAINS)

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Game Universal Reference Model — EgD-URM-001 · EVEglyphDesign</title>
<meta name="description" content="A numbered blueprint for a 3D educational game delivered at a URL on open standards.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--cream:#fdfaf4;--cream2:#f7f2e7;--ink:#1a1a1a;--line:#e7e1d3;--mute:#6b665c;--orng:#e87722}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--cream);color:var(--ink);
 font:400 17px/1.62 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1060px;margin:0 auto;padding:0 26px}}
a{{color:var(--ink);text-decoration-color:var(--orng);text-underline-offset:3px}}
a:hover{{color:var(--orng)}}
header{{border-bottom:1px solid var(--line);padding:14px 0;position:sticky;top:0;
 background:rgba(253,250,244,.94);z-index:20;font-size:13px}}
header .wrap{{display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}}
header b{{font-weight:700;letter-spacing:.02em}}
header .mu{{color:var(--mute)}}
.hero{{padding:74px 0 48px;border-bottom:1px solid var(--line)}}
.eyebrow{{color:var(--orng);font:600 11px/1 Inter;letter-spacing:.30em;text-transform:uppercase}}
h1{{font:700 clamp(38px,6.4vw,66px)/1.03 Fraunces,Georgia,serif;margin:16px 0 0;letter-spacing:-.018em}}
.rule{{width:88px;height:3px;background:var(--orng);margin:22px 0 24px}}
.lede{{font-size:20px;line-height:1.55;max-width:58ch;color:#2c2a26}}
.meta{{margin-top:26px;display:flex;flex-wrap:wrap;gap:8px 26px;font-size:13px;color:var(--mute)}}
.meta b{{color:var(--ink);font-weight:600}}
.cta{{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}}
.btn{{display:inline-block;padding:12px 20px;border:1.4px solid var(--ink);border-radius:2px;
 font:600 14px Inter;text-decoration:none;background:transparent}}
.btn:hover{{background:var(--ink);color:var(--cream)}}
.btn.pri{{background:var(--orng);border-color:var(--orng);color:#fff}}
.btn.pri:hover{{background:var(--ink);border-color:var(--ink);color:#fff}}
section.blk{{padding:52px 0;border-bottom:1px solid var(--line)}}
h2{{font:600 clamp(26px,3.4vw,36px)/1.15 Fraunces,Georgia,serif;margin:0 0 10px;letter-spacing:-.012em}}
h3{{font:600 22px/1.25 Fraunces,Georgia,serif;margin:34px 0 4px}}
h3 .n{{color:var(--orng);font-family:Inter;font-weight:700;font-size:14px;
 display:inline-block;min-width:34px}}
p{{max-width:70ch}}
.mu{{color:var(--mute)}}
.blurb{{color:var(--mute);margin:2px 0 12px;font-size:15px}}
.tw{{overflow-x:auto;border:1px solid var(--line);border-radius:3px;background:var(--cream2)}}
table{{border-collapse:collapse;width:100%;min-width:660px;font-size:14px;background:transparent}}
th{{text-align:left;font:600 10.5px Inter;letter-spacing:.09em;text-transform:uppercase;
 color:var(--mute);padding:10px 12px;border-bottom:1.6px solid var(--orng);white-space:nowrap}}
td{{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top;line-height:1.45}}
tbody tr:nth-child(odd){{background:var(--cream)}}
tbody tr:last-child td{{border-bottom:0}}
td.id{{font-weight:700;white-space:nowrap;font-variant-numeric:tabular-nums}}
td.cap{{font-weight:600;min-width:150px}}
code{{font:13px/1.4 ui-monospace,Menlo,Consolas,monospace;background:var(--cream);
 border:1px solid var(--line);border-radius:2px;padding:1px 5px}}
.st{{font:600 11px Inter;letter-spacing:.05em;text-transform:uppercase;white-space:nowrap;
 padding:3px 7px;border-radius:2px;border:1px solid var(--line);color:var(--mute)}}
.st-canon{{border-color:var(--line)}}
.st-proposed{{border-color:var(--orng);color:var(--orng)}}
.st-decision{{background:var(--orng);border-color:var(--orng);color:#fff}}
.st-open{{border-color:var(--ink);color:var(--ink)}}
.nav{{font-size:13px;color:var(--mute);margin:18px 0 6px;line-height:2.1}}
.nav a{{display:inline-block;min-width:26px;text-align:center;border:1px solid var(--line);
 border-radius:2px;padding:2px 7px;text-decoration:none;background:var(--cream2)}}
.nav a:hover{{border-color:var(--orng)}}
.grid{{display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));margin-top:26px}}
figure{{margin:0;border:1px solid var(--line);border-radius:3px;overflow:hidden;background:var(--cream2)}}
figure img{{display:block;width:100%;height:auto;background:var(--cream)}}
figcaption{{padding:10px 13px;font-size:13.5px;border-top:1px solid var(--line)}}
.cards{{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(228px,1fr));margin-top:24px}}
.card{{border:1px solid var(--line);border-left:3px solid var(--orng);border-radius:3px;
 padding:16px 18px;background:var(--cream2)}}
.card h4{{margin:0 0 6px;font:600 16px Inter}}
.card p{{margin:0;font-size:14px;color:var(--mute)}}
ol{{max-width:70ch}} ol li{{margin-bottom:9px}}
footer{{padding:38px 0 60px;font-size:12.5px;color:var(--mute)}}
footer p{{margin:5px 0}}
@media(max-width:640px){{.hero{{padding:46px 0 34px}}section.blk{{padding:38px 0}}}}
</style></head><body>

<header><div class="wrap">
<b>EVEglyphDesign</b>
<span class="mu">EgD-URM-001</span>
<span class="mu">&middot; Blueprint L0</span>
<span style="flex:1"></span>
<a href="{PDF}">PDF</a>
<a href="play/">Rendering demo</a>
<a href="#wireframes">Wireframes</a>
<a href="#model">Model</a>
<a href="#reference">Reference</a>
</div></header>

<div class="hero"><div class="wrap">
<div class="eyebrow">Blueprint &middot; for review and approval</div>
<h1>Game Universal<br>Reference Model</h1>
<div class="rule"></div>
<p class="lede">A numbered blueprint for a 3D educational game delivered at a URL on open
standards &mdash; structured so every section maps outward to other reference models and
enterprise architectures.</p>
<div class="meta">
<span><b>Document</b> EgD-URM-001</span>
<span><b>Key</b> EgD-KEY-2026-07</span>
<span><b>Domains</b> {D['meta']['domains']}</span>
<span><b>Capabilities</b> {D['meta']['capabilities']}</span>
<span><b>Version</b> {D['meta']['version']}</span>
</div>
<div class="cta">
<a class="btn pri" href="play/">Open the rendering demo &rarr;</a>
<a class="btn" href="{PDF}">Read the blueprint (PDF)</a>
<a class="btn" href="{ASSESS}">GenAI library fit assessment \u2014 EgD-URM-002 (PDF)</a>
<a class="btn" href="model/EgD-URM-001-crosswalk.csv">Crosswalk sheet (CSV)</a>
</div>
</div></div>

<section class="blk"><div class="wrap">
<h2>The proof, first</h2>
<p>A world authored in Godot 4.7, exported to a 125&nbsp;KB binary glTF file &mdash; 29 nodes,
8 meshes, 5 materials &mdash; and running in a browser tab with no plugin and no install.
That file is the seam the whole architecture rests on: the engine can be replaced, the
scene cannot be taken away.</p>
<div class="cards">
<div class="card"><h4>glTF 2.0</h4><p>ISO/IEC 12113:2022. The interchange contract between the
authoring lane and the delivery lane.</p></div>
<div class="card"><h4>WebGL 2.0</h4><p>The only renderer Godot can target on the web, and the
one every browser already has.</p></div>
<div class="card"><h4>Numbered sections</h4><p>Stable identifiers, never reused, never
renumbered. Contracts and test plans can cite them.</p></div>
<div class="card"><h4>Crosswalk by design</h4><p>One section may map to many external nodes.
Repeating a field into several models is the mapping, not duplication.</p></div>
</div>
</div></section>

<section class="blk" id="model"><div class="wrap">
<h2>The model</h2>
<p><b>L1</b> is a domain, numbered <code>n</code>. <b>L2</b> is a capability, numbered
<code>n.n</code>, and is always one testable sentence. <b>L3</b> is a component and belongs to
the technical design, not here. Status: <span class="st st-canon">Canon</span> is in force,
<span class="st st-proposed">Proposed</span> needs a ruling,
<span class="st st-decision">Decision</span> is a recommended but open fork,
<span class="st st-open">Open</span> is waiting on information.</p>
<div class="nav">{nav}</div>
{''.join(dom_html)}
</div></section>

<section class="blk" id="wireframes"><div class="wrap">
<h2>Wireframes</h2>
<p>Eight screens. Each names the capability numbers it implements, so a screen can be reviewed
against the model rather than against taste. Line drawings on purpose &mdash; arguing about
colour before the flow is agreed wastes everybody's time.</p>
<div class="grid">{wf_html}</div>
</div></section>

<section class="blk" id="reference"><div class="wrap">
<h2>Reference-sample library</h2>
<p>{len(REF)} pinned repositories and specifications, each checked live against its host
before it was written down. Nothing here is a guessed tag.
See <a href="https://github.com/EVEglyphDesign/game-universal-reference-model/blob/main/reference/README.md">the library README</a>
for the fetch script and size warnings.</p>
<div class="tw"><table><thead><tr><th>ID</th><th>Source</th><th>Category</th><th>Pinned ref</th>
<th>Licence</th></tr></thead><tbody>{ref_html}</tbody></table></div>
</div></section>

<section class="blk"><div class="wrap">
<h2>What happens next</h2>
<ol>
<li><b>Close the engine decision</b> &mdash; section 11.2. Godot web export, a browser-native
runtime, or two lanes with glTF as the seam.</li>
<li><b>Approve or renumber the L1 domains.</b> Fifteen is a judgement call and this is the cheap
moment to change it.</li>
<li><b>Rule on the Proposed rows.</b> Each needs a yes, a no, or a rewrite.</li>
<li><b>Name the first chapter to build.</b> What We Kept, or Four Lost Days.</li>
<li><b>Confirm the product title</b> &mdash; section 1.4 is open.</li>
</ol>
<p>The technical design then inherits these numbers and adds L3. Nothing may be built that has
no parent number here; if something needs to be, the blueprint was wrong and comes back for
amendment rather than being quietly extended.</p>
</div></section>

<footer><div class="wrap">
<p>&copy; 2026 EVEglyphDesign. All rights reserved. Controlled copy.
Document <b>EgD-URM-001</b> &middot; Key <b>EgD-KEY-2026-07</b>.</p>
<p>Standards: <a href="https://www.khronos.org/gltf/">Khronos glTF</a> &middot;
<a href="https://www.khronos.org/news/press/khronos-gltf-2.0-released-as-an-iso-iec-international-standard">glTF 2.0 as ISO/IEC 12113:2022</a> &middot;
<a href="https://docs.godotengine.org/en/latest/tutorials/export/exporting_for_web.html">Godot web export constraints</a>.
Related: <a href="https://eveglyphdesign.github.io/godot-action-adventure-starter/">EgD-GDS-001 starter</a> &middot;
<a href="https://eveglyphdesign.github.io/eve-glyph-boot-contract/">Executive Boot Contract</a>.</p>
<p><i>Pour le bien-&ecirc;tre du peuple.</i></p>
</div></footer>
</body></html>
"""
open(f"{ROOT}/docs/index.html", "w").write(HTML)
print("index.html", len(HTML), "bytes ·", D["meta"]["capabilities"], "capabilities ·",
      len(REF), "references ·", len(D["wireframes"]), "wireframes")
