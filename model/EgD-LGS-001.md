# Gated Sections and Basic Lessons

## Why this document exists

The reference model `EgD-URM-001` set out fifteen domains and eighty-eight capabilities. Domain 4, Learning Design, is the domain the game exists to carry, and it is the domain that has no structure underneath it. `4.4` says content is delivered as numbered chapters with an explicit unlock rule. The unlock rule has never been written down. This document writes it down.

It specifies nothing new about the story and invents no doctrine. It takes what the game already has — three shapes, three chapters, one Church review gate — and puts numbers and gates on it so the same structure can be built four times without being re-argued four times.

**Nothing here is built until it is approved.** That is deliberate, and it is a correction. Two surfaces were produced for this chapter before this structure existed, and both of them were scenery.

## The correction this document is answering to

| # | What was done | What the canon already said |
| --- | --- | --- |
| 1 | A 3D field was published with Uriel standing on a dais as a guide, with five lines of dialogue. | *"Uriel is named in the quoted text because the text names him. He is not a character, a guide, or a mechanic in the game."* — the chapter source, section VII. |
| 2 | A second Chapter Three was authored from scratch. | Chapter Three already exists and is public at [quatre-jours.html](https://eveglyphdesign.github.io/eve-hyperloop/game/quatre-jours.html), canon-bounded and clean. |
| 3 | A walking surface was delivered with no lesson, no gate and nothing to count. | The mechanic is written in the source: *"find the four days nobody counted, and put them back."* |

The 3D field stays published, relabelled as a rendering demonstration of the runtime capabilities. It is not the game and it will not be presented as the game.

## What already exists

| Piece | Where | State |
| --- | --- | --- |
| Three shapes, three lessons | [the game landing page](https://eveglyphdesign.github.io/eve-hyperloop/game/) | Live. Circle, triangle, sphere are already the teaching spine. |
| Adult access gate | Same page | Live. A trusted adult requests access; the mission opens when the child is confirmed. |
| Chapter Two, What We Kept | [what-we-kept.html](https://eveglyphdesign.github.io/eve-hyperloop/game/what-we-kept.html) | Live. Trilingual puzzle on the Acadian expulsion. |
| Chapter Three, The Four Lost Days | [quatre-jours.html](https://eveglyphdesign.github.io/eve-hyperloop/game/quatre-jours.html) | Live. Two instructional lines, correct sources, no gating. |
| Chapter source and boundaries | [LES-QUATRE-JOURS-PERDUS.md](https://github.com/EVEglyphDesign/paix-educational-game/blob/main/world/enoch/LES-QUATRE-JOURS-PERDUS.md) | Canon. Defines what the game takes and what it refuses. |
| Church review gate | `EgD-URM-001` section 1.2 | Canon. A release requirement, not a stage. |

The gap is narrow and specific: **the sections are not numbered and nothing is gated.** A child can reach the end of Chapter Three without counting anything.

## How the numbers work

Three levels, and they are the same three levels as the reference model, so a section number can be handed to an architect and placed on any other model.

| Level | Form | Meaning | Example |
| --- | --- | --- | --- |
| Spine | `Sn` | A section kind. Chapter-independent. Every chapter has all eight. | `S3` The work |
| Instance | `Cn.Sm` | Section `m` as it appears in chapter `n`. | `C3.S3` Count the twelve gates |
| Gate | `Gm` | The rule that must pass before `Sm` opens. | `G3` Evidence gate |
| Lesson | `Ln` | A basic lesson primitive used inside a section. | `L1` Circle |
| Artefact | `Cn.Am` | What the child produced in `Cn.Sm`. This is the evidence. | `C3.A5` The completed year |

The rule that makes this worth numbering: **`S3` means the same kind of thing in every chapter.** A reviewer who has read `C2.S3` knows what `C4.S3` will be before it is written. That is the lowest-denominator property — the numbers travel, the content does not have to.

## The section spine

Eight sections. Every chapter has all eight, in this order, with no exceptions and no chapter-specific additions. A chapter that needs a ninth section has been designed wrong.

| ID | Section | What happens | URM |
| --- | --- | --- | --- |
| S0 | Threshold | The adult opens the mission. The fiction notice is displayed. The child is told what the chapter is about and offered the skip. Nothing is interactive yet. | 2.1, 2.4, 2.6 |
| S1 | Circle | The child draws the circle: what is the boundary of this problem, what is inside it and what is outside. | 4.3 |
| S2 | Triangle | The child places the triangle: three good reasons for the decision the chapter turns on. | 4.3 |
| S3 | The work | The chapter's own mechanic. This is the only section whose content differs between chapters. | 4.4 |
| S4 | What is missing | The child finds the uncounted thing. The chapter does not tell them what it is. | 4.6 |
| S5 | Put it back | The restoration. Arithmetic a child can do, performed by the child, not watched. | 4.4 |
| S6 | Sphere | The lesson belongs to everyone. The child hands it to one other person and that hand-off is recorded. | 4.3, 4.5 |
| S7 | Evidence | The artefacts the child produced are shown back to them and to the guardian. No score, no time, no streak. | 4.6, 2.7 |

Two properties of this spine matter more than its content. It has **no combat section**, because the source says the game is not a fight. And **S4 precedes S5**, so the child always finds the gap before being allowed to close it — being shown the answer and then asked to type it is not a lesson.

## The gates

A gate is a condition, not a button. Each gate guards entry to the section of the same number.

| ID | Gate | Opens when | Class |
| --- | --- | --- | --- |
| G0 | Adult gate | A trusted adult has requested access and the child has been confirmed. Already live on the landing page. | Safeguarding |
| G1 | Consent and skip gate | The fiction notice has been displayed and the child has either continued or taken the skip. The skip is never penalised. | Safeguarding |
| G2 | Circle gate | The child has drawn a boundary. Any boundary. The gate checks that one was drawn, never whether it was correct. | Evidence |
| G3 | Triangle gate | Three reasons exist and are the child's own words. Fewer than three does not open it; the game asks for the third. | Evidence |
| G4 | Work gate | The chapter mechanic has been completed to its own stated condition. | Evidence |
| G5 | Finding gate | The child has named what is missing. Fixed-answer checked against a reviewed list, never generated. | Fixed-output |
| G6 | Restoration gate | The restoration is arithmetically correct. This is the one gate that can be failed, and failing it returns the child to S4 with what they got, not to the start. | Mastery |
| G7 | Service gate | The lesson has been handed to one other person and that person has acknowledged it. | Service |

Three gate rules that hold across all four chapters:

- **A gate never opens on time spent.** Sitting in a section longer does not advance it. This is `4.6` and it is the reason there is no timer anywhere in the spine.
- **Only `G6` can be failed.** Every other gate is a completeness check. The child cannot be wrong about their own boundary or their own three reasons.
- **The Stand-Up interrupt is not a gate.** Twelve minutes of active play triggers the sixty-six-second break wherever the child is, including mid-gate, and the gate state is preserved across it. `URM 2.3`.

## The basic lessons

Three primitives, already live on the landing page as *tres formas, tres lecciones*. They are not decoration and they are not per-chapter. They are the whole teaching method, and every chapter teaches all three again in its own material.

| ID | Primitive | The question it teaches | Where it lands |
| --- | --- | --- | --- |
| L1 | Circle | Where does this problem stop? What is not my business here? | S1 |
| L2 | Triangle | Can I give three good reasons? If I can only give one, I am guessing. | S2 |
| L3 | Sphere | Who else does this belong to? A lesson kept by one person is not finished. | S6 |

Alongside the three shapes each chapter carries exactly one **arithmetic lesson** — one piece of number work small enough for a child to hold and real enough to be true. It sits in S5 and it is what the chapter is actually for.

| Chapter | Arithmetic lesson |
| --- | --- |
| C1 | Three shapes, one twin. Counting to three and knowing why each step was taken. |
| C2 | Three things kept — family, language, faith — carried by a people who were scattered and did not drop any of them. |
| C3 | Twelve gates times thirty days is three hundred and sixty. The year is three hundred and sixty-four. Four are missing, and they go at the quarters. |
| C4 | Not yet specified. The slot is held and the shape of it is known. |

## The four chapters

The source says four lost days gives four chapters, and that Chapter Two is already one of them. The mapping below is a reading of what exists, not canon, and it is the first thing that needs your confirmation.

| ID | Chapter | Portal | State |
| --- | --- | --- | --- |
| C1 | The mission: get your twin | First | Live. Not yet S0-S7. |
| C2 | What We Kept | Third | Live. Spine to fit. |
| C3 | The Four Lost Days | Fourth | Live. Needs full spine. |
| C4 | Unnamed | Sixth | Slot held. Yours to name. |

The four uncounted days sit in the first, third, fourth and sixth portals, and on a circle they fall at the quarters. The chapters inherit those positions. Nothing is said out loud about the shape that appears; the child restores four points and the shape comes up under their own hand.

## Chapter Three, worked in full

This is the one chapter specified end to end, as the pattern for the other three.

| ID | Section | What the child does | Artefact | Gate out |
| --- | --- | --- | --- | --- |
| C3.S0 | Threshold | Reads that this is a calendar from an old book, that it is heritage and astronomy and not doctrine, and that they may skip. | — | G1 |
| C3.S1 | Circle | Draws the year as one closed ring. The ring is the boundary: a year is a thing that comes back to where it started. | C3.A1 the ring | G2 |
| C3.S2 | Triangle | Gives three reasons a year needs to be counted at all. Their own words, not a menu. | C3.A2 three reasons | G3 |
| C3.S3 | The work | Touches each of the twelve gates and counts its thirty days. Six gates where the sun rises, six where it sets. | C3.A3 twelve gates counted, 360 | G4 |
| C3.S4 | What is missing | Is told the year is three hundred and sixty-four and is not told the difference. Names the gap themselves. | C3.A4 the number four | G5 |
| C3.S5 | Put it back | Places four days on the ring, in the first, third, fourth and sixth portals. The ring closes at 364. | C3.A5 the completed year | G6 |
| C3.S6 | Sphere | Teaches the count to one other person and records who. | C3.A6 the hand-off | G7 |
| C3.S7 | Evidence | Sees their ring, their three reasons and their completed year, together, as the record of what they did. | C3.A7 the record | — |

**What Chapter Three must not contain.** These are not preferences. They are the boundaries the chapter source already set, and the first 3D surface broke the first one.

- Uriel is quoted where the text quotes him. He is not a character, a guide, a narrator or a mechanic.
- No Watchers, no Nephilim, no parables, no dream visions, no judgement passage. One section of the book, the astronomical one.
- Nothing frightening. A child should not have to be frightened in order to be taught something true.
- Both halves of the canon statement are said: the book is not in the Catholic canon, and it is canonical Scripture in the Ethiopian and Eritrean Orthodox Tewahedo Churches and for the Beta Israel.
- No claim that the 364-day year should replace any calendar in use.

## What the structure refuses

| Refusal | Reason | URM |
| --- | --- | --- |
| No streaks, no daily login, no follower counts | Standing is earned through evidenced help to others. | 4.5 |
| No generated catechetical answers | Answers are reviewed and deterministic. Generation is not permitted on the child surface. | 4.2 |
| No chat, voice, uploads, ads, trackers or outbound links | Closed communication walls on the child surface. | 2.1 |
| No progress measured in minutes | Progress is evidenced by artefacts the learner produced. | 4.6 |
| No chapter published without the Church review gate | Doctrinal conformance is a release requirement. | 1.2 |
| No ninth section, no chapter-specific gate | If a chapter needs one, the chapter is wrong, not the spine. | 4.4 |

## Crosswalk

The section numbers are the join. Any section can be handed to another model without carrying the story with it.

| Spine | URM capability | TOGAF layer | Standards analogue |
| --- | --- | --- | --- |
| S0 | 2.6 Consent and skip gates | Business | Enrolment and informed consent |
| S1, S2, S6 | 4.3 Lesson primitives | Application | Learning objective |
| S3 | 4.4 Chapter and progression model | Application | Learning activity |
| S4, S5 | 4.6 Assessment and mastery evidence | Data | Formative assessment |
| S6 | 4.5 Service-and-evidence credibility | Business | Peer teaching, evidenced |
| S7 | 4.6, 2.7 Guardian visibility | Data | Learner record, portfolio |

## What needs your decision

Five things, and none of them should be guessed at.

1. **The chapter-to-portal mapping.** Is the landing mission Chapter One, and does C2 sit in the third portal and C3 in the fourth as read above?
2. **Chapter Four.** The slot is held in the sixth portal. It is not for anyone else to name.
3. **`G7`, the service gate.** Requiring a hand-off to another person before a chapter closes is the strongest claim in this document. It is also the one that could strand a child who has nobody to teach. It may need an offline path.
4. **Where the spine is fitted first.** Chapter Three is the natural pilot because its arithmetic is the cleanest, but Chapter One reaches every child before any other.
5. **The 3D lane.** Whether the rendering demonstration ever becomes a chapter surface, or whether the chapters stay in the flat trilingual form they already work in.

Nothing is built until these are answered.
