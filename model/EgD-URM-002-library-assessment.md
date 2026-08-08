# Generative-AI Library Fit Assessment

## The short answer

Two of the ten fit. One fits with a hard boundary. Seven do not belong in this repository, and two of the seven would be canon breaches if a contributor wired them in without reading section 2 first.

That is not a criticism of the libraries. It is a statement about what `EgD-URM-001` is. This repository is a **deterministic document-generation toolchain** wrapped around a **static browser-delivered glTF proof**, governed by canon that forbids open-ended generation on the child surface. Python appears here as a build tool, not as a runtime. Nothing this repository publishes executes Python — the reader gets HTML, SVG, JSON, CSV, PDF and a 125 KB `.glb`.

A list of deep-learning frameworks assessed against that is mostly a list of things to decline. The value of the exercise is in *why* each one is declined, because each refusal is a canon number, and each refusal is therefore reusable the next time a contributor arrives with a framework and enthusiasm.

> A dependency is not free because it is free. It is free at install and expensive forever.

## Where the list came from, and what it gets wrong

The source is a social-media carousel titled *10 Python Libraries for Generative AI*, of the kind circulated for engagement rather than architecture. Before assessing fit, three factual corrections, because a controlled document does not inherit errors from its input.

| Claim in the list | Correction |
| --- | --- |
| "Hugging Face" is a library | Hugging Face is a company and a model hub. The libraries are `transformers`, `datasets`, `tokenizers` and others. The list names an organisation and describes one of its packages. |
| Acme is a current option for building RL agents | [Acme](https://github.com/google-deepmind/acme) shows its most recent release as **v0.4.0, 10 February 2022**. Its README claims only that DeepMind uses it internally and that "things may break occasionally." Four years without a release is not a live dependency. |
| Stable Baselines3 is a growth path | [Stable Baselines3](https://github.com/DLR-RM/stable-baselines3) is maintained but its own README states development is "now focused on bug fixes and maintenance." Latest release `v2.7.0`, 25 July 2025. It is stable in the sense of finished, not in the sense of advancing. |

Three of the ten entries — Acme, Stable Baselines3, and by extension the RL framing — concern reinforcement learning. This repository contains no agent that learns from reward. It contains an eight-year-old following a numbered chapter. The list is therefore roughly one-third irrelevant before any canon test is applied.

## The four gates

Any library entering this repository passes all four. These are not new rules; each is an existing capability number restated as an admission test.

| Gate | Derived from | The test |
| --- | --- | --- |
| **A — Determinism** | `2.2` describe before generate, `4.2` fixed-output catechetical path, `8.4` deterministic puzzle state | Does it introduce non-reproducible output into anything a child sees or anything that is assessed? If yes, it is refused on the child surface without exception. |
| **B — Browser weight** | `6.6` browser scene budget, `9.1` renderer profile, `11.2` the two-lane decision | Does it add bytes to the browser lane? A framework that only ever runs on a build machine passes. A framework whose value requires client-side inference fails. |
| **C — Licence posture** | `1.5` licence posture | Permissive, recorded, and — critically — does the *model weight* carry a licence as well as the code? Apache-2.0 code loading a non-commercial checkpoint is a breach dressed as compliance. |
| **D — Durability** | `EgD-BOOT-003` | Can the output be reproduced from `git clone` and nothing else? A dependency reaching a hosted endpoint at render time fails. |

Gate C is the one most often missed. `diffusers` is Apache-2.0. The checkpoints people load with it frequently are not. The licence of the library tells you nothing about the licence of the thing that produced the image, and `1.5` requires "every third-party asset carries a recorded licence."

## The verdict

| # | Library | A | B | C | D | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | TensorFlow | — | fail | pass | pass | **Decline.** No training happens here. Nothing to serve. |
| 2 | PyTorch | — | fail | pass | pass | **Decline.** Roughly 2–3 GB installed to render a CSV. Contradicts the whole thesis. |
| 3 | JAX | — | fail | pass | pass | **Decline.** Actively developed and excellent; solves no problem this repository has. |
| 4 | `transformers` · HF Hub | fail | fail | risk | fail | **Decline on the child surface.** Possible authoring-side, but see LlamaIndex — the index, not the model, is what is wanted. |
| 5 | Diffusers | fail | fail | fail | fail | **Refuse. Canon breach.** Fails all four. Generated imagery on a child surface collides with `2.2`, `2.4` and `3.7`. |
| 6 | Gradio | pass | n/a | pass | cond. | **Accept, internal only.** See below. |
| 7 | Acme | — | fail | pass | fail | **Decline.** Dormant since 2022, and no RL in scope. |
| 8 | Stable Baselines3 | — | fail | pass | pass | **Decline.** No RL in scope. |
| 9 | Weights & Biases | pass | n/a | risk | fail | **Decline as offered; adopt the idea.** See below. |
| 10 | LlamaIndex | cond. | pass | pass | cond. | **Accept, authoring-side only.** See below. |

Gate values: `cond.` means conditional — accepted only under the boundaries stated below. Gate A is marked "—" where the library would never touch generated child-facing output in any plausible use, so determinism is not the reason it is declined.

### The one refusal that matters

`diffusers` is the dangerous entry, because it is the one a well-meaning contributor is most likely to reach for. "Let the child generate a picture of their village" is an attractive feature and a governance failure.

`2.2` requires the child to describe intent in their own words before any generative step runs — which is a constraint on generation, not a licence for it. `2.4` requires imaginative imagery to be labelled fiction at the point of display. `3.7` bounds worldbuilding as imagination. `1.7` orders safety above capability. A diffusion model cannot guarantee what it emits, cannot be audited per-output at parish scale, and cannot satisfy `1.2`, the Church review gate, because a reviewer cannot review an output that does not exist until a child triggers it.

The compliant pattern already exists in the model: **reviewed assets, chosen by the child.** The child's description selects from a curated, Church-reviewed set. The child experiences authorship. The parish reviews a finite catalogue. `4.2` calls this the fixed-output path and it is the same answer here.

If generation is ever wanted, it belongs on the **authoring** side — an artist generates candidates offline, a human curates, the survivors enter the repository as licensed committed assets with recorded provenance under `1.5` and `3.1`. The child receives a file, not a model.

### Gradio — accept, and keep it off the public surface

`1.2` makes Church review a release requirement, and there is currently no instrument for it. A reviewer is handed a PDF and eight SVG wireframes and asked to approve 88 capabilities. That is a review by endurance.

[Gradio](https://github.com/gradio-app/gradio) is an honest fit for a **local reviewer harness**: load `model/EgD-URM-001.json`, present one capability at a time with its statement, domain, layer and status, and capture approve / reject / comment against the stable ID. Output is a committed review record, not a running service.

Two boundaries. It runs on the reviewer's machine, invoked from `tools/`, and never becomes part of `docs/` — the published surface is static GitHub Pages and must stay static, or Gate D fails and the parish inherits a server to operate. And its output is a file in the repository, per `EgD-BOOT-003`; a review that lives only in a browser tab did not happen.

The cheaper alternative, stated honestly per the spend rule: a generated static HTML checklist with `mailto:` or a form target costs one afternoon in `tools/gen_index.py` and adds zero dependencies. If review happens two or three times a year, take the cheap path. Gradio earns its place only if review becomes continuous.

### LlamaIndex — accept, authoring-side, with the provenance condition

This is the strongest genuine fit on the list, and it fits a problem the repository already has.

Domain 3 commits to a source-tagged narrative corpus with claims classified as record, inference, lore or author framing (`3.1`), citations to primary sources (`3.2`), a bounded Enoch adaptation restricted to 1 Enoch 72–82 (`3.3`), and convergence labelling (`3.8`). That corpus is not small, and it is spread across `acadian-heritage-record`, `enoch-convergence` and `ark-peer-review-ledger`. A writer working on a chapter needs to know, quickly, whether a sentence they want to write is supported, and by what.

[LlamaIndex](https://github.com/run-llama/llama_index) is built for exactly that: ingest a heterogeneous corpus, index it, retrieve with citations attached. It is actively developed — `v0.14.23`, 24 June 2026 — and it is the right shape, because retrieval returns *sources*, and sources are what `3.2` demands.

The condition is strict and it is where most retrieval implementations fail. **Retrieval may surface a claim; it may never classify one.** `3.1` says every narrative claim is tagged record, inference, lore or author framing, and untagged claims do not ship. If a retrieval layer assigns that tag, the classification becomes a model output and the corpus becomes unauditable. The tag is a human act, recorded by a named person, committed to the repository. LlamaIndex finds the passage. A person decides what it is.

Second condition: the index is a build artefact, never the record. If `git clone` plus the corpus cannot rebuild it, Gate D fails. Index files stay out of version control; the corpus and the tags stay in.

### Weights & Biases — decline the tool, keep the instinct

[Weights & Biases](https://wandb.ai/) tracks experiments. There are no experiments here. But the instinct behind it — that a run should leave an auditable record — is already canon in this repository, and better implemented than a hosted dashboard would be.

`verification/_verify_report.json` and `verification/play_report.json` are committed run records. They survive a vendor outage, a lapsed subscription and an account migration. `1.6` requires that canon breaches be appended to a register rather than silently corrected, and a git-committed JSON report does that natively. A hosted tracker moves the record off the record, which is the thing `EgD-BOOT-003` exists to prevent, and `5.5` — data belongs to the person and can be exported without permission from the platform — reads oddly against a repository that would need to ask a vendor for its own build history.

Adopt the discipline instead: every generator in `tools/` writes a dated report into `verification/`. That is the same benefit, in-repo, at no cost.

## What would actually improve this repository

The honest finding of this assessment is that the premise of the question is wrong. The gap between this repository and a stronger version of itself is not a missing generative-AI framework. It is five items of engineering hygiene, none of which requires a new dependency, and two of which are live defects against canon this repository already declares.

| # | Finding | Class | Why it matters |
| --- | --- | --- | --- |
| 1 | `docs/play/index.html` loads `three.module.js` and `GLTFLoader.js` from `unpkg.com` at runtime | **D — durability** | The version is pinned at `0.160.0`, which is good practice, but the bytes are not in the repository. A CDN outage, an unpublish, or a network-restricted parish takes the live 3D proof offline. `git clone` does not currently yield a working proof. Vendor the two files into `docs/play/vendor/` with recorded licences per `1.5`. This is roughly 700 KB and it makes the proof permanent. |
| 2 | `docs/play/index.html` requests fonts from `fonts.googleapis.com` and `fonts.gstatic.com` | **C — canon breach against `2.1`** | `2.1` forbids trackers and outbound links on the child surface. Every load of the child-facing page currently makes a third-party request carrying the child's IP address to a third party. Self-host the two typefaces. The fix is an afternoon; the exposure is the sort a safeguarding reviewer finds first. |
| 3 | `model/` and `docs/model/` hold byte-identical copies of all three rendered artefacts | maintainability | Confirmed identical by checksum. Two sources of truth is zero sources of truth — the first divergence will be silent. Generate into one location and have `tools/gen_index.py` copy or link at publish time. |
| 4 | No `.github/workflows`, no pinned Python requirements | reproducibility | The README documents a four-command regeneration sequence, including a two-pass PDF build whose page count must be piped between runs. That is precisely the sequence a human forgets. A workflow that regenerates all artefacts and fails the build on drift turns the documented ritual into an enforced invariant. A `requirements.txt` pinning `reportlab`, `pypdf` and `fonttools` is the difference between a build that works and a build that worked. |
| 5 | 88 capabilities, no schema and no test | integrity | `EgD-URM-001.json` carries `meta`, `sections` and `wireframes`, and the numbering rules are strong — stable IDs, never reused, never renumbered, retired numbers preserved. Nothing enforces them. A twenty-line test asserting ID uniqueness, no gaps in the retired set, valid status values from the four declared, valid layer values, and one-sentence statements per the model's own rule would make those promises checkable. The crosswalk CSV should be validated for row-per-section parity in the same test. |

Findings 1 and 2 are the ones to fix first, and they are fixable this week. Both concern the child-facing surface. Both are cases where the repository's own canon is stricter than the repository's own code — which is the good kind of problem to have, because the standard is already written and agreed.

## The pattern worth keeping

The reason nine of ten libraries are declined is not conservatism. It is that this repository made a decision in `11.2` — glTF as the seam, so the asset layer survives the engine — and that decision has a corollary: nothing that would make a framework the owner of the content is admissible. A model checkpoint is the most engine-like dependency there is: opaque, unversioned in practice, unreproducible, and licensed by someone else.

The libraries that pass are the ones that touch the work on the way in and leave nothing behind in the delivered artefact. Gradio helps a human approve. LlamaIndex helps a human find. Neither ships to the child. That is the test, and it will hold for the next ten libraries as well.

---

**Assessed against** `EgD-URM-001` blueprint v1.0 — 15 domains, 88 capabilities.
**Gates derived from** `1.2`, `1.5`, `1.7`, `2.1`, `2.2`, `2.4`, `3.1`, `3.2`, `3.7`, `4.2`, `6.6`, `8.4`, `9.1`, `11.2`, `EgD-BOOT-003`.
