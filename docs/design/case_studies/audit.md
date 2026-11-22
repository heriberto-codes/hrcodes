# Case Studies Section Design Audit

- Feature slug: `case_studies`
- Audit date: 2026-11-20
- Scope: the implemented homepage `02 / CASE STUDIES` section (`#proof`).
- Status: audit complete; proposed improvements and order below are not design approval.

## Objective and audience

Help prospective clients assess whether Hroman Codes can address a comparable business problem, understand Heriberto's contribution, inspect supporting work, and continue to the project inquiry form.

The audience and conversion objective come from the existing [approved homepage design](../business_focused_homepage/approved-design.md). The user requested a section audit without specifying a new commercial objective. This audit assumes continuity with that brief. It does not reopen the entire homepage or replace the earlier approval.

## Evidence inspected

- Repository foundations: `AGENTS.md`, `architecture.md`, `repo_map.md`, and `docs/system/design-workflow.md`; all are present.
- Current source: [case study template](../../../templates/includes/case_studies.html), [homepage composition](../../../templates/home.html), [homepage styles](../../../static/pages/home.css), [global styles](../../../static/style.css), [homepage enhancements](../../../static/pages/home.js), and the homepage view/base template.
- Historical context: the existing homepage audit, design specification, approved design, workflow state, and completed feature record. These describe the selected Direction B, “Evidence trail.” The historical audit describes an earlier homepage and is not treated as evidence of today's rendering.
- Local Django homepage at `http://127.0.0.1:8000/#proof`, visually inspected in Chromium at 1440 × 1000 and 390 × 844; short-desktop inspection at 1440 × 700.
- Additional layout measurements at 320, 768, 1100, and 1280 CSS pixels wide. These measurements do not substitute for visual/device coverage at every size.
- Browser checks: tab keyboard selection, selected/hidden states, native disclosure operation, cThink hash selection, computed text/focus styles, image loading, and reduced-motion behavior. A separate JavaScript-disabled context verified fallback content; external resources were blocked in that context, so it was a fallback structure check rather than a visual equivalence test.
- Contrast ratios calculated from computed foreground colors and layered background colors using relative luminance. They are rounded below for reporting, not for pass/fail decisions.
- Temporary browser screenshots were captured during the audit; findings and measurements are retained here so they do not depend on session screenshots being available.

No public project destination was opened, no form was submitted, and no production deployment was inspected. The earlier Codex-warning screenshot is unrelated to this UI.

## Current design inventory

- Page placement: Services → Case Studies → Development Process.
- Deep-navy section with a sticky desktop introduction/index and cream case cards; the rail stacks above the cases at 1080px and below.
- Introduction: numbered eyebrow, large “Follow the evidence trail.” heading, relationship-based explanation, Client Work/Founder Product tabs, and a project index.
- Client order: Empowered Path Therapy → Rubix AI → LinkTag → Change Food For Good. Founder Product contains cThink.
- Each case includes identity/role metadata, a screenshot, `Understand → Build → Show` narrative, and a native evidence disclosure. EPT and cThink disclosures start open; the other three start closed.
- Closing band: “Let’s map a practical next step.” and “Discuss Your Project,” linking to `#start-a-project`.

| Case | Existing evidence destinations | Current narrative emphasis |
| --- | --- | --- |
| Empowered Path Therapy | Live site, Figma | Telehealth practice experience and Django foundation |
| Rubix AI | LinkedIn updates, Figma design, prototype, C4 PDF | Marketing product, MVP interface, system design |
| LinkTag | Live application, source | Connection organization, authentication, data workflow |
| Change Food For Good | Live PlantID, source, organization site | Teaching through a working JavaScript/API project |
| cThink | Source repository | Founder product hypothesis and multisensory learning approach |

## Strengths to preserve

- Distinctive navy/cream/peach palette, IBM Plex Mono, numbered labels, thin rules, and restrained period motion connect this section to the rest of the brand.
- Separating client engagements from a founder product gives buyers useful relationship context; this distinction was explicitly approved previously.
- The repeated three-part narrative is more helpful than an unstructured screenshot gallery. Keep its recognizable sequence while making the content more specific.
- Real screenshots and multiple evidence types provide material for both commercial and technical evaluation. PlantID is explicitly described as a class project, and cThink as a product hypothesis.
- Tabs support Left/Right, Home/End, wrapping, focus movement, and selected/hidden states in the tested browser. Enter closed and reopened a native disclosure. The cThink hash selected its panel.
- Without JavaScript, tabs are hidden, both case panels are displayed, and an explanation is present. Reduced-motion emulation removed the period animation.
- No section elements extended beyond the viewport in measured widths from 320 to 1440px. Titles and role metadata did not overlap in the measured layouts.

## Findings, ordered by impact

### 1. Essential case content is too small for comfortable evaluation — high, usability

**Evidence:** Computed body copy is 10.56px, role metadata and evidence actions 9.92px, evidence descriptions 9.6px, step labels 9.28px, tabs 10.4px, and index links 10.88px at the default 16px root size. The desktop and phone screenshots show a strong heading/image hierarchy with much smaller explanatory text. Narrative headings are 14.4px.

**Likely impact:** The content explaining relevance and contribution requires more effort to read than the screenshots and slogans. Small actions also make destination choices harder to scan. Font size alone is not claimed as a WCAG failure.

**Design response:** Give narrative copy, evidence names, and actions a comfortable reading hierarchy, then rebalance spacing and column widths around it. Treat roughly 16px body copy as a mockup starting point to evaluate, not a mandatory brand token or a legal minimum. Preserve the monospaced identity.

### 2. Evidence text and keyboard focus have insufficient contrast — high, accessibility

**Evidence:** Rendered artifact titles inherit peach `#F29576` from the global `strong` rule (`static/style.css:390`), producing approximately **1.96:1** against the composited pale artifact-card background. Step/identity labels use `#B7583E` on cream at **3.94:1**; artifact actions use that color on their layered background at approximately **4.09:1**. All are small text, below the [4.5:1 text requirement](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Muted body copy `#58647C` on cream is approximately **5.00:1** and should not be described as failing contrast.

Keyboard Tab focus on the first PlantID evidence link produced an author-supplied 3px `#FFD26A` outline. Its contrast against the artifact card is approximately **1.25:1**, below the [3:1 contrast required for visual state information](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html). The same yellow token contrasts poorly against cream (approximately 1.20:1).

**Likely impact:** Visitors with low vision may miss evidence labels or lose their keyboard position despite the existence of a focus outline.

**Design response:** Define readable text and focus treatments for both dark and light surfaces. Retain peach as a brand accent while giving essential text a sufficiently dark treatment on pale cards. Validate actual rendered colors, including inherited styles and translucent layers.

### 3. The narrative establishes artifacts more clearly than delivered value — high, content/decision support

**Evidence:** EPT's “Show” text says that the live website and Figma make the work visible; Rubix describes “Multiple proof layers”; LinkTag and PlantID describe inspectable applications/repositories. Role titles are supplied, but there is little explicit distinction between personal ownership, team contribution, delivery constraints, or an observed result. No quantified outcome or client quote appears in this section.

**Likely impact:** A buyer can find work to inspect but must still infer what was delivered, why it mattered, and how much of it Heriberto owned. Technical artifacts require interpretation by a nontechnical prospect.

**Design response:** Retain Understand/Build/Show, but give each case a concise, verified delivery/result summary and explicit contribution. Distinguish shipped capabilities, prototypes, learning outcomes, and hypotheses. Qualitative results are sufficient when substantiated; do not invent metrics, endorsements, ownership, or business impact.

### 4. EPT's date range creates a credibility question — medium, content verification

**Evidence:** The first case visibly reads `Full-Stack Software Engineer · 2024–2016` (`templates/includes/case_studies.html:33`). This runs backward as a conventional year range. The historical design specification explicitly records this exact wording as user-supplied (`design-spec.md:247`), so it is not evidence of an implementation transcription error.

**Likely impact:** An apparent chronology mistake in the first case can distract from the proof and weaken confidence in the metadata.

**Design response:** Ask the owner to confirm the intended dates or alternative wording before revised copy is finalized. Do not guess that the end year is 2026 or silently override the earlier decision.

### 5. Mobile exploration is long and loses its index — medium, usability

**Evidence:** In the default Client Work state, the section is approximately **4529px** high at 1440px wide, **5666px** at 390px, and **5927px** at 320px. At 390px the introductory rail alone is approximately 681px high; the first case starts about 800px below the section start. The rail becomes static on smaller screens. The inquiry CTA appears only after all four cases, and three cases conceal their evidence links behind the same generic “Open evidence notes” label. Opening additional disclosures increases length further.

**Likely impact:** Buyers comparing later cases must travel a considerable distance and scroll back to change the relationship view or reuse the index. The desktop rail shortens navigation, but mobile loses that benefit. These are observed navigation costs, not measured abandonment or conversion loss.

**Design response:** Explore a shorter overview-to-detail path and convenient ways to return to project selection. Surface a meaningful primary evidence action and an earlier inquiry opportunity while reserving secondary artifacts for optional disclosure. Preserve access to all cases; do not assume that pagination, a carousel, or new detail pages are required.

### 6. The sticky desktop index does not fit shorter windows — medium, responsive usability

**Evidence:** At 1440 × 700, while the Rubix case is in view, the sticky rail starts at y=32 and ends near y=760. The Change Food For Good index link occupies approximately y=706–759, entirely below the viewport. The sticky rule is based on width, with no height accommodation (`static/pages/home.css:629`).

**Likely impact:** The last project shortcut is unavailable to pointer users in this common short-window configuration without changing scroll context or viewport size. Keyboard scrolling may behave differently and was not asserted to be blocked.

**Design response:** Make the navigation fit the available height or allow a natural non-sticky flow when it cannot. Include short desktop windows and zoomed layouts in the next visual review.

### 7. The inquiry action's accessible name differs from its visible label — medium, accessibility

**Evidence:** The visible label is “Discuss Your Project”; its explicit accessible name is “Go to the Start a Project form” (`templates/includes/case_studies.html:72`). The accessible name omits the visible words, contrary to [Label in Name](https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html). The adjacent paragraph also describes using “the call,” although this action initially opens the on-page brief form.

**Likely impact:** Speech users who say the visible label may not activate the intended link. Other visitors may expect immediate scheduling rather than a form.

**Design response:** Keep the visible action and its accessible name aligned and describe the actual first step consistently. Preserve the existing inquiry destination.

## Existing components, tokens, and assets to reuse

- Section/template boundary, `#proof`, named project anchors, tab/panel associations, native disclosures, and `#start-a-project` destination.
- Existing palette: navy `#192A51`, deep navy `#101D3B`, cream `#F9E9D5`, peach `#F29576`, ink `#293754`, supporting grey `#AEB7CA`, line tokens, and surface-aware focus treatment derived from the established palette.
- IBM Plex Mono; `--page-max-width`, `--page-gutter`, `--section-space`, and `--supporting-copy-size`. The introduction already uses the larger supporting-copy token.
- Existing case identity, three-step narrative, evidence-card group, and inquiry closing band as reusable compositions.
- `static/pages/images/EPT_home_page.png`, `rubixAIhomepage.png`, `linktag-home.jpg`, `plantid-main.png`, and `cThink.png`; all references should remain read-only during design work. LinkTag preserves its complete 16:9 frame; other images use cropped containers. Text inside screenshots is illustrative, not a substitute for readable HTML content.
- Existing project-specific live, source, prototype, design, and architecture links. Their availability and public permissions require a separate destination review.

## Responsive and accessibility considerations

- Preserve the single semantic content sequence and H2 → H3 → H4 hierarchy, tab keyboard behavior, meaningful image alternatives, no-script access, and reduced-motion fallback.
- Design enlarged copy together with responsive card structure; do not merely increase text inside the existing narrow desktop columns and assume it fits.
- Preserve the 50px tab height and comfortably padded index/disclosure controls. Evidence actions measured about 30px high on desktop; a larger evidence action can improve comfort without claiming every control currently fails target-size requirements.
- Recheck focus against each actual surface, open/closed disclosures, both tab views, short windows, and text enlargement. Positive overflow measurements at default text size do not establish 200% zoom or text-spacing support.
- At 390px, the heading's animated period wrapped onto its own line. Keeping punctuation with the final word is a minor visual recommendation, subordinate to readability and contrast.
- No screen reader, speech-control device, real touch device, or non-Chromium browser was tested. This is a targeted audit, not a full accessibility conformance assessment.

## Constraints, assumptions, and missing evidence

- Preserve the Django view/template boundary and existing brand; introduce no new framework or build tooling.
- Existing homepage decisions establish client/founder separation, case order, three-part narrative, and inquiry direction. Proposed changes need review; this audit does not amend those approvals, workflow state, backlog, or plans.
- The new `case_studies` workspace has no activated automated workflow. The earlier `business_focused_homepage` workflow is `planned`; its historical state is unchanged.
- Required content evidence before final mockup copy: correct EPT chronology, publication permissions, each project's actual ownership and delivery status, and any supportable result. Until confirmed, use only existing verified content and identify provisional copy clearly.
- Missing effectiveness evidence: buyer feedback, analytics, comparative engagement, inquiry attribution, preferred client segment, and ranking of the cases by commercial relevance. Do not treat current order or journey length as proven conversion outcomes.
- Local rendering reflects current repository code, not independently verified deployed parity. Third-party destinations, Figma permissions, application availability, and screenshot freshness were not verified.

## Prioritized opportunities for `turtle-design-mockup`

1. Establish a readable, contrast-safe case narrative and evidence-action hierarchy on phone and desktop, including keyboard focus on cream surfaces.
2. Show a verified contribution/delivery summary before requiring visitors to interpret external artifacts; resolve the EPT date question before final copy.
3. Compare a conservative revision of the evidence trail with a more compact overview/detail treatment, preserving the approved relationship split and access to every case. These are exploration opportunities, not selected directions.
4. Demonstrate shorter-window navigation, a mobile return-to-selection path, and an inquiry opportunity reachable before completing every case.
5. Refine disclosure wording, screenshot framing, accessible action names, and form/call expectations after the primary hierarchy works.

## Proposed design sections in recommended page order

Keep the surrounding homepage sequence **Services → Case Studies → Development Process**. Within Case Studies, propose the following order for review:

1. **Section introduction and evaluation promise:** retain `02 / Case Studies` and explain what buyers can learn from the work.
2. **Relationship selector and project overview/index:** keep Client Work as the default and Founder Product distinct; offer enough context to choose a relevant case.
3. **Selected relationship's case narratives:** retain EPT → Rubix AI → LinkTag → Change Food For Good in Client Work; show cThink in Founder Product. Within each narrative, present identity/contribution, business need, build/delivery, verified result, relevant image, then primary and optional supporting evidence. This describes reading priority, not a prescribed layout or a requirement to hide all but one case.
4. **Project-fit inquiry band:** connect the demonstrated work to “Discuss Your Project,” clearly describing the brief-form step. Explore an additional earlier route without displacing this close.

This is a proposed section structure, not a new page approval. If the automated controller is activated for this workspace, the user must confirm its ordered section list before mockup routing proceeds.
