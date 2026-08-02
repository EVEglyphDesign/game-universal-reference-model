# EgD-URM-001 — Universal Reference Model, single source of truth.
# Every other rendering (JSON, CSV, Markdown, PDF, wireframe labels) derives from this.
# Fields are deliberately repeated into many outputs; that is the point.

PREFIX = "EgD-URM"

# (id, title, statement, togaf, standard, source, status)
# togaf: B=Business  D=Data  A=Application  T=Technology
DOMAINS = [
 ("1", "Governance and Authority", "Who may decide, who must review, and what a controlled artefact is.", [
  ("1.1","Umbrella copyright and dual-helix authority","Church authority and utility authority are paired under one umbrella copyright rather than a single owner.","B","","concepts/dual-helix-governance","Canon"),
  ("1.2","Church review gate","Doctrinal conformance and Church testing are release requirements for any parishioner-facing build.","B","","projects/paix-educational-game","Canon"),
  ("1.3","Controlled-document canon","Specifications ship as PDF with document ID, key ID, content hash, ISO-8601 stamp, watermark, copyright line and closing mark.","B","ISO 8601","concepts/eve-glyph-design-system","Canon"),
  ("1.4","Naming and mark control","Studio name and product title are separate assets; product titles are cleared before publication and third-party marks are never used.","B","","projects/eve-hyperloop","Open"),
  ("1.5","Licence posture","Engine and framework are permissively licensed; narrative content stays EgD-owned; every third-party asset carries a recorded licence.","B","MIT, Apache-2.0","concepts/github-as-durable-asset","Canon"),
  ("1.6","Defect register and change control","Breaches of canon are appended to a register in the same session, never silently corrected.","B","","projects/eve-glyph-boot-contract","Canon"),
  ("1.7","Safety first, betterment second","Where safety and capability conflict, safety wins and the trade is recorded.","B","","concepts/safety-first-betterment-second","Canon"),
 ]),
 ("2", "Safeguarding and Child Protection", "The walls around a child-facing surface, stated before any feature.", [
  ("2.1","Closed communication walls","No chat, voice channels, friend requests, camera, microphone, uploads, advertising, trackers or outbound links on the child surface.","B","","projects/paix-educational-game","Canon"),
  ("2.2","Describe before generate","The child must describe intent in their own words before any generative step runs.","A","","projects/paix-educational-game","Canon"),
  ("2.3","Mandatory Stand-Up","Every twelve minutes of active play triggers a non-skippable 66-second eyes, spine and reach break with a seated accommodation. The interval may be shortened for younger cohorts, never lengthened.","A","","projects/paix-educational-game","Canon"),
  ("2.4","Fictional-imagery notice","Imaginative or symbolic imagery is labelled as fiction at the point of display.","B","","projects/eve-glyph-education","Canon"),
  ("2.5","Age banding and cohort scope","Content, session length and social surface are bounded by age band and school cohort.","B","","projects/eve-glyph-education","Canon"),
  ("2.6","Consent and skip gates","Start position, consent and skip gates run before the guided demo; interaction unlocks only in the play phase.","A","","projects/paix-educational-game","Canon"),
  ("2.7","Guardian visibility","A guardian can see what the child saw without surveilling the child in real time.","B","","projects/eve-glyph-education","Proposed"),
 ]),
 ("3", "Narrative Canon and Provenance", "What the story is allowed to assert, and on whose authority.", [
  ("3.1","Claim classification","Every narrative claim is tagged record, inference, lore, or author framing. Untagged claims do not ship.","D","","projects/acadian-heritage-record","Canon"),
  ("3.2","Source-tagged corpus","Narrative source material carries citations to primary sources and records its own corrections.","D","","projects/ark-peer-review-ledger","Canon"),
  ("3.3","Bounded Enoch adaptation","Only the Astronomical Book, 1 Enoch 72-82, is adapted, for calendar and heritage mechanics. Judgment and Watchers material is excluded from the main path.","D","","projects/acadian-heritage-record","Canon"),
  ("3.4","Heritage chapter line","Acadian survival-and-rebuild chapters use the defensible 1636-1650 Port-Royal arrival range and make no oldest-site claim.","D","","projects/acadian-heritage-record","Canon"),
  ("3.5","Narrator character bench","Uriel is the child-facing companion. Penemue is reserved for a truth-ledger lane. Valentinian Sophia is excluded in favour of Proverbs-Wisdom.","D","","projects/paix-educational-game","Canon"),
  ("3.6","Copyright-limited corpus handling","Public-domain texts are stored in full; copyrighted editions are represented bibliographically only.","D","","projects/enoch-convergence","Canon"),
  ("3.7","Worldbuilding boundary","Ideal-world and double-sphere imagery is framed as imagination, never as a prescriptive real-world claim.","B","","projects/eve-glyph-education","Canon"),
  ("3.8","Convergence labelling","Overlaps between sources are marked direct, structural or speculative, and non-convergences are recorded too.","D","","projects/enoch-convergence","Canon"),
 ]),
 ("4", "Learning Design", "The teaching model the game exists to carry.", [
  ("4.1","Education parent, religion subsection","The parent programme is education; religious education is one part of it.","B","","projects/paix-educational-game","Canon"),
  ("4.2","Fixed-output catechetical path","Catechetical answers are reviewed and deterministic, never open-ended generation.","A","","projects/paix-educational-game","Canon"),
  ("4.3","Lesson primitives","Circle, triangle and sphere are the base geometric lesson objects the mechanics build on.","D","","projects/eve-hyperloop","Canon"),
  ("4.4","Chapter and progression model","Content is delivered as numbered chapters with an explicit unlock rule.","D","","projects/eve-hyperloop","Canon"),
  ("4.5","Service-and-evidence credibility","Standing is earned through evidenced help to others, not follower counts, streaks or engagement.","A","","projects/eve-glyph-education","Canon"),
  ("4.6","Assessment and mastery evidence","Progress is evidenced by artefacts the learner produced, not time on task.","D","","projects/starship-academy-training-series","Proposed"),
  ("4.7","Game as doorway","The game lowers the entry barrier; education, the twin and free choice remain the process it carries.","B","","projects/eve-glyph-education","Canon"),
 ]),
 ("5", "Identity and Digital Twin", "Who the player is to the system, and what the system owes them.", [
  ("5.1","Starter-twin quest","Onboarding is request access, authenticate, fork a starter twin, connect everyday tools.","A","","projects/eve-hyperloop","Canon"),
  ("5.2","Three doors","Humans enter as Mother, Child or Father; institutions are sorted separately as electric utility, other utility, or enterprise.","B","","projects/eve-glyph-education","Canon"),
  ("5.3","Consent-first protection message","The first cross-cultural message is protection, not capability.","B","","projects/eve-glyph-education","Canon"),
  ("5.4","Soft identification tier","Adult surfaces let the reader start freely and ask for identity only after meaningful engagement.","A","","projects/eve-glyph-education","Canon"),
  ("5.5","Twin ownership and portability","The twin's data belongs to the person and can be exported without permission from the platform.","D","","concepts/sovereign-data-rights","Canon"),
  ("5.6","Authentication backend","Identity verification runs through a named backend rather than hard-coded logic.","A","","projects/starship-academy-training-series","Proposed"),
 ]),
 ("6", "World and Level Structure", "How space is described so every chapter is built the same way.", [
  ("6.1","Scene graph contract","One scene per chapter, one root per scene, no cross-scene node paths.","A","glTF 2.0 scene graph","projects/eve-hyperloop","Canon"),
  ("6.2","Metric ground plane","Units are metres. The floor's top surface sits at y = 0 and a character's origin is at its feet.","D","","EgD-GDS-001","Canon"),
  ("6.3","Chapter world inventory","Each chapter declares its geometry, interactables, spawn points and exits as data before it is built.","D","","projects/eve-hyperloop","Proposed"),
  ("6.4","The Village","A shared, voice-first common surface bounded by the child's school or cohort, with no feed-style global discovery.","A","","projects/eve-glyph-education","Canon"),
  ("6.5","Navigation and blocking volumes","Walkable area and blocked area are authored explicitly, not inferred from visual geometry.","A","","EgD-GDS-001","Canon"),
  ("6.6","Browser scene budget","Visible polygon count stays under roughly 50,000 and textures under 1024 px for the browser lane.","T","","EgD-URM-11.1","Canon"),
 ]),
 ("7", "Interaction and Control", "The contract between the player's hands and the world.", [
  ("7.1","Named input actions","Code binds to named actions such as move_forward, never to raw key codes. This buys gamepad support and rebinding for free.","A","","EgD-GDS-001","Canon"),
  ("7.2","Camera-relative movement","Forward means away from the camera. Input is rotated by the camera rig's basis before it becomes velocity.","A","","EgD-GDS-001","Canon"),
  ("7.3","Split camera rig","Yaw lives on a rig node, pitch lives on a spring arm, so rotations cannot interfere and the camera cannot roll or clip walls.","A","","EgD-GDS-001","Canon"),
  ("7.4","Feel constants as contract","SPEED, ACCEL and TURN_SPEED are published tunables. Defaults are 5.5 m/s, 60, and 12.","A","","EgD-GDS-001","Canon"),
  ("7.5","Voice-first village interaction","Movement and voice are the primary interaction metaphor in the common surface, not text entry.","A","","projects/eve-glyph-education","Canon"),
  ("7.6","Touch and gamepad parity","Every action reachable by keyboard is reachable by touch and by gamepad.","A","","EgD-URM-15.4","Proposed"),
 ]),
 ("8", "Simulation and Rules", "What the world does when nobody is pressing anything.", [
  ("8.1","Fixed-tick simulation","Game logic advances on a fixed physics tick independent of frame rate.","A","","projects/carbon-intake","Canon"),
  ("8.2","Sequenced actions","Multi-frame actions such as a sword swing, a cutscene or a boss phase are written as coroutines, not state-machine sprawl.","A","","projects/carbon-intake","Canon"),
  ("8.3","Interaction volumes and timed windows","Hits and triggers use explicit volumes enabled for an explicit number of frames.","A","","EgD-GDS-001","Canon"),
  ("8.4","Deterministic puzzle state","Puzzle outcomes are reproducible from recorded input; no hidden randomness in assessed content.","A","","projects/eve-hyperloop","Canon"),
  ("8.5","Lossy-save assumption","Browser storage is assumed to be unreliable. Progress that matters is recoverable from the server or re-earnable.","D","","EgD-URM-11.1","Canon"),
 ]),
 ("9", "Presentation and Audio", "How it looks and sounds, bounded by the delivery target.", [
  ("9.1","Renderer profile","Browser lane runs WebGL 2.0 with a compatibility-class renderer. Advanced deferred rendering is native-lane only.","T","WebGL 2.0","EgD-URM-11.2","Canon"),
  ("9.2","Lighting and tonemap profile","One directional key light with shadows, AgX tonemapping, ambient contribution from sky.","T","","EgD-GDS-001","Canon"),
  ("9.3","Palette and typography canon","Cream #fdfaf4, cream-2 #f7f2e7, ink #1a1a1a, line #e7e1d3, mute #6b665c, accent orange #e87722. Fraunces display, Inter body.","B","","concepts/eve-glyph-design-system","Canon"),
  ("9.4","UI shell and HUD","Chrome is minimal during play; the safety timer and chapter title are the only persistent elements.","A","","projects/paix-educational-game","Proposed"),
  ("9.5","Audio ceiling","No more than eight to ten simultaneous audio streams in the browser lane; fewer on mobile.","T","Web Audio API","EgD-URM-11.1","Canon"),
 ]),
 ("10", "Asset Pipeline and Open Standards", "The interchange contract. This is the layer that makes the work portable.", [
  ("10.1","glTF 2.0 as the interchange format","Every 3D asset and scene crosses tool boundaries as glTF 2.0, binary .glb preferred. This is the published ISO standard and the lowest common denominator across engines.","D","ISO/IEC 12113:2022","Khronos","Canon"),
  ("10.2","Texture container","Textures ship as KTX2 with Basis Universal supercompression where the runtime supports it, PNG otherwise.","D","KTX 2.0, KHR_texture_basisu","Khronos","Proposed"),
  ("10.3","Resolution and budget ceiling","1024 px texture ceiling for the browser lane; 2048 permitted native.","T","","EgD-URM-6.6","Canon"),
  ("10.4","Naming and folder convention","Assets are named by chapter and role, not by author or date.","D","","concepts/github-as-durable-asset","Proposed"),
  ("10.5","Asset provenance register","Every imported asset records source URL, licence, and pinned commit or version.","D","","projects/carbon-intake","Canon"),
  ("10.6","Authoring toolchain","Blender for modelling, an open engine for scene assembly, both exporting glTF. No proprietary interchange format in the chain.","T","","Khronos","Canon"),
 ]),
 ("11", "Platform, Build and Delivery", "How it becomes a URL.", [
  ("11.1","Browser baseline","The delivery target is a modern browser with WebAssembly and WebGL 2.0. No installer, no store, no plugin.","T","WebAssembly, WebGL 2.0","W3C","Canon"),
  ("11.2","Two-lane engine strategy","A WebGL-2 web runtime is the public lane; a full desktop engine is the authoring and native lane. glTF is the seam between them, so neither lane owns the content.","T","","EgD-URM-10.1","Decision"),
  ("11.3","Hosting profile","GitHub Pages by default. Cross-origin isolation headers are required only if the runtime uses shared-memory threading.","T","COOP, COEP","EgD-URM-11.1","Canon"),
  ("11.4","Reproducible build","Build artefacts are produced by a committed script from a pinned toolchain, never by hand.","T","","projects/eve-glyph-boot-contract","Canon"),
  ("11.5","Public URL as deliverable","Work exists when it is committed, pushed, and fetched successfully from its public URL.","B","","projects/eve-glyph-boot-contract","Canon"),
 ]),
 ("12", "Data, Telemetry and Privacy", "What is recorded, and what is deliberately not.", [
  ("12.1","No trackers on the child surface","No analytics, advertising identifiers or third-party beacons on any child-facing page.","T","","projects/paix-educational-game","Canon"),
  ("12.2","Local-first state","Play state stays on the device unless the player chooses to sync it.","D","","concepts/sovereign-data-rights","Canon"),
  ("12.3","Adult review-signal logging","Engagement and review signals are logged on adult outreach surfaces only, and disclosed there.","D","","projects/eve-glyph-education","Canon"),
  ("12.4","Retention and deletion","Every stored field has a stated retention period and a working deletion path.","D","","concepts/sovereign-data-rights","Proposed"),
  ("12.5","Witnessed, not surveilled","Visibility to a trusted adult is the privacy metaphor; continuous monitoring is not.","B","","projects/victoria-digital-twin-training-surface","Canon"),
 ]),
 ("13", "Integration and Interoperability", "How this model plugs into everything else you own.", [
  ("13.1","Knowledge-graph surface","Narrative, lesson and progress entities are exposed as a temporal knowledge graph rather than locked in the build.","D","","projects/origin-labs-consolidation","Proposed"),
  ("13.2","Agent-tool surface","The graph is exposed over a standard agent-tool protocol so external assistants can read it.","A","MCP","projects/origin-labs-consolidation","Proposed"),
  ("13.3","Portal embedding","The playable embeds inside the parish or institution portal rather than living as a standalone secular surface.","A","","projects/parish-sovereign-gateway","Canon"),
  ("13.4","Crosswalk registry","Every section number here carries a crosswalk row to external reference models. Repeating one field into many target models is expected and permitted.","D","","EgD-URM-13.5","Canon"),
  ("13.5","Lowest-denominator rule","Where two external models disagree, this model holds the simpler shape and maps upward, never downward.","B","","EgD-URM-13.4","Canon"),
 ]),
 ("14", "Operations and Lifecycle", "Keeping it alive and affordable.", [
  ("14.1","Repository as the record","The session is a scratchpad. Anything that matters is recoverable by cloning the repository and nothing else.","B","","projects/eve-glyph-boot-contract","Canon"),
  ("14.2","Release gates","Church review, safety review, accessibility check and a fetched public URL all pass before a release is called done.","B","","projects/paix-educational-game","Canon"),
  ("14.3","Self-healing log","Decisions and corrections are captured as committed log entries, not left in chat.","B","","projects/eve-hyperloop","Canon"),
  ("14.4","Cost control","Spend is measured against a declared daily control before expensive work is authorised.","B","","projects/eve-glyph-boot-contract","Canon"),
  ("14.5","Peer-review intake","A public front door collects parent and peer feedback and routes it to a named channel.","B","","projects/eve-glyph-education","Canon"),
 ]),
 ("15", "Accessibility and Localisation", "Who can actually play it.", [
  ("15.1","Contrast and focus","Text and interactive elements meet published contrast and keyboard-focus guidance.","A","WCAG 2.2","W3C","Proposed"),
  ("15.2","Seated accommodation","Every physical prompt, including the Stand-Up, has a seated equivalent.","A","","projects/paix-educational-game","Canon"),
  ("15.3","Language set","English, French and Spanish are first-class. Strings are externalised, never embedded in scenes.","D","","projects/eve-glyph-education","Canon"),
  ("15.4","Low-end device profile","A named minimum device and connection profile is tested each release.","T","","EgD-URM-11.1","Proposed"),
  ("15.5","Reading-level control","Child-facing text is held to a stated reading level and checked, not assumed.","B","","projects/eve-glyph-education","Proposed"),
 ]),
]

WIREFRAMES = [
 ("W1","Entry — Three Doors","5.2, 5.3, 1.4"),
 ("W2","Safety Notice and Consent Gate","2.1, 2.4, 2.6"),
 ("W3","Chapter Select","4.4, 3.4, 3.3"),
 ("W4","Play Surface — 3D HUD","6.1, 7.2, 7.3, 9.4"),
 ("W5","Stand-Up Break Overlay","2.3, 15.2"),
 ("W6","Twin Quest — Connect Tools","5.1, 5.5, 12.2"),
 ("W7","The Village","6.4, 4.5, 7.5"),
 ("W8","Guardian and Review Panel","1.2, 2.7, 14.2"),
]

def rows():
    out = []
    for num, title, blurb, items in DOMAINS:
        out.append({"id": f"{PREFIX}-{num}", "num": num, "level": 1, "title": title,
                    "statement": blurb, "togaf": "", "standard": "", "source": "", "status": ""})
        for n, t, s, tg, std, src, st in items:
            out.append({"id": f"{PREFIX}-{n}", "num": n, "level": 2, "title": t,
                        "statement": s, "togaf": tg, "standard": std, "source": src, "status": st})
    return out
