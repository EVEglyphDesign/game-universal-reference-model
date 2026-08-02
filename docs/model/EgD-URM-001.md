# Game Universal Reference Model

## What this is, and what it is not

This is the blueprint layer only — the L0 document. It says what the game is made of and numbers every part so the parts can be argued about separately. It does not say how any part is built. That is the technical design, and it comes after you approve these numbers.

The rule is the one you used at Epic: the blueprint carries the numbers, the technical design refers to them, and every layer below inherits them unchanged. Nothing downstream invents its own numbering.

There are **15 domains** and **88 capabilities**. Every capability is one sentence. If a capability needs a paragraph, it is two capabilities and I have got it wrong.

### How to read the numbers

| Level | Form | Meaning | Example |
| --- | --- | --- | --- |
| L1 | `n` | Domain. A part of the system that can be owned by one person. | `7` Interaction and Control |
| L2 | `n.n` | Capability. One testable statement. | `7.2` Camera-relative movement |
| L3 | `n.n.n` | Component. Added in the technical design, not here. | `7.2.1` Input vector rotation |

Numbers are stable identifiers. Once you approve them they are never reused and never renumbered — if a capability dies it is marked withdrawn and its number stays retired. That is what makes them safe to reference from a contract, a test plan or another architecture.

### The crosswalk rule

Each section carries a row in a crosswalk sheet with empty columns for your Epic numbering, TOGAF artefacts, APQC process classifications, ISO references and two free local columns. One section may map to many nodes in a target model, and one target node may receive many sections. Repeating a field into several models is expected and is not duplication — it is the mapping.

Where two external models disagree about shape, this model holds the simpler shape and maps upward. That is the lowest-common-denominator rule, section 13.5, and it is the reason the model is deliberately shallow at L1.

## The decision you need to make first

Research turned up one constraint that changes the architecture, so it goes at the front rather than buried in section 11.

The desktop engine lane and the browser lane do not render the same way. Godot 4 can only target WebGL 2.0 on the web, using its Compatibility renderer; the Forward+ and Mobile renderers are not available in a browser because WebGPU support is not implemented, per the [Godot web export documentation](https://docs.godotengine.org/en/latest/tutorials/export/exporting_for_web.html). The starter project I built you yesterday uses Forward+. That is fine for a desktop build and wrong for a URL.

There are three honest options.

| Option | What you get | What it costs |
| --- | --- | --- |
| A. Godot, web export | One engine, one codebase, desktop and browser. Editor, scene tools, animation, physics all included. | Compatibility renderer only, so simpler lighting. Roughly 25-40 MB of runtime downloaded before the game starts. |
| B. Browser-native runtime | Small download, instant start, renders in any tab, sits naturally inside the parish portal. | No editor. Scenes must be authored elsewhere and imported. More code written by hand. |
| C. Two lanes, glTF as the seam | Author in a full desktop engine, deliver in the browser, with glTF 2.0 as the contract between them. Neither lane owns the content. | Two runtimes to maintain. The seam has to be disciplined. |

**The model recommends C**, and section 11.2 records it as a decision rather than a fact so you can overturn it. The reason is that C is the only option where the asset layer survives the engine. If a runtime is abandoned, or the browser gets WebGPU and the calculus changes, glTF scenes and Blender sources carry forward untouched. Options A and B both make the engine the owner of your content, and you have spent this whole year making sure nothing owns your content.

I have already proved the seam works. The verified Godot world from the starter project exported to a 125 KB binary glTF file — 29 nodes, 8 meshes, 5 materials — and it now loads and runs in a browser. That is the live surface linked from the blueprint page.

## The standards this rests on

| Layer | Standard | Status |
| --- | --- | --- |
| 3D asset and scene interchange | glTF 2.0, binary `.glb` | Published as [ISO/IEC 12113:2022](https://www.khronos.org/news/press/khronos-gltf-2.0-released-as-an-iso-iec-international-standard) by [Khronos](https://www.khronos.org/gltf/) |
| Browser rendering | WebGL 2.0 | Web standard, universally available |
| Browser execution | WebAssembly | Web standard |
| Texture container | KTX 2.0 with Basis Universal | Khronos, optional extension |
| Accessibility | WCAG 2.2 | W3C recommendation |
| Document control | ISO 8601 timestamps, SHA-256 hashes | In force in this document |

A note on currency, because it affects a choice you may be asked about later. [Phoronix reported](https://www.phoronix.com/news/Khronos-glTF-2.1-Released) that Khronos released glTF 2.1 on 11 June 2026, adding multi-file scene composition, embedded thumbnails and a 64-bit container. I could not confirm that on the Khronos landing page, which still describes 2.0 as current, so I have not built the model on 2.1. Section 10.1 anchors on glTF 2.0 because it is the ISO-published version and the one every tool already reads. If 2.1 is confirmed, it is backward compatible and the section text changes, not the architecture.

## The model

Status values: **Canon** is decided and in force. **Proposed** needs your approval. **Decision** is a fork I have recommended but not closed. **Open** is unresolved and waiting on information.

### 1. Governance and Authority

Who may decide, who must review, and what a controlled artefact is.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 1.1 | Umbrella copyright and dual-helix authority | Church authority and utility authority are paired under one umbrella copyright rather than a single owner. | Business | Canon |
| 1.2 | Church review gate | Doctrinal conformance and Church testing are release requirements for any parishioner-facing build. | Business | Canon |
| 1.3 | Controlled-document canon | Specifications ship as PDF with document ID, key ID, content hash, ISO-8601 stamp, watermark, copyright line and closing mark. | Business · ISO 8601 | Canon |
| 1.4 | Naming and mark control | Studio name and product title are separate assets; product titles are cleared before publication and third-party marks are never used. | Business | Open |
| 1.5 | Licence posture | Engine and framework are permissively licensed; narrative content stays EgD-owned; every third-party asset carries a recorded licence. | Business · MIT, Apache-2.0 | Canon |
| 1.6 | Defect register and change control | Breaches of canon are appended to a register in the same session, never silently corrected. | Business | Canon |
| 1.7 | Safety first, betterment second | Where safety and capability conflict, safety wins and the trade is recorded. | Business | Canon |

### 2. Safeguarding and Child Protection

The walls around a child-facing surface, stated before any feature.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 2.1 | Closed communication walls | No chat, voice channels, friend requests, camera, microphone, uploads, advertising, trackers or outbound links on the child surface. | Business | Canon |
| 2.2 | Describe before generate | The child must describe intent in their own words before any generative step runs. | Application | Canon |
| 2.3 | Mandatory Stand-Up | Every twelve minutes of active play triggers a non-skippable 66-second eyes, spine and reach break with a seated accommodation. The interval may be shortened for younger cohorts, never lengthened. | Application | Canon |
| 2.4 | Fictional-imagery notice | Imaginative or symbolic imagery is labelled as fiction at the point of display. | Business | Canon |
| 2.5 | Age banding and cohort scope | Content, session length and social surface are bounded by age band and school cohort. | Business | Canon |
| 2.6 | Consent and skip gates | Start position, consent and skip gates run before the guided demo; interaction unlocks only in the play phase. | Application | Canon |
| 2.7 | Guardian visibility | A guardian can see what the child saw without surveilling the child in real time. | Business | Proposed |

### 3. Narrative Canon and Provenance

What the story is allowed to assert, and on whose authority.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 3.1 | Claim classification | Every narrative claim is tagged record, inference, lore, or author framing. Untagged claims do not ship. | Data | Canon |
| 3.2 | Source-tagged corpus | Narrative source material carries citations to primary sources and records its own corrections. | Data | Canon |
| 3.3 | Bounded Enoch adaptation | Only the Astronomical Book, 1 Enoch 72-82, is adapted, for calendar and heritage mechanics. Judgment and Watchers material is excluded from the main path. | Data | Canon |
| 3.4 | Heritage chapter line | Acadian survival-and-rebuild chapters use the defensible 1636-1650 Port-Royal arrival range and make no oldest-site claim. | Data | Canon |
| 3.5 | Narrator character bench | Uriel is the child-facing companion. Penemue is reserved for a truth-ledger lane. Valentinian Sophia is excluded in favour of Proverbs-Wisdom. | Data | Canon |
| 3.6 | Copyright-limited corpus handling | Public-domain texts are stored in full; copyrighted editions are represented bibliographically only. | Data | Canon |
| 3.7 | Worldbuilding boundary | Ideal-world and double-sphere imagery is framed as imagination, never as a prescriptive real-world claim. | Business | Canon |
| 3.8 | Convergence labelling | Overlaps between sources are marked direct, structural or speculative, and non-convergences are recorded too. | Data | Canon |

### 4. Learning Design

The teaching model the game exists to carry.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 4.1 | Education parent, religion subsection | The parent programme is education; religious education is one part of it. | Business | Canon |
| 4.2 | Fixed-output catechetical path | Catechetical answers are reviewed and deterministic, never open-ended generation. | Application | Canon |
| 4.3 | Lesson primitives | Circle, triangle and sphere are the base geometric lesson objects the mechanics build on. | Data | Canon |
| 4.4 | Chapter and progression model | Content is delivered as numbered chapters with an explicit unlock rule. | Data | Canon |
| 4.5 | Service-and-evidence credibility | Standing is earned through evidenced help to others, not follower counts, streaks or engagement. | Application | Canon |
| 4.6 | Assessment and mastery evidence | Progress is evidenced by artefacts the learner produced, not time on task. | Data | Proposed |
| 4.7 | Game as doorway | The game lowers the entry barrier; education, the twin and free choice remain the process it carries. | Business | Canon |

### 5. Identity and Digital Twin

Who the player is to the system, and what the system owes them.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 5.1 | Starter-twin quest | Onboarding is request access, authenticate, fork a starter twin, connect everyday tools. | Application | Canon |
| 5.2 | Three doors | Humans enter as Mother, Child or Father; institutions are sorted separately as electric utility, other utility, or enterprise. | Business | Canon |
| 5.3 | Consent-first protection message | The first cross-cultural message is protection, not capability. | Business | Canon |
| 5.4 | Soft identification tier | Adult surfaces let the reader start freely and ask for identity only after meaningful engagement. | Application | Canon |
| 5.5 | Twin ownership and portability | The twin's data belongs to the person and can be exported without permission from the platform. | Data | Canon |
| 5.6 | Authentication backend | Identity verification runs through a named backend rather than hard-coded logic. | Application | Proposed |

### 6. World and Level Structure

How space is described so every chapter is built the same way.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 6.1 | Scene graph contract | One scene per chapter, one root per scene, no cross-scene node paths. | Application · glTF 2.0 scene graph | Canon |
| 6.2 | Metric ground plane | Units are metres. The floor's top surface sits at y = 0 and a character's origin is at its feet. | Data | Canon |
| 6.3 | Chapter world inventory | Each chapter declares its geometry, interactables, spawn points and exits as data before it is built. | Data | Proposed |
| 6.4 | The Village | A shared, voice-first common surface bounded by the child's school or cohort, with no feed-style global discovery. | Application | Canon |
| 6.5 | Navigation and blocking volumes | Walkable area and blocked area are authored explicitly, not inferred from visual geometry. | Application | Canon |
| 6.6 | Browser scene budget | Visible polygon count stays under roughly 50,000 and textures under 1024 px for the browser lane. | Technology | Canon |

### 7. Interaction and Control

The contract between the player's hands and the world.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 7.1 | Named input actions | Code binds to named actions such as move_forward, never to raw key codes. This buys gamepad support and rebinding for free. | Application | Canon |
| 7.2 | Camera-relative movement | Forward means away from the camera. Input is rotated by the camera rig's basis before it becomes velocity. | Application | Canon |
| 7.3 | Split camera rig | Yaw lives on a rig node, pitch lives on a spring arm, so rotations cannot interfere and the camera cannot roll or clip walls. | Application | Canon |
| 7.4 | Feel constants as contract | SPEED, ACCEL and TURN_SPEED are published tunables. Defaults are 5.5 m/s, 60, and 12. | Application | Canon |
| 7.5 | Voice-first village interaction | Movement and voice are the primary interaction metaphor in the common surface, not text entry. | Application | Canon |
| 7.6 | Touch and gamepad parity | Every action reachable by keyboard is reachable by touch and by gamepad. | Application | Proposed |

### 8. Simulation and Rules

What the world does when nobody is pressing anything.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 8.1 | Fixed-tick simulation | Game logic advances on a fixed physics tick independent of frame rate. | Application | Canon |
| 8.2 | Sequenced actions | Multi-frame actions such as a sword swing, a cutscene or a boss phase are written as coroutines, not state-machine sprawl. | Application | Canon |
| 8.3 | Interaction volumes and timed windows | Hits and triggers use explicit volumes enabled for an explicit number of frames. | Application | Canon |
| 8.4 | Deterministic puzzle state | Puzzle outcomes are reproducible from recorded input; no hidden randomness in assessed content. | Application | Canon |
| 8.5 | Lossy-save assumption | Browser storage is assumed to be unreliable. Progress that matters is recoverable from the server or re-earnable. | Data | Canon |

### 9. Presentation and Audio

How it looks and sounds, bounded by the delivery target.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 9.1 | Renderer profile | Browser lane runs WebGL 2.0 with a compatibility-class renderer. Advanced deferred rendering is native-lane only. | Technology · WebGL 2.0 | Canon |
| 9.2 | Lighting and tonemap profile | One directional key light with shadows, AgX tonemapping, ambient contribution from sky. | Technology | Canon |
| 9.3 | Palette and typography canon | Cream #fdfaf4, cream-2 #f7f2e7, ink #1a1a1a, line #e7e1d3, mute #6b665c, accent orange #e87722. Fraunces display, Inter body. | Business | Canon |
| 9.4 | UI shell and HUD | Chrome is minimal during play; the safety timer and chapter title are the only persistent elements. | Application | Proposed |
| 9.5 | Audio ceiling | No more than eight to ten simultaneous audio streams in the browser lane; fewer on mobile. | Technology · Web Audio API | Canon |

### 10. Asset Pipeline and Open Standards

The interchange contract. This is the layer that makes the work portable.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 10.1 | glTF 2.0 as the interchange format | Every 3D asset and scene crosses tool boundaries as glTF 2.0, binary .glb preferred. This is the published ISO standard and the lowest common denominator across engines. | Data · ISO/IEC 12113:2022 | Canon |
| 10.2 | Texture container | Textures ship as KTX2 with Basis Universal supercompression where the runtime supports it, PNG otherwise. | Data · KTX 2.0, KHR_texture_basisu | Proposed |
| 10.3 | Resolution and budget ceiling | 1024 px texture ceiling for the browser lane; 2048 permitted native. | Technology | Canon |
| 10.4 | Naming and folder convention | Assets are named by chapter and role, not by author or date. | Data | Proposed |
| 10.5 | Asset provenance register | Every imported asset records source URL, licence, and pinned commit or version. | Data | Canon |
| 10.6 | Authoring toolchain | Blender for modelling, an open engine for scene assembly, both exporting glTF. No proprietary interchange format in the chain. | Technology | Canon |

### 11. Platform, Build and Delivery

How it becomes a URL.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 11.1 | Browser baseline | The delivery target is a modern browser with WebAssembly and WebGL 2.0. No installer, no store, no plugin. | Technology · WebAssembly, WebGL 2.0 | Canon |
| 11.2 | Two-lane engine strategy | A WebGL-2 web runtime is the public lane; a full desktop engine is the authoring and native lane. glTF is the seam between them, so neither lane owns the content. | Technology | Decision |
| 11.3 | Hosting profile | GitHub Pages by default. Cross-origin isolation headers are required only if the runtime uses shared-memory threading. | Technology · COOP, COEP | Canon |
| 11.4 | Reproducible build | Build artefacts are produced by a committed script from a pinned toolchain, never by hand. | Technology | Canon |
| 11.5 | Public URL as deliverable | Work exists when it is committed, pushed, and fetched successfully from its public URL. | Business | Canon |

### 12. Data, Telemetry and Privacy

What is recorded, and what is deliberately not.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 12.1 | No trackers on the child surface | No analytics, advertising identifiers or third-party beacons on any child-facing page. | Technology | Canon |
| 12.2 | Local-first state | Play state stays on the device unless the player chooses to sync it. | Data | Canon |
| 12.3 | Adult review-signal logging | Engagement and review signals are logged on adult outreach surfaces only, and disclosed there. | Data | Canon |
| 12.4 | Retention and deletion | Every stored field has a stated retention period and a working deletion path. | Data | Proposed |
| 12.5 | Witnessed, not surveilled | Visibility to a trusted adult is the privacy metaphor; continuous monitoring is not. | Business | Canon |

### 13. Integration and Interoperability

How this model plugs into everything else you own.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 13.1 | Knowledge-graph surface | Narrative, lesson and progress entities are exposed as a temporal knowledge graph rather than locked in the build. | Data | Proposed |
| 13.2 | Agent-tool surface | The graph is exposed over a standard agent-tool protocol so external assistants can read it. | Application · MCP | Proposed |
| 13.3 | Portal embedding | The playable embeds inside the parish or institution portal rather than living as a standalone secular surface. | Application | Canon |
| 13.4 | Crosswalk registry | Every section number here carries a crosswalk row to external reference models. Repeating one field into many target models is expected and permitted. | Data | Canon |
| 13.5 | Lowest-denominator rule | Where two external models disagree, this model holds the simpler shape and maps upward, never downward. | Business | Canon |

### 14. Operations and Lifecycle

Keeping it alive and affordable.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 14.1 | Repository as the record | The session is a scratchpad. Anything that matters is recoverable by cloning the repository and nothing else. | Business | Canon |
| 14.2 | Release gates | Church review, safety review, accessibility check and a fetched public URL all pass before a release is called done. | Business | Canon |
| 14.3 | Self-healing log | Decisions and corrections are captured as committed log entries, not left in chat. | Business | Canon |
| 14.4 | Cost control | Spend is measured against a declared daily control before expensive work is authorised. | Business | Canon |
| 14.5 | Peer-review intake | A public front door collects parent and peer feedback and routes it to a named channel. | Business | Canon |

### 15. Accessibility and Localisation

Who can actually play it.

| ID | Capability | Statement | Layer | Status |
| --- | --- | --- | --- | --- |
| 15.1 | Contrast and focus | Text and interactive elements meet published contrast and keyboard-focus guidance. | Application · WCAG 2.2 | Proposed |
| 15.2 | Seated accommodation | Every physical prompt, including the Stand-Up, has a seated equivalent. | Application | Canon |
| 15.3 | Language set | English, French and Spanish are first-class. Strings are externalised, never embedded in scenes. | Data | Canon |
| 15.4 | Low-end device profile | A named minimum device and connection profile is tested each release. | Technology | Proposed |
| 15.5 | Reading-level control | Child-facing text is held to a stated reading level and checked, not assumed. | Business | Proposed |

## Wireframes

Eight screens. Each one names the capability numbers it implements, so a screen can be reviewed against the model rather than against taste. They are line drawings on purpose — arguing about colour before the flow is agreed wastes everybody's time.

| Screen | Title | Implements |
| --- | --- | --- |
| W1 | Entry — Three Doors | 5.2, 5.3, 1.4 |
| W2 | Safety Notice and Consent Gate | 2.1, 2.4, 2.6 |
| W3 | Chapter Select | 4.4, 3.4, 3.3 |
| W4 | Play Surface — 3D HUD | 6.1, 7.2, 7.3, 9.4 |
| W5 | Stand-Up Break Overlay | 2.3, 15.2 |
| W6 | Twin Quest — Connect Tools | 5.1, 5.5, 12.2 |
| W7 | The Village | 6.4, 4.5, 7.5 |
| W8 | Guardian and Review Panel | 1.2, 2.7, 14.2 |

The screens are published on the blueprint page at full size.

## What I need from you

Five things, in this order. Everything downstream waits on the first three.

1. **Close the engine decision.** Section 11.2, options A, B or C above.
2. **Approve or renumber the L1 domains.** Fifteen is a judgement call. If your Epic convention wants a different top level, now is the cheap moment to change it — after the technical design it is not.
3. **Rule on the Proposed rows.** There are proposals across the model that need a yes, a no, or a rewrite.
4. **Name the first chapter to build.** Chapter 2, What We Kept, already exists as a trilingual puzzle. Chapter 3, Four Lost Days, has the calendar mechanic. Either could be the first 3D chapter, and the choice changes what gets built first.
5. **Confirm the product title.** Section 1.4 is open. PAIX names the parishioner surface, and the earlier note that a game title carries mark exposure the studio name does not still stands.

## What happens after approval

The technical design inherits these numbers and adds the L3 layer. Each L2 capability gets components, interfaces, data structures and acceptance tests, all numbered beneath its parent. Nothing in the technical design may exist without a parent number here — if something needs to be built that has no number, the blueprint was wrong and comes back for amendment rather than being quietly extended.

That constraint is the whole value of doing it this way. It is also the part that will irritate whoever writes the technical design, which is how you know it is working.

## Sources

Standards: [Khronos glTF](https://www.khronos.org/gltf/), the [glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html), and [glTF 2.0 as ISO/IEC 12113:2022](https://www.khronos.org/news/press/khronos-gltf-2.0-released-as-an-iso-iec-international-standard). Engine constraints: [Exporting for the Web](https://docs.godotengine.org/en/latest/tutorials/export/exporting_for_web.html), Godot documentation. glTF 2.1 report: [Phoronix, 11 June 2026](https://www.phoronix.com/news/Khronos-glTF-2.1-Released), unconfirmed against Khronos at time of issue.

Internal canon: capability statements are drawn from the EVEglyphDesign knowledge record for the PAIX educational game, EVE Hyperloop, EVE Glyph Education, the Acadian Heritage Record, the Enoch Convergence research boundary, Starship Academy, the [Executive Boot Contract](https://github.com/EVEglyphDesign/eve-glyph-boot-contract), and the measured behaviour of [EgD-GDS-001](https://eveglyphdesign.github.io/godot-action-adventure-starter/), the verified Godot starter. The `internal_source` column of the crosswalk sheet records the origin of every row.
