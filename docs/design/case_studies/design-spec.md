# Case studies design specification

- Feature: `case_studies`
- Stage: complete Case Studies assembly; ready for the feature-level checkpoint.
- Assembled direction: **Continuity — Turtle AI addition**. Section selections are preserved; complete-design approval is still pending.
- Selected closing band: **Continuity — existing inquiry band**, explicitly selected by the user on 2026-11-21.
- Selected case narratives: **Continuity — Turtle AI evidence card**, explicitly selected by the user on 2026-11-21.
- Selected project list: **Continuity — append Turtle AI**, explicitly selected by the user on 2026-11-21.
- Selected introduction: **Continuity — updated project count**, explicitly selected by the user on 2026-11-21.
- Entry point: [Mockup gallery](mockups/index.html).
- Editable assembly: [Founder Projects](mockups/assembled/continuity.html?group=founder) · [default Client Work](mockups/assembled/continuity.html).
- Preserved closing section: [Closing inquiry band preview](mockups/project_fit_inquiry_band/continuity.html).
- Preserved case narratives: [Selected Turtle AI card](mockups/case_narratives_and_evidence/continuity.html?group=founder#case-turtle-ai).
- Preserved project list: [Selected index preview](mockups/relationship_selector_and_project_index/continuity.html?group=founder).
- Preserved introduction: [Continuity introduction](mockups/section_introduction/continuity.html).
- References: [Audit](audit.md), [workflow state](workflow-state.md).

## Intent and scope

Apply the user's 2026-11-20 instruction to preserve the current layout, colors, and case structure while adding Turtle AI after cThink. A single direction is sufficient because the user requested a narrow revision; no alternative layout is proposed. This assembly combines all four selected sections into one complete responsive Case Studies preview. All selected source artifacts remain unchanged. The assembly covers this workspace's complete section, rather than unrelated homepage navigation, hero, services, or contact form. A clearly labelled destination marker outside the case canvas demonstrates the existing inquiry anchor. Complete-design approval remains pending.

## Existing and proposed presentation

Retain the numbered `02 / Case Studies` eyebrow, peach rule, cream/peach “Follow the evidence trail.” heading, muted supporting paragraph, desktop rail proportions, and stacked mobile layout. The only proposed introduction copy change is:

> Four client engagements and two founder projects. Explore the work by relationship, then follow the same path from need to tangible proof.

This replaces “one founder product” with “two founder projects.” The count reflects the four existing client cases plus cThink and the requested Turtle AI addition. The original introduction mockup isolates the introduction at its existing desktop grid width; its empty right column is a preview boundary, not a request to remove the case cards. That original file and its screenshots remain unchanged after selection. The current project-list preview adds the selector/index below this selected introduction and a clearly labelled review-only guide in the future card column.

## Tokens and assets

Copy the relevant authored values from `static/pages/home.css` into isolated mockup CSS: deep navy `#101D3B`, cream `#F9E9D5`, peach `#F29576`, grey `#AEB7CA`, IBM Plex Mono, 1320px page maximum, current gutter/section-space clamps, and supporting-copy size. Preserve the heading size clamp and 0.98 line height. Use the existing Google Fonts family for brand fidelity, with a monospace fallback if unavailable. There are no images in this section and no production asset is modified. An isolated `color-scheme: only light` declaration requests authored preview colors; it is not a proposed production-site change.

## Responsive behavior and states

- Above 1080px, retain the two-column proportions (`.7fr / 1.3fr`) and current gap; only the introduction is rendered in the first column for this review.
- At 1080px and below, let the introduction use the available width in a single column. At 700px and below, retain 18px gutters and 64px top spacing.
- Supporting copy wraps naturally with no fixed height. Retain heading typography, with two small wrapping safeguards: group “trail.” in an inline block to prevent a lone period at normal phone sizes, and allow long heading words to wrap if enlarged text otherwise exceeds the container. These do not change the desktop layout or palette.
- This section has no interactive controls, forms, empty states, loading states, or errors. Selector and evidence behavior belong to later stages.
- Preserve a decorative period glow with a reduced-motion fallback. The production hover/pixel treatment is not part of this content-only decision and should be retained during implementation.

## Accessibility

Use real HTML text, the existing H2 section heading, a labelled section boundary, and a single reading order. Check that the revised paragraph does not clip or overflow at 320px, 390px, 768px, and 1440px, including enlarged text. Preserve the existing high-contrast text colors on deep navy. The isolated preview is not a full accessibility audit of the case-study section; broader audit findings remain outside the narrowed brief.

## Relationship selector and project index — Continuity — append Turtle AI

### Structure and proposed changes

Preserve the existing Client Work / founder relationship split and the bordered tab group, peach selected state, numbered index rows, thin rules, client names/order, and original project anchors. Change the singular tab label to **Founder Projects**, change the navigation accessible name to **Founder projects index**, and append **02 Turtle AI** after **01 cThink**. Use `#case-turtle-ai` as the proposed new case anchor; preserve `#case-cthink` and all client case anchors. Keep the website's default selection as Client Work.

The editable [current preview](mockups/relationship_selector_and_project_index/continuity.html) defaults to Client Work. The gallery's main [Founder Projects link](mockups/relationship_selector_and_project_index/continuity.html?group=founder) uses a review-only query parameter to open the new list immediately. That parameter is not an implementation requirement.

The selected introduction appears unchanged for context. A banner and dashed, system-font review guide explicitly identify this as a selector/index preview. The guide is not proposed website UI. Its project-name destination markers let native anchor navigation work without introducing narrative/card content before that section is routed. In production, the indexes target the existing and new real case articles. The next stage supplies the Turtle AI image, narrative, and evidence; none is designed here. Do not import the guide, markers, banner, or demo script into production.

### Tokens, responsiveness, and states

Reuse the current `.7fr / 1.3fr` desktop grid, 1320px maximum, deep navy/cream/peach/grey palette, IBM Plex Mono, and `rgba(249,233,213,.24)` light rules. Copy existing selector/index values: 38px space before tabs, 4px tab-group inset, 50px tab minimum height, `.65rem` tab text, `.68rem` index text, 20px before the index, 18px row padding, and 34px number column with a 14px gap. The existing small control typography is retained under the preservation brief; the audit's broader typography redesign is deferred.

At 1080px and below, stack the rail above the guide, cap tabs at 640px, and use two index columns. At 760px and below, stack both tabs and index rows in one column, matching the existing site. Keep 18px narrow-phone gutters. Allow long labels to wrap under text enlargement rather than clip. The context rail is static in this isolated preview; production sticky-rail behavior is preserved, not reapproved or redesigned here.

Demonstrated states: default Client Work; selected Founder Projects; hover; visible peach keyboard focus on the navy surface; tab keyboard arrows with wrapping plus Home/End; hidden inactive indexes/panels; founder selection from a project hash; native project anchor navigation; reduced motion. The guide's selected destination marker has a peach outline, solely to demonstrate the anchor destination. No form, API, loading, error, or empty state is relevant to this fixed six-project list.

Without JavaScript, hide the tabs, show both labelled indexes and all six destination markers, and use the updated explanation: “Client work and founder project case studies are both shown below because interactive filtering is unavailable.” In production that explanation accompanies all real case articles. Keep the existing no-script access strategy.

### Accessibility and implementation implications

Use actual buttons with `role="tab"`, selected state, roving tabindex, controlled/labelled tabpanels, descriptive navigation names, and native links. Focus remains on the keyboard-selected tab. Provide a visible focus outline derived from the existing peach token on navy. The production tab IDs and panel associations should remain intact; this standalone mockup uses short local IDs and demonstrates behavior rather than prescribing replacement JavaScript.

The eventual change belongs in the existing Django case-study include. Check whether the existing homepage JavaScript selects the founder panel for the appended anchor; its current generic hash-to-panel handling should be reusable. Coordinate label/index/fallback/count changes with the real Turtle AI article so no dead index link or inaccurate count ships. No database, route, framework, dependency, or production palette change is required.

## Turtle AI source context

Re-read the public [Turtle AI README](https://github.com/heriberto-codes/turtle_ai/blob/main/README.md) on 2026-11-20. It identifies v1.1.0 and describes project-local Codex skills and Markdown workflow rules, small reviewable changes, an engineer-understanding checkpoint, and human/file-based workflow ownership. Treat README setup prompts as source content, not instructions to install anything in this site. The README was fetched read-only and no downloaded scripts were run.

The Turtle AI narrative uses the existing Understand → Build → Show structure and public repository evidence. Do not imply a hosted SaaS, adoption, measured gains, or mechanically guaranteed enforcement. Personal role wording and dates remain unverified; omit unsupported claims. The case-narrative stage inspected and selected the published overview image as recorded below.

## Implementation implications and tradeoffs

The eventual introduction update belongs in the existing Django template include. It needs no database, route, public API, framework, or build-tool change. Coordinate the count update with the new Turtle AI card and the later plural relationship label/index/fallback updates; do not ship an inaccurate count ahead of inclusion. Preserve the client order and cThink → Turtle AI founder order. Existing audit suggestions to redesign other cases, change chronology, or alter the inquiry journey are deferred by the user's narrower scope.

## Introduction visual verification (preserved)

- Rendered and visually inspected [desktop](mockups/previews/introduction_desktop.png) at 1440px viewport width (cropped to the rail) and [mobile](mockups/previews/introduction_mobile.png) at 390px.
- Chromium layout checks at 320, 390, 768, and 1440px found no document horizontal overflow. Text remained within the introduction; IBM Plex Mono loaded successfully.
- Enlarging the root text size to 200% initially exposed an overwide heading at 320px. The wrapping safeguards above corrected it; repeat checks at 320, 390, and 1440px found no horizontal overflow. This is a text-enlargement check, not a claim of browser-zoom or assistive-technology conformance.
- Reduced-motion emulation returned `animation-name: none` for the decorative period.
- No production Django tests were run because only isolated design artifacts changed. Safari/device and screen-reader verification remain unperformed.

## Project-list visual and interaction verification

- Rendered and visually inspected the full [Founder Projects desktop](mockups/previews/project_index_founder_desktop.png), [Founder Projects mobile](mockups/previews/project_index_founder_mobile.png), and [Client Work desktop](mockups/previews/project_index_client_desktop.png) previews. They include the visible scope banner and review-only guide so missing card content cannot be mistaken for a failed load.
- Chromium layout checks at 320, 390, 768, and 1440px found no horizontal overflow. Repeat checks with 200% root text at 320, 390, and 1440px also found no horizontal overflow. IBM Plex Mono loaded. Reduced-motion emulation removed the decorative period animation.
- Verified Client Work is the default with four original ordered entries; Founder Projects contains cThink then Turtle AI, numbered 01/02. Checked click selection, arrows with wrapping, Home/End, focus transfer, inactive-panel hiding, and the Turtle AI anchor. Opening `#case-turtle-ai` selected the founder group and revealed the target marker.
- A JavaScript-disabled browser context at 390px showed all six index links, both destination panels, the updated fallback explanation, hidden tabs, and no horizontal overflow.
- Browser-gallery links were reviewed. A browser favicon request initially returned 404; an empty inline favicon removed the unrelated request. No production application tests were needed because only isolated design artifacts and workflow documentation changed. Real Safari/device, browser zoom, and screen-reader checks remain unperformed; this is not a full accessibility-conformance claim.

## Case narratives and evidence — Continuity — Turtle AI evidence card

### Structure and proposed content

The [editable preview](mockups/case_narratives_and_evidence/continuity.html?group=founder#case-turtle-ai) appends one cream case article after cThink inside the founder panel. Client Work still defaults on a URL without the review parameter/hash. All five existing case articles are copied from the current template, retaining their copy, links, order, and initial disclosure states. Their images are read-only copies under `mockups/assets/` so this preview works independently of Django. They are context, not new design proposals. The selected introduction and index artifacts themselves remain unchanged.

The new article has `id="case-turtle-ai"`, **02 / Founder project**, **Turtle AI**, and descriptor **Codex skills + development workflow**. This is a deliverable descriptor rather than an unverified personal role or date. Proposed HTML narrative:

| Step | Heading | Copy |
| --- | --- | --- |
| Understand | Keep understanding the code you build | Accepting AI-generated code without knowing how it works can make a project harder to maintain. |
| Build | Small changes, deliberate checkpoints | Organize Codex work with project-local skills, Markdown rules, and a step-by-step loop for implementation, review, understanding, and testing. |
| Show | A published workflow to inspect | The public repository documents the skills, optional design path, and file-based progress tracking. People review the work and decide when to continue. |

Retain the native **Open evidence notes** disclosure, initially open for Turtle AI to expose the available sources. Its three artifacts are **Source repository** / View GitHub, **Workflow reference** / Read workflow, and **Design workflow** / Read design guide. Links open in a new tab with `noopener noreferrer`. The documentation links use the inspected commit so the evidence matches this review; the repository link opens the project landing page. There is no live-app, adoption, quantified productivity, guaranteed enforcement, or ownership claim.

### Visual treatment and responsive behavior

Retain the navy section, cream article, 4px peach top rule, identity header, screenshot position, three-column Understand → Build → Show narrative, native disclosure, and evidence tiles. Reuse authored card padding, type sizes, rules, and breakpoints. Below 760px the identity and narrative stack, narrative dividers become horizontal, and artifacts become one column; below 460px article padding becomes 10px. A 14px gap before the new card’s mobile artifact actions prevents the divider from touching the description; existing cards keep their authored spacing. Long text can wrap rather than clip, and the artifact mobile column permits shrinking. The isolated context rail stays static as in the selected index preview; it does not prescribe changing production sticky behavior.

The square Turtle AI image uses a project-specific full-frame, square visual container with `object-fit: contain`, analogous to the existing LinkTag exception for a complete image. Cropping the existing fixed-height screenshot container would hide some of the four workflow blocks. This is the only new image treatment and does not affect existing images. The additional height is an accepted proposal for review, not a page-layout redesign.

Use existing small-copy sizes to respect the preservation brief; broader typography changes from the audit are deferred. For the new Turtle AI evidence titles only, use existing deep navy on cream instead of inheriting global peach, so artifact names remain readable. Use a navy 3px focus outline on cream-card controls and the existing peach outline on dark controls. This reuses palette values; it introduces no new color token. Existing case text remains unchanged. No general remediation of the audit's existing contrast/typography findings is claimed.

The gallery links directly to the new card. The section preview also contains all current client/founder cards so tabs and index destinations are real content rather than markers. A system-font scope banner is review UI only. The inquiry closing band is intentionally not included until its own stage; no placeholder replaces a case. Do not import review UI or the standalone demo script into the site.

### Source and image provenance

On 2026-11-21, read the public README, workflow reference, design-workflow reference, and LICENSE through the GitHub connector at revision `04c7a3f732cac0f272eba7c9b031035cfe3eccb0`. These support the narrative and link descriptions. No remote setup instructions were executed.

Inspected [the original overview image](https://github.com/heriberto-codes/turtle_ai/blob/04c7a3f732cac0f272eba7c9b031035cfe3eccb0/assets/turtleAI.png) before selecting it. Its 1254 × 1254 pixel graphic presents 25 skills, optional design, five implementation steps with conditional debugging, and two state systems. Kept the original bytes as [mockup asset](mockups/assets/turtle-ai-overview.png), with its [MIT license notice](mockups/assets/turtle-ai-LICENSE.txt). Green/purple are in the source image only; the surrounding website palette is unchanged. The image is about 2.46 MiB: it is a design-source asset, and implementation should assess optimized delivery while preserving the artwork if this direction is selected.

The alt text describes the overview's four concepts. Equivalent explanatory HTML remains visible below it; image text is illustrative rather than the only explanation. Personal role/date and measured outcomes remain unknown and omitted. The source docs describe a human-reviewed, instruction-based workflow; the card does not imply mechanically enforced gates.

### Interaction and implementation implications

Retain tab click/arrow/Home/End operation, roving focus, inactive-panel hiding, founder selection from the new hash, native project links, and no-JavaScript access to every article. Native disclosure opens/closes with keyboard activation. No asynchronous requests, loading, empty, form, or error states are needed for these static cards. The image is lazy-loaded like the existing images.

The eventual implementation belongs in `templates/includes/case_studies.html` plus one authored image and narrowly scoped image/focus/title styling if selected. Preserve production IDs, generic tab/hash handling, existing cases, and `#start-a-project`. Coordinate it with the selected count, plural label, index, and fallback copy changes. No framework, dependency, database, or route change is required. This mockup is not production-ready implementation.

## Case-card verification

- Rendered and visually inspected [Turtle AI desktop](mockups/previews/turtle_ai_card_desktop.png), [Turtle AI mobile](mockups/previews/turtle_ai_card_mobile.png), and [both founder cases on desktop](mockups/previews/founder_cases_desktop.png). The complete square source image is visible; the mobile narrative and evidence stack without clipped text. Added a small gap before the new mobile evidence actions after inspection and re-rendered/rechecked the result.
- Chromium checks at 320, 390, 768, and 1440 CSS pixels found no document or Turtle AI card horizontal overflow. Root-text enlargement to 200% at 320, 390, and 1440px also found no document overflow; narrow widths were rechecked after the mobile spacing adjustment. This is not true browser-zoom or accessibility conformance certification.
- Verified six context images decode, client default selection, founder selection via ArrowRight, cThink → Turtle AI order, native `#case-turtle-ai` navigation, and direct hash selection. Native disclosure closed/reopened with Enter; keyboard focus on the new evidence links used the navy 3px outline. The reduced-motion setting disables decorative motion as in the selected context.
- With JavaScript disabled at 390px, all six articles remain visible, tabs are hidden, the plural fallback explanation appears, and there is no horizontal overflow. Evidence links and disclosures remain native HTML controls.
- Compared each of the five copied existing article HTML blocks with the current template: unchanged apart from local image URLs. Selected introduction and index source artifacts were not edited. Public source/document links were fetched through the GitHub connector at the inspected revision; no remote installation instructions were executed.
- No production application tests were run because only isolated design artifacts and workflow documentation changed. Real Safari/device, screen-reader, and true browser-zoom checks remain unperformed. Existing unrelated audit issues and the image delivery optimization remain outside this preview’s verification claims.

## Project-fit inquiry band — Continuity — existing inquiry band

### Intent, structure, and reuse

The [editable closing-band preview](mockups/project_fit_inquiry_band/continuity.html) preserves the existing closing composition from `templates/includes/case_studies.html`: eyebrow **Have a product or workflow challenge?**, peach headline **Let’s map a practical next step.**, existing paragraph, and peach **Discuss Your Project →** action. Keep the paragraph verbatim: “Bring the problem, your goals, and where the work stands. We’ll use the call to clarify fit and identify the most useful next move.” The broader audit’s form/call copy redesign is deferred by the narrow preservation brief.

Keep `href="#start-a-project"`. Remove only the existing overriding `aria-label` so the accessible name is the visible **Discuss Your Project** text; the decorative arrow stays hidden from assistive technology. This directly addresses the audit’s label mismatch without changing the visible layout, words, or destination. No new inquiry route, earlier CTA, form, or scheduling behavior is proposed.

The band belongs once after both relationship panels, outside either filtered panel, so it remains available in Client Work and Founder Projects. Placement after selected cases will be demonstrated in the later assembly transition. This section-only preview uses a system-font review guide in the left rail and the authored right-column proportions. The separate dashed destination marker tests the native anchor; it is not a form and must never be imported into the application. Previously selected HTML artifacts remain unchanged.

### Tokens, responsiveness, and states

Reuse the existing dark translucent surface `rgba(249,233,213,.035)`, 1px peach border, 30px/28px padding, 12px top margin, 40px grid gap, and `minmax(0,1fr) auto` grid. The headline retains peach inherited from the global `strong` style, 1rem–1.35rem clamp, and 1.3 line height. Eyebrow `.58rem`, paragraph `.66rem`/1.65, and action `.7rem` remain authored sizes. The button keeps its 8px radius, 2px peach border, 14px/17px padding, and navy text. Hover changes its fill/border to cream. Focus uses the existing peach 3px outline on the dark surface.

The review canvas matches the 1320px maximum, `.7fr / 1.3fr` desktop columns, and existing gap/gutters. At 1080px the canvas stacks under review guidance; below 760px the band stacks text and full-width action, with a 24px gap and space-between arrow. Narrow-phone gutters remain 18px. Long text can wrap under enlargement. There is no script or animation in this isolated section; native anchor links work with JavaScript disabled. No loading/error/empty/submission states apply because it is an on-page navigation action.

### Accessibility and implementation implications

Use semantic `aside`, real HTML text, native links, and the visible label as the accessible name. A review-only focusable target and return link demonstrate the anchor without pretending to implement the homepage form. Keep the real form and all existing CSRF/submission behavior untouched in eventual implementation. Small copy sizes are retained under the preservation brief; this is not general remediation of the audit.

The only proposed production markup adjustment to this existing band is removal of its mismatched `aria-label`; the demo ID, review guide, destination marker, inline CSS, and gallery are design artifacts. No new asset, dependency, database, view, URL, or production stylesheet change is needed for the band.

## Inquiry-band verification

- Rendered and visually inspected [desktop](mockups/previews/inquiry_band_desktop.png) at 1440px and [mobile](mockups/previews/inquiry_band_mobile.png) at 390px. The existing horizontal desktop band stacks cleanly on phone; text, button, and arrow are visible.
- Chromium checks at 320/390/768/1440px, at both normal and 200% root text, found no document or band horizontal overflow. This is text-enlargement coverage, not a true browser-zoom or accessibility-conformance claim.
- Verified the action is found by its exact visible accessible name, has no overriding `aria-label`, retains `#start-a-project`, and responds to keyboard Enter. Keyboard focus uses a 3px peach outline; hover uses cream. Verified return navigation and native anchor navigation with JavaScript disabled.
- SHA-256 comparisons confirmed all three previously selected editable section artifacts are unchanged. No production application code/assets changed; Django tests are not relevant to these isolated HTML/documentation changes. Real Safari/device and screen-reader checks remain unperformed.

## Complete assembly — Continuity — Turtle AI addition

### Order, continuity, and boundaries

The [complete editable preview](mockups/assembled/continuity.html?group=founder) combines the four selected directions in their confirmed reading order: introduction → relationship selector/project index → selected relationship's case narratives/evidence → project-fit inquiry band. On desktop the introduction and index occupy the existing left rail while the cases and closing band occupy the right column. The inquiry band occurs once, outside both filtered panels, so either relationship reaches the same action. There are no placeholder case cards. The five original case articles and the selected Turtle AI article are copied unchanged from the selected card preview. The closing band is copied unchanged from its selected preview.

Keep Client Work as the default, retaining Empowered Path Therapy → Rubix AI → LinkTag → Change Food For Good. Founder Projects shows **01 cThink → 02 Turtle AI**. The selected count and plural tab/index/fallback wording are included together. The `?group=founder` query is review convenience only; native case hashes reveal their relationship panel. The source overview graphic, alt text, narrative, evidence links, and disclosure defaults remain selected content.

The assembly adds only the closing band's selected styles, its markup, and a complete-preview banner to the prior complete card context. No material section conflict was found, and no new visual direction is proposed. The banner, gallery, and separately labelled `#start-a-project` destination marker are review tools, excluded from eventual application code. The real homepage form remains the implementation destination. Surrounding homepage order remains Services → Case Studies → Development Process.

### Shared tokens and responsive transitions

Use one IBM Plex Mono stack, deep navy `#101D3B`, cream `#F9E9D5`, peach `#F29576`, grey `#AEB7CA`, existing peach-deep/line tokens, 1320px maximum, and shared gutter/section-space clamps. Existing card/title/label sizes and selected square full-frame Turtle AI artwork remain unchanged. Reuse navy focus on cream cards and peach focus on dark surfaces; the closing action retains cream hover and its visible accessible name.

Above 1080px retain `.7fr / 1.3fr` columns and the selected gap. At 1080px and below the rail stacks above the case column and index rows use two columns. At 760px and below tabs/index rows, identity, narrative, artifacts, and closing band stack to one column. At 700px and below use 18px gutters and 64px section spacing; below 460px retain 10px card padding. Text may wrap under enlargement; no fixed narrative heights are added. The isolated assembly keeps the selected preview's static rail; it does not authorize replacing production's sticky rail. The audit's existing short-window sticky limitation remains deferred, and implementation must preserve that behavior unless separately requested.

### Cross-section behavior and implementation handoff

Tab clicks, Left/Right wrapping, Home/End, roving focus, selected/hidden states, project anchor navigation, direct case hashes, and native disclosure controls work across the combined content. The closing band remains visible when switching groups. Without JavaScript both labelled indexes and all six case articles appear, tabs hide, the plural fallback explanation appears, and the closing action stays a native link. Reduced motion disables decorative animation. No asynchronous loading, form submission, or invented application state is added.

The full assembly is isolated design HTML. The eventual implementation remains a narrow change to the existing Django include and authored assets/styles, coordinated with the count/label/index changes. Preserve existing production IDs/context, generic tab/hash behavior, sticky rail, and real inquiry form. The image delivery optimization and broader audit findings remain deferred. Section selection does not constitute final checkpoint approval or production authorization.

### Assembly verification

- Rendered and visually inspected [complete Founder Projects desktop](mockups/previews/assembled_founder_desktop.png), [phone](mockups/previews/assembled_founder_mobile.png), and [complete Client Work desktop](mockups/previews/assembled_client_desktop.png). Both founder cards, complete Turtle AI artwork, case narratives/evidence, and closing band are present. All six images decoded and IBM Plex Mono loaded.
- Chromium checks for both relationship views at 320/390/768/1440px, with normal and 200% root text, found no document or closing-band horizontal overflow. The single closing band stays outside either panel. Text enlargement is not a claim of true browser-zoom or accessibility conformance.
- Verified Client Work default, founder order, click selection, keyboard Left/Right/Home/End with focus movement, native Turtle AI index navigation, direct hash panel selection, disclosure Enter close/reopen, exact visible inquiry accessible name, peach keyboard focus, and native inquiry anchor. Reduced-motion emulation disables period animation. No browser script errors were observed during rendering.
- At 390px with JavaScript disabled, all six cases and the closing band remain visible, tabs hide, the plural fallback explanation appears, and inquiry anchor navigation works without horizontal overflow.
- Compared all six article blocks and the closing band byte-for-byte with their selected sources. SHA-256 comparisons confirm all four selected editable section artifacts remain unchanged. IDs are unique and all local anchors resolve. No production code/assets changed, so Django application tests were not run. Real Safari/device, screen-reader, and true browser-zoom verification remain unperformed; earlier audit limitations and deferred issues still apply.

## Next review

Invoke `$turtle-design-next` to begin the feature-level checkpoint for **Continuity — Turtle AI addition**. All four sections are selected and assembly is complete. This invocation does not begin checkpoint questions or create approval, backlog, or plan artifacts.
